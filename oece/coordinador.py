"""Comandos locales, vigilancia estable y conversación guiada persistente.

El análisis abierto con IA lo realiza el cliente elegido con AGENTS.md. Este componente
ejecuta herramientas deterministas; no simula respuestas de un modelo.
"""
import json
from pathlib import Path
import time

from .comun import guardar, leer, sha, bytes_json
from .flujo import Memoria, inventario, procesar

def firma(case_dir):
    case_dir=Path(case_dir)
    value={'documentos':inventario(case_dir)}
    for name in ('expediente.json','hechos.json','analisis.json','normas.json','cotejos.json'):
        path=case_dir/name
        value[name]=sha(path.read_bytes()) if path.exists() else None
    return sha(bytes_json(value))

def observar_una_vez(root,memoria,estable_segundos=3,usar_ocr=True):
    root=Path(root).resolve()
    state_file=memoria.root/'vigilancia.json'
    state=leer(state_file) if state_file.exists() else {}
    results=[]
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.') or folder.is_symlink() or (hasattr(folder,'is_junction') and folder.is_junction()): continue
        if not (folder/'LISTO').is_file() or not (folder/'expediente.json').is_file(): continue
        key=sha(str(folder).encode())
        try:
            current=firma(folder)
            previous=state.get(key,{})
            if previous.get('firma')!=current:
                state[key]={'firma':current,'observado':time.time(),'procesada':False,'intentos':0}
                results.append({'caso':folder.name,'estado':'esperando_archivos'})
            elif previous.get('procesada'):
                # Una entrega alterada no se da por válida en silencio.
                from .flujo import verificar_entrega
                verificar_entrega(Path(previous['entrega']))
            elif time.time()-previous.get('observado',0)>=estable_segundos and previous.get('intentos',0)<3:
                previous['intentos']=previous.get('intentos',0)+1
                try:
                    final,reused=procesar(folder,memoria,usar_ocr)
                    previous.update(procesada=True,entrega=str(final))
                    results.append({'caso':folder.name,'estado':'borrador','entrega':str(final),'reutilizada':reused})
                except Exception as e:
                    previous['error']=type(e).__name__+': '+str(e)
                    results.append({'caso':folder.name,'estado':'error_recuperable','motivo':previous['error']})
                state[key]=previous
        except (ValueError,OSError,json.JSONDecodeError) as e:
            results.append({'caso':folder.name,'estado':'requiere_atencion','motivo':str(e)})
    guardar(state_file,state)
    return results

def responder(case_dir,memoria,mensaje):
    case_dir=Path(case_dir).resolve();key=sha(str(case_dir).encode())
    memoria.mensaje(key,'usuario',mensaje)
    text=mensaje.casefold().strip()
    if any(t in text for t in ('prepara','generar','informe','procesa')):
        final,reused=procesar(case_dir,memoria)
        answer='Borrador y matriz disponibles en '+str(final)+'. '+('Se reutilizó la entrega íntegra.' if reused else 'Se conservó una revisión nueva.')
    elif any(t in text for t in ('falta','observa','estado','cómo','como')):
        from .flujo import preparar
        result,_=preparar(case_dir,memoria)
        answer=result['resumen']+'\n'+'\n'.join(result['preguntas'])
    else:
        answer='Puedo mostrar el estado, listar los datos faltantes o preparar el informe. Para analizar el contenido, usa tu asistente con acceso autorizado a este expediente y las herramientas OECE; AGENTS.md conserva el procedimiento de trabajo.'
    memoria.mensaje(key,'coordinador',answer)
    return answer
