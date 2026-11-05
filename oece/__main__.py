import argparse
import json
from pathlib import Path
import time

from .comun import data_dir, guardar
from .coordinador import observar_una_vez, responder
from .flujo import Memoria, iniciar, preparar, procesar
from .evaluacion import MODULOS

def main():
    p=argparse.ArgumentParser(description='OECE Assistant local')
    p.add_argument('--memoria',type=Path,default=data_dir()/'operacion/.oece')
    sub=p.add_subparsers(dest='accion',required=True)
    new=sub.add_parser('nuevo');new.add_argument('carpeta',type=Path);new.add_argument('--procedimiento',choices=MODULOS,default='ampliacion_consultores');new.add_argument('--solicitante',default='Por identificar');new.add_argument('--sintetico',action='store_true')
    for name in ('leer','procesar','estado'):
        cmd=sub.add_parser(name);cmd.add_argument('carpeta',type=Path);cmd.add_argument('--sin-ocr',action='store_true')
    chat=sub.add_parser('conversar');chat.add_argument('carpeta',type=Path);chat.add_argument('mensaje')
    watch=sub.add_parser('observar');watch.add_argument('raiz',type=Path,nargs='?',default=data_dir()/'operacion');watch.add_argument('--una-vez',action='store_true');watch.add_argument('--intervalo',type=int,default=10)
    server=sub.add_parser('panel');server.add_argument('--raiz',type=Path,default=data_dir()/'operacion');server.add_argument('--puerto','--port',dest='puerto',type=int,default=8765);server.add_argument('--host',default='127.0.0.1')
    library=sub.add_parser('biblioteca');library.add_argument('--reconstruir',action='store_true');library.add_argument('--buscar');library.add_argument('--indice',type=Path,default=data_dir()/'normativa/indices/biblioteca-v1.sqlite')
    tupa=sub.add_parser('tupa');tupa.add_argument('carpeta',type=Path);tupa.add_argument('--codigo');tupa.add_argument('--pagina',type=int)
    req=sub.add_parser('requisitos');req.add_argument('carpeta',type=Path)
    diag=sub.add_parser('diagnostico');diag.add_argument('--fecha')
    ia=sub.add_parser('analizar-ia');ia.add_argument('carpeta',type=Path)
    ia.add_argument('--autorizar-envio',action='store_true')
    ia.add_argument('--previsualizar',action='store_true')
    cmc=sub.add_parser('formatos-cmc');cmc.add_argument('carpeta',type=Path);cmc.add_argument('--modelo',action='store_true')
    migration=sub.add_parser('migrar-rutas');migration.add_argument('--ruta',type=Path);migration.add_argument('--simular',action='store_true')
    backup=sub.add_parser('respaldar');backup.add_argument('carpeta',type=Path);backup.add_argument('archivo',type=Path)
    restore=sub.add_parser('restaurar');restore.add_argument('archivo',type=Path);restore.add_argument('destino',type=Path)
    args=p.parse_args()
    if args.accion=='migrar-rutas':
        from .migracion_rutas import migrar
        print(json.dumps(migrar(args.ruta,preview=args.simular),ensure_ascii=False,indent=2))
        return
    if args.accion=='analizar-ia':
        from .agentes_ia import analizar,previsualizar
        result=(previsualizar(args.carpeta) if args.previsualizar else
                analizar(args.carpeta,autorizar_envio=args.autorizar_envio))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return
    if args.accion=='formatos-cmc':
        from .formatos_cmc import publicar,modelo_vacio
        from .comun import leer,dentro
        result=(modelo_vacio(leer(dentro(args.carpeta,'expediente.json')))
                if args.modelo else publicar(args.carpeta))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return
    memory=Memoria(args.memoria)
    if args.accion=='nuevo': result=iniciar(args.carpeta,args.procedimiento,args.solicitante,args.sintetico)
    elif args.accion in ('leer','estado'):
        result,_=preparar(args.carpeta,memory,not args.sin_ocr)
        if args.accion=='leer':
            guardar(args.carpeta/'lectura.json',result)
            result={'lectura':str(args.carpeta/'lectura.json'),'documentos':len(result['documentos']),'preguntas':result['seleccion']['preguntas']}
        else: result={k:result[k] for k in ('resumen','conteo','preguntas','seleccion')}
    elif args.accion=='procesar':
        final,reused=procesar(args.carpeta,memory,not args.sin_ocr);result={'entrega':str(final),'reutilizada':reused}
    elif args.accion=='conversar': result={'respuesta':responder(args.carpeta,memory,args.mensaje)}
    elif args.accion=='observar':
        while True:
            print(json.dumps(observar_una_vez(args.raiz,memory),ensure_ascii=True),flush=True)
            if args.una_vez: return
            time.sleep(max(3,args.intervalo))
    elif args.accion=='biblioteca':
        from .biblioteca import construir,buscar
        result=construir(args.indice,memory.root/'biblioteca-lecturas') if args.reconstruir else buscar(args.indice,args.buscar or '')
    elif args.accion=='tupa':
        from .comun import leer
        from .tupa import consultar
        result=consultar(leer(args.carpeta/'expediente.json'),args.codigo,args.pagina)
    elif args.accion=='requisitos':
        from .comun import leer
        from .preparacion import planificar,verificar
        result={**planificar(leer(args.carpeta/'expediente.json')),'integridad_fuentes':verificar()}
    elif args.accion=='diagnostico':
        from .diagnostico import comprobar
        result=comprobar(args.fecha)
    elif args.accion=='respaldar':
        from .respaldo import crear
        result=crear(args.carpeta,args.archivo)
    elif args.accion=='restaurar':
        from .respaldo import restaurar
        result=restaurar(args.archivo,args.destino)
    else:
        from .panel import servir
        servir(args.raiz,memory,args.puerto,host=args.host);return
    print(json.dumps(result,ensure_ascii=True,indent=2))

if __name__=='__main__': main()
