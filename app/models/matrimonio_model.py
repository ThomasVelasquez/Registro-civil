from app.models.database import execute_query, fetch_all, fetch_one


TODOS_LOS_CAMPOS = [
    "acta_matrimonio",
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
    "id_ciudadanoMT2"
]


def setup_db():
    query = """
  CREATE TABLE IF NOT EXISTS matrimonio (
    acta_matrimonio INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_folio INTEGER NOT NULL UNIQUE,
    numero_tomo INTEGER NOT NULL UNIQUE,
    fecha_registro_mat TEXT NOT NULL,
    lugar_registro_mat TEXT NOT NULL,
    id_empleado INTEGER NOT NULL,
    fecha_matrimonio TEXT NOT NULL,
    lugar_matrimonio TEXT NOT NULL,
    hora_matrimonio INTEGER NOT NULL,
    id_ciudadanoC1 INTEGER NOT NULL,
    id_ciudadanoC2 INTEGER NOT NULL,
    id_ciudadanoMC1 INTEGER NOT NULL,
    id_ciudadanoPC1 INTEGER NOT NULL,
    id_ciudadanoMC2 INTEGER NOT NULL,
    id_ciudadanoPC2 INTEGER NOT NULL,
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
    acta_matrimonio,
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

    query = """
        INSERT INTO matrimonio(
            acta_matrimonio,numero_folio,numero_tomo,fecha_registro_mat,lugar_registro_mat,
            id_empleado,fecha_matrimonio,lugar_matrimonio,hora_matrimonio,
            id_ciudadanoC1,id_ciudadanoC2,id_ciudadanoMC1,id_ciudadanoPC1,
            id_ciudadanoMC2,id_ciudadanoPC2,id_ciudadanoMT1,id_ciudadanoMT2) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    params = (
        acta_matrimonio,
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
    campos = "acta_matrimonio, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM matrimonio"
    return fetch_all(query)

def obtener_matrimonio_por_acta(acta_matrimonio):
    campos = "acta_matrimonio, " + ", ".join(TODOS_LOS_CAMPOS)
    query = f"SELECT {campos} FROM matrimonio WHERE acta_matrimonio = ?"
    return fetch_one(query, (acta_matrimonio,))


def actualizar_matrimonio_db(
    acta_matrimonio,
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
    id_ciudadanoMT2
):

    query = """
        UPDATE matrimonio SET
            numero_folio = ?,
            numero_tomo = ?,
            fecha_registro_mat = ?,
            lugar_registro_mat = ?,
            id_empleado = ?,
            fecha_matrimonio = ?,
            lugar_matrimonio = ?,
            hora_matrimonio = ?,
            id_ciudadanoC1 = ?,
            id_ciudadanoC2 = ?,
            id_ciudadanoMC1 = ?,
            id_ciudadanoPC1 = ?,
            id_ciudadanoMC2 = ?,
            id_ciudadanoPC2 = ?,
            id_ciudadanoMT1 = ?,
            id_ciudadanoMT2 = ?
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
        acta_matrimonio
    )

    print(params, "parámetros de matrimonio")
    execute_query(query, params)
