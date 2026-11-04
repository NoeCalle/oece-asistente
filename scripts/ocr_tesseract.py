"""Procesa en Ubuntu un trabajo OCR generado por preparar_ocr.py.

Mismos contratos JSON, límites, hashes y cotejos posteriores del OCR Windows.
"""
import argparse
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from oece.comun import guardar, leer, sha
from oece.lectura import _ocr_tesseract


def ejecutar(job_path, root=None):
    job_path=Path(job_path).resolve()
    root=Path(root).resolve() if root is not None else job_path.parent
    if root not in job_path.parents:
        raise ValueError('Trabajo OCR fuera de la raíz elegida')
    task=leer(job_path)
    pages=task.get('pages')
    if not isinstance(pages,list) or not 1<=len(pages)<=10:
        raise ValueError('Seleccionar de 1 a 10 páginas OCR')
    deadline=time.monotonic()+120
    results=[]
    for page in pages:
        number=page.get('page_pdf')
        if type(number) is not int or number<1:
            raise ValueError('Página OCR inválida')
        image=Path(page['image_path']).resolve()
        output=Path(page['output_path']).resolve()
        if not all(root in p.parents for p in (image,output)):
            raise ValueError('Archivo OCR fuera de raíz')
        image_sha=sha(image.read_bytes())
        if page.get('image_sha256')!=image_sha:
            raise ValueError('La imagen cambió antes del OCR')
        remaining=int(deadline-time.monotonic())
        if remaining<=0:
            raise ValueError('Límite de 120 segundos OCR por lote')
        rec=_ocr_tesseract(image,task['source_sha256'],image_sha,number,
                           max(1,min(45,remaining)))
        rec['source_name']=task['source_name']
        if sha(image.read_bytes())!=image_sha:
            raise ValueError('La imagen cambió durante el OCR')
        guardar(output,rec)
        results.append({'page_pdf':number,'output':str(output),'characters':len(rec['text'])})
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job',required=True,type=Path)
    parser.add_argument('--root',type=Path)
    args=parser.parse_args()
    import json
    print(json.dumps(ejecutar(args.job,args.root),ensure_ascii=False,indent=2))
