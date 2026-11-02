"""Recepción, memoria persistente y entregas inmutables para trabajo asistido."""
from collections import Counter
from contextlib import contextmanager, closing
from datetime import datetime, timezone
import csv
import os
import sys
import importlib.metadata
from pathlib import Path
import shutil
import sqlite3
import tempfile
import time

from . import __version__
from .comun import ROOT, bytes_json, csv_seguro, dentro, guardar, leer, sha
from .evaluacion import MODULOS, evaluar
from .informe import redactar
from .lectura import leer_documento

EXTENSIONS={'.pdf','.docx','.txt','.md','.csv','.html','.htm','.xlsx','.png','.jpg','.jpeg','.tif','.tiff'}

def now():
    return datetime.now(timezone.utc).isoformat()

class Memoria:
    def __init__(self,root):
        self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True)
        self.db=self.root/'estado.sqlite'
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('PRAGMA journal_mode=WAL')
            c.executescript('CREATE TABLE IF NOT EXISTS eventos(id INTEGER PRIMARY KEY, caso TEXT, fecha TEXT, estado TEXT, detalle TEXT); CREATE TABLE IF NOT EXISTS mensajes(id INTEGER PRIMARY KEY, caso TEXT, fecha TEXT, rol TEXT, texto TEXT);')
    def evento(self,case,state,detail=''):
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO eventos(caso,fecha,estado,detalle) VALUES(?,?,?,?)',(case,now(),state,detail))
    def mensaje(self,case,role,text):
        if role not in ('usuario','coordinador'): raise ValueError('Rol desconocido')
        with closing(sqlite3.connect(self.db)) as c, c:
            c.execute('INSERT INTO mensajes(caso,fecha,rol,texto) VALUES(?,?,?,?)',(case,now(),role,text[:20000]))
    def historial(self,case):
        with closing(sqlite3.connect(self.db)) as c, c:
            c.row_factory=sqlite3.Row
            return {'eventos':[dict(r) for r in c.execute('SELECT fecha,estado,detalle FROM eventos WHERE caso=? ORDER BY id',(case,))],
                    'mensajes':[dict(r) for r in c.execute('SELECT fecha,rol,texto FROM mensajes WHERE caso=? ORDER BY id',(case,))]}

@contextmanager
def bloqueo(path):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    # Bloqueo del SO: se libera automáticamente al morir el proceso.
    with path.open('a+b') as f:
        f.seek(0);f.write(b'0');f.flush();f.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError:
            raise ValueError('El expediente ya se está procesando')
        try: yield
        finally:
            f.seek(0)
            if os.name=='nt': msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
            else: fcntl.flock(f,fcntl.LOCK_UN)

def inventario(case_dir):
    case_dir=Path(case_dir).resolve()
    folder=case_dir/'documentos'
    if not folder.is_dir(): raise ValueError('Crear la subcarpeta documentos')
    # Verificar también el propio directorio documentos antes de enumerarlo.
    dentro(case_dir,'documentos')
    files=[]
    for p in sorted(folder.rglob('*')):
        relative=p.relative_to(case_dir)
        safe=dentro(case_dir,relative)
        if not safe.is_file(): continue
        if safe.name.startswith('~$') or safe.suffix.lower() in ('.tmp','.part','.crdownload'):
            raise ValueError('Esperando que termine la copia de archivos')
        stat=safe.stat()
        if getattr(stat,'st_file_attributes',0)&(0x1000|0x400000):
            raise ValueError('Archivo solo en la nube; seleccionar conservar siempre en este dispositivo')
        if stat.st_size>30_000_000 or stat.st_size==0: raise ValueError('Archivo vacío o mayor de 30 MB')
        files.append({'archivo':relative.as_posix(),'bytes':stat.st_size,'sha256':sha(safe.read_bytes())})
        if len(files)>100: raise ValueError('Máximo 100 archivos por expediente')
    if not files: raise ValueError('La carpeta documentos está vacía')
    return files

def iniciar(case_dir,procedure='ampliacion_consultores',solicitante='Por identificar',sintetico=False):
    case_dir=Path(case_dir).resolve()
    if procedure not in MODULOS: raise ValueError('Procedimiento desconocido')
    case_dir.mkdir(parents=True,exist_ok=True)
    path=case_dir/'expediente.json'
    if path.exists(): raise ValueError('El expediente ya existe; conservar y editar su ficha')
    (case_dir/'documentos').mkdir(exist_ok=True)
    config={'id':case_dir.name,'procedimiento':procedure,'solicitante':solicitante,'sintetico':sintetico,
            'fecha_solicitud':None,'tipo_persona':None,'origen_proveedor':None,'domicilio':None,
            'historial_rnp_disponible':None,'primera_ampliacion_tras_recategorizacion':None,
            'tramite_en_curso_transicion':None,'categoria_solicitada':None,'experiencias':[],
            'tipo_registro':None,'tipo_tramite':None,'clase_actualizacion':None,'motivo_actualizacion':None,
            'documentos_extranjeros':None,'documentos_en_espanol':None,'actua_por_representante':None}
    guardar(path,config); guardar(case_dir/'hechos.json',[])
    return config

