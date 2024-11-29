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

pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.route("/pacientes", methods=["GET", "POST"])
@role_required("admin")
def ver_pacientes():
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios

        # Consulta para obtener la lista de pacientes
        consulta = "SELECT id_paciente, nombre, apellido, telefono, email , estado FROM pacientes WHERE estado = 'activo' order by apellido asc " 
        cursor.execute(consulta)
        pacientes = cursor.fetchall()

        # Renderizar la plantilla con los pacientes
        return render_template("pacientes.html", pacientes=pacientes)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener los pacientes.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            
@pacientes_bp.route("/nuevo_paciente", methods=["POST"])
def nuevo_paciente():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    email = request.form["email"]

    # Insertar nuevo paciente en la base de datos
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = "INSERT INTO pacientes (nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(consulta, (nombre, apellido, telefono, email))
            conexion.commit()
            flash("Nuevo paciente registrado exitosamente.", "success")
        except Exception as e:
            flash(f"Error al registrar paciente: {e}", "danger")
        finally:
            cursor.close()
            conexion.close()

    return redirect(url_for("pacientes.ver_pacientes"))

@pacientes_bp.route("/editar_paciente", methods=["POST"])
def editar_paciente():
    try:
        # Obtener los datos del formulario
        id_paciente = request.form["id_paciente"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        # Establecer la conexión con la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actualizar el paciente en la base de datos
        consulta = """
        UPDATE pacientes
        SET nombre = %s, apellido = %s, telefono = %s, email = %s
        WHERE id_paciente = %s
        """
        cursor.execute(consulta, (nombre, apellido, telefono, email, id_paciente))
        conexion.commit()

        # Mensaje de éxito
        flash("paciente actualizado con éxito", "success")

        return redirect(url_for('pacientes.ver_pacientes'))  # Redirigir a la página de listado de pacientes

    except Exception as e:
        # Manejo de errores
        flash(f"Error al actualizar el paciente: {e}", "danger")
        return redirect(url_for('pacientes.ver_pacientes'))

    finally:
        # Cerrar la conexión
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
 
 

@pacientes_bp.route("/pacientes/cambiar_estado/<int:id_paciente>", methods=["POST"])
def cambiar_estado(id_paciente):
    try:
        # Establecer la conexión con la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtener el estado actual del paciente
        cursor.execute("SELECT estado FROM pacientes WHERE id_paciente = %s", (id_paciente,))
        estado_actual = cursor.fetchone()

        # Verificar que el estado se haya obtenido correctamente
        if estado_actual is None:
            flash("Paciente no encontrado.", "danger")
            return redirect(url_for('pacientes.ver_pacientes'))

        # Si el estado es 'activo', lo cambiamos a 'inactivo', y viceversa
        nuevo_estado = 'inactivo' if estado_actual[0] == 'activo' else 'activo'

        # Actualizar el estado del paciente en la base de datos
        consulta = "UPDATE pacientes SET estado = %s WHERE id_paciente = %s"
        cursor.execute(consulta, (nuevo_estado, id_paciente))
        conexion.commit()

        flash(f"El estado del paciente ha sido cambiado a {nuevo_estado}.", "success")
        return redirect(url_for('pacientes.ver_pacientes'))

    except Exception as e:
        flash(f"Error al cambiar el estado del paciente: {e}", "danger")
        return redirect(url_for('pacientes.ver_pacientes'))

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@pacientes_bp.route("/pacientes/listar", methods=["GET", "POST"])
def listar_pacientes():
    try:
        # Obtener el parámetro de estado de la URL, si está presente
        estado_filtro = request.args.get("estado")  # 'activo', 'inactivo', o None
        
        # Verificar el valor del filtro
        print(f"Estado del filtro recibido: {estado_filtro}")

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios

        # Consulta para obtener la lista de médicos, con filtro si es necesario
        if estado_filtro:
            consulta = "SELECT * FROM pacientes WHERE estado = %s"
            cursor.execute(consulta, (estado_filtro,))
        else:
            consulta = "SELECT * FROM pacientes"
            cursor.execute(consulta)

        pacientes = cursor.fetchall()

        # Renderizar la plantilla con los médicos
        return render_template("pacientes.html", pacientes=pacientes, estado_filtro=estado_filtro)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener los pacientes.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

