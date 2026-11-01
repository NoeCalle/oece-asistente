"""Prueba del protocolo local sin invocar ni simular un modelo de IA."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def probar(root):
    meta={'io.modelcontextprotocol/protocolVersion':'2026-07-28','io.modelcontextprotocol/clientCapabilities':{},
          'io.modelcontextprotocol/clientInfo':{'name':'oece-portability-probe','version':'1.0'}}
    messages=[{'jsonrpc':'2.0','id':1,'method':'server/discover','params':{'_meta':meta}},
              {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{'_meta':meta}},
              {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'oece_contexto','arguments':{},'_meta':meta}},
              {'jsonrpc':'2.0','id':4,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'oece-legacy-probe','version':'1.0'}}},
              {'jsonrpc':'2.0','method':'notifications/initialized'},
              {'jsonrpc':'2.0','id':5,'method':'tools/list','params':{}}]
    response=subprocess.run([sys.executable,str(Path(__file__).resolve().with_name('servidor_mcp.py')),'--raiz',str(Path(root).resolve())],
                            input=''.join(json.dumps(m)+'\n' for m in messages).encode(),capture_output=True,timeout=30)
    if response.returncode:raise RuntimeError('El proceso MCP terminó con error')
    rows={m['id']:m for m in [json.loads(line) for line in response.stdout.splitlines()]}
    if set(rows)!={1,2,3,4,5} or any('error' in m for m in rows.values()):raise RuntimeError('Respuesta MCP inesperada')
    tools={t['name'] for t in rows[2]['result']['tools']}
    if tools!={t['name'] for t in rows[5]['result']['tools']}:raise RuntimeError('Catálogo incompatible entre protocolos')
    context=rows[3]['result']['structuredContent']
    if rows[3]['result']['isError'] or [c['type'] for c in rows[3]['result']['content']]!=['text']:
        raise RuntimeError('Contenido de contexto MCP inválido')
    return {'protocolo_actual':True,'compatibilidad_initialize':True,'herramientas':len(tools),
            'version_oece':context['version'],'api_modelo_usada':False,'cliente_real_claude_validado':False,
            'fuentes_locales':context['fuentes_locales'],'stdout_solo_json':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--raiz',type=Path,required=True);args=parser.parse_args()
    print(json.dumps(probar(args.raiz),ensure_ascii=False,indent=2))
