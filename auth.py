import secrets
import sqlite3
import time
from functools import wraps

import jwt
import requests
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import get_db

bp = Blueprint("auth", __name__)

GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"

FACEBOOK_AUTH_URI = "https://www.facebook.com/v18.0/dialog/oauth"
FACEBOOK_TOKEN_URI = "https://graph.facebook.com/v18.0/oauth/access_token"
FACEBOOK_USERINFO_URI = "https://graph.facebook.com/me"

APPLE_AUTH_URI = "https://appleid.apple.com/auth/authorize"
APPLE_TOKEN_URI = "https://appleid.apple.com/auth/token"
APPLE_KEYS_URI = "https://appleid.apple.com/auth/keys"


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def _google_configured():
    return bool(current_app.config.get("GOOGLE_CLIENT_ID") and current_app.config.get("GOOGLE_CLIENT_SECRET"))


def _facebook_configured():
    return bool(current_app.config.get("FACEBOOK_CLIENT_ID") and current_app.config.get("FACEBOOK_CLIENT_SECRET"))


def _apple_configured():
    return bool(
        current_app.config.get("APPLE_CLIENT_ID")
        and current_app.config.get("APPLE_TEAM_ID")
        and current_app.config.get("APPLE_KEY_ID")
        and current_app.config.get("APPLE_PRIVATE_KEY")
    )


def _log_in_user(user):
    session.clear()
    session["user_id"] = user["id"]
    session["email"] = user["email"]


def _find_or_link_user(db, provider_column, provider_id, email):
    """Find a user by their provider id, linking it to an existing email if needed."""
    user = db.execute(f"SELECT * FROM users WHERE {provider_column} = ?", (provider_id,)).fetchone()
    if not user and email:
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            db.execute(f"UPDATE users SET {provider_column} = ? WHERE id = ?", (provider_id, user["id"]))
            db.commit()
    return user


def _apple_client_secret():
    now = int(time.time())
    private_key = current_app.config["APPLE_PRIVATE_KEY"].replace("\\n", "\n")
    payload = {
        "iss": current_app.config["APPLE_TEAM_ID"],
        "iat": now,
        "exp": now + 300,
        "aud": "https://appleid.apple.com",
        "sub": current_app.config["APPLE_CLIENT_ID"],
    }
    return jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": current_app.config["APPLE_KEY_ID"]})


