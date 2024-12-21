import logging
import os
import sys

def setup_logging(log_file="app.log"):
    """Configurar el sistema de logging."""
    # Obtener la ruta completa del archivo de logs
    log_dir = os.path.join(os.path.dirname(sys.executable), "logs")
    # log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()  # Mostrar también en la consola
        ]
    )

def log_info(message):
    """Registrar un mensaje informativo."""
    logging.info(message)

def log_warning(message):
    """Registrar un mensaje de advertencia."""
    logging.warning(message)

def log_error(message):
    """Registrar un mensaje de error."""
    logging.error(message)
