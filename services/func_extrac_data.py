import re

# Regex para datos de 941 - Inicio
def extract_payer_name(text):
    pattern = r'TAXPAYER NAME:\s*(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_payment_amount_941(text):
    pattern = r'Payment Amount\s+\$([0-9,]+\.\d{2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_account_number(text):
    pattern = r'Account Number.*(\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_settlement_date(text):
    """Extrae el valor del campo 'Settlement Date' del texto.

    Args:
        text (str): El texto completo del PDF

    Returns:
        str: El valor de 'Settlement Date'
    """
    pattern = r'Settlement Date\s+(\d{2}/\d{2}/\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Settlement Date no encontrado'

# Regex para datos de 941 - Fin

# Regex para datos EDD - Inicio

def extract_payment_amount_edd(text, occurrence=2):
    pattern = r'Payment Amount:\s+\$([0-9,]+\.\d{2})'
    matches = re.findall(pattern, text)
    if len(matches) >= occurrence:
        return matches[occurrence - 1]
    return None

def extract_name(text):
    pattern = r'Name:\s*(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_payment_date(text):
    """Extrae el valor del campo 'Payment Date' del texto.

    Args:
        text (str): El texto completo del PDF

    Returns:
        str: El valor de 'Payment Date'
    """
    pattern = r'Payment Date:\s*(\d{2}-[A-Za-z]{3}-\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Payment Date no encontrado'

# Regex para datos de EDD - Fin

# Regex para datos PDF General - Inicio

def extract_payment_amount_general_941(text):
    pattern = r'TOTAL FEDERAL DEPOSIT\s+(\d+\.\d{2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_payment_amount_general_edd(text):
    pattern = r'TOTAL STATE DEPOSIT\s+(\d+\.\d{2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_company_name(text):
    """Extrae el nombre de la empresa del primer renglón del texto.

    Args:
        text (str): El texto completo del documento

    Returns:
        str: El nombre de la empresa
    """
    # Dividir el texto en líneas y tomar la primera línea
    primera_linea = text.split('\n')[0]

    # Expresión regular para eliminar la parte entre paréntesis y la información de la página
    pattern = r'^(.*?)(?:\s*\(.*\)\s*Page\s*\d+)?$'
    match = re.match(pattern, primera_linea)
    if match:
        return match.group(1).strip()
    return 'Nombre de la empresa no encontrado.'


def extract_payment_date(text):
    """Extrae el valor del campo 'Payment Date' del texto.

    Args:
        text (str): El texto completo del PDF

    Returns:
        str: El valor de 'Payment Date'
    """
    pattern = r'Payment Date:\s*(\d{2}-[A-Za-z]{3}-\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

# Regex para datos de PDF General - Fin

if __name__ == "__main__":

    # Ejemplo de uso
    texto = """ALEJANDRAS FASHION INC (A03) Page 39

Payroll Register Report
From: 10/21/2024 To 10/27/2024 Check Date: 11/01/2024

Employee Name Employee ID Date Check Number Net
DEPARTMENT - ALL
EMPLOYER'S EXPENSES ACTUAL
Social Security 10383.95
Medicare 2428.50
Federal Unemployment 91.13
State Unemployment 334.14
Employment Training Fund Tax 15.19
Worker's Comp. Expense 0.00
TOTAL EMPLOYER'S EXPENSES 13252.91
EMPLOYEE(S) DEDUCTIONS ACTUAL
Federal W/H 10158.00
Social Security 10383.99
Medicare 2428.56
State W/H 2246.58
CA SDI 1842.33
Garnish 297.50
Calsavers 105.73
TOTAL EMPLOYEE(S) DEDUCTIONS 27462.69
TOTAL NET PAYROLL 140020.38
TOTAL PAYROLL COST 180735.98
TOTAL FEDERAL DEPOSIT 35783.00
TOTAL STATE DEPOSIT 4438.24

Prepared by Chermisqui and Associates 11/07/24 12:00 PM

"""

    name_EED = extract_company_name(texto)
    print(f'Name: {name_EED}')
