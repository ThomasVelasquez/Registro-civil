from app.models.database import execute_query, fetch_all, fetch_one

TODOS_LOS_CAMPOS_DB = [
    "numero_folio",
    "numero_tomo",
    "fecha_registro_mat",
    "lugar_registro_mat",
    "id_empleado",
    "fecha_matrimonio",
    "lugar_matrimonio",
    "hora_matrimonio",
    "id_ciudadanoC1",
    "id_ciudadanoC2",
    "id_ciudadanoMC1",
    "id_ciudadanoPC1",
    "id_ciudadanoMC2",
    "id_ciudadanoPC2",
    "id_ciudadanoMT1",
    "id_ciudadanoMT2",
]

TODOS_LOS_CAMPOS = ["acta_matrimonio"] + TODOS_LOS_CAMPOS_DB


def setup_db():
    """Crea la tabla matrimonio si no existe."""
    query = """
        CREATE TABLE IF NOT EXISTS matrimonio(
            acta_matrimonio INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_folio INTEGER NOT NULL UNIQUE,
            numero_tomo INTEGER NOT NULL UNIQUE,
            fecha_registro_mat TEXT NOT NULL,
            lugar_registro_mat TEXT NOT NULL,
            id_empleado INTEGER NOT NULL,
            fecha_matrimonio TEXT NOT NULL,
            lugar_matrimonio TEXT NOT NULL,
            hora_matrimonio TEXT NOT NULL,
            id_ciudadanoC1 INTEGER NOT NULL,
            id_ciudadanoC2 INTEGER NOT NULL,
            id_ciudadanoMC1 INTEGER NOT NULL,
            id_ciudadanoPC1 INTEGER,
            id_ciudadanoMC2 INTEGER NOT NULL,
            id_ciudadanoPC2 INTEGER,
            id_ciudadanoMT1 INTEGER NOT NULL,
            id_ciudadanoMT2 INTEGER NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
            FOREIGN KEY (id_ciudadanoC1) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoC2) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoMC1) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoMC2) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoPC1) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoPC2) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoMT1) REFERENCES ciudadano(id_ciudadano),
            FOREIGN KEY (id_ciudadanoMT2) REFERENCES ciudadano(id_ciudadano)
        )
    """
    execute_query(query)


def crear_matrimonio_db(
    numero_folio,
    numero_tomo,
    fecha_registro_mat,
    lugar_registro_mat,
    id_empleado,
    fecha_matrimonio,
    lugar_matrimonio,
    hora_matrimonio,
    id_ciudadanoC1,
    id_ciudadanoC2,
    id_ciudadanoMC1,
    id_ciudadanoPC1,
    id_ciudadanoMC2,
    id_ciudadanoPC2,
    id_ciudadanoMT1,
    id_ciudadanoMT2,
):
    """Inserta un nuevo registro de matrimonio en la base de datos."""

    campos = ", ".join(TODOS_LOS_CAMPOS_DB)
    placeholders = ", ".join(["?"] * len(TODOS_LOS_CAMPOS_DB))

    query = f"""
        INSERT INTO matrimonio ({campos}) 
        VALUES ({placeholders})
    """

    params = (
        numero_folio,
        numero_tomo,
        fecha_registro_mat,
        lugar_registro_mat,
        id_empleado,
        fecha_matrimonio,
        lugar_matrimonio,
        hora_matrimonio,
        id_ciudadanoC1,
        id_ciudadanoC2,
        id_ciudadanoMC1,
        id_ciudadanoPC1,
        id_ciudadanoMC2,
        id_ciudadanoPC2,
        id_ciudadanoMT1,
        id_ciudadanoMT2,
    )

    print(params, "Parámetros modelo.")
    execute_query(query, params)


def obtener_los_matrimonios():
    """Obtiene todos los registros de matrimonio."""

    campos = "acta_matrimonio, " + ", ".join(TODOS_LOS_CAMPOS_DB)
    query = f"SELECT {campos} FROM matrimonio"
    return fetch_all(query)


def obtener_matrimonio_por_acta(acta_matrimonio):
    """Obtiene un registro de matrimonio por su número de acta."""

    campos = "acta_matrimonio, " + ", ".join(TODOS_LOS_CAMPOS_DB)
    query = f"SELECT {campos} FROM matrimonio WHERE acta_matrimonio = ?"
    return fetch_one(query, (acta_matrimonio,))


def actualizar_matrimonio_db(
    numero_folio,
    numero_tomo,
    fecha_registro_mat,
    lugar_registro_mat,
    id_empleado,
    fecha_matrimonio,
    lugar_matrimonio,
    hora_matrimonio,
    id_ciudadanoC1,
    id_ciudadanoC2,
    id_ciudadanoMC1,
    id_ciudadanoPC1,
    id_ciudadanoMC2,
    id_ciudadanoPC2,
    id_ciudadanoMT1,
    id_ciudadanoMT2,
    acta_matrimonio,
):
    """
    Actualiza un registro de matrimonio con todos los campos.
    Esta función es llamada por la ruta PATCH, que le envía los datos combinados
    (antiguos + nuevos).
    """

    set_clauses = [f"{campo} = ?" for campo in TODOS_LOS_CAMPOS_DB]
    query = f"""
        UPDATE matrimonio SET
            {", ".join(set_clauses)}
        WHERE acta_matrimonio = ?
    """

    params = (
        numero_folio,
        numero_tomo,
        fecha_registro_mat,
        lugar_registro_mat,
        id_empleado,
        fecha_matrimonio,
        lugar_matrimonio,
        hora_matrimonio,
        id_ciudadanoC1,
        id_ciudadanoC2,
        id_ciudadanoMC1,
        id_ciudadanoPC1,
        id_ciudadanoMC2,
        id_ciudadanoPC2,
        id_ciudadanoMT1,
        id_ciudadanoMT2,
        acta_matrimonio,
    )

    print(params, "parámetros de matrimonio (actualización).")
    execute_query(query, params)


