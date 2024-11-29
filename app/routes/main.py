from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
)

#Blueprint: Permite modularizar la aplicación en componentes.
#render_template: Renderiza plantillas HTML con datos dinámicos
#request: Gestiona solicitudes HTTP (como datos enviados por un formulario).
#session: Maneja sesiones de usuario.
#flash: Permite enviar mensajes temporales al usuario.
#redirect: Redirige a otra URL.
#url_for: Genera rutas dinámicamente.
#abort: Termina la solicitud con un código de error HTTP.

from ..conexion_bd  import obtener_conexion
from functools import wraps
def role_required(*required_roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get("rol")
            if user_role not in required_roles:
                flash("No tienes permisos para esa acción.", "danger")
                return redirect(
                    url_for("alumnos.alumnos")
                )  # Redirige al usuario a la página de inicio o a una página de error
            return f(*args, **kwargs)

        return decorated_function

    return wrapper
main = Blueprint("main", __name__)


@main.route("/" , methods=["GET", "POST"]) #Es la ruta de la URL en la aplicación.Esa ruta acepta solicitudes de tipo GET (para mostrar la página) y POST (para procesar datos enviados, como formularios).
def index():
    
    
    return redirect(url_for("login.login"))# Renderiza la plantilla `login.html`, pasando la lista de clientes como contexto.

@main.route("/logout")
def logout():
    session.clear()  # Limpia todos los datos de la sesión
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("login.login"))





    