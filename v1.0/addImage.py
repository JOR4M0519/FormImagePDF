import os
import cv2
from tkinter import Tk, Button, Label, Entry, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Variables globales
base_pdf_path = None  # Ruta dinámica del PDF base
overlay_pdf_path = os.path.join("Matriculas PDF", "overlay_temp.pdf")  # Archivo temporal para superposición
photo_path = None  # Ruta dinámica para guardar la foto
x, y = 480, 805  # Coordenadas para la imagen
max_width, max_height = 90, 90  # Tamaño máximo de la imagen
output_folder = "Matriculas PDF"
output_folder_Photo = "Photos"

# Función para capturar una foto con la cámara
def capture_photo():
    global photo_path
    """Captura una foto desde la cámara web y la guarda centrada con proporción 1:1."""
    if not base_pdf_path:
        status_label.config(text="Por favor selecciona o arrastra un archivo PDF base primero.")
        return

    result_name = file_name_entry.get().strip()  # Obtener el nombre del archivo
    if not result_name:
        status_label.config(text="Por favor ingresa un nombre para el archivo.")
        return

    # Guardar la imagen con el mismo nombre que el PDF, pero con extensión .jpg
    photo_path = os.path.join(output_folder_Photo, f"{result_name}.jpg")
    if not os.path.exists(output_folder_Photo):
        os.makedirs(output_folder_Photo)

    cap = cv2.VideoCapture(0)
    print("Presiona 'c' para capturar la foto o 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara.")
            break

        # Mostrar la imagen en la ventana
        cv2.imshow("Captura de Foto", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):  # Capturar la foto
            height, width, _ = frame.shape
            side = min(width, height)

            # Calcular los márgenes para centrar el recorte
            left = (width - side) // 2
            top = (height - side) // 2
            right = left + side
            bottom = top + side

            # Recortar la imagen al centro
            cropped = frame[top:bottom, left:right]

            # Convertir a PIL para guardar
            image = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
            image.save(photo_path)
            print(f"Foto guardada en: {photo_path}")
            status_label.config(text=f"Foto guardada: {photo_path}")
            break
        elif key == ord('q'):  # Salir
            print("Saliendo sin capturar.")
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para seleccionar el PDF base
def select_pdf():
    global base_pdf_path
    base_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if base_pdf_path:
        status_label.config(text=f"Archivo PDF seleccionado: {base_pdf_path}")

# Función para manejar el arrastre de archivos
def on_drop(event):
    global base_pdf_path
    base_pdf_path = event.data.strip()
    if base_pdf_path.endswith(".pdf"):
        status_label.config(text=f"Archivo PDF seleccionado: {base_pdf_path}")
    else:
        status_label.config(text="Por favor arrastra un archivo PDF válido.")

# Función para integrar la imagen al PDF
def generate_pdf():
    """Incrusta la foto en el PDF base y genera el PDF final."""
    global photo_path
    if not base_pdf_path:
        status_label.config(text="Por favor selecciona o arrastra un archivo PDF base primero.")
        return
    if not photo_path:
        status_label.config(text="Por favor captura una foto primero.")
        return

    result_name = file_name_entry.get().strip()
    if not result_name.endswith(".pdf"):
        result_name += ".pdf"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_pdf_path = os.path.join(output_folder, result_name)  # Asignar el nombre del archivo ingresado

    page_width, page_height = get_pdf_page_size(base_pdf_path)

    create_image_overlay(overlay_pdf_path, photo_path, x, y, max_width, max_height, page_width, page_height)
    merge_image_with_pdf(base_pdf_path, overlay_pdf_path, output_pdf_path)

    status_label.config(text=f"PDF generado correctamente: {output_pdf_path}")

# Funciones auxiliares para manejar el PDF
def get_pdf_page_size(pdf_path):
    pdf = PdfReader(pdf_path)
    page = pdf.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    return width, height

def create_image_overlay(output_path, image_path, x, y, max_width, max_height, page_width, page_height):
    c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
    c.drawImage(ImageReader(image_path), x, y, max_width, max_height)
    c.save()

def merge_image_with_pdf(base_pdf_path, overlay_pdf_path, output_pdf_path):
    base_pdf = PdfReader(base_pdf_path)
    overlay_pdf = PdfReader(overlay_pdf_path)
    writer = PdfWriter()

    for base_page, overlay_page in zip(base_pdf.pages, overlay_pdf.pages):
        base_page.merge_page(overlay_page)
        writer.add_page(base_page)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    os.remove(overlay_pdf_path)
    print("Archivo temporal eliminado.")

# Crear la interfaz gráfica con TkinterDnD
root = TkinterDnD.Tk()
root.title("Captura de Foto e Integración en PDF")

# Botón para seleccionar el PDF base
select_pdf_button = Button(root, text="Seleccionar PDF Base", command=select_pdf)
select_pdf_button.pack(pady=10)

# Entrada para el nombre del archivo resultante
Label(root, text="Nombre del archivo PDF:").pack(pady=5)
file_name_entry = Entry(root, width=30)
file_name_entry.insert(0, "Matricula- - (#)")
file_name_entry.pack(pady=5)

# Área para arrastrar el archivo PDF
drop_label = Label(root, text="Arrastra aquí el archivo PDF", bg="lightgray", width=40, height=2)
drop_label.pack(pady=10)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", on_drop)

# Botón para capturar la foto
capture_button = Button(root, text="Tomar Foto", command=capture_photo)
capture_button.pack(pady=10)

# Botón para generar el PDF
generate_button = Button(root, text="Generar PDF", command=generate_pdf)
generate_button.pack(pady=10)

# Etiqueta para mostrar el estado
status_label = Label(root, text="Estado: Listo")
status_label.pack(pady=20)

# Iniciar la interfaz
root.mainloop()
