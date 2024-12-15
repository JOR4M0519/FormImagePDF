let pdfBasePath = null; // Variable global para almacenar el path del PDF base

function showAlert(message, type = "danger") {
    const alertPlaceholder = document.getElementById("alert-placeholder");
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
    alertPlaceholder.innerHTML = alertHTML;
}

function uploadPDF() {
    const formData = new FormData(document.getElementById("uploadForm"));

    fetch("/upload_pdf", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                pdfBasePath = data.path; // Almacenar el path del PDF base
                showAlert(data.message, "success");
            } else {
                showAlert(data.message, "danger");
            }
        })
        .catch(error => {
            console.error("Error al subir PDF:", error);
        });
}


function generatePDF() {
    const resultName = document.getElementById("result_name").value;
    const photoPath = "static/Photos/" + resultName + ".jpg";

    if (!pdfBasePath || !photoPath || !resultName) {
        showAlert("Por favor verifica los datos.", "warning");
        return;
    }

    fetch("/generate_pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pdf_path: pdfBasePath, photo_path: photoPath, result_name: resultName }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                showAlert(data.message, "success");
                document.getElementById("printPDF").disabled = false
            } else {
                showAlert(data.message, "danger");
            }
        })
        .catch((error) => {
            console.error("Error al generar PDF:", error);
            showAlert("Hubo un error inesperado al generar el PDF.", "danger");
        });
}


function printGeneratedPDF() {
    // Obtener el nombre del PDF generado
    const pdfName = document.getElementById("result_name").value.trim();

    if (!pdfName) {
        alert("Por favor, ingresa un nombre válido para el archivo PDF.");
        return;
    }

    const pdfPath = `/PDF/${pdfName}.pdf`; // Ruta del PDF generado

    // Abre el PDF en una nueva ventana/pestaña
    const printWindow = window.open(pdfPath, "_blank");

    if (printWindow) {
        // Esperar a que el PDF cargue y luego imprimirlo automáticamente
        printWindow.onload = () => {
            printWindow.print();
        };
    } else {
        alert("No se pudo abrir el PDF. Verifica la ruta o los permisos.");
    }
}




let videoStream; // Variable global para el stream de la cámara

// Inicializar la cámara cuando el modal se abre
function startCamera() {
    const result_name = document.getElementById("result_name").value;
    console.log(result_name != "" , result_name.includes("Matricula"))
    if(result_name != "" && result_name.includes("Matricula")){
        const video = document.getElementById("camera-stream");

        navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            videoStream = stream;
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error("Error al acceder a la cámara:", error);
        });
    }else{
        const modalElement  = document.getElementById("cameraModal");
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        stopCamera()
        modalInstance.hide();
        showAlert("Digite el nombre correcto para guardar 'Nombre del Archivo Resultante' ","danger")
    }
}

// Detener la cámara cuando el modal se cierra
function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach((track) => track.stop());
        videoStream = null;
    }
}

// Capturar la foto del stream en tiempo real
function capturePhoto() {
    const video = document.getElementById("camera-stream");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // Establece las dimensiones del canvas en función del video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    if (canvas.width === 0 || canvas.height === 0) {
        console.error("El video no está inicializado correctamente.");
        showAlert("Error: La cámara no está lista.", "danger");
        return;
    }

    // Dibuja el fotograma actual del video en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir el contenido del canvas a una imagen en Base64
    const imageData = canvas.toDataURL("image/jpeg");

    // Mostrar la foto en la previsualización
    const photoPreview = document.getElementById("photo-preview");
    photoPreview.src = imageData;

    // Enviar la imagen al backend
    fetch("/capture_photo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            image: imageData,
            result_name: document.getElementById("result_name").value,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            showAlert(data.message, "success");
        })
        .catch((error) => {
            showAlert("Error al capturar la foto:", "danger");
            console.error("Error al capturar la foto:", error);
        });
}

// Vincular los eventos del modal
document.addEventListener("DOMContentLoaded", () => {
    const cameraModal = document.getElementById("cameraModal");

    // Inicia la cámara cuando se abre el modal
    cameraModal.addEventListener("shown.bs.modal", startCamera);

    // Detén la cámara cuando se cierra el modal
    cameraModal.addEventListener("hidden.bs.modal", stopCamera);
});

