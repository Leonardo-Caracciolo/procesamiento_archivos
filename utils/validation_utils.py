def validate_year_month(year, month):
    """Validar que el año y mes seleccionados sean correctos."""
    if not year.isdigit() or not 2000 <= int(year) <= 2030:
        raise ValueError("El año seleccionado no es válido.")
    if month not in [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]:
        raise ValueError("El mes seleccionado no es válido.")

def is_weekly_file(file_name, year):
    """Verificar si un archivo tiene formato semanal."""
    try:
        base_name = file_name.split(".")[0]
        if len(base_name) == 8:
            day, month, file_year = int(base_name[:2]), int(base_name[2:4]), int(base_name[4:])
            return 1 <= day <= 31 and 1 <= month <= 12 and file_year == int(year)
    except ValueError:
        pass
    return False
