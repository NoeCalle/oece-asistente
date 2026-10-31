"""Panel local sin servicios externos; acciones con token y origen verificado."""
import base64
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import threading
from urllib.parse import parse_qs, urlsplit
import uuid

from .comun import ROOT, dentro, guardar, leer, sha
from .coordinador import observar_una_vez
from .flujo import iniciar, procesar, verificar_entrega

def crear_servidor(root,memory,port=8765):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    token=secrets.token_hex(32);pool=ThreadPoolExecutor(max_workers=1)
    jobs={};lock=threading.Lock()
    def case(case_id):
        if len(case_id)>80 or not case_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in case_id):
            raise ValueError('Identificador de expediente inválido')
        return dentro(root,case_id)
    def launch(folder):
        key=folder.name
        with lock:
            if jobs.get(key,{}).get('estado')=='procesando': return
            jobs[key]={'estado':'procesando'}
        def run():
            try:
                path,reused=procesar(folder,memory)
                with lock: jobs[key]={'estado':'borrador','revision':path.name,'reutilizada':reused}
            except Exception as e:
                with lock: jobs[key]={'estado':'requiere_atencion','motivo':str(e)}
        pool.submit(run)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def valid_host(self):
            return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
        def send(self,status,payload,mime='application/json; charset=utf-8'):
            raw=payload if isinstance(payload,bytes) else json.dumps(payload,ensure_ascii=True).encode()
            self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(raw)))
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store')
            self.send_header('X-Frame-Options','DENY')
            self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers();self.wfile.write(raw)
        def do_GET(self):
            if not self.valid_host(): self.send(403,{'error':'Host no permitido'});return
            url=urlsplit(self.path);query=parse_qs(url.query)
            try:
                if url.path=='/':
                    page=(ROOT/'web/index.html').read_text(encoding='utf-8').replace('__TOKEN__',token)
                    self.send(200,page.encode(),'text/html; charset=utf-8')
                elif url.path=='/api/casos':
                    items=[]
                    for folder in sorted(root.iterdir()):
                        if not folder.is_dir() or not (folder/'expediente.json').is_file() or folder.name.startswith('.'): continue
                        try:
                            folder=case(folder.name);config=leer(folder/'expediente.json')
                            outputs=folder/'salida'
                            revisions=sorted((d for d in outputs.iterdir() if (d/'entrega.json').is_file()),key=lambda p:p.stat().st_mtime,reverse=True) if outputs.is_dir() else []
                            item={'carpeta':folder.name,'ficha':config,'revisiones':[d.name for d in revisions], 'trabajo':jobs.get(folder.name,{})}
                            if revisions:
                                r=leer(revisions[0]/'matriz.json');item.update(conteo=r['conteo'],preguntas=r['preguntas'])
                            items.append(item)
                        except (ValueError,OSError,json.JSONDecodeError): continue
                    self.send(200,{'casos':items,'raiz':str(root)})
                elif url.path=='/api/pedido':
                    folder=case(query['caso'][0])
                    self.send(200,{'texto':f'Revisa el expediente en {folder}. Sigue AGENTS.md: lee los documentos, completa los hechos con citas verificables, analiza el procedimiento y genera una nueva revisión del informe Word y la matriz. No inventes datos ni registres aprobación humana.'})
                elif url.path=='/descargar':
                    folder=case(query['caso'][0]);revision=query['revision'][0];name=query['archivo'][0]
                    if len(revision)!=64 or any(c not in '0123456789abcdef' for c in revision): raise ValueError('Revisión inválida')
                    if name not in ('informe.docx','matriz.csv','matriz.json','entrega.json'): raise ValueError('Archivo no permitido')
                    target=dentro(folder,'salida/'+revision);verificar_entrega(target)
                    data=dentro(target,name).read_bytes()
                    mime={'informe.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','matriz.csv':'text/csv; charset=utf-8'}.get(name,'application/json')
                    self.send(200,data,mime)
                else: self.send(404,{'error':'No encontrado'})
            except (KeyError,ValueError,OSError,json.JSONDecodeError) as e: self.send(400,{'error':str(e)})
        def do_POST(self):
            origin=self.headers.get('Origin')
            allowed={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
            if not self.valid_host() or self.headers.get('X-OECE-Token')!=token or (origin and origin not in allowed):
                self.send(403,{'error':'Solicitud no autorizada'});return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=45_000_000: raise ValueError('Límite de carga 45 MB por envío')
                data=json.loads(self.rfile.read(length))
                if not isinstance(data,dict): raise ValueError('Se requiere un objeto de datos')
                if self.path=='/api/nuevo':
                    cid='exp-'+uuid.uuid4().hex[:12];folder=case(cid)
                    config=iniciar(folder,data.get('procedimiento','ampliacion_consultores'),data.get('solicitante','Por identificar'))
                    self.send(200,{'caso':cid,'ficha':config})
                elif self.path=='/api/ficha':
                    folder=case(data['caso']);previous=leer(folder/'expediente.json');updates=data['ficha']
                    allowed_keys=set(previous)-{'id','sintetico'}
                    if set(updates)-allowed_keys: raise ValueError('Campo no permitido')
                    previous.update(updates)
                    from .evaluacion import seleccionar
                    seleccionar(previous)
                    guardar(folder/'expediente.json',previous);self.send(200,{'ok':True})
                elif self.path=='/api/archivo':
                    folder=case(data['caso']);name=data['nombre']
                    if not isinstance(name,str) or name!=Path(name.replace('\\','/')).name or name in ('','.','..') or len(name)>180 or any(c in name for c in '<>:"/\\|?*') or name.endswith((' ','.')) or name.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}:
                        raise ValueError('Nombre de archivo inválido')
                    target=dentro(folder,'documentos/'+name)
                    if target.exists(): raise ValueError('Ya existe ese nombre; conservar el original y usar otro nombre para subsanaciones')
                    raw=base64.b64decode(data['contenido'],validate=True)
                    if not 0<len(raw)<=30_000_000: raise ValueError('Archivo vacío o supera 30 MB')
                    if len(list((folder/'documentos').rglob('*')))>=100: raise ValueError('Máximo 100 archivos')
                    # Creación exclusiva para no sobrescribir una incorporación concurrente.
                    with target.open('xb') as stream: stream.write(raw)
                    self.send(200,{'ok':True})
                elif self.path=='/api/procesar':
                    folder=case(data['caso']);launch(folder);self.send(202,{'estado':'procesando'})
                elif self.path=='/api/detener':
                    self.send(200,{'estado':'detenido'})
                    threading.Thread(target=self.server.shutdown,daemon=True).start()
                else: self.send(404,{'error':'No encontrado'})
            except (KeyError,ValueError,OSError,TypeError,json.JSONDecodeError) as e: self.send(400,{'error':str(e)})
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.oece_token=token;server.oece_pool=pool;server.oece_jobs=jobs
    return server

def servir(root,memory,port=8765):
    server=crear_servidor(root,memory,port)
    stop=threading.Event()
    def watch():
        # Preparación automática local; no llama a un modelo ni transmite documentos.
        while not stop.wait(10):
            try: observar_una_vez(root,memory)
            except Exception as e: memory.evento('vigilancia','error_recuperable',type(e).__name__)
    worker=threading.Thread(target=watch,daemon=True);worker.start()
    print(f'OECE Assistant http://127.0.0.1:{server.server_port}',flush=True)
    try: server.serve_forever()
    finally:
        stop.set();server.server_close();server.oece_pool.shutdown(wait=True)
