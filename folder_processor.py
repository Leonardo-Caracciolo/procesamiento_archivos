import os
from file_processor import process_file

def process_client_folders(parent_folder, year, month):
    """Recorrer carpetas de clientes y procesar archivos."""
    payroll_folder_name = f"Payroll {year}"
    year_folder_name = f"{year}"

    for client_folder in os.listdir(parent_folder):
        client_path = os.path.join(parent_folder, client_folder)

        if not os.path.isdir(client_path):
            continue

        # Buscar subcarpetas específicas
        payroll_path = os.path.join(client_path, payroll_folder_name)
        year_path = os.path.join(client_path, year_folder_name)

        target_path = payroll_path if os.path.exists(payroll_path) else year_path if os.path.exists(year_path) else None

        if not target_path:
            print(f"No se encontró una carpeta válida en: {client_path}")
            continue

        print(f"Ingresando a carpeta: {target_path}")

        # Procesar archivos en la carpeta
        for file_name in os.listdir(target_path):
            file_path = os.path.join(target_path, file_name)
            process_file(file_path, year, month)
