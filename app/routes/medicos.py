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

medicos_bp = Blueprint("medicos", __name__)

@medicos_bp.route("/medicos", methods=["GET", "POST"])
def ver_medicos():
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios

        # Consulta para obtener la lista de pacientes
        consulta = "SELECT * FROM medicos WHERE estado = 'activo' order by apellido asc  "
        cursor.execute(consulta)
        medicos = cursor.fetchall()

        # Renderizar la plantilla con los pacientes
        return render_template("medicos.html", medicos = medicos)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener los medicos.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            

@medicos_bp.route("/medicos/nuevo", methods=["POST"])
def nuevo_medico():
    try:
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        especialidad = request.form.get("especialidad")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        estado = request.form.get("estado")

        # Validación básica de los datos
        if not nombre or not apellido or not especialidad or not telefono or not email or not estado:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("medicos.ver_medicos"))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Insertar un nuevo médico
        consulta = """
            INSERT INTO medicos (nombre, apellido, especialidad, telefono, email, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, apellido, especialidad, telefono, email, estado)
        cursor.execute(consulta, valores)
        conexion.commit()

        flash("Médico agregado exitosamente.", "success")
        return redirect(url_for("medicos.ver_medicos"))

    except Exception as e:
        print(f"Error al agregar médico: {e}")
        flash("Hubo un error al intentar agregar el médico.", "danger")
        return redirect(url_for("medicos.ver_medicos"))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@medicos_bp.route("/medicos/editar", methods=["POST"])
def editar_medico():
    try:
        # Obtener los datos del formulario
        id_medico = request.form.get("id_medico")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        especialidad = request.form.get("especialidad")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        estado = request.form.get("estado")

        # Validación básica
        if not id_medico or not nombre or not apellido or not especialidad or not telefono or not email or not estado:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("medicos.ver_medicos"))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actualizar el médico en la base de datos
        consulta = """
            UPDATE medicos
            SET nombre = %s, apellido = %s, especialidad = %s, telefono = %s, email = %s, estado = %s
            WHERE id_medico = %s
        """
        valores = (nombre, apellido, especialidad, telefono, email, estado, id_medico)
        cursor.execute(consulta, valores)
        conexion.commit()

        flash("Médico actualizado exitosamente.", "success")
        return redirect(url_for("medicos.ver_medicos"))

    except Exception as e:
        print(f"Error al editar médico: {e}")
        flash("Hubo un error al intentar actualizar el médico.", "danger")
        return redirect(url_for("medicos.ver_medicos"))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@medicos_bp.route("/cambiar_estado", methods=["POST"])
def cambiar_estado():
    try:
        # Obtener datos del formulario
        id_medico = request.form.get("id_medico")
        nuevo_estado = request.form.get("estado")

        if not id_medico or not nuevo_estado:
            flash("Datos incompletos para cambiar el estado.", "danger")
            return redirect(url_for("medicos.ver_medicos"))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actualizar el estado del médico
        consulta = "UPDATE medicos SET estado = %s WHERE id_medico = %s"
        cursor.execute(consulta, (nuevo_estado, id_medico))
        conexion.commit()

        flash(f"Estado del médico con ID {id_medico} cambiado a {nuevo_estado}.", "success")
        return redirect(url_for("medicos.ver_medicos"))

    except Exception as e:
        print(f"Error al cambiar el estado del médico: {e}")
        flash("Hubo un error al cambiar el estado del médico.", "danger")
        return redirect(url_for("medicos.ver_medicos"))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@medicos_bp.route("/medicos/listar", methods=["GET", "POST"])
def listar_medicos():
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
            consulta = "SELECT * FROM medicos WHERE estado = %s"
            cursor.execute(consulta, (estado_filtro,))
        else:
            consulta = "SELECT * FROM medicos"
            cursor.execute(consulta)

        medicos = cursor.fetchall()

        # Renderizar la plantilla con los médicos
        return render_template("medicos.html", medicos=medicos, estado_filtro=estado_filtro)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener los medicos.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

