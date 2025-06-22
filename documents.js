document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('documentModal');
    const closeModalBtn = document.querySelector('.close-btn');
    const viewAllLinks = document.querySelectorAll('.view-all');
    const modalTitle = document.getElementById('modalTitle');

    // --- Mock Data ---
    // In a real application, this data would come from a server
    const allDocuments = {
        'Factura Fiscală': [
            { id: 'FF-2023-08-15-001', date: '15.08.2023' },
            { id: 'FF-2023-08-14-005', date: '14.08.2023' },
            { id: 'FF-2023-08-14-002', date: '14.08.2023' },
            { id: 'FF-2023-08-13-010', date: '13.08.2023' },
            { id: 'FF-2023-08-12-007', date: '12.08.2023' },
            { id: 'FF-2023-08-11-003', date: '11.08.2023' }
        ],
        'Bon Fiscal': [
            { id: 'BF-2023-08-15-012', date: '15.08.2023' },
            { id: 'BF-2023-08-15-011', date: '15.08.2023' },
            { id: 'BF-2023-08-14-034', date: '14.08.2023' },
            { id: 'BF-2023-08-14-031', date: '14.08.2023' }
        ],
         'Aviz de Însoțire': [
            { id: 'AI-2023-08-15-002', date: '15.08.2023' },
            { id: 'AI-2023-08-14-001', date: '14.08.2023' },
            { id: 'AI-2023-08-12-004', date: '12.08.2023' },
            { id: 'AI-2023-08-11-009', date: '11.08.2023' },
            { id: 'AI-2023-08-10-008', date: '10.08.2023' }
        ]
    };

    // Function to open the modal
    function openModal(docType) {
        modalTitle.textContent = docType;
        const docs = allDocuments[docType];
        const docList = modal.querySelector('.modal-doc-list');
        docList.innerHTML = ''; // Clear previous list

        if (docs) {
            docs.forEach(doc => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${doc.id}</span><span>${doc.date}</span><button class="view-btn">Vezi</button>`;
                docList.appendChild(li);
            });
        }
        
        modal.style.display = 'block';
    }

    // Function to close the modal
    function closeModal() {
        modal.style.display = 'none';
    }

    // Event listeners for "View All" links
    viewAllLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const card = e.target.closest('.doc-card');
            const docType = card.querySelector('h3').textContent;
            openModal(docType);
        });
    });

    // Event listener for the close button
    closeModalBtn.addEventListener('click', closeModal);

    // Event listener to close modal if user clicks outside of it
    window.addEventListener('click', function(e) {
        if (e.target == modal) {
            closeModal();
        }
    });
}); 