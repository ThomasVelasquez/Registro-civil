from app.models.database import execute_query, fetch_all, fetch_one




def setup_db():
    query = '''
        CREATE TABLE IF NOT EXISTS defuncion (
            acta_defuncion INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  
            numero_folio INTEGER NOT NULL UNIQUE, 
            numero_tomo INTEGER NOT NULL UNIQUE, 
            fecha_registro_def TEXT NOT NULL,
            lugar_registro_def TEXT NOT NULL,
            fecha_fallecimiento TEXT NOT NULL,
            lugar_fallecimiento TEXT NOT NULL,
            hora_fallecimiento TEXT NOT NULL,
            causa_fallecimiento TEXT NOT NULL,
            forma_fallecimiento TEXT NOT NULL,
            nro_certificado_defuncion INTEGER NOT NULL,
            fecha_expedicion_defuncion TEXT NOT NULL,
            autoridad_expide_defuncion TEXT NOT NULL,
            numero_mpps_autoridad_def INTEGER NOT NULL,
            denominacion_dependencia_salud TEXT NOT NULL,
            relacion_con_fallecido TEXT NOT NULL,
            id_ciudadano INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano),
            id_ciudadano_declarante INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano_declarante) REFERENCES ciudadano(id_ciudadano),
            id_ciudadano_FM INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano_FM) REFERENCES ciudadano(id_ciudadano),
            id_ciudadano_FP INTEGER NOT NULL,
            FOREIGN KEY (id_ciudadano_FP) REFERENCES ciudadano(id_ciudadano),
            id_empleado INTEGER NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        )
    '''
    execute_query(query)

def crear_defuncion_db(numero_folio, numero_tomo, fecha_registro_def,
                       lugar_registro_def, fecha_fallecimiento, lugar_fallecimiento,
                       hora_fallecimiento, causa_fallecimiento, forma_fallecimiento,
                       nro_certificado_defuncion, fecha_expedicion_defuncion,
                       autoridad_expide_defuncion, numero_mpss_autoridad_def,
                       denominacion_dependencia_salud, relacion_con_fallecido,
                       id_ciudadano, id_ciudadano_declarante, id_ciudadano_FM,
                       id_ciudadano_FP, id_empleado):

    query = """
        INSERT INTO defuncion (
                    numero_folio,numero_tomo,fecha_registro_def,
                    lugar_registro_def,fecha_fallecimiento,lugar_fallecimiento,
                    hora_fallecimiento,causa_fallecimiento,forma_fallecimiento,
                    nro_certificado_defuncion,fecha_expedicion_defuncion,
                    autoridad_expide_defuncion,numero_mpss_autoridad_def,
                    denominacion_dependencia_salud,relacion_con_fallecido,
                    id_ciudadano, id_ciudadano_declarante, id_ciudadano_FM,
                    id_ciudadano_FP, id_empleado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        numero_folio, numero_tomo, fecha_registro_def,
        lugar_registro_def, fecha_fallecimiento, lugar_fallecimiento,
        hora_fallecimiento, causa_fallecimiento, forma_fallecimiento,
        nro_certificado_defuncion, fecha_expedicion_defuncion,
        autoridad_expide_defuncion, numero_mpss_autoridad_def,
        denominacion_dependencia_salud, relacion_con_fallecido,
        id_ciudadano, id_ciudadano_declarante, id_ciudadano_FM,
        id_ciudadano_FP, id_empleado
    )
    
    print(params, 'parametros modelo')
    
    execute_query(query, params)