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

citas_bp = Blueprint("citas", __name__)

@citas_bp.route("/citas", methods=["GET", "POST"])
def ver_citas():
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios

        # Consulta para obtener la lista de pacientes
        consulta = """
            SELECT citas.id_cita, 
            citas.id_paciente,
            citas.id_medico,
                   pacientes.nombre AS nombre_paciente, 
                   pacientes.apellido AS apellido_paciente,
                   medicos.nombre AS nombre_medico, 
                   medicos.apellido AS apellido_medico,
                   citas.fecha_hora ,
                   citas.motivo ,
                   citas.estado
        
            FROM citas
            JOIN pacientes ON citas.id_paciente = pacientes.id_paciente
            JOIN medicos ON citas.id_medico = medicos.id_medico
        """
        cursor.execute(consulta)
        citas = cursor.fetchall()

        # Renderizar la plantilla con los pacientes
        return render_template("citas.html", citas = citas)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener las citas.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            
@citas_bp.route("/citas/crear", methods=["POST"])
def crear_cita():
    try:
        id_paciente = request.form["id_paciente"]
        id_medico = request.form["id_medico"]
        fecha_hora = request.form["fecha_hora"]
        motivo = request.form["motivo"]
        estado = request.form["estado"]

        # Validar los campos (opcional)
        if not id_paciente or not id_medico or not fecha_hora or not motivo or not estado:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("citas.ver_citas"))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Insertar la cita en la base de datos
        consulta = """
            INSERT INTO citas (id_paciente, id_medico, fecha_hora, motivo, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (id_paciente, id_medico, fecha_hora, motivo, estado))
        conexion.commit()

        flash("Cita creada exitosamente.", "success")
        return redirect(url_for("citas.ver_citas"))

    except Exception as e:
        print(f"Error al crear la cita: {e}")
        flash("Hubo un error al intentar crear la cita.", "danger")
        return redirect(url_for("citas.ver_citas"))

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
        
@citas_bp.route("/citas/editar", methods=["POST"])
def editar_cita():
    try:
        id_cita = request.form["id_cita1"]
        id_paciente = request.form["id_paciente1"]
        id_medico = request.form["id_medico1"]
        fecha_hora = request.form["fecha_hora1"]
        motivo = request.form["motivo1"]
        estado = request.form["estado1"]

        # Validar los campos
        if not id_paciente or not id_medico or not fecha_hora or not motivo or not estado:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('citas.ver_citas'))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actualizar la cita en la base de datos
        consulta = """
            UPDATE citas
            SET id_paciente = %s, id_medico = %s, fecha_hora = %s, motivo = %s, estado = %s
            WHERE id_cita = %s
        """
        cursor.execute(consulta, (id_paciente, id_medico, fecha_hora, motivo, estado, id_cita))
        conexion.commit()

        flash("Cita actualizada exitosamente.", "success")
        return redirect(url_for("citas.ver_citas"))

    except Exception as e:
        print(f"Error al actualizar la cita: {e}")
        flash("Hubo un error al intentar actualizar la cita.", "danger")
        return redirect(url_for("citas.ver_citas"))

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
@citas_bp.route("/citas/cambiar_estado", methods=["POST"])
def cambiar_estado():
    try:
        # Obtener datos del formulario
        id_cita= request.form.get("id_cita1")
        nuevo_estado = request.form.get("estado")

        if not id_cita or not nuevo_estado:
            flash("Datos incompletos para cambiar el estado.", "danger")
            return redirect(url_for("citas.ver_citas"))

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actualizar el estado del médico
        consulta = "UPDATE citas SET estado = %s WHERE id_cita = %s"
        cursor.execute(consulta, (nuevo_estado, id_cita))
        conexion.commit()

        flash(f"Estado del médico con ID {id_cita} cambiado a {nuevo_estado}.", "success")
        return redirect(url_for("citas.ver_citas"))

    except Exception as e:
        print(f"Error al cambiar el estado de la cita: {e}")
        flash("Hubo un error al cambiar el estado de la cita.", "danger")
        return redirect(url_for("citas.ver_citas"))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@citas_bp.route("/citas/listar", methods=["GET", "POST"])
def listar_citas():
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
            consulta = """
            SELECT citas.id_cita, 
            citas.id_paciente,
            citas.id_medico,
                   pacientes.nombre AS nombre_paciente, 
                   pacientes.apellido AS apellido_paciente,
                   medicos.nombre AS nombre_medico, 
                   medicos.apellido AS apellido_medico,
                   citas.fecha_hora ,
                   citas.motivo ,
                   citas.estado
        
            FROM citas
            JOIN pacientes ON citas.id_paciente = pacientes.id_paciente
            JOIN medicos ON citas.id_medico = medicos.id_medico WHERE citas.estado = %s 
        """
            
            cursor.execute(consulta, (estado_filtro,))
        else:
            consulta = """
            SELECT citas.id_cita, 
            citas.id_paciente,
            citas.id_medico,
                   pacientes.nombre AS nombre_paciente, 
                   pacientes.apellido AS apellido_paciente,
                   medicos.nombre AS nombre_medico, 
                   medicos.apellido AS apellido_medico,
                   citas.fecha_hora ,
                   citas.motivo ,
                   citas.estado
        
            FROM citas
            JOIN pacientes ON citas.id_paciente = pacientes.id_paciente
            JOIN medicos ON citas.id_medico = medicos.id_medico
        """
            cursor.execute(consulta)

        citas = cursor.fetchall()

        # Renderizar la plantilla con los médicos
        return render_template("citas.html", citas=citas, estado_filtro=estado_filtro)

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return render_template("index.html", mensaje="Error al obtener citas.")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            
            
