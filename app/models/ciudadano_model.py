from app.models.database import execute_query, fetch_all, fetch_one

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

def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS ciudadano (
            id_ciudadano INTEGER NOT NULL PRIMARY KEY, 
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


def obtener_todos_ciudadanos():
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano"
    return fetch_all(query)


def obtener_ciudadano_por_cedula(cedula):
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano WHERE cedula = ?"
    return fetch_one(query, (cedula,))


def actualizar_ciudadano_db(cedula, primer_nombre, segundo_nombre, primer_apellido, 
                            segundo_apellido, genero, nacionalidad, estado_civil, 
                            domicilio, fecha_nacimiento,profesion):
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
            profesion = ?,
        WHERE cedula = ?
    """
    params = (
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
        genero, nacionalidad, estado_civil, domicilio, fecha_nacimiento, profesion, cedula
    )
    execute_query(query, params)


""" def eliminar_ciudadano_db(cedula):
    query = "DELETE FROM ciudadano WHERE cedula = ?"
    execute_query(query, (cedula,)) """
