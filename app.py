from flask import Flask, render_template, request, redirect
from database import conectar_db

app = Flask(__name__)

@app.route('/')
def index():
    conexion = conectar_db()
    if not conexion: return "Error de conexión"
    try:
        cursor = conexion.cursor()
        query = "SELECT i.id, i.titulo, i.estado, u.nombre FROM incidencias i JOIN usuarios u ON i.usuario_id = u.id ORDER BY i.id ASC;"
        cursor.execute(query)
        lista_incidencias = cursor.fetchall()
    except Exception as e:
        lista_incidencias = []
    finally:
        cursor.close()
        conexion.close()
    
    return render_template('index.html', incidencias=lista_incidencias)

@app.route('/registrar', methods=['POST'])
def registrar():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    nivel = request.form['nivel']
    usuario_id = request.form['usuario_id']
    estado = "Pendiente" # Todo reporte nuevo inicia como pendiente

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # 1. Insertar incidencia
            query_inc = "INSERT INTO incidencias (titulo, descripcion, nivel, estado, usuario_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(query_inc, (titulo, descripcion, nivel, estado, usuario_id))
            inc_id = cursor.fetchone()[0]

            # 2. Insertar rastro de auditoría
            query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
            detalles = f"Registro web de incidencia nivel {nivel}"
            cursor.execute(query_aud, (usuario_id, 'CREACION', 'incidencias', inc_id, detalles))

            conexion.commit()
        except Exception as e:
            conexion.rollback()
            print(f"Error al guardar: {e}")
        finally:
            cursor.close()
            conexion.close()

    # Redirigir a la vista principal para ver la tabla actualizada
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)