def preparar(case_dir,memoria,usar_ocr=True):
    case_dir=Path(case_dir).resolve(); config_raw=(case_dir/'expediente.json').read_bytes(); config=leer(case_dir/'expediente.json')
    if not isinstance(config.get('id'),str) or not config['id'].strip(): raise ValueError('ID de expediente requerido')
    if not isinstance(config.get('solicitante'),str): raise ValueError('Nombre del solicitante inválido')
    originals=inventario(case_dir); docs=[]; duplicates=[]; hashes=set()
    for item in originals:
        source=dentro(case_dir,item['archivo'])
        if item['sha256'] in hashes:
            duplicates.append(item['archivo']);continue
        hashes.add(item['sha256'])
        if source.suffix.lower() not in EXTENSIONS:
            content={'sha256':item['sha256'],'fragmentos':[], 'advertencias':['Formato pendiente de conversión; no se omite el original']}
        else:
            content=leer_documento(source,memoria.root/'lecturas',usar_ocr)
        if item['sha256']!=content['sha256']: raise ValueError('Original cambió durante la preparación')
        docs.append({**item,**content,'id':'D'+item['sha256'][:12]})
    facts_path=case_dir/'hechos.json'
    facts_raw=facts_path.read_bytes() if facts_path.exists() else b'[]'
    import json
    from .lectura import aplicar_cotejos
    checks_path=case_dir/'cotejos.json'
    checks_raw=checks_path.read_bytes() if checks_path.exists() else b'[]'
    aplicar_cotejos(docs,json.loads(checks_raw))
    result=evaluar(config,docs,json.loads(facts_raw))
    from .requisitos import planificar,verificar
    plan=planificar(config)
    if plan['estado']=='plan_de_revision':
        plan['integridad_fuentes']=verificar()
        result['plan_documental']=plan
    analysis_path=case_dir/'analisis.json'
    analysis_raw=analysis_path.read_bytes() if analysis_path.exists() else b'[]'
    analysis=json.loads(analysis_raw)
    from .biblioteca import validar_normas
    norms_path=case_dir/'normas.json'
    norms_raw=norms_path.read_bytes() if norms_path.exists() else b'[]'
    norms=validar_normas(json.loads(norms_raw))
    known={row['id'] for row in result['matriz']}|{d['id'] for d in docs}|{n['codigo'] for n in norms}
    if not isinstance(analysis,list) or len(analysis)>100: raise ValueError('Análisis inválido')
    for para in analysis:
        if not isinstance(para.get('texto'),str) or not para.get('autor') or not para.get('referencias'):
            raise ValueError('Cada párrafo analítico requiere texto, autor y referencias')
        if any(ref not in known for ref in para['referencias']): raise ValueError('Referencia de análisis inexistente')
    dependencies={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted((ROOT/'oece').glob('*.py'))}
    for rel in ('rules/consultores/criterios-documentales.v1.json','rules/procedimientos.v1.1.json','rules/finanzas.v1.2.json','rules/requisitos-ampliaciones.v1.5.json','normativa/indice-tupa.v0.1.json','normativa/decisiones-piloto.v0.3.json','normativa/catalogo.json','templates/informe.v1.json','scripts/ocr_windows.ps1'):
        dependencies[rel]=sha((ROOT/rel).read_bytes())
    if plan['sha256_registro']!=dependencies['rules/requisitos-ampliaciones.v1.5.json']:
        raise ValueError('El registro de requisitos cambió durante la preparación; reintentar')
    snapshot={'version':__version__,'config_sha256':sha(config_raw),'hechos_sha256':sha(facts_raw),'cotejos_sha256':sha(checks_raw),
              'analisis_sha256':sha(analysis_raw),'normas_sha256':sha(norms_raw),'archivos':originals,'dependencias':dependencies,
              'runtime':{'python':sys.version.split()[0],**{n:importlib.metadata.version(n) for n in ('pypdf','python-docx','Pillow')}},
              'extraccion_sha256':sha(bytes_json(docs))}
    execution=sha(bytes_json(snapshot));counts=dict(Counter(row['resultado'] for row in result['matriz']))
    questions=list(result['seleccion']['preguntas'])
    questions.extend(f'{r["id"]}: {r["motivo"]}' for r in result['matriz'] if r['resultado'] in ('no_determinable','no_cumple'))
    for d in docs:
        if d['advertencias']: questions.extend(d['id']+': '+w for w in d['advertencias'])
    if config_raw!=(case_dir/'expediente.json').read_bytes() or inventario(case_dir)!=originals:
        raise ValueError('El expediente cambió durante la preparación')
    conclusion='Se propone completar o aclarar los puntos señalados antes de emitir una conclusión favorable sobre el trámite.' if questions else 'Las verificaciones documentales ejecutadas no presentan diferencias. Corresponde revisar la propuesta y adoptar la decisión administrativa por el órgano competente.'
    result.update(id_ejecucion=execution,expediente=config['id'],solicitante=config['solicitante'],
                  procedimiento=config['procedimiento'],titulo=MODULOS[config['procedimiento']],sintetico=config.get('sintetico') is True,
                  fecha_solicitud=config.get('fecha_solicitud'),instantanea=snapshot,documentos=docs,duplicados=duplicates,
                  conteo=counts,preguntas=list(dict.fromkeys(questions)),conclusion=conclusion,analisis=analysis,normas_adicionales=norms,
                  resumen=f'Borrador documental de {MODULOS[config["procedimiento"]].lower()}. '+('Se examinó un documento.' if len(docs)==1 else f'Se examinaron {len(docs)} documentos distintos.')+' La conclusión se limita al alcance y a las evidencias indicadas.',
                  antecedentes=[f'Se recibió la documentación de {config["solicitante"]} para {MODULOS[config["procedimiento"]].lower()}.',
                                'Fecha de solicitud declarada: '+str(config.get('fecha_solicitud') or 'por precisar')+'.'])
    return result, {'expediente.json':config_raw,'hechos.json':facts_raw,'analisis.json':analysis_raw,'normas.json':norms_raw,'cotejos.json':checks_raw}

