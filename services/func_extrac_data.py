import re


def extract_payment_amount(text, occurrence=1):
    pattern = r'Payment Amount\s+\$([0-9,]+\.\d{2})'
    matches = re.findall(pattern, text)
    if len(matches) >= occurrence:
        return matches[occurrence - 1]
    return None

def extract_account_number(text):
    pattern = r'Account Number.*(\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_payer_name(text):
    pattern = r'TAXPAYER NAME:\s*(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def extract_name(text):
    pattern = r'NAME:\s*(.*)'
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
    return None


if __name__ == "__main__":

    # Ejemplo de uso
    texto = """11/7/24, 12:10 PM

TAXPAYER NAME: ALEJANDRA S FASHIÓON INC

Deposit Confirmation
Your payment has been accepted.

Payment Successful

Welcome To EFTPS - Payments

TIN: xxxxx6163

An EFT Acknowledgement Number has been provided for this payment. Please keep this number for your records.

REMINDER: REMEMBER TO FILE ALL RETURNS WHEN DUE!

EFT ACKNOWLEDGEMENT NUMBER:

270471391950351

Payment Information

Entered Data

Taxpayer EIN

XXXxxXX0 163

Tax Form 941 Employers Federal Tax
Tax Type Federal Tax Deposit

Tax Period Q4/2024

Payment Amount $35,783.00

Settlement Date 11/08/2024

Account Number XOX0000X5293

Account Type CHECKING

Routing Number 122235821

Bank Name US BANK NA

https://www.eftps.gov/eftps/payments/payment-confirmation-flow?execution=e3s2

11
"""

    payment_amount = extract_payment_amount(texto)
    print(f'Payment Amount: ${payment_amount}')
