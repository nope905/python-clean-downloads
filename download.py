import os
import shutil
import logging
import pandas as pd
from datetime import datetime

# Verificar y crear directorios si no existen
log_directory = 'D:/descargas/logs'
os.makedirs(log_directory, exist_ok=True)

target_directory = 'D:/descargas'
os.makedirs(target_directory, exist_ok=True)

# Configuración del logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'archivo_log.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

download_folder = 'C:/Users/Nope/Downloads'
target_folder = 'D:/descargas'
log_data = []

def categorize_file(file_name):
    extension = os.path.splitext(file_name)[1].lower()
    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'imagenes'
    elif extension in ['.pdf', '.docx', '.txt']:
        return 'documentos'
    elif extension in ['.mp4', '.mkv', '.avi']:
        return 'videos'
    elif extension in ['.zip', '.rar', '.tar']:
        return 'archivos_comprimidos'
    elif extension in ['.exe', '.msi']:
        return 'ejecutables'
    else:
        return 'otros'

def move_files():
    for file_name in os.listdir(download_folder):
        source = os.path.join(download_folder, file_name)
        if os.path.isfile(source):
            try:
                category = categorize_file(file_name)
                destination_folder = os.path.join(target_folder, category)
                os.makedirs(destination_folder, exist_ok=True)
                destination = os.path.join(destination_folder, file_name)
                shutil.move(source, destination)
                logging.info(f'{file_name} movido a {destination_folder}')
                
                # Registrar los detalles del archivo movido
                log_data.append({
                    'file_name': file_name,
                    'source': source,
                    'destination': destination,
                    'category': category,
                    'timestamp': datetime.now()
                })
            except FileNotFoundError as fnf_error:
                logging.error(f'Archivo no encontrado: {fnf_error}')
            except PermissionError as perm_error:
                logging.error(f'Permiso denegado: {perm_error}')
            except Exception as e:
                logging.error(f'Error al mover {file_name}: {e}')

if __name__ == "__main__":
    move_files()
    
    # Crear un DataFrame y exportar a un archivo CSV
    df = pd.DataFrame(log_data)
    df.to_csv(os.path.join(log_directory, 'movimiento_archivos.csv'), index=False)
