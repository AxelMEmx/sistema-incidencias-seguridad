from database import conectar_db

def registrar_incidencia(titulo, descripcion, nivel, estado, usuario_id):
    conexion = conectar_db()
    if not conexion: return

    try:
        cursor = conexion.cursor()
        query_inc = "INSERT INTO incidencias (titulo, descripcion, nivel, estado, usuario_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
        cursor.execute(query_inc, (titulo, descripcion, nivel, estado, usuario_id))
        inc_id = cursor.fetchone()[0]

        query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
        detalles = f"Registro de incidencia nivel {nivel}"
        cursor.execute(query_aud, (usuario_id, 'CREACION', 'incidencias', inc_id, detalles))

        conexion.commit()
        print(f"Incidencia {inc_id} y auditoría guardadas correctamente de forma simultánea")

    except Exception as e:
        conexion.rollback()
        print(f"Error crítico, se canceló toda la transacción: {e}")
    finally:
        cursor.close()
        conexion.close()
if __name__ == "__main__":
    registrar_incidencia("Corte de energía", "Falla eléctrica en el sector B", "Alta", "Pendiente", 1)