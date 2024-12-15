import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2
from PIL import Image
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import base64
from io import BytesIO

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = "uploads"
PHOTO_FOLDER = "static/Photos"
PDF_FOLDER = "PDF"
OVERLAY_TEMP = os.path.join(PDF_FOLDER, "overlay_temp.pdf")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PHOTO_FOLDER"] = PHOTO_FOLDER
app.config["PDF_FOLDER"] = PDF_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PHOTO_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

# Función para capturar fotos
def capture_photo(photo_path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        height, width, _ = frame.shape
        side = min(width, height)

        left = (width - side) // 2
        top = (height - side) // 2
        cropped = frame[top:top + side, left:left + side]

        image = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        image.save(photo_path)
    cap.release()

# Rutas Flask
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files["pdf_file"]
    if file:
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(pdf_path)
        return jsonify({"success": True, "message": "PDF subido correctamente.", "path": pdf_path})
    return jsonify({"success": False, "message": "Error al subir el PDF."})

@app.route("/capture_photo", methods=["POST"])
def capture_photo_route():
    # Obtener los datos enviados desde el frontend
    data = request.json
    image_data = data.get("image")  # Imagen en Base64
    result_name = data.get("result_name", "Matricula")  # Nombre del archivo
    photo_path = os.path.join(app.config["PHOTO_FOLDER"], f"{result_name}.jpg")  # Ruta de la foto

    # Validar que la imagen esté presente
    if not image_data:
        return jsonify({"success": False, "message": "No se recibió la imagen."})

    try:
        image_data = image_data.split(",")[1]  # Remover el encabezado "data:image/jpeg;base64,"
        image = Image.open(BytesIO(base64.b64decode(image_data)))

        # Recortar la imagen al centro (proporción cuadrada)
        width, height = image.size
        side = min(width, height)  # Lado del cuadrado más pequeño
        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side

        # Realizar el recorte centrado
        cropped_image = image.crop((left, top, right, bottom))

        # Guardar la imagen como archivo JPEG
        os.makedirs(app.config["PHOTO_FOLDER"], exist_ok=True)  # Crear la carpeta si no existe
        cropped_image.save(photo_path, "JPEG")

        return jsonify({"success": True, "message": "Foto capturada con éxito.", "path": photo_path})
    except Exception as e:
        print("Error al procesar la imagen:", e)
        return jsonify({"success": False, "message": "Error al procesar la imagen."})

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.json
        pdf_path = data.get("pdf_path")
        photo_path = data.get("photo_path")
        result_name = data.get("result_name", "Matricula") + ".pdf"
        output_pdf_path = os.path.join(PDF_FOLDER, result_name)

        if not pdf_path or not photo_path:
            return jsonify({"success": False, "message": "Faltan datos para generar el PDF."})

        page_width, page_height = get_pdf_page_size(pdf_path)
        create_image_overlay(OVERLAY_TEMP, photo_path, 480, 805, 90, 90, page_width, page_height)
        merge_image_with_pdf(pdf_path, OVERLAY_TEMP, output_pdf_path)

        return jsonify({"success": True, "message": "PDF generado con éxito.", "path": output_pdf_path})
    except Exception as e:
        # Capturar el error y enviar el mensaje al frontend
        print(f"Error en /generate_pdf: {e}")
        return jsonify({"success": False, "message": f"Error al generar el PDF: {str(e)}"})

def get_pdf_page_size(pdf_path):
    """Obtiene el tamaño de la primera página del PDF."""
    pdf = PdfReader(pdf_path)
    first_page = pdf.pages[0]
    media_box = first_page.MediaBox
    width = float(media_box[2]) - float(media_box[0])
    height = float(media_box[3]) - float(media_box[1])
    return width, height

def create_image_overlay(output_path, image_path, x, y, max_width, max_height, page_width, page_height):
    c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
    c.drawImage(ImageReader(image_path), x, y, max_width, max_height)
    c.save()



def merge_image_with_pdf(base_pdf_path, overlay_pdf_path, output_pdf_path):
    """Combina un PDF base con una imagen superpuesta preservando los formularios."""
    # Leer el PDF base y el PDF con la imagen superpuesta
    base_pdf = PdfReader(base_pdf_path)
    overlay_pdf = PdfReader(overlay_pdf_path)

    # Iterar sobre las páginas y fusionarlas
    for base_page, overlay_page in zip(base_pdf.pages, overlay_pdf.pages):
        # Fusionar visualmente la página de overlay sobre la página base
        PageMerge(base_page).add(overlay_page).render()

    # Escribir el PDF combinado conservando los formularios
    PdfWriter(output_pdf_path, trailer=base_pdf).write()

    print(f"PDF generado correctamente: {output_pdf_path}")

    os.remove(overlay_pdf_path)


if __name__ == "__main__":
    app.run(debug=True)
