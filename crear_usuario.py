from database import conectar_db

def insertar_usuario_demo(nombre,rol):
    conexion = conectar_db()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO usuarios (nombre,rol) VALUES (%s, %s) RETURNING id;"
        cursor.execute(query, (nombre,rol))
        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
        print(f"¡Usuario guardado con éxito! Se le asignó el ID: {nuevo_id}")
    
    except Exception as error:
        print(f"Ocurrió un error al insertar {error}")

    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    insertar_usuario_demo("Oficial Ramírez","Agente")