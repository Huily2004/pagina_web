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

main = Blueprint("main", __name__)


@main.route("/" , methods=["GET", "POST"]) #Es la ruta de la URL en la aplicación.Esa ruta acepta solicitudes de tipo GET (para mostrar la página) y POST (para procesar datos enviados, como formularios).
def index():
    
    
    return render_template("index.html")# Renderiza la plantilla `index.html`, pasando la lista de clientes como contexto.

@main.route("/logout")
def logout():
    session.clear()  # Limpia todos los datos de la sesión
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("login.login"))



    