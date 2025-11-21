from app.models.database import execute_query, fetch_all, fetch_one

TODOS_LOS_CAMPOS = [
    "id_empleado",
    "id_ciudadano",
    "numero_empleado",
    "oficina_registro",
    "numero_resolucion",
    "fecha_resolucion",
    "numero_gaceta",
    "fecha_gaceta",
]


def setup_db():
    query = """
        CREATE TABLE IF NOT EXISTS empleado (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ciudadano INTEGER NOT NULL,
            numero_empleado INTEGER NOT NULL UNIQUE,
            oficina_registro TEXT NOT NULL, 
            numero_resolucion TEXT NOT NULL, 
            fecha_resolucion TEXT NOT NULL,
            numero_gaceta TEXT NOT NULL,
            fecha_gaceta TEXT NOT NULL,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano) 
        )
    """
    execute_query(query)


def crear_empleado_db(
    id_empleado,
    id_ciudadano,
    numero_empleado,
    oficina_registro,
    numero_resolucion,
    fecha_resolucion,
    numero_gaceta,
    fecha_gaceta):

    query = """
        INSERT INTO empleado (
            id_empleado, id_ciudadano, numero_empleado,
            oficina_registro, numero_resolucion, fecha_resolucion,
            numero_gaceta, fecha_gaceta
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        id_empleado,
        id_ciudadano,
        numero_empleado,
        oficina_registro,
        numero_resolucion,
        fecha_resolucion,
        numero_gaceta,
        fecha_gaceta,
    )
    
    print(params,'<-- parametros empleado_model crear_empleado_db')

    execute_query(query, params)


def obtener_todos_empleados():
    campos = "id_empleado, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM empleado"
    return fetch_all(query)

def obtener_empleados_con_ciudadanos():

    query = """
        SELECT 
            e.*,                 -- Todos los campos de la tabla empleado
            c.cedula,            -- Cedula del ciudadano/empleado
            c.primer_nombre,     -- Primer nombre del ciudadano/empleado
            c.segundo_nombre,    -- Segundo nombre
            c.primer_apellido,   -- Primer apellido
            c.segundo_apellido   -- Segundo apellido
        FROM 
            empleado e
        JOIN 
            ciudadano c ON e.id_ciudadano = c.id_ciudadano
        ORDER BY
            e.numero_empleado;
    """
    return fetch_all(query)