document.addEventListener('DOMContentLoaded', () => {
    const validationList = document.getElementById('validation-list');
    const modal = document.getElementById('edit-modal');
    const closeModalBtn = modal.querySelector('.close-button');
    const saveBtn = document.getElementById('save-doc-type-btn');
    const docTypeSelect = document.getElementById('doc-type-select');
    const modalFilenameInput = document.getElementById('modal-filename-input');

    if (!validationList) return;

    // --- Mock Data ---
    const mockDocuments = [
        { id: 1, name: 'factura-martie-2024.pdf', detectedTypeKey: 'doc_facturi', status: 'pending' },
        { id: 2, name: 'contract-prestari-serv.docx', detectedTypeKey: 'doc_contracte', status: 'pending' },
        { id: 3, name: 'aviz-marfa-0012.pdf', detectedTypeKey: 'doc_avize', status: 'validated' },
        { id: 4, name: 'scan-chitanță-04.jpg', detectedTypeKey: 'doc_bonuri', status: 'pending' },
        { id: 5, name: 'raport-casa-zilnic.xlsx', detectedTypeKey: 'doc_rapoarte', status: 'validated' },
        { id: 6, name: 'extras-bancar-aprilie.pdf', detectedTypeKey: 'doc_extrase', status: 'pending' },
        { id: 7, name: 'document-necunoscut.txt', detectedTypeKey: 'doc_unknown', status: 'pending' },
    ];

    const docTypes = {
        doc_facturi: 'Facturi Fiscale',
        doc_contracte: 'Contracte',
        doc_avize: 'Avize de Însoțire',
        doc_cec: 'Cecuri',
        doc_bonuri: 'Bonuri Fiscale',
        doc_rapoarte: 'Rapoarte de Casă',
        doc_extrase: 'Extrase Bancare',
        doc_procese: 'Procese Verbale',
        doc_unknown: 'Necunoscut',
    };

    let currentEditingItem = null;

    // --- Functions ---
    const renderList = () => {
        validationList.innerHTML = '';
        mockDocuments.forEach(doc => {
            const docElement = createValidationItemElement(doc);
            validationList.appendChild(docElement);
        });
        // Apply translations after rendering
        const currentLang = localStorage.getItem('language') || 'ro';
        setLanguage(currentLang);
    };
    
    const createValidationItemElement = (doc) => {
        const item = document.createElement('div');
        item.classList.add('validation-item');
        item.dataset.id = doc.id;
        
        const statusKey = doc.status === 'pending' ? 'status_pending' : 'status_validated';
        const detectedTypeRo = docTypes[doc.detectedTypeKey] || 'Necunoscut';

        item.innerHTML = `
            <div class="file-details">
                <span class="material-symbols-outlined file-icon">${getFileIcon(doc.name)}</span>
                <span>${doc.name}</span>
            </div>
            <div>
                 <span class="file-type-badge" data-key="${doc.detectedTypeKey}">${detectedTypeRo}</span>
            </div>
            <div>
                <span class="status-badge ${doc.status}" data-key="${statusKey}">${doc.status}</span>
            </div>
            <div class="action-buttons">
                <button class="action-btn validate" data-key="action_validate" ${doc.status === 'validated' ? 'disabled' : ''}>
                    <span class="material-symbols-outlined">check</span> Validare
                </button>
                <button class="action-btn edit" data-key="action_edit">
                    <span class="material-symbols-outlined">edit</span> Editare
                </button>
                <button class="action-btn delete" data-key="action_delete">
                    <span class="material-symbols-outlined">delete</span> Ștergere
                </button>
            </div>
        `;

        // Add event listeners for buttons
        item.querySelector('.validate').addEventListener('click', () => validateDoc(doc.id));
        item.querySelector('.edit').addEventListener('click', () => openEditModal(doc.id));
        item.querySelector('.delete').addEventListener('click', () => deleteDoc(doc.id));

        return item;
    };

    const validateDoc = (id) => {
        const doc = mockDocuments.find(d => d.id === id);
        if (doc) {
            doc.status = 'validated';
            renderList();
        }
    };

    const deleteDoc = (id) => {
        const index = mockDocuments.findIndex(d => d.id === id);
        if (index > -1) {
            mockDocuments.splice(index, 1);
            renderList();
        }
    };

    const openEditModal = (id) => {
        currentEditingItem = mockDocuments.find(d => d.id === id);
        if (!currentEditingItem) return;

        modalFilenameInput.value = currentEditingItem.name;
        docTypeSelect.innerHTML = '';
        for (const key in docTypes) {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = docTypes[key];
            option.setAttribute('data-key', key)
            if (key === currentEditingItem.detectedTypeKey) {
                option.selected = true;
            }
            docTypeSelect.appendChild(option);
        }
        
        const currentLang = localStorage.getItem('language') || 'ro';
        setLanguage(currentLang);
        modal.style.display = 'flex';
    };

    const closeEditModal = () => {
        modal.style.display = 'none';
        currentEditingItem = null;
    };

    const saveDocType = () => {
        if (currentEditingItem) {
            const newName = modalFilenameInput.value.trim();
            if (newName) {
                currentEditingItem.name = newName;
            }
            currentEditingItem.detectedTypeKey = docTypeSelect.value;
            closeEditModal();
            renderList();
        }
    };

    // Copied from upload.js to have consistent icons
    const getFileIcon = (filename) => {
        const extension = filename.split('.').pop().toLowerCase();
        switch (extension) {
            case 'pdf': return 'picture_as_pdf';
            case 'png': case 'jpg': case 'jpeg': return 'image';
            case 'csv': case 'xlsx': case 'xls': return 'summarize';
            case 'txt': case 'doc': case 'docx': return 'article';
            case 'json': return 'code';
            default: return 'draft';
        }
    };

    // --- Initial Load & Event Listeners ---
    closeModalBtn.addEventListener('click', closeEditModal);
    saveBtn.addEventListener('click', saveDocType);
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            closeEditModal();
        }
    });

    renderList();
}); 