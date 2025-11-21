from app.models.database import execute_query, fetch_all, fetch_one, execute_many_query # <-- Se asume 'execute_many_query'

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


def obtener_ciudadano_por_cedula(cedula):
    campos = "id_ciudadano, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM ciudadano WHERE cedula = ?"
    return fetch_one(query, (cedula,))


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


def actualizar_ciudadano_parcial_db(id_ciudadano_o_cedula, datos_a_actualizar):
   
    
    CAMPOS_CIUDADANO_EDITABLES = [
        'cedula', 
        'primer_nombre', 
        'segundo_nombre', 
        'primer_apellido', 
        'segundo_apellido', 
        'genero', 
        'domicilio',
        
    ]

    campos_validos = {
        k: v for k, v in datos_a_actualizar.items() 
        if k in CAMPOS_CIUDADANO_EDITABLES and v is not None
    }

    if not campos_validos:
        print("Error: No se recibieron campos válidos para actualizar al ciudadano.")
        return 0

   
    set_clauses = [f"{campo} = ?" for campo in campos_validos.keys()]
    set_query = ", ".join(set_clauses)
    
    
    query = f"""
        UPDATE ciudadano SET
            {set_query}
        WHERE id_ciudadano = ? OR cedula = ? 
    """
    
    params = list(campos_validos.values()) + [id_ciudadano_o_cedula, id_ciudadano_o_cedula]
    
    
    execute_query(query, params)