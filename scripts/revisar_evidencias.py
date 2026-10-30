"""Importa decisiones explícitas en otra carpeta sintética, conservando la entrada."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile

from ejecutar_expediente import digest, encoded, inside, prepare
from proponer_evidencias import PROFILE, RULES, propose
from trazabilidad_evidencias import validate_decision


def reviewed_config(case_dir, bundle, decisions, profile_path=PROFILE, rules_path=RULES):
    fresh = propose(case_dir, profile_path, rules_path)
    if encoded(bundle) != encoded(fresh):
        raise ValueError("Propuestas alteradas o desactualizadas; genere otro lote")
    if decisions.get("lote_sha256") != digest(encoded(bundle)):
        raise ValueError("Las decisiones pertenecen a otro lote")
    proposals = {p["id"]: p for p in bundle["propuestas"]}
    selected, seen = [], set()
    for review in decisions["decisiones"]:
        ident = review["propuesta_id"]
        if ident not in proposals or ident in seen:
            raise ValueError("Propuesta desconocida o decisión duplicada")
        seen.add(ident)
        if review["decision"] == "pendiente":
            continue
        validate_decision(review)
        selected.append(review)
    raw = (Path(case_dir) / "expediente.json").read_bytes()
    if digest(raw) != bundle["instantanea_entrada"]["config_sha256"]:
        raise ValueError("Configuración de entrada cambió")
    case = json.loads(raw)
    links = case.setdefault("vinculos", {})
    for review in selected:
        proposal = proposals[review["propuesta_id"]]
        current = links.setdefault(proposal["control"], [])
        current[:] = [e for e in current if (e["documento"], e["ubicacion"]) !=
                      (proposal["documento"], proposal["ubicacion"])]
        if review["decision"] != "aceptada":
            continue
        item = {"documento": proposal["documento"], "ubicacion": proposal["ubicacion"],
                "origen": "propuesta_textual_revisada", "revision_evidencia": {
                    **review, **{k: proposal[k] for k in (
                        "control", "documento", "ubicacion", "fuente_sha256", "fragmento_sha256", "anclas", "perfil_sha256")}}}
        # Una revisión explícita añade procedencia a un vínculo declarado previo.
        current.append(item)
    case["revision_evidencias"] = {
        "implementacion_revision_sha256": digest(Path(__file__).read_bytes()),
        "lote_sha256": digest(encoded(bundle)), "decisiones_sha256": digest(encoded(decisions)),
        "decisiones_explicitas": selected, "aceptadas": sum(r["decision"] == "aceptada" for r in selected),
        "rechazadas": sum(r["decision"] == "rechazada" for r in selected),
        "pendientes": len(proposals) - len(selected),
        "nota": "Identidad del revisor declarada, no autenticada. No aprueba requisitos jurídicos."}
    return case


def export_reviewed(case_dir, bundle, decisions, destination, profile_path=PROFILE, rules_path=RULES):
    case_dir, destination = Path(case_dir).resolve(), Path(destination).resolve()
    if case_dir == destination or case_dir in destination.parents or destination in case_dir.parents:
        raise ValueError("Destino debe estar separado de la entrada")
    if destination.exists():
        raise ValueError("Destino ya existe; use otra carpeta para conservar revisiones")
    case = reviewed_config(case_dir, bundle, decisions, profile_path, rules_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".revision-", dir=destination.parent))
    expected = {d["id"]: d["sha256"] for d in bundle["instantanea_entrada"]["documentos"]}
    try:
        (temp / "documentos").mkdir()
        for n, document in enumerate(case["documentos"], 1):
            source = inside(case_dir, document["archivo"])
            raw = source.read_bytes()
            if digest(raw) != expected[document["id"]]:
                raise ValueError("Documento cambió antes de exportar revisión")
            relative = f"documentos/{n:03d}{source.suffix.lower()}"
            (temp / relative).write_bytes(raw)
            document["archivo"] = relative
        (temp / "expediente.json").write_bytes(encoded(case))
        (temp / "propuestas.json").write_bytes(encoded(bundle))
        (temp / "decisiones.json").write_bytes(encoded(decisions))
        # Valida de nuevo las huellas y citas de los vínculos antes de publicar.
        result = prepare(temp, Path(rules_path))
        if digest((case_dir / "expediente.json").read_bytes()) != bundle["instantanea_entrada"]["config_sha256"]:
            raise ValueError("Entrada cambió antes de publicar revisión")
        (temp / "revision_entrega.json").write_bytes(encoded({
            "estado": "revision_documental_sintetica", "ejecucion_preparada": result["id_ejecucion"],
            "archivos": {p.relative_to(temp).as_posix(): digest(p.read_bytes())
                         for p in sorted(temp.rglob("*")) if p.is_file()}}))
        os.rename(temp, destination)
    finally:
        if temp.exists():
            if temp.resolve().parent != destination.parent:
                raise ValueError("Temporal fuera del destino previsto")
            shutil.rmtree(temp)
    return case["revision_evidencias"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, required=True)
    parser.add_argument("--propuestas", type=Path, required=True)
    parser.add_argument("--decisiones", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    bundle = json.loads(args.propuestas.read_bytes())
    decisions = json.loads(args.decisiones.read_bytes())
    print(json.dumps(export_reviewed(args.entrada, bundle, decisions, args.salida), ensure_ascii=True))
