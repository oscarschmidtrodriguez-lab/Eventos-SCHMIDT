"""Motor de diseño de interiores.

`generar_diseno()` convierte una petición en lenguaje natural ("quiero mi casa
elegante y moderna, con 3 habitaciones...") en un proyecto de interiorismo
completo: concepto, paleta, materiales, estancias, plan de iluminación,
consejos y presupuesto orientativo.

- Si hay credenciales de Anthropic (ANTHROPIC_API_KEY), el proyecto lo
  redacta Claude con salida estructurada, usando el catálogo de estilos
  como guía.
- Si no las hay (o la llamada falla), lo genera el motor local a partir del
  catálogo de `estilos.py`, así la app funciona siempre.
"""

import os
import re
from typing import List

from pydantic import BaseModel

from .estilos import ESTILO_POR_DEFECTO, ESTILOS, detectar_estilo

MODELO = os.environ.get("INTERIORISMO_MODEL", "claude-opus-5")

ESTANCIAS_EXTRA = {
    "despacho": {
        "claves": ["despacho", "oficina", "teletrabajo", "estudio", "trabajar desde casa"],
        "nombre": "Despacho",
        "distribucion": "Mesa perpendicular a la ventana para tener luz natural lateral sin reflejos en pantalla.",
        "mobiliario": ["Escritorio de 160×75 cm", "Silla ergonómica", "Estantería o armario cerrado a medida"],
        "decoracion": ["Tablero de corcho o pizarra integrado en la pared", "Una planta de fácil cuidado"],
        "toque": "Luz de trabajo a 4000 K sobre la mesa y cálida en el resto: separa trabajo y descanso.",
    },
    "infantil": {
        "claves": ["niño", "niños", "niña", "niñas", "bebé", "bebe", "hijos", "infantil"],
        "nombre": "Dormitorio infantil",
        "distribucion": "Zona de descanso, zona de juego despejada en el centro y almacenaje bajo accesible para el niño.",
        "mobiliario": ["Cama evolutiva", "Cajas y baldas a su altura", "Mesa de actividades"],
        "decoracion": ["Alfombra lavable", "Papel pintado suave en una sola pared"],
        "toque": "Materiales lavables y esquinas redondeadas sin renunciar al estilo de la casa.",
    },
    "cine": {
        "claves": ["cine", "home cinema", "sala de juegos", "proyector"],
        "nombre": "Sala de cine",
        "distribucion": "Sofá a 2,5–3 m de la pantalla, paredes oscuras y cortinas opacas.",
        "mobiliario": ["Sofá reclinable", "Proyector 4K y pantalla", "Mueble para consolas y sonido"],
        "decoracion": ["Paneles acústicos textiles", "Alfombra gruesa"],
        "toque": "Rodapié LED de baja intensidad para moverse sin molestar la imagen.",
    },

    # ---- Estancias premium: casas de ensueño Engel & Völkers ----

    "spa": {
        "claves": ["spa", "sauna", "hammam", "jacuzzi", "wellness", "bienestar", "relajacion", "relajación"],
        "nombre": "Spa privado",
        "distribucion": "Zona de aguas con sauna finlandesa, ducha de contrastes (lluvia tropical + chorro frío) y zona de relax con tumbonas térmicas. Piscina climatizada o jacuzzi integrado si hay espacio.",
        "mobiliario": [
            "Sauna finlandesa de cedro rojo con cristal para 4 personas",
            "Ducha de contrastes con cascada, lluvia tropical y chorro de agua fría",
            "Tumbonas térmicas de piedra con calefacción radiante",
            "Jacuzzi empotrado para 2-4 personas con cromoterápia LED",
        ],
        "decoracion": [
            "Revestimiento de piedra natural en paredes de agua",
            "Iluminación cromática regulable (2700 K a RGB para cromoterapia)",
            "Plantas de humedad: helechos, bambú",
            "Toallas de rizo egipcio en estanterías de teca",
        ],
        "toque": "El spa no es un baño grande: tiene un circuito (sauna → ducha fría → descanso) y una luz que baja progresivamente del cálido al ámbar. Es un ritual, no una instalación.",
    },
    "bodega": {
        "claves": ["bodega", "vino", "vinos", "cava", "wine", "vinoteca"],
        "nombre": "Bodega de vinos",
        "distribucion": "Sala climatizada (14-16 °C, 65-75 % HR) con botelleros de pared, mesa de cata para 6 y zona de decantación con luz puntual.",
        "mobiliario": [
            "Botelleros de roble y hierro forjado para 300-500 botellas en pared",
            "Mesa de cata de roble macizo para 6 con iluminación cenital",
            "Enfriador-expositor de vidrio templado para vinos de servicio",
            "Sillones de cuero para sobremesa junto a la mesa",
        ],
        "decoracion": [
            "Pared de piedra vista o ladrillo visto como fondo",
            "Iluminación LED cálida (2400 K) en las baldas de los botelleros",
            "Mapa de regiones vinícolas enmarcado",
        ],
        "toque": "Puerta de vidrio templado con control de clima: la bodega se ve desde el pasillo como una joyería, pero mantiene temperatura y humedad perfectas.",
    },
    "gimnasio": {
        "claves": ["gimnasio", "gym", "fitness", "entrenamiento", "entrenar", "deporte"],
        "nombre": "Gimnasio privado",
        "distribucion": "Sala con suelo de caucho o tarima técnica, espejo de pared completa, zona de peso libre y zona de cardio frente a pantalla o ventanal.",
        "mobiliario": [
            "Espejo de pared completa (suelo a techo) en un lado",
            "Rack de musculación multifuncional (Technogym o similar)",
            "Cinta de correr y bicicleta estática frente al ventanal o pantalla 65″",
            "Set de mancuernas y kettlebells en estantería de acero",
            "Banco regulable y esterilla",
        ],
        "decoracion": [
            "Suelo de caucho negro o gris de alto impacto",
            "Ventilación forzada o ventana practicable para renovar el aire",
            "Altavoz Bluetooth empotrado para música de entrenamiento",
        ],
        "toque": "El espejo es obligatorio, pero la luz LED perimetral detrás del espejo lo convierte en un gym de boutique: motivación visual sin deslumbramiento.",
    },
    "vestidor_lujo": {
        "claves": ["vestidor", "walk-in", "closet", "armario vestidor", "dressing"],
        "nombre": "Vestidor de lujo",
        "distribucion": "Walk-in closet con isla central (cajones y superficie de apoyo), módulos de suelo a techo con iluminación LED en baldas, zona de zapatos con expositor y espejo de cuerpo entero.",
        "mobiliario": [
            "Isla central con cajones forrados de terciopelo y encimera de mármol",
            "Módulos de roble o lacado con baldas, barras y cajones de suelo a techo",
            "Expositor de zapatos retroiluminado con estantes de cristal",
            "Espejo de cuerpo entero con iluminación de boutique (3000 K, CRI ≥ 95)",
            "Butaca o puf para calzarse",
        ],
        "decoracion": [
            "Moqueta o alfombra de lana gruesa en el suelo para confort descalzo",
            "Tiradores de latón o cuero",
            "Bandejas de piedra o piel para accesorios",
        ],
        "toque": "La isla central convierte el vestidor en una boutique privada: no es un armario abierto, es un ritual de vestirse. LED cálido en cada balda para ver los colores reales.",
    },
    "garaje_galeria": {
        "claves": ["garaje", "garage", "coches", "coche", "coleccion", "colección", "showroom"],
        "nombre": "Garaje-galería",
        "distribucion": "Garaje de diseño con suelo de resina epoxi de alto brillo, iluminación tipo showroom, y zona de estar para contemplar la colección.",
        "mobiliario": [
            "Suelo de resina epoxi gris oscuro de alto brillo (efecto concesionario)",
            "Iluminación LED lineal en perímetro y focos orientables sobre cada plaza",
            "Estantería de acero y vidrio para cascos, maquetas y memorabilia",
            "Sofá o banco de cuero para contemplar la colección",
            "Plataforma giratoria (opcional) para el coche protagonista",
        ],
        "decoracion": [
            "Pared de fondo con logo o lámina de arte automovilístico",
            "Panel perforado de herramientas como pieza decorativa (si hay taller)",
            "Vidrieras o puertas de cristal para ver los coches desde la casa",
        ],
        "toque": "La puerta del garaje con cristal templado: los coches se ven desde el pasillo o el salón como una obra de arte. Es la foto que Engel & Völkers pone en su web.",
    },
    "piscina_cubierta": {
        "claves": ["piscina cubierta", "piscina climatizada", "piscina interior", "natacion", "natación", "nadar"],
        "nombre": "Piscina cubierta climatizada",
        "distribucion": "Piscina interior de 10-15 m con carril de natación, climatización del agua y del ambiente, ventanales laterales al jardín y zona de tumbonas.",
        "mobiliario": [
            "Piscina de obra revestida de gresite o piedra natural (10-15 m × 4 m)",
            "Tumbonas de teca junto a la piscina sobre pavimento antideslizante",
            "Sistema de deshumidificación y climatización del ambiente",
            "Ducha y vestuario auxiliar junto a la entrada",
        ],
        "decoracion": [
            "Ventanales de suelo a techo con vistas al jardín",
            "Iluminación LED subacuática (blanca o cromática)",
            "Plantas tropicales en maceteros grandes para crear ambiente de resort",
        ],
        "toque": "El techo retráctil o las puertas plegables permiten que en verano sea una piscina exterior y en invierno un spa cubierto: lo mejor de los dos mundos.",
    },
}


