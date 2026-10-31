"""Comprueba adquisición documental de un alcance explícito; no su vigencia jurídica."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from indexar_normativa import MANIFESTS, ROOT, read_json, safe_source
from verificar_biblioteca import official


def assess(root=ROOT, plan_path="normativa/cobertura-piloto.v0.1.json", manifests=MANIFESTS, originals=False):
    root = Path(root).resolve()
    plan_file = (root / plan_path).resolve()
    if root not in plan_file.parents:
        raise ValueError("Plan fuera de la raíz")
    raw = plan_file.read_bytes()
    plan = json.loads(raw)
    if plan.get("habilita_reglas") is not False or not plan.get("grupos"):
        raise ValueError("Plan sin grupos o que pretende habilitar reglas")
    manifest_paths = [(root / name).resolve() for name in manifests]
    if any(root not in path.parents for path in manifest_paths):
        raise ValueError("Manifiesto fuera de la raíz")
    items = [item for path in manifest_paths for item in read_json(path)["archivos"]]
    by_name = {item["name"]: item for item in items}
    if len(by_name) != len(items):
        raise ValueError("Archivo duplicado en manifiestos")
    groups, ids, used = [], set(), set()
    for group in plan["grupos"]:
        if group["id"] in ids or not group.get("archivos_obligatorios"):
            raise ValueError("Grupo duplicado o vacío")
        ids.add(group["id"])
        if group["prioridad"] not in ("principal", "complementaria"):
            raise ValueError("Prioridad desconocida")
        names = group["archivos_obligatorios"]
        if len(names) != len(set(names)):
            raise ValueError("Requisito documental duplicado")
        documents = []
        for name in names:
            used.add(name)
            item = by_name.get(name)
            entry = {"archivo": name, "estado": "no_manifestado"}
            if item:
                if not official(item["source_url"]) or not official(item.get("source_page", item["source_url"])):
                    raise ValueError("Procedencia fuera de fuentes oficiales: " + name)
                entry.update(sha256=item["sha256"], source_url=item["source_url"],
                             estado="manifestado_no_verificado_localmente",
                             requiere_ocr=item.get("verificacion", {}).get("requiere_ocr", False))
                if originals:
                    source = (root / item["local_path"]).resolve()
                    if root not in source.parents:
                        raise ValueError("Ruta fuera de la biblioteca")
                    if not source.is_file():
                        entry["estado"] = "original_local_faltante"
                    else:
                        safe_source(root, item)
                        entry["estado"] = "original_local_verificado"
            documents.append(entry)
        groups.append({"id": group["id"], "prioridad": group["prioridad"],
                       "archivos": documents, "pendiente_juridico": group["pendiente_juridico"]})
    missing = [d["archivo"] for g in groups for d in g["archivos"] if d["estado"] in
               ("no_manifestado", "original_local_faltante")]
    return {"procedimiento": plan["procedimiento"], "plan_sha256": hashlib.sha256(raw).hexdigest(),
            "estado_adquisicion": "pendiente" if missing else
                "completa_en_alcance_versionado" if originals else "solo_cobertura_de_manifiestos",
            "originales_verificados": originals, "archivos_obligatorios_distintos": len(used),
            "faltantes": missing, "grupos": groups, "cierre_juridico": False,
            "apta_para_evaluacion": False, "nota": "Presencia e integridad dentro del alcance declarado; no exhaustividad, vigencia ni suficiencia jurídica."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verificar-originales", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(assess(originals=args.verificar_originales), ensure_ascii=False, indent=2))
