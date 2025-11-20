from app.models.database import execute_query, fetch_all, fetch_one, execute_many_query # <-- Se asume 'execute_many_query'

# Lista de todos los campos que tiene la tabla Ciudadano
TODOS_LOS_CAMPOS = [
    'cedula', 
    'primer_nombre', 
    'segundo_nombre', 
    'primer_apellido', 
    'segundo_apellido', 
    'genero', 
    'nacionalidad', 
    'estado_civil', 
    'domicilio', 
    'fecha_nacimiento',
    'profesion'
]

# --- 1. SETUP INICIAL ---
def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS ciudadano (
            id_ciudadano INTEGER PRIMARY KEY AUTOINCREMENT, 
            cedula INTEGER NOT NULL UNIQUE, 
            primer_nombre TEXT NOT NULL, 
            segundo_nombre TEXT, 
            primer_apellido TEXT NOT NULL, 
            segundo_apellido TEXT, 
            genero TEXT NOT NULL, 
            nacionalidad TEXT NOT NULL, 
            estado_civil TEXT NOT NULL, 
            domicilio TEXT NOT NULL, 
            fecha_nacimiento TEXT NOT NULL,
            profesion TEXT NOT NULL
        )
    '''
    execute_query(query)


# --- 2. CREAR UN SOLO CIUDADANO ---
def crear_ciudadano_db(cedula, primer_nombre, segundo_nombre, primer_apellido, 
                      segundo_apellido, genero, nacionalidad, estado_civil, 
                      domicilio, fecha_nacimiento, profesion):

    query = """
        INSERT INTO ciudadano (
            cedula, primer_nombre, segundo_nombre, primer_apellido, 
            segundo_apellido, genero, nacionalidad, estado_civil, 
            domicilio, fecha_nacimiento, profesion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        cedula, primer_nombre, segundo_nombre, primer_apellido, 
        segundo_apellido, genero, nacionalidad, estado_civil, 
        domicilio, fecha_nacimiento, profesion
    )
    
    print(params,'parametros modelo')
    
    execute_query(query, params)


# --- 3. CARGA MASIVA DE CIUDADANOS (NUEVA FUNCIÓN) ---
def insertar_multiples_ciudadanos_db(lista_de_datos):
    """
    Inserta múltiples filas de ciudadanos en la base de datos usando execute_many.
    
    :param lista_de_datos: Una lista de tuplas con los datos del ciudadano
                           en el orden definido por TODOS_LOS_CAMPOS.
    """
    query = """
        INSERT INTO ciudadano (
            cedula, primer_nombre, segundo_nombre, primer_apellido, 
            segundo_apellido, genero, nacionalidad, estado_civil, 
            domicilio, fecha_nacimiento, profesion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    # execute_many_query debe manejar la conexión, cursor y cursor.executemany(query, lista_de_datos)
    execute_many_query(query, lista_de_datos)


# --- 4. OBTENER TODOS ---
def obtener_todos_ciudadanos():
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano"
    return fetch_all(query)


# --- 5. OBTENER POR CÉDULA ---
def obtener_ciudadano_por_cedula(cedula):
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano WHERE cedula = ?"
    return fetch_one(query, (cedula,))


# --- 6. ACTUALIZAR CIUDADANO ---
def actualizar_ciudadano_db(cedula, primer_nombre, segundo_nombre, primer_apellido, 
                            segundo_apellido, genero, nacionalidad, estado_civil, 
                            domicilio, fecha_nacimiento, profesion):
    query = """
        UPDATE ciudadano SET
            primer_nombre = ?, 
            segundo_nombre = ?, 
            primer_apellido = ?, 
            segundo_apellido = ?, 
            genero = ?, 
            nacionalidad = ?, 
            estado_civil = ?, 
            domicilio = ?, 
            fecha_nacimiento = ?,
            profesion = ?
        WHERE cedula = ? 
    """
    params = (
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
        genero, nacionalidad, estado_civil, domicilio, fecha_nacimiento, profesion, cedula
    )
    execute_query(query, params)


# --- 7. ELIMINAR CIUDADANO (Descomentado si lo necesitas) ---
""" 
def eliminar_ciudadano_db(cedula):
    query = "DELETE FROM ciudadano WHERE cedula = ?"
    execute_query(query, (cedula,)) 
"""