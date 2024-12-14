import os

def find_folder_with_number_and_month(path, year, number, month):
    
    year_folder = None
    
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if str(year) in name and "Payroll" in name:
                year_folder = os.path.join(root, name)
            elif str(year) in name and "payroll" in name:
                year_folder = os.path.join(root, name)
            elif str(year) in name:
                    year_folder = os.path.join(root, name)

    if year_folder is not None: 
        
        for root, dirs, files in os.walk(year_folder):
            for name in dirs:
                if str(number) in name and month in name:
                    return os.path.join(root, name)
                elif str(number) in name:
                    return os.path.join(root, name)
    return None

# Ejemplo de uso
path = r"C:\Users\seba\Downloads\InputsTesteo-20241213T020658Z-001\InputsTesteo\V18 cOMPANY"
number = 12
month = "December"
year = 2024

result = find_folder_with_number_and_month(path, year, number, month)
if result:
    print(f'La carpeta que contiene el número {number} y el mes {month} es: {result}')
    print(result)
else:
    print(f'No se encontró ninguna carpeta que contenga el número {number} y el mes {month}.')
