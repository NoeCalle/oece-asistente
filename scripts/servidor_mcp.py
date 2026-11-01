"""Lanzador stdio independiente del directorio de trabajo y proveedor de IA."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oece.mcp_local import servir

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Herramientas OECE por MCP local; no usa API de modelo')
    parser.add_argument('--raiz',type=Path,required=True,help='Única raíz local autorizada para expedientes')
    args=parser.parse_args()
    servir(args.raiz)
