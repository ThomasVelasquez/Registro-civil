from app.models.database import execute_query, fetch_all, fetch_one


def setup_db():
    query = """
        CREATE TABLE IF NOT EXISTS divorcio (
            sentencia_div INTEGER PRIMARY KEY AUTOINCREMENT,  
            numero_expediente INTEGER NOT NULL UNIQUE,
            asunto_principal TEXT NOT NULL,
            numero_folio INTEGER NOT NULL UNIQUE, 
            numero_tomo INTEGER NOT NULL UNIQUE, 
            fecha_registro_div TEXT NOT NULL,
            lugar_registro_div TEXT NOT NULL, 
            fecha_sentencia_div TEXT NOT NULL,
            lugar_sentencia_div TEXT NOT NULL,
            hora_sentencia_div TEXT NOT NULL,
            causa_divorcio TEXT NOT NULL,
            poder_judicial TEXT NOT NULL,
            nombre_abogado TEXT NOT NULL,
            numero_ipsa INTEGER NOT NULL,
            acta_matrimonio INTEGER NOT NULL UNIQUE,
            motivo TEXT NOT NULL,
            id_ciudadano_1 INTEGER NOT NULL,
            id_ciudadano_2 INTEGER NOT NULL,
            id_empleado INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano_1) REFERENCES ciudadano(id_ciudadano), 
            FOREIGN KEY (id_ciudadano_2) REFERENCES ciudadano(id_ciudadano), 
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
            FOREIGN KEY (acta_matrimonio) REFERENCES matrimonio(acta_matrimonio) 
        )
    """
    execute_query(query)


def crear_divorcio_db(
    numero_expediente,
    asunto_principal,
    numero_folio,
    numero_tomo,
    fecha_registro_div,
    lugar_registro_div,
    fecha_sentencia_div,
    lugar_sentencia_div,
    hora_sentencia_div,
    causa_divorcio,
    poder_judicial,
    nombre_abogado,
    numero_ipsa,
    acta_matrimonio,
    motivo,
    id_ciudadano_1,
    id_ciudadano_2,
    id_empleado,
):

    query = """
        INSERT INTO divorcio (  
            numero_expediente, asunto_principal, numero_folio, numero_tomo,
            fecha_registro_div, lugar_registro_div, fecha_sentencia_div, lugar_sentencia_div, hora_sentencia_div, causa_divorcio,
            poder_judicial, nombre_abogado, numero_ipsa, acta_matrimonio, motivo, id_ciudadano_1, id_ciudadano_2, id_empleado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    params = (
        numero_expediente,
        asunto_principal,
        numero_folio,
        numero_tomo,
        fecha_registro_div,
        lugar_registro_div,
        fecha_sentencia_div,
        lugar_sentencia_div,
        hora_sentencia_div,
        causa_divorcio,
        poder_judicial,
        nombre_abogado,
        numero_ipsa,
        acta_matrimonio,
        motivo,
        id_ciudadano_1,
        id_ciudadano_2,
        id_empleado,
    )
    
    print("PARAMS:", params)
    
    execute_query(query, params)
