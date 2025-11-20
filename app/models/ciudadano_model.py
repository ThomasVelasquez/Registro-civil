from app.models.database import execute_query, fetch_all, fetch_one, execute_many_query # <-- Se asume 'execute_many_query'

# Lista de todos los campos que tiene la tabla Ciudadano
TODOS_LOS_CAMPOS = [
    # 'cedula', 
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

def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS ciudadano (
            id_ciudadano INTEGER PRIMARY KEY AUTOINCREMENT, 
            cedula INTEGER UNIQUE, 
            primer_nombre TEXT NOT NULL, 
            segundo_nombre TEXT, 
            primer_apellido TEXT NOT NULL, 
            segundo_apellido TEXT, 
            genero TEXT NOT NULL, 
            nacionalidad TEXT NOT NULL, 
            estado_civil TEXT NOT NULL, 
            domicilio TEXT NOT NULL, 
            fecha_nacimiento TEXT NOT NULL,
            profesion TEXT
        )
    '''
    execute_query(query)


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
    
    last_id = execute_query(query, params)
    return last_id 


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
    execute_many_query(query, lista_de_datos)


def obtener_todos_ciudadanos():
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano"
    return fetch_all(query)


def obtener_ciudadano_por_id(id_ciudadano):
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano WHERE id_ciudadano = ?"
    return fetch_one(query, (id_ciudadano,))


def actualizar_ciudadano_db(id_ciudadano, cedula, primer_nombre, segundo_nombre, primer_apellido, 
                            segundo_apellido, genero, nacionalidad, estado_civil, 
                            domicilio, fecha_nacimiento, profesion):
    query = """
        UPDATE ciudadano SET
            cedula = ?,
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
        WHERE id_ciudadano = ? OR cedula = ? 
    """
    params = (
        id_ciudadano, cedula,
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
        genero, nacionalidad, estado_civil, domicilio, fecha_nacimiento, profesion
    )
    execute_query(query, params)


""" def eliminar_ciudadano_db(id_ciudadano):
    query = "DELETE FROM ciudadano WHERE id_ciudadano = ?"
    execute_query(query, (id_ciudadano,)) """
