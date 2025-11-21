from app.models.database import execute_query, fetch_all, fetch_one

TODOS_LOS_CAMPOS = [
    "sentencia_divorcio",
    "numero_expediente",
    "asunto_principal",
    "numero_folio",
    "numero_tomo",
    "fecha_registro_div",
    "lugar_registro_div",
    "id_empleado",
    "fecha_sentencia",
    "lugar_sentencia",
    "poder_judicial",
    "nombre_abogado",
    "numero_ipsa_abogado",
    "acta_matrimonio",
    "motivo"
]

def setup_db():
    query = """
        CREATE TABLE IF NOT EXISTS divorcio (
            sentencia_divorcio INTEGER PRIMARY KEY AUTOINCREMENT,  
            numero_expediente INTEGER NOT NULL UNIQUE,
            asunto_principal TEXT NOT NULL UNIQUE,
            numero_folio INTEGER NOT NULL UNIQUE, 
            numero_tomo INTEGER NOT NULL UNIQUE, 
            fecha_registro_div TEXT NOT NULL,
            lugar_registro_div TEXT NOT NULL,
            id_empleado INTEGER NOT NULL,
            fecha_sentencia TEXT NOT NULL,
            lugar_sentencia TEXT NOT NULL,
            poder_judicial TEXT NOT NULL,
            nombre_abogado TEXT NOT NULL,
            numero_ipsa_abogado INTEGER NOT NULL,
            acta_matrimonio INTEGER NOT NULL,
            motivo TEXT NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
            FOREIGN KEY (acta_matrimonio) REFERENCES matrimonio(acta_matrimonio) 
        )
    """
    execute_query(query)


def crear_divorcio_db(
    numero_expediente, asunto_principal, numero_folio, numero_tomo,
    fecha_registro_div, lugar_registro_div,
    id_empleado,
    fecha_sentencia, lugar_sentencia,
    poder_judicial, nombre_abogado, numero_ipsa_abogado,
    acta_matrimonio, motivo):

    query = """
        INSERT INTO divorcio (  
            numero_expediente, asunto_principal, numero_folio, numero_tomo,
            fecha_registro_div, lugar_registro_div,
            id_empleado,
            fecha_sentencia, lugar_sentencia,
            poder_judicial, nombre_abogado, numero_ipsa_abogado,
            acta_matrimonio, motivo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        numero_expediente, asunto_principal, numero_folio, numero_tomo,
        fecha_registro_div, lugar_registro_div,
        id_empleado,
        fecha_sentencia, lugar_sentencia,
        poder_judicial, nombre_abogado, numero_ipsa_abogado,
        acta_matrimonio, motivo
    )
    
    print("PARAMS:", params)
    
    execute_query(query, params)



def obtener_divorcios_con_matrimonio_y_ciudadanos():
    
    query = """
        SELECT
            d.*,                        
            m.fecha_matrimonio,          
            m.lugar_matrimonio,          
            m.acta_matrimonio,         
            
            -- Datos del Cónyuge 1 (C1)
            c1.cedula AS cedula_c1,
            c1.primer_nombre AS nombre1_c1,
            c1.primer_apellido AS apellido1_c1,
            
            -- Datos del Cónyuge 2 (C2)
            c2.cedula AS cedula_c2,
            c2.primer_nombre AS nombre1_c2,
            c2.primer_apellido AS apellido1_c2
            
        FROM
            divorcio d
        JOIN
            matrimonio m ON d.acta_matrimonio = m.acta_matrimonio
        JOIN
            ciudadano c1 ON m.id_ciudadanoC1 = c1.id_ciudadano
        JOIN
            ciudadano c2 ON m.id_ciudadanoC2 = c2.id_ciudadano
        ORDER BY
            d.fecha_registro_div DESC;
    """
    return fetch_all(query)

def obtener_por_sentencia_divorcio(sentencia_id):
    """Obtiene un registro de divorcio por su clave primaria (sentencia_divorcio)."""
    
    campos_select = ", ".join([f"d.{c}" for c in TODOS_LOS_CAMPOS]) 

    

    query = f"""
        SELECT
            {campos_select}, 
            m.fecha_matrimonio, 
            m.lugar_matrimonio, 
            m.acta_matrimonio, 
            
            -- Datos del Cónyuge 1 (C1)
            c1.cedula AS cedula_c1,
            c1.primer_nombre AS nombre1_c1,
            c1.primer_apellido AS apellido1_c1,
            
            -- Datos del Cónyuge 2 (C2)
            c2.cedula AS cedula_c2,
            c2.primer_nombre AS nombre1_c2,
            c2.primer_apellido AS apellido1_c2
            
        FROM
            divorcio d
        JOIN
            matrimonio m ON d.acta_matrimonio = m.acta_matrimonio
        JOIN
            ciudadano c1 ON m.id_ciudadanoC1 = c1.id_ciudadano
        JOIN
            ciudadano c2 ON m.id_ciudadanoC2 = c2.id_ciudadano
        WHERE
            d.sentencia_divorcio = ?;
    """
    return fetch_one(query, (sentencia_id,))



def actualizar_divorcio_db(
    sentencia_id, 
    lugar_sentencia, poder_judicial, asunto_principal, motivo, 
    lugar_registro_div, nombre_abogado, numero_ipsa_abogado
    ):
    """Actualiza los campos editables del registro de divorcio."""
    
    query = """
        UPDATE divorcio
        SET 
            lugar_sentencia = ?,
            poder_judicial = ?,
            asunto_principal = ?,
            motivo = ?,
            lugar_registro_div = ?,
            nombre_abogado = ?,
            numero_ipsa_abogado = ?
        WHERE sentencia_divorcio = ?
    """
    
    params = (
        lugar_sentencia, poder_judicial, asunto_principal, motivo, 
        lugar_registro_div, nombre_abogado, numero_ipsa_abogado,
        sentencia_id 
    )
    
    execute_query(query, params)