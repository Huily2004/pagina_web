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

login_bp = Blueprint("login", __name__)




@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        contrasena = request.form["contrasena"]

        # Verificar usuario y contraseña
        conexion =obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                consulta = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
                cursor.execute(consulta, (nombre_usuario, contrasena))
                usuario = cursor.fetchone()
                session["nombre"] = usuario["nombre_usuario"]
                
                if usuario:
                    # Credenciales válidas
                    session["usuario"] = usuario["nombre_usuario"] 
                    session["rol"] = usuario["rol"]  
                   # Guardar el usuario en la sesión
                    return redirect(url_for("pacientes.ver_pacientes"))
                else:
                    flash("Usuario o contraseña incorrectos.", "error")
            except Exception as e:
                flash(f"Error al consultar la base de datos: {e}", "error")
            finally:
                cursor.close()
                conexion.close()

    return render_template("login.html")
@login_bp.route("/registro", methods=["POST"])
def registro():
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]


    # Verificar que el nombre de usuario no esté registrado
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(consulta, (nombre_usuario,))
            usuario = cursor.fetchone()

            if usuario:
                flash("El nombre de usuario ya está registrado.", "error")
                return redirect(url_for("login"))
            else:
                # Insertar nuevo usuario
                consulta_insert = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
                cursor.execute(consulta_insert, (nombre_usuario, contrasena))
                conexion.commit()
                flash("Registro exitoso, ahora puedes iniciar sesión.", "success")
                return redirect(url_for("pacientes.ver_pacientes"))
        except Exception as e:
            flash(f"Error al registrar el usuario: {e}", "error")
        finally:
            cursor.close()
            conexion.close()

    return redirect(url_for("login.login"))