# --------------------------------------------------------------------------
# Esquema del proyecto (también es el formato de salida estructurada de Claude)
# --------------------------------------------------------------------------

class Color(BaseModel):
    nombre: str
    hex: str
    uso: str


class Material(BaseModel):
    nombre: str
    donde: str


class Estancia(BaseModel):
    nombre: str
    distribucion: str
    mobiliario: List[str]
    iluminacion: List[str]
    decoracion: List[str]
    toque_experto: str


class CapaLuz(BaseModel):
    tipo: str
    detalle: str
    temperatura: str


class Iluminacion(BaseModel):
    concepto: str
    viga_led: str
    capas: List[CapaLuz]


class Render(BaseModel):
    pared: str
    suelo: str
    techo: str
    viga: str
    sofa: str
    madera: str
    acento: str
    metal: str
    textil: str
    led: str


class Partida(BaseModel):
    partida: str
    rango: str


class Proyecto(BaseModel):
    titulo: str
    concepto: str
    principios: List[str]
    paleta: List[Color]
    materiales: List[Material]
    estancias: List[Estancia]
    iluminacion: Iluminacion
    render: Render
    consejos: List[str]
    presupuesto: List[Partida]


# --------------------------------------------------------------------------
# Lectura de la petición
# --------------------------------------------------------------------------

