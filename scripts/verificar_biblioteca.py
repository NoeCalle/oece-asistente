"""Verifica metadatos y trazabilidad; no evalua requisitos juridicos."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def official(url):
    host = urlparse(url).hostname or ""
    return url.startswith("https://") and any(host == d or host.endswith("." + d) for d in ("gob.pe", "elperuano.pe"))

def validate(check_originals=False):
    catalogue = read("normativa/catalogo.json")
    records = catalogue["normas"]
    ids = [n["id"] for n in records]
    require(len(ids) == len(set(ids)), "IDs normativos duplicados")
    for n in records:
        require(n["validacion"]["apta_para_reglas"] is False, "Regla normativa sin aprobacion")
        for relation in n["relaciones"]:
            require(relation["destino"] in ids, "Relacion normativa inexistente")
        for source in n["fuentes"]:
            require(official(source["url"]), "Fuente fuera de dominios oficiales")
        for value in (n["fecha_publicacion"], n["fecha_emision"], n["vigencia"]["desde"], n["vigencia"]["hasta"]):
            if value is not None:
                date.fromisoformat(value)
    manifests = read("normativa/manifiesto-descargas-2026-10-29.json")["archivos"] + read("normativa/manifiesto-continuacion-2026-10-30.json")["archivos"]
    by_name = {d["name"]: d for d in manifests}
    require(len(by_name) == len(manifests), "Archivos duplicados en manifiestos")
    for d in manifests:
        require(official(d["source_url"]), "Origen no oficial en manifiesto")
        require(bool(re.fullmatch("[a-f0-9]{64}", d["sha256"])), "Hash mal formado")
        path = (ROOT / d["local_path"]).resolve()
        require(ROOT in path.parents, "Ruta fuera del proyecto")
        if check_originals:
            require(path.is_file(), "Original local faltante: " + d["name"])
            require(path.stat().st_size == d["bytes"], "Tamano distinto: " + d["name"])
            require(hashlib.sha256(path.read_bytes()).hexdigest() == d["sha256"], "Hash distinto: " + d["name"])
    matrix = read("rules/consultores/matriz.v0.1.json")
    controls = matrix["reglas"]
    control_ids = [r["id"] for r in controls]
    require(len(control_ids) == len(set(control_ids)), "Controles duplicados")
    require(matrix["ejecutable"] is False, "Matriz candidata habilitada")
    for control in controls:
        require(control["habilitada"] is False and control["aprobacion_humana"] is None, "Control sin revision activado")
        source = control["fuente"]
        require(source["archivo"] in by_name, "Evidencia de control inexistente")
        document = by_name[source["archivo"]]
        require(source["sha256"] == document["sha256"], "Hash de control no coincide")
        require(source["url"] == document["source_url"], "URL de control no coincide")
        pages = document.get("verificacion", {}).get("pages")
        require(isinstance(source["pagina_pdf"], int) and source["pagina_pdf"] >= 1, "Pagina invalida")
        if pages:
            require(source["pagina_pdf"] <= pages, "Pagina fuera del documento")
    cases = read("tests/fixtures/consultores/casos-especificacion.json")
    require(cases["tipo"] == "especificacion_no_ejecutada", "Estado de casos incorrecto")
    for case in cases["casos"]:
        require(case["control"] in control_ids, "Caso sin control")
        require(case["ejecutado"] is False, "Caso no implementado marcado ejecutado")
    links = 0
    for folder in ("docs",):
        for path in (ROOT / folder).rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                require(resolved.exists(), "Enlace interno roto: " + str(path.relative_to(ROOT)) + " -> " + target)
                links += 1
    return {"catalogo": len(records), "archivos_manifestados": len(manifests), "controles": len(controls), "casos_especificados": len(cases["casos"]), "enlaces_locales": links, "originales_verificados": check_originals, "alcance": "integridad y referencias; no validacion juridica ni pruebas del asistente"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verificar-originales", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.verificar_originales), ensure_ascii=False, indent=2))
