const uploadForm = document.getElementById('uploadForm');
    const runPipelineButton = document.getElementById('runPipeline');
    const outputDiv = document.getElementById('output');

    // Handle file upload
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData();
        const fileInput = document.getElementById('file');

        if (!fileInput.files[0]) {
            alert('Please select a file!');
            return;
        }

        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('http://127.0.0.1:5000/uploads', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const data = await response.json();
            outputDiv.style.display = 'block';
            outputDiv.textContent = `File uploaded successfully! Path: ${data.file_path}`;
        } catch (error) {
            outputDiv.style.display = 'block';
            outputDiv.textContent = `Error: ${error.message}`;
        }
    });

    // Handle running the pipeline
    runPipelineButton.addEventListener('click', async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/run_pipeline', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`Pipeline execution failed: ${response.statusText}`);
            }

            const data = await response.json();
            outputDiv.style.display = 'block';
            outputDiv.textContent = `Pipeline executed successfully! Result: ${data.message}`;
        } catch (error) {
            outputDiv.style.display = 'block';
            outputDiv.textContent = `Error: ${error.message}`;
        }
    });