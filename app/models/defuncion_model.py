from app.models.database import execute_query, fetch_all, fetch_one

TODOS_LOS_CAMPOS = [
    'acta_defuncion',
    'numero_folio',
    'numero_tomo',
    'fecha_registro_def',
    'lugar_registro_def',
    'id_empleado',
    'id_ciudadano',
    'fecha_fallecimiento',
    'lugar_fallecimiento',
    'hora_fallecimiento',
    'causa',
    'forma',
    'nro_certificado_def',
    'fecha_expedicion_def',
    'autoridad_expide_def',
    'numero_mpps_autoridad_def',
    'denominacion_dependencia_salud',
    'id_ciudadano_declarante',
    'relacion_con_fallecido',
    'id_ciudadanoC',
    'id_ciudadano_FM',
    'id_ciudadano_FP'
]


def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS defuncion (
            acta_defuncion INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_folio INTEGER NOT NULL UNIQUE,
            numero_tomo INTEGER NOT NULL UNIQUE,
            fecha_registro_def TEXT NOT NULL,
            lugar_registro_def TEXT NOT NULL,
            id_empleado INTEGER NOT NULL,
            id_ciudadano INTEGER NOT NULL,
            fecha_fallecimiento TEXT NOT NULL,
            lugar_fallecimiento TEXT NOT NULL,
            hora_fallecimiento TEXT NOT NULL,
            causa TEXT NOT NULL,
            forma TEXT NOT NULL,
            nro_certificado_def INTEGER NOT NULL,
            fecha_expedicion_def TEXT NOT NULL,
            autoridad_expide_def TEXT NOT NULL,
            numero_mpps_autoridad_def INTEGER NOT NULL,
            denominacion_dependencia_salud TEXT NOT NULL,
            id_ciudadano_declarante INTEGER NOT NULL,
            relacion_con_fallecido TEXT NOT NULL,
            id_ciudadanoC INTEGER,
            id_ciudadano_FM INTEGER NOT NULL,
            id_ciudadano_FP INTEGER,
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano), 
            FOREIGN KEY (id_ciudadano_declarante) REFERENCES ciudadano(id_ciudadano), 
            FOREIGN KEY (id_ciudadanoC) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadano_FM) REFERENCES ciudadano(id_ciudadano), 
            FOREIGN KEY (id_ciudadano_FP) REFERENCES ciudadano(id_ciudadano)  
        )
    '''
    execute_query(query)

def crear_defuncion_db(
    numero_folio, numero_tomo, fecha_registro_def, lugar_registro_def,
    id_empleado, id_ciudadano,
    fecha_fallecimiento, lugar_fallecimiento, hora_fallecimiento,
    causa, forma,
    nro_certificado_def, fecha_expedicion_def, autoridad_expide_def,
    numero_mpps_autoridad_def, denominacion_dependencia_salud,
    id_ciudadano_declarante, relacion_con_fallecido,
    id_ciudadanoC, id_ciudadano_FM, id_ciudadano_FP):

    query = """
        INSERT INTO defuncion (
            numero_folio, numero_tomo, fecha_registro_def, lugar_registro_def,
            id_empleado, id_ciudadano,
            fecha_fallecimiento, lugar_fallecimiento, hora_fallecimiento,
            causa, forma,
            nro_certificado_def, fecha_expedicion_def, autoridad_expide_def,
            numero_mpps_autoridad_def, denominacion_dependencia_salud,
            id_ciudadano_declarante, relacion_con_fallecido,
            id_ciudadanoC, id_ciudadano_FM, id_ciudadano_FP
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        numero_folio, numero_tomo, fecha_registro_def, lugar_registro_def,
        id_empleado, id_ciudadano,
        fecha_fallecimiento, lugar_fallecimiento, hora_fallecimiento,
        causa, forma,
        nro_certificado_def, fecha_expedicion_def, autoridad_expide_def,
        numero_mpps_autoridad_def, denominacion_dependencia_salud,
        id_ciudadano_declarante, relacion_con_fallecido,
        id_ciudadanoC, id_ciudadano_FM, id_ciudadano_FP
    )
    
    print(params, 'parámetros modelo.')
    
    execute_query(query, params)
    
def obtener_todas_defunciones():
    campos = "acta_defuncion, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM defuncion"
    return fetch_all(query)

def obtener_defuncion_por_acta(acta_defuncion):
    campos = "acta_defuncion, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM defuncion WHERE acta_defuncion = ?"
    return fetch_one(query, (acta_defuncion,))

def actualizar_defuncion_db(
    acta_defuncion, numero_folio, numero_tomo,
    fecha_registro_def, lugar_registro_def,
    id_empleado, id_ciudadano,
    fecha_fallecimiento, lugar_fallecimiento, hora_fallecimiento,
    causa, forma,
    nro_certificado_def, fecha_expedicion_def, autoridad_expide_def,
    numero_mpps_autoridad_def, denominacion_dependencia_salud,
    id_ciudadano_declarante, relacion_con_fallecido,
    id_ciudadanoC, id_ciudadano_FM, id_ciudadano_FP):
    
    query = """
        UPDATE defuncion SET
            numero_folio = ?,
            numero_tomo = ?,
            fecha_registro_def = ?,
            lugar_registro_def = ?,
            id_empleado = ?,
            id_ciudadano = ?,
            fecha_fallecimiento = ?,
            lugar_fallecimiento = ?,
            hora_fallecimiento = ?,
            causa = ?,
            forma = ?,
            nro_certificado_def = ?,
            fecha_expedicion_def = ?,
            autoridad_expide_def = ?,
            numero_mpps_autoridad_def = ?,
            denominacion_dependencia_salud = ?,
            id_ciudadano_declarante = ?,
            relacion_con_fallecido = ?,
            id_ciudadanoC = ?,
            id_ciudadano_FM = ?,
            id_ciudadano_FP = ?
        WHERE acta_defuncion = ?
    """
    params = (
        numero_folio, numero_tomo, fecha_registro_def, lugar_registro_def,
        id_empleado, id_ciudadano,
        fecha_fallecimiento, lugar_fallecimiento, hora_fallecimiento,
        causa, forma,
        nro_certificado_def, fecha_expedicion_def, autoridad_expide_def,
        numero_mpps_autoridad_def, denominacion_dependencia_salud,
        id_ciudadano_declarante, relacion_con_fallecido,
        id_ciudadanoC, id_ciudadano_FM, id_ciudadano_FP,
        acta_defuncion 
    )
    execute_query(query, params)
    

