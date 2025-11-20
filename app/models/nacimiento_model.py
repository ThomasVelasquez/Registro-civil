from app.models.database import execute_query, fetch_all, fetch_one

TODOS_LOS_CAMPOS = [
    'numero_folio',
    'numero_tomo', 
    'fecha_registro_nac', 
    'lugar_registro_nac',
    'lugar_nacimiento', 
    'hora_nacimiento',
    'nro_certificado_medico',
    'fecha_expedicion_cert',
    'autoridad_expide_cert',
    'numero_mpps_autoridad',
    'nombre_centro_salud',
    'documentos_presentandos',
    'id_ciudadano',
    'id_empleado',
    'id_ciudadanoM',
    'id_ciudadanoP',
    'id_ciudadanoNT1',
    'id_ciudadanoNT2'
]

def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS nacimiento(
            acta_nacimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_folio INTEGER NOT NULL UNIQUE, 
            numero_tomo INTEGER NOT NULL UNIQUE, 
            fecha_registro_nac TEXT NOT NULL,
            lugar_registro_nac TEXT NOT NULL,
            lugar_nacimiento TEXT NOT NULL,
            hora_nacimiento TEXT NOT NULL,
            nro_certificado_medico INTEGER NOT NULL,
            fecha_expedicion_cert TEXT NOT NULL,
            autoridad_expide_cert TEXT NOT NULL,
            numero_mpps_autoridad INTEGER NOT NULL,
            nombre_centro_salud TEXT NOT NULL,
            documentos_presentandos TEXT NOT NULL,
            id_ciudadano INTEGER NOT NULL,
            id_empleado INTEGER NOT NULL,
            id_ciudadanoM INTEGER NOT NULL,
            id_ciudadanoP INTEGER NOT NULL,
            id_ciudadanoNT1 INTEGER NOT NULL,
            id_ciudadanoNT2 INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
            FOREIGN KEY (id_ciudadanoM) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoP) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoNT1) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoNT2) REFERENCES ciudadano(id_ciudadano)
        )
    '''
    execute_query(query)
    
def crear_nacimiento_db(numero_folio, numero_tomo, fecha_registro_nac,
                        lugar_registro_nac, lugar_nacimiento, hora_nacimiento,
                        nro_certificado_medico, fecha_expedicion_cert,
                        autoridad_expide_cert, numero_mpps_autoridad, nombre_centro_salud,
                        documentos_presentandos, id_ciudadano, id_empleado, id_ciudadanoM,
                        id_ciudadanoP, id_ciudadanoNT1, id_ciudadanoNT2):
    
    query = """
        INSERT INTO nacimiento(
            numero_folio, numero_tomo, fecha_registro_nac,
            lugar_registro_nac, lugar_nacimiento, hora_nacimiento,
            nro_certificado_medico, fecha_expedicion_cert,
            autoridad_expide_cert, numero_mpps_autoridad,
            nombre_centro_salud, documentos_presentandos,
            id_ciudadano, id_empleado, id_ciudadanoM, id_ciudadanoP,
            id_ciudadanoNT1, id_ciudadanoNT2
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    params = (
        numero_folio, numero_tomo, fecha_registro_nac,
        lugar_registro_nac, lugar_nacimiento, hora_nacimiento,
        nro_certificado_medico, fecha_expedicion_cert,
        autoridad_expide_cert, numero_mpps_autoridad,
        nombre_centro_salud, documentos_presentandos,
        id_ciudadano, id_empleado, id_ciudadanoM, id_ciudadanoP,
        id_ciudadanoNT1, id_ciudadanoNT2
    )
    
    print(params, "Parametros modelo.")
    
    execute_query(query, params)
    
def obtener_los_nacimientos():
    campos = "acta_nacimiento, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM nacimiento"
    return fetch_all(query)

def obtener_nacimiento_por_acta(acta_nacimiento):
    campos = "acta_nacimiento, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM nacimiento WHERE acta_nacimiento = ?"
    return fetch_one(query, (acta_nacimiento,))

def actualizar_nacimiento_db(
    acta_nacimiento, numero_folio, numero_tomo, fecha_registro_nac,
    lugar_registro_nac, lugar_nacimiento, hora_nacimiento,
    nro_certificado_medico, fecha_expedicion_cert,
    autoridad_expide_cert, numero_mpps_autoridad, nombre_centro_salud,
    documentos_presentandos, id_ciudadano, id_empleado, id_ciudadanoM,
    id_ciudadanoP, id_ciudadanoNT1, id_ciudadanoNT2):
    
    query = """
        UPDATE nacimiento SET
            numero_folio = ?,
            numero_tomo = ?,
            fecha_registro_nac = ?,
            lugar_registro_nac = ?,
            lugar_nacimiento = ?,
            hora_nacimiento = ?,
            nro_certificado_medico = ?,
            fecha_expedicion_cert = ?,
            autoridad_expide_cert = ?,
            numero_mpps_autoridad = ?,
            nombre_centro_salud = ?,
            documentos_presentandos = ?,
            id_ciudadano = ?,
            id_empleado = ?,
            id_ciudadanoM = ?,
            id_ciudadanoP = ?,
            id_ciudadanoNT1 = ?,
            id_ciudadanoNT2 = ?
        WHERE acta_nacimiento = ?
    """
  
    params = (
        numero_folio, numero_tomo, fecha_registro_nac,
        lugar_registro_nac, lugar_nacimiento, hora_nacimiento,
        nro_certificado_medico, fecha_expedicion_cert,
        autoridad_expide_cert, numero_mpps_autoridad,
        nombre_centro_salud, documentos_presentandos,
        id_ciudadano, id_empleado, id_ciudadanoM, id_ciudadanoP,
        id_ciudadanoNT1, id_ciudadanoNT2,
        acta_nacimiento 
    )
    
    print(params, "parametros de nacimiento")
    execute_query(query, params)
    
""" def eliminar_nacimiento_db(acta_nacimiento):
    query = "DELETE FROM nacimiento WHERE acta_nacimiento = ?"
    execute_query(query, (acta_nacimiento)) """