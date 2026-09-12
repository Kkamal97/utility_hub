async function convertSinglePage() {
    const fileInput = document.getElementById('pdfFileInput');
    if (!fileInput.files.length) return alert('Please select a PDF file.');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('page_number', document.getElementById('pageNumberInput').value);
    formData.append('output_format', document.getElementById('formatSelect').value);

    const statusText = document.getElementById('statusText');
    statusText.innerText = 'Converting page...';

    try {
        const response = await fetch('/api/pdf/convert-page', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Conversion failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `page_${document.getElementById('pageNumberInput').value}.${document.getElementById('formatSelect').value}`;
        a.click();

        statusText.innerText = 'Page downloaded successfully!';
    } catch (err) {
        statusText.innerText = 'Error processing file.';
        alert(err.message);
    }
}

async function convertAllPages() {
    const fileInput = document.getElementById('pdfFileInput');
    if (!fileInput.files.length) return alert('Please select a PDF file.');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('output_format', document.getElementById('formatSelect').value);

    const statusText = document.getElementById('statusText');
    statusText.innerText = 'Processing full PDF...';

    try {
        const response = await fetch('/api/pdf/convert-all', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'ZIP export failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'pdf_pages.zip';
        a.click();

        statusText.innerText = 'ZIP file downloaded successfully!';
    } catch (err) {
        statusText.innerText = 'Error exporting ZIP.';
        alert(err.message);
    }
}