def _numero(patron, texto, defecto=None):
    m = re.search(patron, texto)
    return int(m.group(1)) if m else defecto


def analizar_peticion(texto):
    """Extrae del texto libre lo que un interiorista preguntaría en la primera visita."""
    t = (texto or "").lower()
    palabras_num = {"un": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6}
    for palabra, n in palabras_num.items():
        t = re.sub(rf"\b{palabra}\b(?=\s+(?:habitaci|dormitori|cuarto|baño))", str(n), t)
    return {
        "habitaciones": _numero(r"(\d+)\s*(?:habitaci|dormitori|cuarto)", t, 2),
        "banos": _numero(r"(\d+)\s*baños?", t, 1),
        "m2": _numero(r"(\d{2,4})\s*(?:m2|m²|metros)", t),
        "exterior": any(k in t for k in ["terraza", "jardin", "jardín", "patio", "piscina", "porche", "balcon", "balcón"]),
        "piscina": "piscina" in t,
        "mascotas": any(k in t for k in ["perro", "gato", "mascota"]),
        "chimenea": "chimenea" in t,
        "vestidor": "vestidor" in t,
        "extras": [clave for clave, e in ESTANCIAS_EXTRA.items() if any(k in t for k in e["claves"])],
    }


# --------------------------------------------------------------------------
# Motor local (sin IA)
# --------------------------------------------------------------------------

