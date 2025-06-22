document.addEventListener('DOMContentLoaded', function () {
    const tableWrapper = document.getElementById('editable-table-wrapper');
    const addRowBtn = document.getElementById('add-row-btn');
    const saveBtn = document.getElementById('save-btn');

    if (!tableWrapper || !addRowBtn || !saveBtn) {
        console.error('Required elements for result page not found.');
        return;
    }

    let headers = [];

    function createTable(data) {
        if (data.length > 0) {
            headers = Object.keys(data[0]);
        } else {
            // Если данных нет, создаем заголовок по умолчанию
            headers = ['Column 1', 'Column 2'];
        }

        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        
        // Table Head
        const headerRow = document.createElement('tr');
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        const actionTh = document.createElement('th');
        actionTh.textContent = 'Actions';
        headerRow.appendChild(actionTh);
        thead.appendChild(headerRow);

        // Table Body
        data.forEach(rowData => {
            tbody.appendChild(createRow(rowData));
        });

        table.appendChild(thead);
        table.appendChild(tbody);
        tableWrapper.innerHTML = '';
        tableWrapper.appendChild(table);
    }

    function createRow(rowData) {
        const row = document.createElement('tr');
        headers.forEach(header => {
            const cell = document.createElement('td');
            cell.textContent = rowData[header] || '';
            cell.setAttribute('contenteditable', 'true');
            row.appendChild(cell);
        });

        // Delete button cell
        const actionCell = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '❌';
        deleteBtn.className = 'delete-row-btn';
        deleteBtn.onclick = () => row.remove();
        actionCell.appendChild(deleteBtn);
        row.appendChild(actionCell);

        return row;
    }

    function addRow() {
        const newRowData = {};
        headers.forEach(header => newRowData[header] = '');
        const tableBody = tableWrapper.querySelector('tbody');
        if (tableBody) {
            tableBody.appendChild(createRow(newRowData));
        }
    }

    function saveAndDownload() {
        const table = tableWrapper.querySelector('table');
        if (!table) return;

        const tableData = [];
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const rowData = {};
            const cells = row.querySelectorAll('td[contenteditable="true"]');
            cells.forEach((cell, index) => {
                rowData[headers[index]] = cell.textContent;
            });
            tableData.push(rowData);
        });
        
        // Use the downloadUrl passed from the template
        fetch(downloadUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(tableData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // Extract filename from URL and add _edited.xlsx
            const originalFilename = downloadUrl.split('/').pop();
            a.download = `${originalFilename.split('.').slice(0, -1).join('.')}_edited.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        })
        .catch(error => console.error('Error downloading file:', error));
    }

    // Initial setup
    createTable(typeof tableData !== 'undefined' ? tableData : []);
    addRowBtn.addEventListener('click', addRow);
    saveBtn.addEventListener('click', saveAndDownload);
}); 