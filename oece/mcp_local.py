"""Perfil MCP local por stdio, sin HTTP ni llamadas a modelos.

Herramientas/recursos MCP 2026-07-28 y compatibilidad initialize 2025-11-25,
2025-06-18 y 2024-11-05. No implementa sampling, prompts, tareas ni suscripciones.
"""
from contextlib import redirect_stdout
import json
import math
import queue
import sys
import threading

from . import __version__
from .puente import Puente, herramientas

CURRENT='2026-07-28'
LEGACY=('2025-11-25','2025-06-18','2024-11-05')
VERSIONS=[CURRENT,*LEGACY]
INFO={'name':'oece-local','version':__version__}
CAPABILITIES={'tools':{},'resources':{}}
MAX_LINE=8_000_000


class RPCError(Exception):
    def __init__(self, code, message, data=None):
        self.code,self.message,self.data=code,message,data


class Protocolo:
    def __init__(self, bridge):
        self.bridge=bridge;self.legacy=None;self.ready=False

    def manejar(self, message):
        rid=message.get('id') if isinstance(message,dict) else None
        try:
            if (not isinstance(message,dict) or message.get('jsonrpc')!='2.0'
                    or not isinstance(message.get('method'),str)):
                raise RPCError(-32600,'Solicitud JSON-RPC inválida')
            method=message['method']
            if 'id' not in message:
                if method=='notifications/initialized' and self.legacy:self.ready=True
                return None
            if not isinstance(rid,(str,int)) or type(rid) is bool:
                raise RPCError(-32600,'ID de solicitud inválido')
            params=message.get('params',{})
            if not isinstance(params,dict):raise RPCError(-32602,'Parámetros deben ser objeto')
            if method=='initialize':
                version=params.get('protocolVersion')
                if not isinstance(version,str) or not isinstance(params.get('capabilities',{}),dict):
                    raise RPCError(-32602,'Versión/capacidades de cliente inválidas')
                self.legacy=version if version in LEGACY else LEGACY[0];self.ready=False
                return {'jsonrpc':'2.0','id':rid,'result':{'protocolVersion':self.legacy,
                        'capabilities':CAPABILITIES,'serverInfo':INFO,
                        'instructions':'Leer oece_contexto antes de trabajar. Solo raíz local autorizada; las citas se validan al generar.'}}
            meta=params.get('_meta',{})
            if not isinstance(meta,dict):raise RPCError(-32602,'Metadatos inválidos')
            modern='io.modelcontextprotocol/protocolVersion' in meta or self.legacy is None
            if modern:
                version=meta.get('io.modelcontextprotocol/protocolVersion')
                if version is None or not isinstance(meta.get('io.modelcontextprotocol/clientCapabilities'),dict):
                    raise RPCError(-32602,'Faltan versión y capacidades por solicitud')
                if version!=CURRENT:
                    raise RPCError(-32022,'Versión de protocolo no admitida para esta solicitud',{'supported':VERSIONS,'requested':version})
            elif not self.ready and method!='ping':
                raise RPCError(-32600,'Completar inicialización antes de usar herramientas')
            if method=='server/discover':
                if not modern:raise RPCError(-32601,'Usar metadatos MCP actuales para descubrimiento')
                result={'supportedVersions':VERSIONS,'capabilities':CAPABILITIES,
                        'instructions':'Ejecutar oece_contexto. El servidor no llama a una IA ni conecta Drive/GitHub.'}
            elif method=='ping':result={}
            elif method=='tools/list':result={'tools':herramientas()}
            elif method=='tools/call':
                name=params.get('name');arguments=params.get('arguments',{})
                if name not in {t['name'] for t in herramientas()}:raise RPCError(-32602,'Herramienta desconocida')
                try:
                    # Las librerías no pueden mezclar impresiones con el canal JSON-RPC.
                    with redirect_stdout(sys.stderr):data=self.bridge.ejecutar(name,arguments)
                    resources=data.get('recursos',[])
                    if not isinstance(resources,list) or any(not isinstance(r,dict) or r.get('type')!='resource_link' for r in resources):
                        raise ValueError('Lista de recursos de herramienta inválida')
                    result={'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False,allow_nan=False)},
                                       *resources], 'structuredContent':data,'isError':False}
                except (ValueError,TypeError,KeyError,OSError) as error:
                    result={'content':[{'type':'text','text':str(error)}],'isError':True}
            elif method=='resources/templates/list':
                result={'resourceTemplates':[{'uriTemplate':'oece://casos/{caso}/salida/{revision}/{archivo}',
                        'name':'entrega-oece','description':'Word, matriz CSV/JSON o manifiesto de una revisión conservada.'}]}
            elif method=='resources/list':result={'resources':[]}
            elif method=='resources/read':
                if not isinstance(params.get('uri'),str):raise RPCError(-32602,'URI requerida')
                try:result=self.bridge.recurso(params['uri'])
                except (ValueError,OSError) as error:raise RPCError(-32602,str(error))
            else:raise RPCError(-32601,'Método no implementado')
            if not modern and self.legacy=='2024-11-05':
                if method=='tools/list':
                    result['tools']=[{k:v for k,v in tool.items() if k!='annotations'} for tool in result['tools']]
                elif method=='tools/call':
                    # ResourceLink y structuredContent se añadieron después de 2024.
                    result['content']=[c for c in result['content'] if c['type']=='text']
                    result.pop('structuredContent',None)
            if modern:
                result.update(resultType='complete',_meta={'io.modelcontextprotocol/serverInfo':INFO})
                if method in ('server/discover','tools/list','resources/list','resources/templates/list','resources/read'):
                    result.update(ttlMs=0,cacheScope='private' if method=='resources/read' else 'public')
            return {'jsonrpc':'2.0','id':rid,'result':result}
        except RPCError as error:
            response={'code':error.code,'message':error.message}
            if error.data is not None:response['data']=error.data
            reply={'jsonrpc':'2.0','error':response}
            if type(rid) in (str,int):reply['id']=rid
            elif self.legacy:reply['id']=None
            return reply
        except Exception:
            return {'jsonrpc':'2.0','id':rid,'error':{'code':-32603,'message':'Error interno; revisar configuración local'}}