def _luces_estancia(nombre, estilo):
    led = estilo["render"]["led"]
    base = {
        "Salón-comedor": [
            f"Tira LED cálida 2700 K integrada en la viga del techo ({estilo['viga']}), regulable, como luz ambiental principal.",
            "Foseado perimetral en falso techo para bañar las paredes de luz indirecta.",
            "Lámpara de pie junto al sofá para lectura (luz de acento).",
            "Colgante o lámparas decorativas sobre la mesa del comedor a 75 cm de la mesa.",
        ],
        "Cocina": [
            "Downlights empotrados orientables 3000 K sobre la zona de trabajo.",
            "Perfil LED bajo muebles altos para iluminar la encimera sin sombras.",
            "Colgantes sobre la isla o península a 70–80 cm de la encimera.",
        ],
        "Dormitorio principal": [
            "Retroiluminación LED cálida 2700 K tras el cabecero, regulable.",
            "Apliques de lectura orientables a cada lado de la cama.",
            "Tira LED con sensor de movimiento en el interior del armario.",
        ],
        "Baño": [
            "Espejo con LED integrado 3000–4000 K para una luz fiel en la cara.",
            "Hornacina de ducha con LED lineal estanco (IP65).",
            "Downlights estancos en techo, con regulación para un modo relax.",
        ],
        "Exterior": [
            "Bañadores de pared rasantes 2700 K para dar profundidad.",
            "Balizas en el suelo para marcar recorridos.",
        ],
    }
    return base.get(nombre, [
        "Luz general indirecta cálida 2700–3000 K regulable.",
        "Luz de tarea puntual donde se trabaja o se lee.",
    ]) + ([f"Toda la luz en un tono cálido coherente (referencia de color {led})."] if nombre == "Salón-comedor" else [])


def _estancia(nombre, datos, estilo, superficie=None):
    return {
        "nombre": nombre + (f" · ~{superficie} m²" if superficie else ""),
        "distribucion": datos["distribucion"],
        "mobiliario": list(datos["mobiliario"]),
        "iluminacion": _luces_estancia(nombre, estilo),
        "decoracion": list(datos["decoracion"]),
        "toque_experto": datos["toque"],
    }


def _formato_eur(n):
    return f"{n:,.0f} €".replace(",", ".")


