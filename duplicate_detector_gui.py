"""
Interfaz gráfica para el detector de archivos duplicados.

Este módulo proporciona una interfaz gráfica de usuario (GUI) construida con
Tkinter para el detector de archivos duplicados. Permite a los usuarios
seleccionar directorios y ejecutar análisis de duplicados de manera visual
e intuitiva.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import duplicate_file_detector as detector


class DuplicateDetectorGUI:
    """
    Interfaz gráfica para el detector de archivos duplicados.
    
    Esta clase crea una ventana GUI que permite a los usuarios seleccionar
    un directorio, analizar archivos duplicados y mostrar los resultados
    de manera visual.
    
    Attributes:
        root (tk.Tk): Ventana principal de la aplicación.
        path_var (tk.StringVar): Variable que almacena la ruta del directorio seleccionado.
        status_label (ttk.Label): Etiqueta para mostrar el estado y resultados del análisis.
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica del detector de duplicados.
        
        Args:
            root (tk.Tk): La ventana raíz de Tkinter para la aplicación.
        """
        self.root = root
        self.root.title("Detector de Archivos Duplicados")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """
        Crea y organiza todos los widgets de la interfaz gráfica.
        
        Configura la estructura visual de la aplicación incluyendo:
        - Campo de entrada para la ruta del directorio
        - Botón para explorar directorios
        - Botón para iniciar el análisis
        - Etiqueta para mostrar el estado y resultados
        """
        # Frame for folder selection
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        self.path_var = tk.StringVar()

        ttk.Label(frame, text="Directorio a analizar:").pack(anchor="w")
        path_entry = ttk.Entry(frame, textvariable=self.path_var, width=50)
        path_entry.pack(fill="x", padx=(0, 5), pady=5, side="left")

        browse_btn = ttk.Button(frame, text="📁 Buscar", command=self.browse_folder)
        browse_btn.pack(pady=5)

        # Analyze button
        analyze_btn = ttk.Button(self.root, text="🔍 Analizar duplicados", command=self.run_analysis)
        analyze_btn.pack(pady=10)

        # Result / status
        self.status_label = ttk.Label(self.root, text="", wraplength=450, foreground="blue")
        self.status_label.pack(pady=10)

    def browse_folder(self):
        """
        Abre un diálogo para seleccionar un directorio.
        
        Permite al usuario navegar y seleccionar un directorio del sistema
        de archivos. La ruta seleccionada se almacena en path_var.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def run_analysis(self):
        """
        Inicia el proceso de análisis de archivos duplicados.
        
        Valida que se haya seleccionado un directorio válido y ejecuta
        el análisis en un hilo separado para mantener la interfaz responsiva.
        Muestra un mensaje de error si el directorio no es válido.
        
        Raises:
            messagebox.showerror: Si el directorio seleccionado no es válido.
        """
        directory = self.path_var.get().strip()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Por favor selecciona un directorio válido.")
            return

        self.status_label.config(text="Analizando archivos...")

        # Run the detection in a separate thread to keep GUI responsive
        threading.Thread(target=self.analyze_duplicates, args=(directory,), daemon=True).start()

    def analyze_duplicates(self, directory):
        """
        Ejecuta el análisis de archivos duplicados en el directorio especificado.
        
        Esta función se ejecuta en un hilo separado para evitar bloquear la
        interfaz gráfica durante el análisis. Utiliza las funciones del módulo
        detector para encontrar duplicados, calcular espacio recuperable y
        guardar resultados en CSV.
        
        Args:
            directory (str): Ruta del directorio a analizar.
        
        Note:
            Esta función actualiza la etiqueta de estado con los resultados
            del análisis una vez completado el proceso.
        """
        duplicates = detector.find_duplicate_files(directory)
        total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
        space_reclaimable = detector.calculate_reclaimable_space(duplicates)

        detector.save_results_to_csv(duplicates)

        result_msg = (
            f"✅ Análisis completado.\n"
            f"Ficheros duplicados encontrados: {total_duplicates}\n"
            f"Espacio potencialmente liberable: {detector.format_size(space_reclaimable)}\n"
            f"Resultados guardados en 'duplicados.csv'"
        )

        self.status_label.config(text=result_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateDetectorGUI(root)
    root.mainloop()
