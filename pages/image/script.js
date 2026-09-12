async function resizeImage() {
    const fileInput = document.getElementById('imageFileInput');
    const width = document.getElementById('widthInput').value;
    const height = document.getElementById('heightInput').value;

    if (!fileInput.files.length) return alert('Please select an image file.');
    if (!width || !height) return alert('Please specify both width and height.');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('output_format', document.getElementById('formatSelect').value);

    const statusText = document.getElementById('statusText');
    statusText.innerText = 'Resizing...';

    try {
        const response = await fetch('/api/image/resize', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to resize image');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const ext = document.getElementById('formatSelect').value.toLowerCase();
        a.download = `resized_image.${ext === 'jpg' ? 'jpg' : 'png'}`;
        a.click();

        statusText.innerText = 'Image downloaded successfully!';
    } catch (err) {
        statusText.innerText = 'Error processing image.';
        alert(err.message);
    }
}