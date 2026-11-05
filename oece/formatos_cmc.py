"""Ficha maestra independiente de las tres plantillas CMC, con trazabilidad.

No infiere experiencia acreditada ni emite CMC. Exporta datos semánticos para
tres formatos en orden; el mapeo a celdas se definirá al recibir las plantillas.
"""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re
import tempfile
import os
import shutil

from pypdf import PdfReader

from .comun import bytes_json, dentro, guardar, leer, sha
from .flujo import inventario

VERSION = "cmc-datos-v1"
SOURCE = "datos-cmc.json"
DESTINATION = "datos_formatos_cmc"
MONEY = Decimal("0.01")
STATUSES = ("propuesta_incluir", "pendiente", "excluida")
FIELDS = ("numero_tramite", "rnp", "fecha_corte", "activo_corriente",
          "pasivo_corriente")
WORK_FIELDS = ("objeto", "entidad", "numero_contrato", "fecha_contrato",
               "fecha_recepcion", "monto_contrato", "moneda_contrato",
               "porcentaje_participacion", "monto_liquidado",
               "descuento_equipamiento", "otros_descuentos",
               "monto_experiencia", "estado", "anios_marcados")
MONEY_FIELDS = ("monto_contrato", "monto_liquidado",
                "descuento_equipamiento", "otros_descuentos",
                "monto_experiencia")
FACTOR_NAMES = ("actividad", "financiero", "ejecucion")


def modelo_vacio(config=None):
    config = config or {}
    return {
        "version": VERSION,
        "expediente": {
            "proveedor": config.get("solicitante") or None,
            "numero_tramite": None,
            "tipo_tramite": config.get("procedimiento") or "aumento_cmc",
            "rnp": None, "fecha_corte": None,
            "activo_corriente": None, "pasivo_corriente": None,
        },
        "obras": [],
        "factores": {name: {"valor": None, "sustento": "",
                            "referencias": [], "norma_por_verificar": ""}
                    for name in FACTOR_NAMES},
        "consultas": [],
        "observaciones": [],
    }


def _string(value, field, maximum=1000, nullable=False):
    if value is None and nullable:
        return None
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError("Campo de texto inválido: " + field)
    return value


def _list(value, field, maximum=500):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Lista inválida: " + field)
    return value


def _date(value, name):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Fecha inválida: " + name)
    try:
        checked = date.fromisoformat(value)
    except ValueError:
        raise ValueError("Fecha inválida: " + name) from None
    if checked.isoformat() != value:
        raise ValueError("Fecha no canónica: " + name)
    return value


def _decimal(value, name, minimum=Decimal("0")):
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"-?\d{1,15}(?:\.\d{1,4})?", value):
        raise ValueError("Importe decimal no canónico: " + name)
    result = Decimal(value)
    if result < minimum:
        raise ValueError("Importe fuera de rango: " + name)
    return result


