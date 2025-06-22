document.addEventListener('DOMContentLoaded', () => {
    const editBtn = document.getElementById('edit-profile-btn');
    const saveBtn = document.getElementById('save-profile-btn');

    if (!editBtn) return;

    const profileData = {
        firstName: 'Alexandru',
        lastName: 'Popescu',
        status: 'Contabil Șef',
        company: 'Contasfera SRL'
    };
    
    const textElements = {
        firstName: document.getElementById('first-name-text'),
        lastName: document.getElementById('last-name-text'),
        status: document.getElementById('status-text'),
        company: document.getElementById('company-text'),
    };

    const inputElements = {
        firstName: document.getElementById('first-name-input'),
        lastName: document.getElementById('last-name-input'),
        status: document.getElementById('status-input'),
        company: document.getElementById('company-input'),
    };
    
    const loadProfileData = () => {
        for (const key in profileData) {
            textElements[key].textContent = profileData[key];
            inputElements[key].value = profileData[key];
        }
    };

    const toggleEditMode = (isEditing) => {
        for (const key in textElements) {
            textElements[key].style.display = isEditing ? 'none' : 'block';
            inputElements[key].style.display = isEditing ? 'block' : 'none';
        }
        editBtn.style.display = isEditing ? 'none' : 'inline-flex';
        saveBtn.style.display = isEditing ? 'inline-flex' : 'none';
    };

    editBtn.addEventListener('click', () => toggleEditMode(true));
    
    saveBtn.addEventListener('click', () => {
        for (const key in profileData) {
            profileData[key] = inputElements[key].value;
        }
        loadProfileData();
        toggleEditMode(false);
    });

    // Initial load
    loadProfileData();
}); 