def generar_local(peticion, clave_estilo):
    estilo = ESTILOS[clave_estilo]
    info = analizar_peticion(peticion)
    m2 = info["m2"] or (60 + 25 * info["habitaciones"] + 8 * info["banos"])
    e = estilo["estancias"]

    estancias = [
        _estancia("Recibidor", {
            "distribucion": "Primera impresión de la casa: un mueble bajo o banco, espejo y armario ropero empotrado.",
            "mobiliario": ["Consola o banco estrecho (máx. 35 cm de fondo)", "Armario empotrado para abrigos y calzado"],
            "decoracion": ["Espejo grande para ampliar y rebotar la luz", "Un objeto escultórico o una planta"],
            "toque": "Luz cálida al entrar, activada por sensor: la casa te recibe encendida.",
        }, estilo),
        _estancia("Salón-comedor", e["salon"], estilo, round(m2 * 0.32)),
        _estancia("Cocina", e["cocina"], estilo, round(m2 * 0.12)),
        _estancia("Dormitorio principal", e["dormitorio"], estilo, round(m2 * 0.14)),
    ]
    if info["vestidor"]:
        estancias[-1]["mobiliario"].append("Vestidor abierto a continuación del dormitorio con iluminación LED en baldas y barras")
    if info["habitaciones"] > 1:
        n = info["habitaciones"] - 1
        sec = dict(e["dormitorio"])
        sec["distribucion"] = f"{n} dormitorio{'s' if n > 1 else ''} secundario{'s' if n > 1 else ''} con la misma base de materiales y colores más suaves; cama de 135 cm, armario empotrado y escritorio junto a la ventana."
        estancias.append(_estancia("Dormitorios secundarios", sec, estilo))
    banos = _estancia("Baño", e["bano"], estilo)
    if info["banos"] > 1:
        banos["nombre"] = f"Baños ({info['banos']})"
        banos["distribucion"] += " El baño principal en suite con ducha doble; el resto con la misma línea de materiales."
    estancias.append(banos)
    for clave in info["extras"]:
        x = ESTANCIAS_EXTRA[clave]
        estancias.append(_estancia(x["nombre"], x, estilo))
    if info["exterior"]:
        ext = _estancia("Exterior", e["exterior"], estilo)
        if info["piscina"]:
            ext["mobiliario"].append("Zona de tumbonas junto a la piscina con sombrillas de lona cruda")
            ext["iluminacion"].append("Focos LED subacuáticos cálidos en la piscina")
        estancias.append(ext)

    consejos = [
        "Planifica la iluminación antes de la obra: los perfiles LED de vigas y foseados necesitan canalización y drivers accesibles.",
        "Usa LED de alto índice de reproducción cromática (CRI ≥ 90): los colores y materiales se ven como son.",
        "Instala reguladores o domótica (escenas: día, cena, cine, noche). La misma casa cambia por completo con la luz.",
        "Pide muestras físicas de pintura y suelo y míralas con luz de mañana y de noche antes de decidir.",
        "Mide dos veces: sofá, mesa y alfombra se eligen con planos, no a ojo.",
    ]
    if info["mascotas"]:
        consejos.append("Con mascotas: tejidos de alto rendimiento lavables y suelos resistentes al rayado (porcelánico o vinílico).")
    if info["chimenea"]:
        consejos.append("La chimenea será el punto focal del salón: orienta el sofá hacia ella y no hacia la TV.")

    lo, hi = estilo["coste_m2"]
    presupuesto = [
        {"partida": "Obra y acabados (suelos, pintura, techos)", "rango": f"{_formato_eur(m2 * lo * 0.45)} – {_formato_eur(m2 * hi * 0.45)}"},
        {"partida": "Cocina y baños", "rango": f"{_formato_eur(m2 * lo * 0.25)} – {_formato_eur(m2 * hi * 0.25)}"},
        {"partida": "Iluminación LED e instalación eléctrica", "rango": f"{_formato_eur(m2 * lo * 0.10)} – {_formato_eur(m2 * hi * 0.10)}"},
        {"partida": "Mobiliario y decoración", "rango": f"{_formato_eur(m2 * lo * 0.20)} – {_formato_eur(m2 * hi * 0.20)}"},
        {"partida": f"Total orientativo para ~{m2} m²", "rango": f"{_formato_eur(m2 * lo)} – {_formato_eur(m2 * hi)}"},
    ]

    return {
        "titulo": f"Tu casa {estilo['nombre'].lower()}",
        "concepto": estilo["concepto"],
        "principios": list(estilo["principios"]),
        "paleta": [{"nombre": n, "hex": h, "uso": u} for n, h, u in estilo["paleta"]],
        "materiales": [{"nombre": n, "donde": d} for n, d in estilo["materiales"]],
        "estancias": estancias,
        "iluminacion": {
            "concepto": "Iluminación en tres capas (ambiental, de tarea y de acento), toda regulable y en tonos cálidos, con la luz indirecta como protagonista para que la casa se sienta acogedora.",
            "viga_led": f"En el salón, {estilo['viga']}. Perfil de aluminio con difusor opal, LED 2700 K CRI ≥ 90, 10–14 W/m y driver regulable accesible.",
            "capas": [
                {"tipo": "Ambiental", "detalle": "LED indirecto en vigas, foseados y cortineros; ilumina techos y paredes, nunca deslumbra.", "temperatura": "2700 K"},
                {"tipo": "Tarea", "detalle": "Cocina, lectura, escritorio y espejo del baño: luz directa y suficiente donde se trabaja.", "temperatura": "3000–4000 K"},
                {"tipo": "Acento", "detalle": "Hornacinas, cuadros, plantas y texturas de pared; crea profundidad y ambiente de noche.", "temperatura": "2700 K"},
            ],
        },
        "render": dict(estilo["render"]),
        "consejos": consejos,
        "presupuesto": presupuesto,
    }


# --------------------------------------------------------------------------
# Claude
# --------------------------------------------------------------------------

