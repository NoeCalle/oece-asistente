"""Lanzador stdio independiente del directorio de trabajo y proveedor de IA."""
import argparse
import os
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oece.mcp_local import servir
from oece.comun import data_dir

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Herramientas OECE por MCP local; no usa API de modelo')
    parser.add_argument('--raiz',type=Path,default=None,help='Raíz de expedientes; por defecto OECE_DATA_DIR/operacion')
    parser.add_argument('--caso',default=os.environ.get('OECE_MCP_CASO'),
                        help='Expediente único autorizado para esta sesión MCP')
    args=parser.parse_args()
    servir(args.raiz if args.raiz is not None else data_dir()/'operacion',
           caso_autorizado=args.caso)