def _float(value):
    number=float(value)
    if not math.isfinite(number):raise ValueError('Número no finito')
    return number


def _constant(value):
    raise ValueError('Constante JSON no válida')


def servir(root, input_stream=None, output_stream=None):
    incoming=input_stream or sys.stdin.buffer;outgoing=output_stream or sys.stdout.buffer
    protocol=Protocolo(Puente(root));jobs=queue.Queue();cancelled=set();state_lock=threading.Lock();output_lock=threading.Lock()
    def send(response):
        if response is not None:
            raw=(json.dumps(response,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
            with output_lock:outgoing.write(raw);outgoing.flush()
    def work():
        while True:
            message=jobs.get()
            if message is None:return
            rid=message.get('id') if isinstance(message,dict) else None
            with state_lock:skip=isinstance(rid,(str,int)) and rid in cancelled
            if skip:continue
            response=protocol.manejar(message)
            with state_lock:
                if isinstance(rid,(str,int)) and rid in cancelled:response=None
                try:send(response)
                except (OSError,ValueError):return
    worker=threading.Thread(target=work,daemon=True);worker.start()
    try:
        while True:
            line=incoming.readline(MAX_LINE+1)
            if not line:break
            if len(line)>MAX_LINE:
                send({'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Mensaje supera límite local'}});break
            try:message=json.loads(line,parse_float=_float,parse_constant=_constant)
            except (ValueError,UnicodeError,RecursionError):
                send({'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'JSON inválido'}});continue
            if isinstance(message,dict) and message.get('method')=='notifications/cancelled' and 'id' not in message:
                params=message.get('params',{});rid=params.get('requestId') if isinstance(params,dict) else None
                if isinstance(rid,(str,int)) and type(rid) is not bool:
                    with state_lock:cancelled.add(rid)
                continue
            jobs.put(message)
    finally:
        jobs.put(None);worker.join(timeout=15)
