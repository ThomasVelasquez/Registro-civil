from app.models.database import fetch_all, fetch_one

def get_volumen_total():
    """Obtiene el conteo de registros en las 4 tablas principales."""
    query = """
        SELECT 'Nacimientos' AS tipo, COUNT(*) AS total FROM nacimiento
        UNION ALL
        SELECT 'Matrimonios', COUNT(*) FROM matrimonio
        UNION ALL
        SELECT 'Divorcios', COUNT(*) FROM divorcio
        UNION ALL
        SELECT 'Defunciones', COUNT(*) FROM defuncion;
    """
    return fetch_all(query)


def get_registros_por_anio(anio):
    """Obtiene el conteo de actas registradas en el año dado."""
    query = """
        SELECT 'Nacimientos' AS tipo, COUNT(*) AS total 
        FROM nacimiento 
        WHERE strftime('%Y', fecha_registro_nac) = ?
        UNION ALL
        SELECT 'Matrimonios', COUNT(*) 
        FROM matrimonio 
        WHERE strftime('%Y', fecha_registro_mat) = ?
        UNION ALL
        SELECT 'Divorcios', COUNT(*) 
        FROM divorcio 
        WHERE strftime('%Y', fecha_registro_div) = ?
        UNION ALL
        SELECT 'Defunciones', COUNT(*) 
        FROM defuncion 
        WHERE strftime('%Y', fecha_registro_def) = ?
    """
    params = (str(anio), str(anio), str(anio), str(anio))
    return fetch_all(query, params)


def get_top_empleados_nacimiento():
    """Muestra los 5 empleados que han registrado más nacimientos."""
    query = """
        SELECT 
            c.primer_nombre || ' ' || c.primer_apellido AS Nombre_Completo,
            COUNT(n.acta_nacimiento) AS Total_Registros
        FROM nacimiento n
        JOIN empleado e ON n.id_empleado = e.id_empleado
        JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
        GROUP BY n.id_empleado
        ORDER BY Total_Registros DESC
        LIMIT 5;
    """
    return fetch_all(query)