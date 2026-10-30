"""Propone coincidencias textuales auditables; todas requieren revisión explícita."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

from ejecutar_expediente import ROOT, digest, encoded, prepare

PROFILE = ROOT / "rules/consultores/perfil-evidencias.v0.1.json"
RULES = ROOT / "rules/consultores/matriz.v0.1.json"


def normalized(text):
    chars, positions = [], []
    for i, char in enumerate(text):
        folded = "".join(c for c in unicodedata.normalize("NFD", char) if unicodedata.category(c) != "Mn").casefold()
        chars.extend(folded)
        positions.extend([i] * len(folded))
    return "".join(chars), positions


def match_groups(text, groups):
    folded, positions = normalized(text)
    anchors = []
    for group in groups:
        found = []
        for term in group:
            literal = normalized(term)[0]
            match = re.search(r"(?<!\w)" + re.escape(literal) + r"(?!\w)", folded)
            if match:
                found.append((match.start(), match.end(), term))
        if not found:
            return []
        start, end, term = min(found)
        start, end = positions[start], positions[end - 1] + 1
        while end < len(text) and unicodedata.category(text[end]) == "Mn":
            end += 1
        anchors.append({"inicio": start, "fin": end, "cita": text[start:end], "termino_perfil": term})
    return anchors


def propose(case_dir, profile_path=PROFILE, rules_path=RULES):
    result = prepare(Path(case_dir), Path(rules_path))
    raw = Path(profile_path).read_bytes()
    profile = json.loads(raw)
    known = {row["id"] for row in result["matriz"]}
    controls = profile["controles"]
    if profile.get("tipo") != "busqueda_textual_no_regla_juridica" or profile.get("procedimiento") != result["procedimiento"]:
        raise ValueError("Perfil de búsqueda incompatible")
    ids = [control["id"] for control in controls]
    limit = profile["limite_por_control"]
    if len(ids) != len(set(ids)) or set(ids) - known or type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("Controles o límite del perfil inválidos")
    for control in controls:
        groups = control["grupos"]
        if not isinstance(groups, list) or not groups or any(not isinstance(group, list) or not group or any(not isinstance(t, str) or not t.strip() or len(t) > 100 for t in group) for group in groups):
            raise ValueError("Términos de perfil inválidos")
    candidates, omitted, flagged, duplicates = [], 0, 0, 0
    for control in controls:
        selected = 0
        for document in result["documentos"]:
            if document["duplicado_de"]:
                duplicates += 1
                continue
            for fragment in document["fragmentos"]:
                if fragment["alertas"]:
                    flagged += 1
                    continue
                text = fragment["texto"]
                anchors = match_groups(text, control["grupos"])
                if not anchors:
                    continue
                if selected >= limit:
                    omitted += 1
                    continue
                core = {"control": control["id"], "documento": document["id"],
                        "ubicacion": fragment["ubicacion"], "fuente_sha256": document["sha256"],
                        "fragmento_sha256": digest(text.encode("utf-8")), "anclas": anchors,
                        "perfil_sha256": digest(raw)}
                warnings = []
                if re.search(r"\b(no|sin|pendiente|falta|fictici\w*|demostracion)\b", normalized(text)[0]):
                    warnings.append("contexto_con_negacion_ausencia_o_caracter_ficticio")
                candidates.append({**core, "id": digest(encoded(core)), "texto": text,
                                   "estado": "pendiente_revision", "confianza": None,
                                   "apta_para_evaluacion": False, "advertencias": warnings,
                                   "motivo": "Coincidencia literal de los grupos del perfil; no acredita el requisito"})
                selected += 1
    if Path(profile_path).read_bytes() != raw:
        raise ValueError("Perfil cambió durante la propuesta")
    return {"version": "0.1.0", "sintetico": True, "tipo": "propuestas_no_aprobadas",
            "expediente": result["expediente"], "ejecucion_entrada": result["id_ejecucion"],
            "instantanea_entrada": result["instantanea"],
            "perfil_sha256": digest(raw), "implementacion_sha256": digest(Path(__file__).read_bytes()),
            "controles_cubiertos": ids, "controles_sin_perfil": sorted(known - set(ids)),
            "omitidas_por_limite": omitted, "visitas_a_fragmentos_con_alerta": flagged,
            "visitas_a_documentos_duplicados": duplicates, "propuestas": candidates,
            "nota": "Conteos de visitas son por control. No se evalúa vigencia, autenticidad ni suficiencia jurídica."}


def decision_template(bundle):
    return {"lote_sha256": digest(encoded(bundle)), "decisiones": [
        {"propuesta_id": p["id"], "decision": "pendiente", "revisor": None, "fecha": None, "motivo": ""}
        for p in bundle["propuestas"]]}


def save_new(path, value):
    path = Path(path)
    raw = encoded(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError("El archivo existe con otro contenido; use otra ruta")
        return
    with path.open("xb") as stream:
        stream.write(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--plantilla-decisiones", type=Path, required=True)
    args = parser.parse_args()
    bundle = propose(args.entrada)
    save_new(args.salida, bundle)
    save_new(args.plantilla_decisiones, decision_template(bundle))
    print(json.dumps({"propuestas": len(bundle["propuestas"]), "aprobadas_automaticamente": 0}))
