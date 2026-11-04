"""Genera configuración local MCP para revisar/importar; no edita clientes."""
import argparse
import json
from pathlib import Path
import sys
import os


def configurar(root=None, python=None):
    selected = Path(root) if root is not None else Path(os.environ.get('OECE_DATA_DIR', './data')).expanduser()/'operacion'
    return {'mcpServers':{'oece':{'command':str(Path(python or sys.executable).resolve()),
            'args':[str(Path(__file__).resolve().with_name('servidor_mcp.py')),'--raiz',str(selected.resolve())],
            'env':{'PYTHONIOENCODING':'utf-8','PYTHONUNBUFFERED':'1'}}}}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Preparar configuración MCP sin API de modelo')
    parser.add_argument('--raiz',type=Path)
    parser.add_argument('--python',type=Path)
    parser.add_argument('--salida',type=Path,default=Path(os.environ.get('OECE_DATA_DIR', './data')).expanduser()/'config/oece-mcp.json')
    args=parser.parse_args();args.salida.parent.mkdir(parents=True,exist_ok=True)
    args.salida.write_text(json.dumps(configurar(args.raiz,args.python),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(args.salida.resolve()))
