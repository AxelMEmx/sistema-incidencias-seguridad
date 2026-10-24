from database import conectar_db

def obtener_incidencias():
    conexion = conectar_db()
    if not conexion: return

    try:
        cursor = conexion.cursor()

        query = """
            SELECT i.id, i.titulo, i.estado, u.nombre
            FROM incidencias i
            JOIN usuarios u ON i.usuario_id = u.id;
            """
        cursor.execute(query)

        registros = cursor.fetchall()

        print("--- REPORTE DE INCIDENCIAS ---")
        for fila in registros:
            print(f"ID: {fila[0]} | {fila[1]} | Estado: {fila[2]} | Agente: {fila[3]}")

    except Exception as e:
        print("Error al leer datos: {e}")
    finally:
        cursor.close()
        conexion.close()
        
if __name__ == "__main__":
    obtener_incidencias()