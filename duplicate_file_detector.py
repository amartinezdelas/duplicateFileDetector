"""
Detector de archivos duplicados.

Este módulo proporciona funcionalidades para encontrar archivos duplicados
en un directorio y sus subdirectorios utilizando hashes SHA-256, calcular
el espacio recuperable y exportar los resultados a un archivo CSV.
"""

import os
import hashlib
import csv
from collections import defaultdict


def compute_file_hash(path, block_size=65536):
    """
    Calcula el hash SHA-256 de un archivo.
    
    Args:
        path (str): Ruta al archivo del cual calcular el hash.
        block_size (int, optional): Tamaño del bloque para leer el archivo.
                                   Por defecto 65536 bytes.
    
    Returns:
        str or None: Hash SHA-256 en formato hexadecimal si es exitoso,
                    None si ocurre un error.
    
    Examples:
        >>> compute_file_hash("archivo.txt")
        'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    """
    sha256 = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(block_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error al leer {path}: {e}")
        return None


def find_duplicate_files(base_directory):
    """
    Encuentra archivos duplicados en un directorio y sus subdirectorios.
    
    Args:
        base_directory (str): Directorio base donde buscar archivos duplicados.
    
    Returns:
        dict: Diccionario donde las claves son hashes y los valores son listas
              de rutas de archivos que tienen ese hash (solo incluye grupos
              con más de un archivo).
    
    Examples:
        >>> duplicates = find_duplicate_files("/mi/directorio")
        >>> print(duplicates)
        {'abc123...': ['/ruta/archivo1.txt', '/ruta/archivo2.txt']}
    """
    hash_to_files = defaultdict(list)
    total_files = 0

    for dirpath, _, filenames in os.walk(base_directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_hash = compute_file_hash(full_path)
            if file_hash:
                hash_to_files[file_hash].append(full_path)
                total_files += 1

    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}
    return duplicates


def calculate_reclaimable_space(duplicates):
    """
    Calcula el espacio total que se puede recuperar eliminando duplicados.
    
    Args:
        duplicates (dict): Diccionario de archivos duplicados obtenido de
                          find_duplicate_files().
    
    Returns:
        int: Espacio total en bytes que se puede recuperar manteniendo
             solo una copia de cada archivo duplicado.
    
    Note:
        El cálculo asume que se mantendrá una copia de cada grupo de
        duplicados (la primera en la lista) y se eliminarán las demás.
    """
    space = 0
    for paths in duplicates.values():
        # Space is reclaimed from all duplicates except one
        for path in paths[1:]:
            try:
                space += os.path.getsize(path)
            except Exception as e:
                print(f"Error al obtener tamaño de {path}: {e}")
    return space


def save_results_to_csv(duplicates, filename="duplicados.csv"):
    """
    Guarda los resultados de archivos duplicados en un archivo CSV.
    
    Args:
        duplicates (dict): Diccionario de archivos duplicados.
        filename (str, optional): Nombre del archivo CSV de salida.
                                 Por defecto "duplicados.csv".
    
    Note:
        El archivo CSV contiene dos columnas: "Hash" y "Ruta de archivo duplicado".
        Cada fila representa un archivo duplicado con su hash correspondiente.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Hash", "Ruta de archivo duplicado"])
        for hash_val, paths in duplicates.items():
            for path in paths:
                writer.writerow([hash_val, path])


def format_size(bytes):
    """
    Convierte bytes a una representación legible con unidades apropiadas.
    
    Args:
        bytes (int): Tamaño en bytes a convertir.
    
    Returns:
        str: Representación formateada del tamaño con unidades
             (B, KB, MB, GB, TB).
    
    Examples:
        >>> format_size(1024)
        '1.00 KB'
        >>> format_size(1536)
        '1.50 KB'
        >>> format_size(1048576)
        '1.00 MB'
    """
    for unit in ['B','KB','MB','GB','TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


def main():
    """
    Función principal que ejecuta el detector de archivos duplicados.
    
    Solicita al usuario un directorio para analizar, encuentra archivos
    duplicados, calcula el espacio recuperable y guarda los resultados
    en un archivo CSV.
    """
    directory = input("Introduce el directorio a analizar: ").strip()

    if not os.path.isdir(directory):
        print("Ruta no válida.")
        return

    print("Analizando archivos...")
    duplicates = find_duplicate_files(directory)
    total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
    reclaimable_space = calculate_reclaimable_space(duplicates)

    save_results_to_csv(duplicates)

    print("\n✅ Análisis completado.")
    print(f"Ficheros duplicados encontrados: {total_duplicates}")
    print(f"Espacio potencialmente liberable: {format_size(reclaimable_space)}")
    print("Resultado exportado a 'duplicados.csv'.")


if __name__ == "__main__":
    main()
