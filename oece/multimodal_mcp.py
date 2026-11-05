"""Herramientas documentales multimodales locales para cualquier cliente MCP.

Sin proveedores, claves, HTTP ni llamadas a modelos: la IA del cliente recibe
páginas en imágenes, propone datos/cálculos y OECE valida y publica el borrador.
"""
import base64
from datetime import datetime, timezone
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile

from pypdf import PdfReader

from .agentes_ia import (_generar_word, _leer_validar, comprobar_calculos,
                         previsualizar, validar_referencias, verificar_revision)
from .comun import bytes_json, dentro, guardar, leer, sha
from .flujo import inventario
from .lectura import binario

LECTURAS = "lecturas-ia-trabajo.json"
CALCULOS = "calculos-ia-trabajo.json"
MAX_IMAGEN = 4_000_000


def documento_pdf(case_dir, documento):
    files = inventario(case_dir)
    item = next((f for f in files if "D" + f["sha256"][:12] == documento), None)
    if not item or Path(item["archivo"]).suffix.lower() != ".pdf":
        raise ValueError("ID de PDF no encontrado en el expediente")
    source = dentro(case_dir, item["archivo"])
    reader = PdfReader(source)
    if reader.is_encrypted:
        raise ValueError("PDF cifrado: facilitar copia legible")
    count = len(reader.pages)
    if not count or count > 500:
        raise ValueError("Número de páginas fuera de los límites")
    return item, source, count