def verificar_entrega(folder):
    folder=Path(folder);manifest=leer(folder/'entrega.json')
    for name,digest in manifest['archivos'].items():
        if sha(dentro(folder,name).read_bytes())!=digest: raise ValueError('Entrega conservada alterada: '+name)
    return manifest

def procesar(case_dir,memoria,usar_ocr=True):
    case_dir=Path(case_dir).resolve()
    key=sha(str(case_dir).encode())
    with bloqueo(memoria.root/'bloqueos'/key):
        memoria.evento(key,'extrayendo')
        try:
            result,raws=preparar(case_dir,memoria,usar_ocr)
            output=case_dir/'salida';output.mkdir(exist_ok=True)
            dentro(case_dir,'salida')
            final=output/result['id_ejecucion']
            if final.exists():
                verificar_entrega(final)
                memoria.evento(key,'borrador','Entrega íntegra reutilizada '+final.name)
                return final,True
            temporary=Path(tempfile.mkdtemp(prefix='.preparando-',dir=output))
            try:
                (temporary/'originales').mkdir()
                for n,item in enumerate(result['instantanea']['archivos'],1):
                    source=dentro(case_dir,item['archivo']);raw=source.read_bytes()
                    if sha(raw)!=item['sha256']: raise ValueError('Original cambió antes de conservarlo')
                    (temporary/'originales'/f'{n:03d}{source.suffix.lower()}').write_bytes(raw)
                for name,raw in raws.items():
                    source=case_dir/name
                    if source.exists() and source.read_bytes()!=raw: raise ValueError('La configuración, hechos o análisis cambiaron')
                    (temporary/name).write_bytes(raw)
                guardar(temporary/'matriz.json',result)
                with (temporary/'matriz.csv').open('w',encoding='utf-8-sig',newline='') as stream:
                    writer=csv.writer(stream);writer.writerow(['Control','Resultado','Punto','Motivo','Evidencias','Fuente normativa'])
                    for row in result['matriz']:
                        src=row['fuente_normativa']
                        values=[row['id'],row['resultado'],row['control'],row['motivo'],
                                '; '.join(e['documento']+' '+e['ubicacion'] for e in row['evidencias']),
                                src['disposicion']+' p. '+str(src['pagina_pdf']) if src else 'Por motivar en análisis asistido']
                        writer.writerow([csv_seguro(v) for v in values])
                redactar(result,temporary/'informe.docx')
                for rel,digest in result['instantanea']['dependencias'].items():
                    if sha((ROOT/rel).read_bytes())!=digest: raise ValueError('La implementación o criterios cambiaron durante la entrega; reintentar')
                files={p.relative_to(temporary).as_posix():sha(p.read_bytes()) for p in sorted(temporary.rglob('*')) if p.is_file()}
                guardar(temporary/'entrega.json',{'id_ejecucion':result['id_ejecucion'],'fecha':now(),'archivos':files,
                                                'estado':'borrador','alcance':result['alcance']})
                # OneDrive/antivirus puede retener un handle tras cerrar el Word.
                # Reintentar únicamente la publicación atómica, sin sobrescribir.
                for attempt in range(5):
                    try:
                        os.rename(temporary,final)
                        break
                    except PermissionError:
                        if final.exists() or attempt==4: raise
                        time.sleep(.15*(2**attempt))
            finally:
                if temporary.exists():
                    if temporary.resolve().parent!=output.resolve(): raise ValueError('Temporal fuera del destino')
                    shutil.rmtree(temporary)
            memoria.evento(key,'requiere_datos' if result['preguntas'] else 'borrador',final.name)
            return final,False
        except Exception as error:
            memoria.evento(key,'error_recuperable',type(error).__name__)
            raise
