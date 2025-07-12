function previewImage(event) {
    const image = document.getElementById('uploadedImage');
    const imagePreview = document.getElementById('imagePreview');
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            image.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

document.getElementById('fileInput').addEventListener('change', previewImage);

function submitForm() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    const resultDiv = document.getElementById('result');

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<h2>Error: ${data.error}</h2>`;
        } else {
            resultDiv.innerHTML = `<h2>Prediction: ${data.prediction}</h2>`;
        }
    })
    .catch(error => {
        resultDiv.innerHTML = `<h2>Error: ${error}</h2>`;
    });
}
