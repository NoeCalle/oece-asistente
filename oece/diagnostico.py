"""Comprobación local de preparación; no instala, conecta cuentas ni acredita vigencia."""
from datetime import date
import importlib.metadata
from pathlib import Path
import shutil
import sqlite3
import sys

from . import __version__
from .comun import ROOT,dentro,sha


def comprobar(fecha_caso=None):
    from .biblioteca import fuentes
    from .preparacion import verificar
    from .lectura import binario
    checks=[]
    def add(name,ok,detail):checks.append({'nombre':name,'ok':bool(ok),'detalle':detail})
    add('Python',sys.version_info>=(3,12),sys.version.split()[0])
    for module,distribution in [('pypdf','pypdf'),('docx','python-docx'),('PIL','Pillow'),('pdfplumber','pdfplumber')]:
        try:__import__(module);add(distribution,True,importlib.metadata.version(distribution))
        except (ImportError,importlib.metadata.PackageNotFoundError):add(distribution,False,'Instalar dependencias de requirements-indexacion.txt')
    originals=fuentes();missing=[];changed=[]
    for item in originals:
        p=dentro(ROOT,item['local_path'])
        if not p.is_file():missing.append(item['name'])
        elif sha(p.read_bytes())!=item['sha256']:changed.append(item['name'])
    add('Biblioteca original',not missing and not changed,{'esperados':len(originals),'faltantes':missing,'alterados':changed})
    index=ROOT/'normativa/indices/biblioteca-v1.sqlite'
    try:
        with sqlite3.connect(index.resolve().as_uri()+'?mode=ro',uri=True) as c:
            count=c.execute('SELECT count(*) FROM fragmentos').fetchone()[0]
        add('Búsqueda normativa',count>0,{'fragmentos':count})
    except (sqlite3.Error,OSError):add('Búsqueda normativa',False,'Reconstruir índice con python -m oece biblioteca --reconstruir')
    try:add('Plan de cinco trámites',True,verificar())
    except (ValueError,OSError,ImportError,KeyError) as error:add('Plan de cinco trámites',False,str(error))
    try:binario('pdftoppm.exe');poppler=True
    except ValueError:poppler=False
    ocr=bool(poppler and shutil.which('powershell.exe'))
    cutoff=date(2026,10,31);requested=date.fromisoformat(fecha_caso) if fecha_caso else date.today()
    return {'version':__version__,'estado':'preparado_para_borradores_asistidos' if all(c['ok'] for c in checks) else 'requiere_preparacion',
            'comprobaciones':checks,'ocr_windows_disponible':ocr,'corte_documental':cutoff.isoformat(),
            'fecha_considerada':requested.isoformat(),'requiere_revision_normativa_por_fecha':requested>cutoff,
            'mensaje_normativo':'Verificar fuentes y reglas de las fechas del expediente; la comprobación técnica no acredita vigencia.',
            'api_de_modelo_requerida':False,'cliente_ia':'El asistente conversacional elegido aporta la interpretación; no se conecta automáticamente a otro cliente.'}
