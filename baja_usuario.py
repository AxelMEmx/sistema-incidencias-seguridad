from database import conectar_db

def dar_baja_usuario(usuario_baja_id, admin_id):
    conexion = conectar_db()
    if not conexion: return

    try:
        cursor = conexion.cursor()

        query_baja = "UPDATE usuarios SET activo = FALSE WHERE id = %s;"
        cursor.execute(query_baja, (usuario_baja_id,))

        query_aud = "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, detalles) VALUES (%s, %s, %s, %s, %s);"
        detalles = f"Baja lógica del usuario ID {usuario_baja_id}"
        cursor.execute(query_aud, (admin_id, 'BAJA_LOGICA','usuarios', usuario_baja_id, detalles))

        conexion.commit()
        print(f"Usuario {usuario_baja_id} dado de baja lógicamente.")

    except Exception as e:
        conexion.rollback()
        print(f"Error en la transacción: {e}")
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    # Simulamos que el usuario 1 es un administrador dando de baja al usuario 1 (él mismo por ahora)
    dar_baja_usuario(1, 1)