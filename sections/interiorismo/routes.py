import json
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from auth import login_required
from extensions import get_db

from .disenador import generar_diseno
from .estilos import ESTILOS

bp = Blueprint("interiorismo", __name__, url_prefix="/interiorismo")

EJEMPLOS = [
    "Quiero mi casa elegante y moderna, minimalista en blanco y negro, con espacios abiertos de lujo y una decoración acogedora. Luces LED encima de una viga del techo.",
    "Piso de 90 m² con 2 habitaciones y terraza, estilo nórdico, luminoso y cálido para una pareja que teletrabaja.",
    "Casa de campo de 200 m² con 4 dormitorios, 3 baños, piscina y chimenea, estilo mediterráneo para una familia con niños y un perro.",
    "Loft industrial de 110 m² con cocina abierta con isla, ladrillo visto y sala de cine.",
]


def _asegurar_tabla(db):
    db.execute(
        """CREATE TABLE IF NOT EXISTS disenos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            peticion TEXT NOT NULL,
            estilo TEXT NOT NULL,
            fuente TEXT NOT NULL,
            proyecto TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )


def _diseno_o_404(diseno_id):
    db = get_db()
    _asegurar_tabla(db)
    row = db.execute(
        "SELECT * FROM disenos WHERE id = ? AND user_id = ?", (diseno_id, session["user_id"])
    ).fetchone()
    if row is None:
        abort(404)
    return row


@bp.route("/")
@login_required
def index():
    db = get_db()
    _asegurar_tabla(db)
    recientes_rows = db.execute(
        "SELECT id, peticion, estilo, fuente, proyecto, created_at FROM disenos WHERE user_id = ? ORDER BY id DESC LIMIT 12",
        (session["user_id"],),
    ).fetchall()
    # Parsear los proyectos para obtener títulos y demás datos
    disenos = []
    for row in recientes_rows:
        proyecto_data = json.loads(row["proyecto"])
        disenos.append({
            "id": row["id"],
            "peticion": row["peticion"],
            "estilo": row["estilo"],
            "fuente": row["fuente"],
            "proyecto": proyecto_data,
            "created_at": row["created_at"],
        })
    return render_template(
        "interiorismo/inicio.html",
        estilos=ESTILOS,
        ejemplos=EJEMPLOS,
        disenos=disenos,
    )


@bp.route("/disenar", methods=["POST"])
@login_required
def disenar():
    peticion = (request.form.get("peticion") or "").strip()
    ajuste = (request.form.get("ajuste") or "").strip()
    estilo_oculto = request.form.get("estilo_oculto") or None
    # Si viene vacío, tratar como None
    estilo_oculto = estilo_oculto if estilo_oculto else None
    if not peticion:
        flash("Escribe cómo quieres tu casa para empezar a diseñarla.")
        return redirect(url_for("interiorismo.index"))
    if ajuste:
        peticion = f"{peticion}\n\nAjustes pedidos sobre la propuesta anterior: {ajuste}"
    if len(peticion) > 4000:
        flash("La descripción es demasiado larga (máximo 4000 caracteres).")
        return redirect(url_for("interiorismo.index"))

    proyecto, estilo, fuente, aviso = generar_diseno(peticion, estilo_oculto)
    if aviso:
        flash(aviso)

    db = get_db()
    _asegurar_tabla(db)
    cur = db.execute(
        "INSERT INTO disenos (user_id, peticion, estilo, fuente, proyecto, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (session["user_id"], peticion, estilo, fuente, json.dumps(proyecto, ensure_ascii=False),
         datetime.now().isoformat(timespec="seconds")),
    )
    db.commit()
    return redirect(url_for("interiorismo.ver", diseno_id=cur.lastrowid))


@bp.route("/<int:diseno_id>")
@login_required
def ver(diseno_id):
    row = _diseno_o_404(diseno_id)
    proyecto_data = json.loads(row["proyecto"])
    estilo_nombre = ESTILOS.get(row["estilo"], {}).get("nombre", row["estilo"])
    return render_template(
        "interiorismo/proyecto.html",
        id=row["id"],
        proyecto=proyecto_data,
        peticion=row["peticion"],
        estilo=estilo_nombre,
        fuente=row["fuente"],
    )


@bp.route("/<int:diseno_id>/borrar", methods=["POST"])
@login_required
def borrar(diseno_id):
    _diseno_o_404(diseno_id)
    db = get_db()
    db.execute("DELETE FROM disenos WHERE id = ?", (diseno_id,))
    db.commit()
    flash("Diseño eliminado.")
    return redirect(url_for("interiorismo.index"))