SISTEMA = """Eres un interiorista y arquitecto de interiores de primer nivel mundial, \
con experiencia en villas de lujo, penthouses y propiedades exclusivas como las que \
vende Engel & Völkers, las que se viralizan en Pinterest y las que aparecen en \
las cuentas de Instagram de diseño de interiores (@dezeen, @elledecor, @archdigest).

Tu referencia visual: las casas de ensueño de revistas como Architectural Digest, \
AD España, Elle Decoration — viviendas que combinan arquitectura espectacular \
(dobles alturas, ventanales panorámicos, infinity pools) con interiorismo cálido \
y habitable. No diseñas showrooms fríos: diseñas hogares donde la vida es hermosa.

Cómo trabajas:
- Respetas al máximo lo que pide el cliente; lo que no diga, lo decides tú con criterio \
profesional, siempre aspirando al nivel más alto que el presupuesto permita.
- Distribución: priorizas espacios abiertos y luminosos con dobles alturas donde sea posible, \
circulaciones generosas y transición interior-exterior fluida (mismo pavimento, puertas \
de gran luz, pérgolas bioclimáticas).
- Paleta: 4–6 colores con código HEX real y reparto de uso (regla 60/30/10 o 70/20/10).
- Materiales de primera: mármoles con nombre (Calacatta, Sahara Noir, Portoro), maderas \
nobles (roble ahumado, teca, nogal), piedra natural, vidrio de control solar. Nombra \
formato, acabado y dónde va cada uno.
- Mobiliario de diseño: menciona marcas de referencia (Minotti, B&B Italia, Poliform, \
Cassina, Kettal para exterior) con medidas clave.
- Domótica: integra sistema KNX o similar (escenas de luz, persianas motorizadas, \
clima por zonas, audio multiroom) siempre que el estilo lo permita.
- Cocinas de ensueño: islas de 3-4 m, electrodomésticos integrados (Gaggenau, Miele), \
office/despensa oculto, grifo de diseño.
- Baños tipo spa: ducha lluvia doble, bañera exenta de diseño (Agape, Boffi, Falper), \
suelo radiante, mármol de suelo a techo.
- Exterior premium: infinity pool con rebosadero, pérgola bioclimática, cocina de \
verano, fire pit, jardín paisajístico con iluminación nocturna.
- Iluminación en tres capas (ambiental, tarea, acento), cálida (2700–3000 K), regulable, \
CRI ≥ 90, controlada por domótica con escenas (día, atardecer, cena, cine, noche). \
Incluye SIEMPRE luz LED integrada en una viga del techo del salón, describiendo cómo se \
instala (perfil, difusor, dirección de la luz, driver) y por qué queda perfecta.
- Cada estancia termina con un "toque_experto": el detalle que haría que la foto de esa \
estancia se guardara en un tablero de Pinterest o se publicara en Architectural Digest.
- Presupuesto orientativo en euros por partidas, con un total.
- `render` son los colores HEX para una ilustración del salón (pared, suelo, techo, viga, \
sofá, madera, acento, metal, textil y el color de la luz LED).

Piensa en cada proyecto como si fuera la propiedad estrella del catálogo de una \
inmobiliaria de lujo: cada detalle cuenta para la foto, para la vida y para el valor \
de reventa. Sé específico, concreto y evita generalidades vacías."""


def _guia_estilo(clave):
    e = ESTILOS[clave]
    paleta = ", ".join(f"{n} {h} ({u})" for n, h, u in e["paleta"])
    return (
        f"Estilo elegido: {e['nombre']} — {e['lema']}.\n"
        f"Referencia de concepto: {e['concepto']}\n"
        f"Principios: {' '.join(e['principios'])}\n"
        f"Paleta de referencia: {paleta}\n"
        f"Viga LED de referencia: {e['viga']}\n"
        f"Coste orientativo del estilo: {e['coste_m2'][0]}–{e['coste_m2'][1]} €/m² (reforma integral + mobiliario)."
    )


def _claude_disponible():
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return True


def generar_con_claude(peticion, clave_estilo):
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.parse(
        model=MODELO,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        system=SISTEMA,
        messages=[{
            "role": "user",
            "content": f"{_guia_estilo(clave_estilo)}\n\nLo que quiere el cliente:\n{peticion}",
        }],
        output_format=Proyecto,
    )
    if response.stop_reason != "end_turn" or response.parsed_output is None:
        raise RuntimeError(f"Respuesta incompleta de Claude (stop_reason={response.stop_reason})")
    return response.parsed_output.model_dump()


def generar_diseno(peticion, clave_estilo=None):
    """Devuelve (proyecto, clave_estilo, fuente, aviso); fuente es 'ia' o 'local'."""
    if clave_estilo not in ESTILOS:
        clave_estilo = detectar_estilo(peticion) if peticion else ESTILO_POR_DEFECTO

    aviso = None
    if _claude_disponible():
        try:
            return generar_con_claude(peticion, clave_estilo), clave_estilo, "ia", None
        except Exception as exc:  # la app debe responder siempre: caemos al motor local
            aviso = f"La IA no respondió ({type(exc).__name__}); se ha usado el motor experto local."
    return generar_local(peticion, clave_estilo), clave_estilo, "local", aviso
