from database import conectar_db

def actualizar_estado_incidencia(incidencia_id, nuevo_estado, usuario_id):
    conexion = conectar_db()
    if not conexion: return

    try:
        cursor = conexion.cursor()
        
        # 1. Modificar el registro existente
        query_update = "UPDATE incidencias SET estado = %s WHERE id = %s;"
        cursor.execute(query_update, (nuevo_estado, incidencia_id))

        # 2. Registrar la acción de modificación en la bitácora
        query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
        detalles = f"Cambio de estado a: {nuevo_estado}"
        cursor.execute(query_aud, (usuario_id, 'ACTUALIZACION', 'incidencias', incidencia_id, detalles))

        conexion.commit()
        print(f"Incidencia {incidencia_id} actualizada a '{nuevo_estado}' y auditada correctamente.")

    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar la transacción: {e}")
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    # Cambiamos el estado de la incidencia ID 1 a 'Resuelta', acción realizada por el usuario ID 1
    actualizar_estado_incidencia(1, "Resuelta", 1)