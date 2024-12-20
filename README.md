# Generador de Matrículas PDF

Este proyecto permite la captura de fotografías en tiempo real y la generación de PDFs dinámicos utilizando plantillas preexistentes. Además, mantiene campos de formulario y elementos interactivos en el PDF resultante.

---

## **Requisitos Previos**

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes componentes:

### **Software Requerido**
1. **Python 3.8+**

### **Bibliotecas de Python**
Ejecuta el siguiente comando para instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### **Estructura del Proyecto**

```bash
ForImagePDF/
├── app.py                # Archivo principal del servidor Flask
├── templates/
│   └── index.html        # Interfaz HTML principal
├── static/
│   ├── css/
│   │   └── styles.css    # Estilos personalizados
│   ├── js/
│   │   └── scripts.js    # Funciones JavaScript
│   └── Photos/           # Carpeta donde se almacenan las fotos capturadas
├── uploads/              # Carpeta donde se almacenan los PDFs subidos
├── PDF/                  # Carpeta donde se almacenan los PDFs generados
├── requirements.txt      # Lista de dependencias de Python
└── README.md             # Este archivo
```
### **Cómo Ejecutar el Proyecto**

# Generador de Matrículas PDF

Este proyecto permite capturar fotografías en tiempo real y generar PDFs personalizados utilizando una plantilla base.

---

## **Cómo Ejecutar el Proyecto**

### 1. Clona el Repositorio

Clona el repositorio en tu máquina local utilizando Git:

```bash
git clone https://github.com/JOR4M0519/FormImagePDF.git
cd ForImagePDF
```

### 2. Configura las Dependencias

Instala las bibliotecas necesarias especificadas en el archivo `requirements.txt` ejecutando:

```bash
pip install -r requirements.txt
```

### 3. Inicia el Servidor Flask

## Forma 1
Ejecuta el archivo start.bat

Esto ejecutará la aplicación y podrás acceder a ella desde tu navegador en la siguiente dirección:
```bash
http://localhost:5000
```

## Forma 2
Ejecuta el archivo principal del proyecto (`app.py`) para iniciar el servidor Flask:

```bash
python app.py
```

Esto ejecutará la aplicación y podrás acceder a ella desde tu navegador en la siguiente dirección:
```bash
http://127.0.0.1:5000
```
## **Funcionalidades Principales**

### **1. Subir PDF Base**
- Permite al usuario cargar un archivo PDF base que servirá como plantilla para la generación del documento final.

### **2. Capturar Foto**
- Abre la cámara en tiempo real mediante un **modal** (ventana emergente) para permitir una previsualización.
- La imagen capturada se recorta automáticamente a un formato cuadrado y se guarda en la carpeta `static/Photos/`.

### **3. Generar PDF**
- Combina el PDF base cargado con la foto capturada y lo guarda en la carpeta `PDF/` con el nombre especificado.
- **Preserva los campos interactivos** del PDF original (botones, formularios, etc.).

---

## **Cómo Funciona el Proyecto**

### **1. Subir el PDF Base**
   - En la interfaz principal, selecciona el archivo PDF base y haz clic en **"Subir PDF"**.
   - Ingresa un nombre para el archivo resultante (ejemplo: `Matricula-nombre-grado`).
### **2. Capturar la Foto**
   - Haz clic en **"Abrir Cámara"** para mostrar la previsualización en tiempo real.
   - Captura la foto haciendo clic en **"Capturar Foto"** y verifica la previsualización de la imagen guardada.
    
### **3. Generar el PDF Final**
   - Haz clic en **"Generar PDF"** para fusionar la foto con el PDF base.
Nota: La imagen y PDF Se guardan con el mismo nombre
---

### Licencia
Este proyecto está bajo la Licencia MIT.
