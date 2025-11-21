from flask import request, jsonify
from app.models import ciudadano_model
from sqlite3 import IntegrityError
import csv  
import io  

REQUIRED_FIELDS = [
    # 'cedula',
    "primer_nombre",
    "primer_apellido",
    "genero",
    "nacionalidad",
    "estado_civil",
    "domicilio",
    "fecha_nacimiento",
    # 'profesion'
]

CSV_FIELDS_ORDER = [
    "cedula",
    "primer_nombre",
    "segundo_nombre",
    "primer_apellido",
    "segundo_apellido",
    "genero",
    "nacionalidad",
    "estado_civil",
    "domicilio",
    "fecha_nacimiento",
    "profesion",
]


def setup_routes(ciudadano_bp):

    @ciudadano_bp.route("", methods=["POST"])
    def crear_ciudadano():
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in data or data.get(field) is None
        ]

        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Faltan campos obligatorios.",
                        "campos_faltantes": missing_fields,
                    }
                ),
                400,
            )

        cedula = data.get("cedula") or data.get("id_number")
        primer_nombre = data.get("primer_nombre") or data.get("first_name")
        segundo_nombre = data.get("segundo_nombre") or data.get("second_name")
        primer_apellido = (
            data.get("primer_apellido")
            or data.get("first_lastName")
            or data.get("first_lastName")
        )
        segundo_apellido = data.get("segundo_apellido") or data.get("second_lastName")
        genero = data.get("genero") or data.get("gender")
        nacionalidad = data.get("nacionalidad") or data.get("nationality")
        estado_civil = data.get("estado_civil") or data.get("civil_status")
        domicilio = data.get("domicilio") or data.get("address")
        fecha_nacimiento = data.get("fecha_nacimiento") or data.get("birth_date")
        profesion = data.get("profesion") or data.get("profession")

        try:
            nuevo_id = ciudadano_model.crear_ciudadano_db(
                cedula,
                primer_nombre,
                segundo_nombre,
                primer_apellido,
                segundo_apellido,
                genero,
                nacionalidad,
                estado_civil,
                domicilio,
                fecha_nacimiento,
                profesion,
            )
            return (
                jsonify({"message": "Ciudadano creado.", "id_ciudadano": nuevo_id}),
                201,
            )

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: La cédula ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @ciudadano_bp.route("/cargar-csv", methods=["POST"])
    def cargar_csv():
        if "file" not in request.files:
            return (
                jsonify(
                    {
                        "error": "No se encontró ningún archivo en la solicitud (expected key: 'file')."
                    }
                ),
                400,
            )

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No se seleccionó ningún archivo."}), 400

        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"))
        except UnicodeDecodeError:
            return (
                jsonify(
                    {
                        "error": "Error de codificación: Asegúrese que el archivo es UTF-8 o ASCII."
                    }
                ),
                400,
            )

        lector_csv = csv.reader(stream, delimiter=",")

        try:
            next(lector_csv)
        except StopIteration:
            return jsonify({"error": "El archivo CSV está vacío."}), 400

        datos_a_insertar = []
        registros_fallidos = 0

        for i, fila in enumerate(lector_csv):

            if len(fila) == len(CSV_FIELDS_ORDER):
                try:
                    datos_ciudadano = (int(fila[0]),) + tuple(fila[1:])
                    datos_a_insertar.append(datos_ciudadano)

                except ValueError:
                    registros_fallidos += 1
                    print(
                        f"Fila {i+2} ignorada: Cédula ({fila[0]}) no es un número entero válido."
                    )

                except Exception:
                    registros_fallidos += 1
                    print(f"Fila {i+2} ignorada por error de formato inesperado.")

            else:
                registros_fallidos += 1
                print(
                    f"Fila {i+2} ignorada: Número incorrecto de campos ({len(fila)}), se esperaban {len(CSV_FIELDS_ORDER)}."
                )

        if not datos_a_insertar:
            return (
                jsonify(
                    {
                        "error": f"No hay datos válidos para insertar. {registros_fallidos} registro(s) fallido(s)."
                    }
                ),
                400,
            )

        try:
            ciudadano_model.insertar_multiples_ciudadanos_db(datos_a_insertar)

            mensaje_exito = (
                f"Carga masiva exitosa. {len(datos_a_insertar)} ciudadano(s) creado(s)."
            )
            if registros_fallidos > 0:
                mensaje_exito += f" ({registros_fallidos} registro(s) no fueron procesados por error de formato)."

            return jsonify({"message": mensaje_exito}), 201

        except IntegrityError:
            return (
                jsonify(
                    {
                        "error": "Error: Una o más cédulas ya existen en la base de datos (IntegrityError)."
                    }
                ),
                400,
            )
        except Exception as e:
            print(f"Error al insertar múltiples ciudadanos en DB: {e}")
            return (
                jsonify(
                    {
                        "error": "Ocurrió un error al intentar la inserción masiva en la DB.",
                        "detalle_tecnico": str(e),
                    }
                ),
                500,
            )

    @ciudadano_bp.route("/", methods=["GET"])
    def listar_ciudadanos():
        ciudadanos = ciudadano_model.obtener_todos_ciudadanos()
        return jsonify(ciudadanos), 200

    @ciudadano_bp.route("/<int:id_ciudadano>", methods=["GET"])
    def obtener_ciudadano(id_ciudadano):

        ciudadano = ciudadano_model.obtener_ciudadano_por_cedula(id_ciudadano)

        if ciudadano:

            return jsonify(ciudadano), 200

        return jsonify({"message": "Ciudadano no encontrado."}), 404

    @ciudadano_bp.route("/<int:cedula>", methods=["PUT"])
    def actualizar_ciudadano(id_ciudadano):
        data = request.get_json()

        if not data:
            return (
                jsonify({"error": "No se recibieron datos JSON para actualizar."}),
                400,
            )

        cedula = data.get("cedula") or data.get("id_number")
        primer_nombre = data.get("primer_nombre") or data.get("first_name")
        segundo_nombre = data.get("segundo_nombre") or data.get("second_name")
        primer_apellido = (
            data.get("primer_apellido")
            or data.get("first_lastName")
            or data.get("first_lastName")
        )
        segundo_apellido = data.get("segundo_apellido") or data.get("second_lastName")
        genero = data.get("genero") or data.get("gender")
        nacionalidad = data.get("nacionalidad") or data.get("nationality")
        estado_civil = data.get("estado_civil") or data.get("civil_status")
        domicilio = data.get("domicilio") or data.get("address")
        fecha_nacimiento = data.get("fecha_nacimiento") or data.get("birth_date")
        profesion = data.get("profesion") or data.get("profession")

        try:
            ciudadano_model.actualizar_ciudadano_db(
                cedula,
                primer_nombre,
                segundo_nombre,
                primer_apellido,
                segundo_apellido,
                genero,
                nacionalidad,
                estado_civil,
                domicilio,
                fecha_nacimiento,
                profesion,
            )
            return jsonify({"message": f"Ciudadano {id_ciudadano} actualizado."}), 200
        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error de integridad al actualizar. Revise que los campos obligatorios estén presentes y no sean NULL.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )
        except Exception as e:
            return (
                jsonify({"error": "Error al actualizar.", "detalle_tecnico": str(e)}),
                500,
            )


    @ciudadano_bp.route("/<int:id_o_cedula>", methods=["PATCH"])
    def actualizar_ciudadano_parcial(id_o_cedula):
        data = request.get_json()

        if not data:
            return jsonify({"Error": "No se recibieron datos JSON para actualizar."}), 400

        datos_para_modelo = {}

        mapeo_campos = {
            "first_name": "primer_nombre",
            "second_name": "segundo_nombre",
            "first_lastName": "primer_apellido",
            "second_lastName": "segundo_apellido",
            "gender": "genero",
            "address": "domicilio",
            "id_number": "cedula",
        }

        for key_frontend, key_backend in mapeo_campos.items():
            if key_frontend in data:
                datos_para_modelo[key_backend] = data.get(key_frontend)
            elif key_backend in data:
                datos_para_modelo[key_backend] = data.get(key_backend)

        if not datos_para_modelo:
            return (
                jsonify(
                    {
                        "Error": "El cuerpo de la solicitud no contiene campos válidos para actualizar."
                    }
                ),
                400,
            )

        try:
            ciudadano_model.actualizar_ciudadano_parcial_db(id_o_cedula, datos_para_modelo)

            return (
                jsonify({"Message": f"Ciudadano {id_o_cedula} actualizado parcialmente."}),
                200,
            )

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error de integridad: Puede que la cédula que intenta actualizar ya exista en otro registro.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )
        except Exception as e:
            print(f"Error en PATCH /ciudadanos: {e}")
            return (
                jsonify({"error": "Error al actualizar.", "detalle_tecnico": str(e)}),
                500,
            )
