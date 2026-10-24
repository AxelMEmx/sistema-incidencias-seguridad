from flask import Flask, render_template, request, redirect
from database import conectar_db

app = Flask(__name__)

@app.route('/')
def index():
    conexion = conectar_db()
    if not conexion: return "Error de conexión"
    
    try:
        cursor = conexion.cursor()
        
        # 1. NUEVO: Consultas para el panel de estadísticas
        cursor.execute("SELECT COUNT(*) FROM incidencias;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incidencias WHERE estado = 'Pendiente';")
        pendientes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incidencias WHERE nivel = 'Alta';")
        criticas = cursor.fetchone()[0]

        # Consulta original de la tabla
        query = "SELECT i.id, i.titulo, i.estado, u.nombre FROM incidencias i JOIN usuarios u ON i.usuario_id = u.id ORDER BY i.id ASC;"
        cursor.execute(query)
        lista_incidencias = cursor.fetchall()
    except Exception as e:
        total = pendientes = criticas = 0
        lista_incidencias = []
    finally:
        cursor.close()
        conexion.close()
    
    # Enviamos los números nuevos al HTML
    return render_template('index.html', incidencias=lista_incidencias, total=total, pendientes=pendientes, criticas=criticas)

@app.route('/registrar', methods=['POST'])
def registrar():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    nivel = request.form['nivel']
    usuario_id = request.form['usuario_id']
    estado = "Pendiente" 

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query_inc = "INSERT INTO incidencias (titulo, descripcion, nivel, estado, usuario_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(query_inc, (titulo, descripcion, nivel, estado, usuario_id))
            inc_id = cursor.fetchone()[0]

            query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
            detalles = f"Registro web de incidencia nivel {nivel}"
            cursor.execute(query_aud, (usuario_id, 'CREACION', 'incidencias', inc_id, detalles))

            conexion.commit()
        except Exception as e:
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()
    return redirect('/')

# 2. NUEVO: Ruta para cambiar el estado con el botón de la web
@app.route('/resolver/<int:id_incidencia>', methods=['POST'])
def resolver(id_incidencia):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Cambiamos el estado
            query_update = "UPDATE incidencias SET estado = 'Resuelta' WHERE id = %s;"
            cursor.execute(query_update, (id_incidencia,))
            
            # Auditoría de la acción
            query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query_aud, (1, 'ACTUALIZACION', 'incidencias', id_incidencia, "Resuelta desde sistema web"))
            
            conexion.commit()
        except Exception as e:
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)