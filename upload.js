document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const browseLink = document.querySelector('.browse-link');

    if (!dropZone) return;

    // --- Event Listeners ---
    
    dropZone.addEventListener('click', () => fileInput.click());
    browseLink.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });
    
    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    // --- File Handling ---

    const handleFiles = (files) => {
        for (const file of files) {
            const fileItem = createFileListElement(file);
            fileList.appendChild(fileItem);
            
            // Simulate AI processing
            setTimeout(() => {
                processFile(file, fileItem);
            }, 1000 + Math.random() * 1500); // Random delay for realism
        }
    };

    const processFile = (file, fileItem) => {
        const detectedType = recognizeDocumentType(file.name);
        
        const typeBadge = fileItem.querySelector('.file-type-badge');
        const statusDiv = fileItem.querySelector('.file-status');

        typeBadge.textContent = detectedType.ro;
        typeBadge.setAttribute('data-key', detectedType.key);

        statusDiv.innerHTML = `
            <span class="material-symbols-outlined status-icon success">check_circle</span>
            <span data-key="status_success">Success</span>
        `;
        
        // Ensure new text is translated if language is switched
        const currentLang = localStorage.getItem('language') || 'ro';
        setLanguage(currentLang);
    };

    // --- "AI" Recognition Logic ---

    const recognizeDocumentType = (filename) => {
        const name = filename.toLowerCase();
        
        if (name.includes('factur') || name.includes('invoice')) return { ro: 'Factură Fiscală', key: 'doc_facturi' };
        if (name.includes('contract')) return { ro: 'Contract', key: 'doc_contracte' };
        if (name.includes('aviz')) return { ro: 'Aviz de Însoțire', key: 'doc_avize' };
        if (name.includes('cec') || name.includes('check')) return { ro: 'Cec', key: 'doc_cec' };
        if (name.includes('bon') || name.includes('receipt')) return { ro: 'Bon Fiscal', key: 'doc_bonuri' };
        if (name.includes('raport') && name.includes('casa')) return { ro: 'Raport de Casă', key: 'doc_rapoarte' };
        if (name.includes('extras') || name.includes('statement')) return { ro: 'Extras Bancar', key: 'doc_extrase' };
        if (name.includes('proces') && name.includes('verbal')) return { ro: 'Proces Verbal', key: 'doc_procese' };
        
        return { ro: 'Necunoscut', key: 'doc_unknown' };
    };

    // --- UI Element Creation ---

    const getFileIcon = (filename) => {
        const extension = filename.split('.').pop().toLowerCase();
        switch (extension) {
            case 'pdf': return 'picture_as_pdf';
            case 'png':
            case 'jpg':
            case 'jpeg': return 'image';
            case 'csv':
            case 'xlsx':
            case 'xls': return 'summarize';
            case 'txt': return 'article';
            case 'json': return 'code';
            default: return 'draft';
        }
    };

    const createFileListElement = (file) => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');

        fileItem.innerHTML = `
            <div class="file-details">
                <span class="material-symbols-outlined file-icon">${getFileIcon(file.name)}</span>
                <span class="file-name">${file.name}</span>
            </div>
            <div>
                <span class="file-type-badge" data-key="type_detecting">Detectare...</span>
            </div>
            <div class="file-status">
                <span class="material-symbols-outlined status-icon loading">progress_activity</span>
                <span data-key="status_processing">Processing...</span>
            </div>
        `;
        return fileItem;
    };
}); 