def obtener_matrimonios_con_ciudadanos():
    """Obtiene una lista de matrimonios, incluyendo datos básicos de los cónyuges."""

    query = """
        SELECT
            m.*, 
            -- Datos del Cónyuge 1 (C1)
            c1.cedula AS cedula_c1,
            c1.primer_nombre AS nombre1_c1,
            c1.primer_apellido AS apellido1_c1,
            -- Datos del Cónyuge 2 (C2)
            c2.cedula AS cedula_c2,
            c2.primer_nombre AS nombre1_c2,
            c2.primer_apellido AS apellido1_c2
        FROM
            matrimonio m
        JOIN
            ciudadano c1 ON m.id_ciudadanoC1 = c1.id_ciudadano
        JOIN
            ciudadano c2 ON m.id_ciudadanoC2 = c2.id_ciudadano
        ORDER BY 
            m.fecha_registro_mat DESC;
    """
    return fetch_all(query)


def obtener_certificado_por_acta(acta_matrimonio):
    """
    Obtiene un registro de matrimonio ANIDANDO los datos de los 9 ciudadanos.
    Se seleccionan los campos explícitamente para evitar la colisión de alias con m.*.
    """
    query = """
        SELECT
            m.acta_matrimonio,
            m.numero_folio,
            m.numero_tomo,
            m.fecha_registro_mat,
            m.lugar_registro_mat,
            m.fecha_matrimonio,
            m.lugar_matrimonio,
            m.hora_matrimonio,
            
            -- Los IDs originales (id_ciudadanoC1, id_ciudadanoC2, etc.) ya NO se incluyen aquí.
            
            -- Empleado (Registrador Civil)
            json_object(
                'id', e.id_empleado,
                'primer_nombre', c_emp.primer_nombre,
                'primer_apellido', c_emp.primer_apellido
            ) AS id_empleado,
            
            -- Cónyuge 1 (C1)
            json_object(
                'id', c1.id_ciudadano,
                'primer_nombre', c1.primer_nombre,
                'primer_apellido', c1.primer_apellido
            ) AS id_ciudadanoC1,
            
            -- Padre C1 (PC1)
            json_object(
                'id', c_pc1.id_ciudadano,
                'primer_nombre', c_pc1.primer_nombre,
                'primer_apellido', c_pc1.primer_apellido
            ) AS id_ciudadanoPC1,
            
            -- Madre C1 (MC1)
            json_object(
                'id', c_mc1.id_ciudadano,
                'primer_nombre', c_mc1.primer_nombre,
                'primer_apellido', c_mc1.primer_apellido
            ) AS id_ciudadanoMC1,

            -- Cónyuge 2 (C2)
            json_object(
                'id', c2.id_ciudadano,
                'primer_nombre', c2.primer_nombre,
                'primer_apellido', c2.primer_apellido
            ) AS id_ciudadanoC2,
            
            -- Padre C2 (PC2)
            json_object(
                'id', c_pc2.id_ciudadano,
                'primer_nombre', c_pc2.primer_nombre,
                'primer_apellido', c_pc2.primer_apellido
            ) AS id_ciudadanoPC2,
            
            -- Madre C2 (MC2)
            json_object(
                'id', c_mc2.id_ciudadano,
                'primer_nombre', c_mc2.primer_nombre,
                'primer_apellido', c_mc2.primer_apellido
            ) AS id_ciudadanoMC2,
            
            -- Testigo 1 (MT1)
            json_object(
                'id', c_mt1.id_ciudadano,
                'primer_nombre', c_mt1.primer_nombre,
                'primer_apellido', c_mt1.primer_apellido
            ) AS id_ciudadanoMT1,
            
            -- Testigo 2 (MT2)
            json_object(
                'id', c_mt2.id_ciudadano,
                'primer_nombre', c_mt2.primer_nombre,
                'primer_apellido', c_mt2.primer_apellido
            ) AS id_ciudadanoMT2

        FROM
            matrimonio m
        -- Join para Cónyuges
        JOIN ciudadano c1 ON m.id_ciudadanoC1 = c1.id_ciudadano
        JOIN ciudadano c2 ON m.id_ciudadanoC2 = c2.id_ciudadano
        -- Join para Padres/Madres de C1
        LEFT JOIN ciudadano c_pc1 ON m.id_ciudadanoPC1 = c_pc1.id_ciudadano
        LEFT JOIN ciudadano c_mc1 ON m.id_ciudadanoMC1 = c_mc1.id_ciudadano
        -- Join para Padres/Madres de C2
        LEFT JOIN ciudadano c_pc2 ON m.id_ciudadanoPC2 = c_pc2.id_ciudadano
        LEFT JOIN ciudadano c_mc2 ON m.id_ciudadanoMC2 = c_mc2.id_ciudadano
        -- Join para Testigos
        JOIN ciudadano c_mt1 ON m.id_ciudadanoMT1 = c_mt1.id_ciudadano
        JOIN ciudadano c_mt2 ON m.id_ciudadanoMT2 = c_mt2.id_ciudadano
        -- Join para Empleado (Registrador Civil)
        JOIN empleado e ON m.id_empleado = e.id_empleado
        JOIN ciudadano c_emp ON e.id_ciudadano = c_emp.id_ciudadano
        WHERE m.acta_matrimonio = ?
    """
    return fetch_one(query, (acta_matrimonio,))