def _verify_apple_id_token(id_token):
    header = jwt.get_unverified_header(id_token)
    keys_resp = requests.get(APPLE_KEYS_URI, timeout=10)
    keys_resp.raise_for_status()
    jwk = next(k for k in keys_resp.json()["keys"] if k["kid"] == header["kid"])
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
    return jwt.decode(
        id_token,
        public_key,
        algorithms=["RS256"],
        audience=current_app.config["APPLE_CLIENT_ID"],
        issuer="https://appleid.apple.com",
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and user["password_hash"] and check_password_hash(user["password_hash"], password):
            _log_in_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        flash("Email o contraseña incorrectos.")
    return render_template(
        "login.html",
        google_enabled=_google_configured(),
        facebook_enabled=_facebook_configured(),
        apple_enabled=_apple_configured(),
    )


@bp.route("/login/google")
def login_google():
    if not _google_configured():
        flash("El inicio de sesión con Google no está configurado.")
        return redirect(url_for("auth.login"))

    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state
    redirect_uri = url_for("auth.login_google_callback", _external=True)
    params = {
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return redirect(f"{GOOGLE_AUTH_URI}?{query}")


@bp.route("/login/google/callback")
def login_google_callback():
    if not _google_configured():
        return redirect(url_for("auth.login"))

    state = request.args.get("state")
    if not state or state != session.pop("oauth_state", None):
        flash("La sesión de Google ha caducado, inténtalo de nuevo.")
        return redirect(url_for("auth.login"))

    code = request.args.get("code")
    if not code:
        flash("No se pudo iniciar sesión con Google.")
        return redirect(url_for("auth.login"))

    redirect_uri = url_for("auth.login_google_callback", _external=True)
    token_resp = requests.post(
        GOOGLE_TOKEN_URI,
        data={
            "client_id": current_app.config["GOOGLE_CLIENT_ID"],
            "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    if not token_resp.ok:
        flash("No se pudo validar el inicio de sesión con Google.")
        return redirect(url_for("auth.login"))

    access_token = token_resp.json().get("access_token")
    userinfo_resp = requests.get(
        GOOGLE_USERINFO_URI,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if not userinfo_resp.ok:
        flash("No se pudo obtener tu cuenta de Google.")
        return redirect(url_for("auth.login"))

    info = userinfo_resp.json()
    google_sub = info.get("sub")
    email = (info.get("email") or "").strip().lower()

    db = get_db()
    user = _find_or_link_user(db, "google_sub", google_sub, email)

    if not user:
        flash(f"La cuenta {email} no tiene acceso a este panel. Pide que te den de alta.")
        return redirect(url_for("auth.login"))

    _log_in_user(user)
    return redirect(url_for("index"))


@bp.route("/login/facebook")
def login_facebook():
    if not _facebook_configured():
        flash("El inicio de sesión con Facebook no está configurado.")
        return redirect(url_for("auth.login"))

    state = secrets.token_urlsafe(16)
    session["oauth_state_facebook"] = state
    redirect_uri = url_for("auth.login_facebook_callback", _external=True)
    params = {
        "client_id": current_app.config["FACEBOOK_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "email",
        "state": state,
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return redirect(f"{FACEBOOK_AUTH_URI}?{query}")


@bp.route("/login/facebook/callback")
def login_facebook_callback():
    if not _facebook_configured():
        return redirect(url_for("auth.login"))

    state = request.args.get("state")
    if not state or state != session.pop("oauth_state_facebook", None):
        flash("La sesión de Facebook ha caducado, inténtalo de nuevo.")
        return redirect(url_for("auth.login"))

    code = request.args.get("code")
    if not code:
        flash("No se pudo iniciar sesión con Facebook.")
        return redirect(url_for("auth.login"))

    redirect_uri = url_for("auth.login_facebook_callback", _external=True)
    token_resp = requests.get(
        FACEBOOK_TOKEN_URI,
        params={
            "client_id": current_app.config["FACEBOOK_CLIENT_ID"],
            "client_secret": current_app.config["FACEBOOK_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": redirect_uri,
        },
        timeout=10,
    )
    if not token_resp.ok:
        flash("No se pudo validar el inicio de sesión con Facebook.")
        return redirect(url_for("auth.login"))

    access_token = token_resp.json().get("access_token")
    userinfo_resp = requests.get(
        FACEBOOK_USERINFO_URI,
        params={"fields": "id,email", "access_token": access_token},
        timeout=10,
    )
    if not userinfo_resp.ok:
        flash("No se pudo obtener tu cuenta de Facebook.")
        return redirect(url_for("auth.login"))

    info = userinfo_resp.json()
    facebook_id = info.get("id")
    email = (info.get("email") or "").strip().lower()

    db = get_db()
    user = _find_or_link_user(db, "facebook_id", facebook_id, email)

    if not user:
        flash(f"La cuenta {email or 'de Facebook'} no tiene acceso a este panel. Pide que te den de alta.")
        return redirect(url_for("auth.login"))

    _log_in_user(user)
    return redirect(url_for("index"))


@bp.route("/login/apple")
def login_apple():
    if not _apple_configured():
        flash("El inicio de sesión con Apple no está configurado.")
        return redirect(url_for("auth.login"))

    state = secrets.token_urlsafe(16)
    session["oauth_state_apple"] = state
    redirect_uri = url_for("auth.login_apple_callback", _external=True)
    params = {
        "client_id": current_app.config["APPLE_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "response_mode": "form_post",
        "scope": "email name",
        "state": state,
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return redirect(f"{APPLE_AUTH_URI}?{query}")


@bp.route("/login/apple/callback", methods=["POST"])
def login_apple_callback():
    if not _apple_configured():
        return redirect(url_for("auth.login"))

    state = request.form.get("state")
    if not state or state != session.pop("oauth_state_apple", None):
        flash("La sesión de Apple ha caducado, inténtalo de nuevo.")
        return redirect(url_for("auth.login"))

    code = request.form.get("code")
    if not code:
        flash("No se pudo iniciar sesión con Apple.")
        return redirect(url_for("auth.login"))

    redirect_uri = url_for("auth.login_apple_callback", _external=True)
    token_resp = requests.post(
        APPLE_TOKEN_URI,
        data={
            "client_id": current_app.config["APPLE_CLIENT_ID"],
            "client_secret": _apple_client_secret(),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        timeout=10,
    )
    if not token_resp.ok:
        flash("No se pudo validar el inicio de sesión con Apple.")
        return redirect(url_for("auth.login"))

    id_token = token_resp.json().get("id_token")
    try:
        claims = _verify_apple_id_token(id_token)
    except Exception:
        flash("No se pudo verificar tu cuenta de Apple.")
        return redirect(url_for("auth.login"))

    apple_sub = claims.get("sub")
    email = (claims.get("email") or "").strip().lower()

    db = get_db()
    user = _find_or_link_user(db, "apple_sub", apple_sub, email)

    if not user:
        flash(f"La cuenta {email or 'de Apple'} no tiene acceso a este panel. Pide que te den de alta.")
        return redirect(url_for("auth.login"))

    _log_in_user(user)
    return redirect(url_for("index"))


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    db = get_db()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Rellena email y contraseña.")
            return render_template("registro.html")
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.")
            return render_template("registro.html")

        try:
            db.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, generate_password_hash(password)),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash(f"Ya existe una cuenta con el email {email}.")
            return render_template("registro.html")

        estaba_logueado = "user_id" in session
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not estaba_logueado:
            _log_in_user(user)
            return redirect(url_for("index"))

        flash(f"Cuenta creada para {email}.")
        return redirect(url_for("index"))

    return render_template("registro.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
