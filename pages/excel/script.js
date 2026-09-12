let excelBlob = null;

async function convertTable() {
    const rawText = document.getElementById('tableInput').value.trim();
    if (!rawText) return alert('Please paste data first');

    const statusText = document.getElementById('statusText');
    statusText.innerText = 'Processing...';

    try {
        const res = await fetch('/api/excel/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_text: rawText })
        });

        if (!res.ok) throw new Error('Conversion failed');

        excelBlob = await res.blob();
        statusText.innerText = 'Excel Generated!';
        document.getElementById('downloadBtn').style.display = 'inline-flex';
    } catch (err) {
        statusText.innerText = 'Error processing text';
        alert(err.message);
    }
}

function downloadFile() {
    if (!excelBlob) return;
    const url = window.URL.createObjectURL(excelBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Standardized_SOP.xlsx';
    a.click();
}

function clearForm() {
    document.getElementById('tableInput').value = '';
    document.getElementById('downloadBtn').style.display = 'none';
    document.getElementById('statusText').innerText = 'Ready to process';
    excelBlob = null;
}