def _fmt(value):
    return str(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def _check_ref(ref, sources, field):
    if not isinstance(ref, dict) or set(ref) != {"documento", "pagina", "cita"}:
        raise ValueError("Referencia incompleta: " + field)
    source = sources.get(ref["documento"])
    if not source or not source["archivo"].lower().endswith(".pdf"):
        raise ValueError("Referencia a PDF no incorporado: " + field)
    page = ref["pagina"]
    if type(page) is not int or not 1 <= page <= source["paginas"]:
        raise ValueError("Referencia con página inexistente: " + field)
    if not isinstance(ref["cita"], str) or not 1 <= len(ref["cita"]) <= 500:
        raise ValueError("Cita visual inválida: " + field)
    # La ubicación se comprueba; la literalidad del texto queda pendiente de cotejo.
    return {"documento": ref["documento"], "pagina": page, "cita": ref["cita"]}


def validar(case_dir, data):
    """Comprueba forma, tipos, inventario y localizadores; no valida verdad del escaneo."""
    case_dir = Path(case_dir).resolve()
    if not isinstance(data, dict) or set(data) != {
        "version", "expediente", "obras", "factores", "consultas", "observaciones"
    } or data["version"] != VERSION:
        raise ValueError("Usar la estructura cmc-datos-v1 completa")
    config = leer(dentro(case_dir, "expediente.json"))
    if config["procedimiento"] != "aumento_cmc":
        raise ValueError("Los tres formatos CMC solo corresponden a aumento_cmc")
    inv = inventario(case_dir)
    sources = {}
    for item in inv:
        if item["archivo"].lower().endswith(".pdf"):
            path = dentro(case_dir, item["archivo"])
            reader = PdfReader(path)
            if reader.is_encrypted:
                raise ValueError("PDF cifrado en evidencia CMC")
            sources["D" + item["sha256"][:12]] = {**item, "paginas": len(reader.pages)}

    exp = data["expediente"]
    if not isinstance(exp, dict) or set(exp) != {"proveedor", *FIELDS, "tipo_tramite"}:
        raise ValueError("Campos de expediente CMC distintos del contrato")
    _string(exp["proveedor"], "proveedor", 300, nullable=True)
    if exp["proveedor"] and exp["proveedor"] != config["solicitante"]:
        raise ValueError("El proveedor no coincide con el expediente original")
    if exp["tipo_tramite"] != config["procedimiento"]:
        raise ValueError("Tipo de trámite CMC distinto del expediente")
    _string(exp["numero_tramite"], "numero_tramite", 100, nullable=True)
    _string(exp["rnp"], "rnp", 100, nullable=True)
    _date(exp["fecha_corte"], "fecha_corte")
    for f in ("activo_corriente", "pasivo_corriente"):
        _decimal(exp[f], f)
    _list(data["obras"], "obras", 150)
    seen = set()
    for obra in data["obras"]:
        if not isinstance(obra, dict) or set(obra) != {"id", *WORK_FIELDS, "motivo_estado",
                                                      "participacion_aplicada", "evidencias", "observaciones"}:
            raise ValueError("Obra CMC sin los campos requeridos")
        key = _string(obra["id"], "id", 80)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", key) or key in seen:
            raise ValueError("ID de obra inválido o duplicado")
        seen.add(key)
        for f in ("objeto", "entidad", "numero_contrato"):
            _string(obra[f], f, 500, nullable=True)
        for f in ("fecha_contrato", "fecha_recepcion"):
            _date(obra[f], f)
        for f in MONEY_FIELDS:
            _decimal(obra[f], f)
        _string(obra["moneda_contrato"], "moneda_contrato", 10, nullable=True)
        participation = _decimal(obra["porcentaje_participacion"], "porcentaje_participacion")
        if participation is not None and participation > 100:
            raise ValueError("Participación supera 100 %")
        if obra["participacion_aplicada"] not in (None, True, False) or type(obra["participacion_aplicada"]) is int:
            raise ValueError("Aplicación de participación requiere sí/no/pendiente")
        if obra["estado"] not in STATUSES:
            raise ValueError("Estado de obra no permitido")
        _string(obra["motivo_estado"], "motivo_estado", 1500, nullable=True)
        years = _list(obra["anios_marcados"], "anios_marcados", 120)
        if any(type(year) is not int or not 1900 <= year <= 2100 for year in years) or len(years) != len(set(years)):
            raise ValueError("Años marcados inválidos o duplicados")
        notes = _list(obra["observaciones"], "observaciones", 100)
        for note in notes:
            _string(note, "observación obra", 1500)
        evidences = _list(obra["evidencias"], "evidencias", 250)
        for ev in evidences:
            if not isinstance(ev, dict) or set(ev) != {"campo", "documento", "pagina", "cita"}:
                raise ValueError("Evidencia de obra incompleta")
            if ev["campo"] not in WORK_FIELDS and ev["campo"] != "motivo_estado":
                raise ValueError("Campo de evidencia de obra desconocido")
            _check_ref({k: ev[k] for k in ("documento", "pagina", "cita")}, sources, ev["campo"])
        # Un importe propuesto sin cita directa al original NO es computable.
        if obra["estado"] == "propuesta_incluir" and not evidences:
            raise ValueError("Obra propuesta sin ninguna evidencia")
    factors = data["factores"]
    if not isinstance(factors, dict) or set(factors) != set(FACTOR_NAMES):
        raise ValueError("Se requieren factores de actividad, financiero y ejecución")
    for k, f in factors.items():
        if not isinstance(f, dict) or set(f) != {"valor", "sustento", "referencias", "norma_por_verificar"}:
            raise ValueError("Estructura de factor inválida: " + k)
        _decimal(f["valor"], "factor " + k)
        _string(f["sustento"], "sustento de factor", 2000)
        _string(f["norma_por_verificar"], "norma por verificar", 1500)
        for ref in _list(f["referencias"], "referencias de factor", 50):
            _check_ref(ref, sources, "factor " + k)
    for consult in _list(data["consultas"], "consultas", 50):
        if not isinstance(consult, dict) or set(consult) != {"servicio", "realizada", "fecha", "resultado", "referencias"}:
            raise ValueError("Consulta web CMC incompleta")
        _string(consult["servicio"], "servicio", 150)
        if type(consult["realizada"]) is not bool:
            raise ValueError("Consulta debe ser sí/no, no estimación")
        _date(consult["fecha"], "fecha consulta")
        _string(consult["resultado"], "resultado consulta", 1500)
        if consult["realizada"] and not consult["fecha"]:
            raise ValueError("Consulta declarada sin fecha")
        for ref in _list(consult["referencias"], "referencias consulta", 25):
            _check_ref(ref, sources, "consulta")
    for note in _list(data["observaciones"], "observaciones", 150):
        _string(note, "observación", 2000)
    return {"inventario": inv, "documentos_pdf": len(sources)}


def preparar(case_dir, data):
    """Los tres paquetes contienen datos, no una plantilla imitada."""
    validar(case_dir, data)
    works = data["obras"]
    issues = []
    included = []
    for item in works:
        evidences = {v["campo"] for v in item["evidencias"]}
        if item["estado"] == "propuesta_incluir":
            missing = [k for k in ("monto_experiencia", "fecha_contrato", "fecha_recepcion")
                       if item[k] is None]
            missing.extend(k for k in ("monto_experiencia", "fecha_recepcion")
                           if k not in evidences)
            if item["porcentaje_participacion"] not in (None, "100", "100.00") and item["participacion_aplicada"] is not True:
                missing.append("participacion_aplicada")
            if missing:
                issues.append(f"{item['id']}: falta o requiere cotejo " + ", ".join(dict.fromkeys(missing)))
            else:
                included.append(item)
        elif item["estado"] == "pendiente":
            issues.append(f"{item['id']}: inclusión pendiente de determinar")
        elif item["estado"] == "excluida" and not item["motivo_estado"]:
            issues.append(f"{item['id']}: exclusión sin fundamento")
    count_included = sum(1 for item in works if item["estado"] == "propuesta_incluir")
    total = sum((Decimal(o["monto_experiencia"]) for o in included), Decimal("0"))
    sum_confirmable = bool(works) and count_included > 0 and count_included == len(included) and not any(
        item["estado"] == "pendiente" for item in works)
    period_missing = [o["id"] for o in included if not o["anios_marcados"]]
    for key in period_missing:
        issues.append(f"{key}: años pendientes de marcar en formato 2 (sin inferencia automática)")
    factors = data["factores"]
    factor_values = [factors[k]["valor"] for k in FACTOR_NAMES]
    for key in FACTOR_NAMES:
        if factors[key]["valor"] is None or not factors[key]["sustento"] or not factors[key]["norma_por_verificar"]:
            issues.append("Factor " + key + ": valor o fundamento normativo pendiente")
    g = (sum((Decimal(v) for v in factor_values), Decimal("0"))
         if all(v is not None for v in factor_values) else None)
    # La aritmética puede mostrarse como provisional; nunca afirmar otorgamiento.
    cmc = total * g if sum_confirmable and g is not None and not period_missing else None
    phase1 = {
        "version": VERSION, "tipo": "entregable_01_datos",
        "expediente": data["expediente"], "obras": works,
        "obras_propuestas_calculables": [o["id"] for o in included],
        "sumatoria_experiencia_parcial_soles": _fmt(total) if included else None,
        "sumatoria_completa": sum_confirmable,
        "advertencia": "Montos propuestos por IA; no son experiencia acreditada o aceptada.",
        "pendientes": issues,
    }
    phase2 = {
        "version": VERSION, "tipo": "entregable_02_datos",
        "origen": "entregable_01_datos",
        "obras_y_anios": [
            {"id": o["id"], "objeto": o["objeto"], "fecha_contrato": o["fecha_contrato"],
             "fecha_recepcion": o["fecha_recepcion"], "monto_experiencia": o["monto_experiencia"],
             "anios_marcados": o["anios_marcados"], "evidencias": o["evidencias"]}
            for o in included
        ],
        "sumatoria_experiencia_provisional_soles": _fmt(total) if sum_confirmable else None,
        "factores": factors, "G_provisional": _fmt(g) if g is not None else None,
        "advertencia": "Años y factores requieren regla y verificación normativa antes de emplearse.",
        "pendientes": issues,
    }
    phase3 = {
        "version": VERSION, "tipo": "entregable_03_datos",
        "origen": ["entregable_01_datos", "entregable_02_datos"],
        "encabezado_referencia": "OECE–DRNP–SDOR",
        "expediente": data["expediente"],
        "obras_propuestas": [o["id"] for o in included],
        "sumatoria_obras_provisional_soles": _fmt(total) if sum_confirmable else None,
        "factor_a": factors["actividad"]["valor"],
        "factor_f": factors["financiero"]["valor"],
        "factor_e": factors["ejecucion"]["valor"],
        "G_provisional": _fmt(g) if g is not None else None,
        "CMC_calculada_provisional_soles": _fmt(cmc) if cmc is not None else None,
        "CMC_a_otorgar": None,
        "consultas": data["consultas"],
        "estado": "borrador_pendiente_revision",
        "advertencia": "Ninguna CMC está acreditada u otorgada por este paquete.",
        "pendientes": issues,
    }
    return (phase1, phase2, phase3)


def publicar(case_dir):
    """Guarda 3 archivos JSON versionados; no modifica plantillas ni originales."""
    case_dir = Path(case_dir).resolve()
    source = dentro(case_dir, SOURCE)
    raw = source.read_bytes()
    data = leer(source)
    views = preparar(case_dir, data)
    original_files = inventario(case_dir)
    identity = {"version": VERSION, "fuente_sha256": sha(raw),
                "documentos": original_files, "implementacion_sha256": sha(Path(__file__).read_bytes())}
    revision = sha(bytes_json(identity))
    folder = dentro(case_dir, DESTINATION + "/" + revision)
    if folder.is_dir():
        verificar_publicacion(folder)
        return {"revision": revision, "carpeta": str(folder), "reutilizada": True,
                "pendientes": len(views[2]["pendientes"]), "plantillas_recibidas": False}
    parent = dentro(case_dir, DESTINATION)
    parent.mkdir(exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".cmc-preparando-", dir=parent))
    try:
        if inventario(case_dir) != original_files or source.read_bytes() != raw:
            raise ValueError("Fuentes del expediente cambiaron durante preparación")
        guardar(temporary / "ficha-maestra.json", data)
        names = ("entregable-01-datos.json", "entregable-02-datos.json",
                 "entregable-03-datos.json")
        for name, payload in zip(names, views):
            guardar(temporary / name, payload)
        files = {p.name: sha(p.read_bytes()) for p in temporary.iterdir() if p.is_file()}
        guardar(temporary / "integridad-cmc.json", {
            "revision": revision, "archivos": files, "fuente_sha256": sha(raw),
            "inventario": original_files, "estado": "datos_listos_para_mapeo",
            "plantillas_nativas_recibidas": False,
            "nota": "Datos extraídos y calculados; verificar antes de llenar formatos institucionales."
        })
        if inventario(case_dir) != original_files or source.read_bytes() != raw:
            raise ValueError("Fuentes modificadas antes de publicación CMC")
        os.rename(temporary, folder)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"revision": revision, "carpeta": str(folder), "reutilizada": False,
            "pendientes": len(views[2]["pendientes"]), "plantillas_recibidas": False,
            "archivos": list(names)}


def verificar_publicacion(folder):
    folder = Path(folder).resolve()
    if not re.fullmatch("[a-f0-9]{64}", folder.name):
        raise ValueError("Revisión de datos CMC inválida")
    manifest = leer(dentro(folder, "integridad-cmc.json"))
    for name, digest in manifest["archivos"].items():
        if name not in ("ficha-maestra.json", "entregable-01-datos.json",
                        "entregable-02-datos.json", "entregable-03-datos.json"):
            raise ValueError("Archivo del paquete CMC no permitido")
        if sha(dentro(folder, name).read_bytes()) != digest:
            raise ValueError("Paquete CMC alterado")
    return manifest