def pagina_visual(case_dir, documento, pagina):
    """Devuelve contenido MCP 'image'; nunca se escribe una copia pública."""
    if type(pagina) is not int:
        raise ValueError("Número de página inválido")
    item, source, count = documento_pdf(case_dir, documento)
    if not 1 <= pagina <= count:
        raise ValueError("Página no existe en el documento")
    with tempfile.TemporaryDirectory(prefix="oece-visual-") as folder:
        target = Path(folder) / "pagina"
        try:
            subprocess.run([binario("pdftoppm.exe"), "-f", str(pagina),
                            "-l", str(pagina), "-singlefile", "-scale-to",
                            "2000", "-jpeg", "-jpegopt", "quality=85",
                            str(source), str(target)],
                           check=True, timeout=60, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except (subprocess.SubprocessError, OSError) as error:
            raise ValueError("No se pudo convertir la página; comprobar Poppler") from error
        image = target.with_suffix(".jpg")
        if not image.is_file() or not 0 < image.stat().st_size <= MAX_IMAGEN:
            raise ValueError("Imagen de página ausente o mayor de 4 MB; requiere segmentar")
        raw = image.read_bytes()
    if sha(source.read_bytes()) != item["sha256"]:
        raise ValueError("PDF original modificado durante la conversión")
    return {"documento": documento, "archivo": item["archivo"],
            "sha256": item["sha256"], "pagina": pagina, "paginas": count,
            "mimeType": "image/jpeg", "data": base64.b64encode(raw).decode("ascii"),
            "imagen_sha256": sha(raw),
            "advertencia": "Imagen para interpretación del cliente IA. La lectura no constituye cotejo humano."}


def validar_lecturas(case_dir, items, *, exigir_todos=False):
    """Solo acepta datos con ID/huella/página realmente existentes."""
    if not isinstance(items, list) or len(items) > 25:
        raise ValueError("Máximo 25 lecturas visuales por lote")
    preview = previsualizar(case_dir)
    sources = {"D" + f["sha256"][:12]: f for f in preview["archivos"]}
    seen = set()
    validated = []
    for d in items:
        if not isinstance(d, dict):
            raise ValueError("Registro visual inválido")
        did = d.get("id")
        if did not in sources or did in seen:
            raise ValueError("Documento visual inexistente o duplicado")
        seen.add(did)
        src = sources[did]
        if d.get("sha256") != src["sha256"] or d.get("archivo") != src["archivo"]:
            raise ValueError("Lectura visual no coincide con el PDF original")
        item, source, pages = documento_pdf(case_dir, did)
        if d.get("paginas") != pages:
            raise ValueError("Conteo de páginas alterado")
        if sha(source.read_bytes()) != item["sha256"]:
            raise ValueError("PDF original modificado")
        lectura = d.get("lectura")
        _leer_validar(lectura, pages)
        validated.append({"id": did, "archivo": src["archivo"], "sha256": src["sha256"],
                          "paginas": pages, "lectura": lectura, "cotejo_visual": "pendiente"})
    if exigir_todos and seen != set(sources):
        missing = [src["archivo"] for did, src in sources.items() if did not in seen]
        raise ValueError("Faltan documentos PDF por analizar: " + ", ".join(missing))
    return validated


def leer_lecturas(case_dir):
    path = dentro(case_dir, LECTURAS)
    if not path.is_file():
        raise ValueError("Registrar primero la lectura visual de cada PDF mediante oece_guardar")
    return validar_lecturas(case_dir, leer(path))


def calcular_local(case_dir, operaciones, alertas):
    docs = leer_lecturas(case_dir)
    if not isinstance(operaciones, list) or not isinstance(alertas, list):
        raise ValueError("Operaciones y alertas requieren listas")
    result = comprobar_calculos({"operaciones": operaciones, "alertas": alertas}, docs)
    if len(bytes_json(result)) > 2_000_000:
        raise ValueError("Resultados de cálculo demasiado grandes")
    snap = sha(dentro(case_dir, LECTURAS).read_bytes())
    guardar(dentro(case_dir, CALCULOS),
            {"lecturas_sha256": snap, "resultado": result,
             "responsable": "propuestas del cliente IA, aritmética local Decimal"})
    return result


def publicar_local(case_dir, sintesis, modelo):
    """Crea revisión inmutable de los resultados del cliente, sin invocar una IA."""
    case_dir = Path(case_dir).resolve()
    if not isinstance(modelo, str) or not re.fullmatch(r"[A-Za-z0-9 ._/-]{1,100}", modelo):
        raise ValueError("Nombre de cliente/modelo inválido")
    from .comun import ROOT
    if case_dir == ROOT or (ROOT / "normativa") in case_dir.parents:
        raise ValueError("Carpeta normativa no es expediente")
    preview = previsualizar(case_dir)
    docs = validar_lecturas(case_dir, leer(dentro(case_dir, LECTURAS)), exigir_todos=True)
    validar_referencias(sintesis, docs)
    calculations = dentro(case_dir, CALCULOS)
    if not calculations.is_file():
        raise ValueError("Antes de publicar, utilizar oece_calcular_liquidacion")
    calculation = leer(calculations)
    reading_path = dentro(case_dir, LECTURAS)
    if calculation.get("lecturas_sha256") != sha(reading_path.read_bytes()):
        raise ValueError("Los cálculos no corresponden a las lecturas actuales")
    results = calculation["resultado"]
    if not isinstance(results, dict) or "operaciones" not in results:
        raise ValueError("Resultados de cálculos inválidos")
    # Recalcular las operaciones y verificar que el archivo de trabajo no fue editado.
    original = {"operaciones": [
        {key: operation[key] for key in ("descripcion", "tipo", "operandos",
                                        "resultado_documento", "resultado_fuente", "comentario")}
        for operation in results["operaciones"]], "alertas": results.get("alertas", [])}
    if comprobar_calculos(original, docs) != results:
        raise ValueError("Cálculos locales alterados")
    config = leer(dentro(case_dir, "expediente.json"))
    model = "cliente-mcp:" + modelo
    deps = {"version": "multimodal-mcp-1", "modelo": model, "expediente": config,
            "documentos": preview["todos"], "lecturas_sha256": sha(reading_path.read_bytes()),
            "calculos_sha256": sha(calculations.read_bytes()), "sintesis": sintesis}
    revision = sha(bytes_json(deps))
    folder = dentro(case_dir, "analisis_ia/" + revision)
    if folder.exists():
        verificar_revision(folder)
        return {"revision": revision, "carpeta": str(folder), "reutilizada": True,
                "modelo": model, "estado": "borrador_ia"}
    info = {"version": "multimodal-mcp-1",
            "fecha": datetime.now(timezone.utc).isoformat(),
            "expediente": config, "modelo": model, "documentos": docs,
            "calculos": results, "sintesis": sintesis,
            "omitidos": preview["omitidos"], "estado": "borrador_ia", "aprobado": False,
            "advertencia": "Lecturas de IA sin cotejo humano; sin validación administrativa"}
    out = dentro(case_dir, "analisis_ia")
    out.mkdir(exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".mcp-temporal-", dir=out))
    try:
        guardar(temp / "analisis-ia.json", info)
        guardar(temp / "calculos-ia.json", results)
        guardar(temp / "lecturas-ia.json", docs)
        (temp / "originales").mkdir()
        for n, f in enumerate(preview["archivos"], 1):
            source = dentro(case_dir, f["archivo"])
            dest = temp / "originales" / f"{n:03d}.pdf"
            shutil.copyfile(source, dest)
            if sha(dest.read_bytes()) != f["sha256"]:
                raise ValueError("Original cambiado al generar la revisión")
        _generar_word(info, temp / "informe-ia.docx")
        # Verificar que no cambió el expediente durante la preparación.
        if (inventario(case_dir) != preview["todos"]
                or leer(dentro(case_dir, "expediente.json")) != config
                or sha(reading_path.read_bytes()) != deps["lecturas_sha256"]
                or sha(calculations.read_bytes()) != deps["calculos_sha256"]):
            raise ValueError("Las fuentes cambiaron durante el informe")
        content = {p.relative_to(temp).as_posix(): sha(p.read_bytes())
                   for p in sorted(temp.rglob("*")) if p.is_file()}
        guardar(temp / "integridad-ia.json",
                {"revision": revision, "archivos": content, "modelo": model,
                 "envio_autorizado": False, "origen": "mcp-local-sin-api",
                 "originales": preview["archivos"]})
        os.rename(temp, folder)
    finally:
        if temp.exists():
            shutil.rmtree(temp)
    return {"revision": revision, "carpeta": str(folder), "reutilizada": False,
            "modelo": model, "estado": "borrador_ia",
            "observaciones": len(sintesis["observaciones"]),
            "calculos": len(results["operaciones"])}
