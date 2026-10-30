"""Comprueba citas y declaraciones de revisión; no autentica al revisor."""
from datetime import datetime
import hashlib
import json


def validate_decision(review):
    if review.get("decision") not in ("aceptada", "rechazada"):
        raise ValueError("Decisión de revisión inválida")
    for key in ("revisor", "motivo"):
        if not isinstance(review.get(key), str) or not review[key].strip():
            raise ValueError("Revisión sin " + key)
    try:
        timestamp = datetime.fromisoformat(review["fecha"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Fecha de revisión inválida") from error
    if timestamp.tzinfo is None:
        raise ValueError("Fecha de revisión sin zona horaria")


def validate_link(review, source_sha, text, control, document, locator):
    validate_decision(review)
    if review["decision"] != "aceptada":
        raise ValueError("Evidencia sin aceptación explícita")
    if (review.get("control"), review.get("documento"), review.get("ubicacion")) != (control, document, locator):
        raise ValueError("Revisión trasladada a otro control o localizador")
    if review.get("fuente_sha256") != source_sha:
        raise ValueError("Fuente de evidencia revisada cambió")
    if review.get("fragmento_sha256") != hashlib.sha256(text.encode("utf-8")).hexdigest():
        raise ValueError("Fragmento de evidencia revisada cambió")
    if not review.get("anclas"):
        raise ValueError("Evidencia revisada sin citas")
    for anchor in review["anclas"]:
        start, end = anchor.get("inicio"), anchor.get("fin")
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
            raise ValueError("Rango de cita inválido")
        if text[start:end] != anchor.get("cita"):
            raise ValueError("Cita de evidencia revisada no coincide")
    core = {k: review[k] for k in ("control", "documento", "ubicacion", "fuente_sha256",
                                   "fragmento_sha256", "anclas", "perfil_sha256")}
    expected = hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")).hexdigest()
    if review.get("propuesta_id") != expected:
        raise ValueError("Identificador de propuesta no coincide con la revisión")
