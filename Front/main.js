document.addEventListener("DOMContentLoaded", function() {
    // --- SELECTORI ELEMENTE ---
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const body = document.body;
    const faqLink = document.getElementById('faq-link');
    const dashboardLink = document.getElementById('dashboard-link');

    let charts = {};

    // =================================================================
    // LOGICA PENTRU PAGINA FAQ și ACORDEON
    // =================================================================
    
    // Comutare la pagina FAQ
    if (faqLink) {
        faqLink.addEventListener('click', (e) => {
            e.preventDefault();
            body.classList.add('faq-active');
            window.scrollTo(0, 0); // Deruleaza la inceputul paginii
        });
    }

    // Revenire la Dashboard
    if (dashboardLink) {
        dashboardLink.addEventListener('click', (e) => {
            e.preventDefault();
            // Eliminam clasa si activam/dezactivam link-urile din meniu
            body.classList.remove('faq-active');
            dashboardLink.classList.add('active');
            if (faqLink) faqLink.classList.remove('active');
            window.scrollTo(0, 0); // Deruleaza la inceputul paginii
        });
    }
    
    // Logica pentru acordeonul FAQ
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            // Inchide toate celelalte raspunsuri deschise
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            // Comuta starea (deschis/inchis) pentru elementul curent
            item.classList.toggle('active');
        });
    });

    // =================================================================
    // LOGICA PENTRU GRAFICE (CHARTS)
    // =================================================================

    function getThemeColors() {
        const styles = getComputedStyle(body);
        return {
            textColor: styles.getPropertyValue('--color-text-secondary').trim(),
            gridColor: styles.getPropertyValue('--color-border').trim(),
            lineColor1: '#50D1AA', // Venituri
            lineColor2: '#E984A0', // Cheltuieli
            pointBorderColor: styles.getPropertyValue('--color-primary').trim(),
            doughnutBg1: styles.getPropertyValue('--color-accent').trim(),
            doughnutBg2: styles.getPropertyValue('--color-primary').trim(),
            doughnutBorder: styles.getPropertyValue('--color-secondary').trim(),
        };
    }

    function initializeOrUpdateCharts() {
        const colors = getThemeColors();

        // Distruge graficele existente inainte de a le recrea
        Object.values(charts).forEach(chart => chart.destroy());

        // --- Grafic Venituri (Revenue Chart) ---
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        charts.revenue = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Venituri',
                    data: [10, 18, 15, 22, 18, 23, 19, 22, 21, 25, 24, 28],
                    borderColor: colors.lineColor1, tension: 0.4, pointBackgroundColor: colors.lineColor1,
                    pointBorderColor: colors.pointBorderColor, pointRadius: 5, borderWidth: 2
                }, {
                    label: 'Cheltuieli',
                    data: [8, 10, 9, 12, 14, 15, 12, 14, 13, 16, 15, 17],
                    borderColor: colors.lineColor2, tension: 0.4, pointBackgroundColor: colors.lineColor2,
                    pointBorderColor: colors.pointBorderColor, pointRadius: 5, borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    y: {
                        grid: { color: colors.gridColor, borderDash: [5, 5] },
                        ticks: { color: colors.textColor, callback: (value) => `MDL ${value}k` }
                    },
                    x: { grid: { display: false }, ticks: { color: colors.textColor } }
                },
                plugins: { legend: { position: 'top', align: 'end', labels: { color: colors.textColor, usePointStyle: true, pointStyle: 'rect' } } }
            }
        });

        // --- Grafic Campanie (Campaign Chart) ---
        const campaignCtx = document.getElementById('campaignChart').getContext('2d');
        charts.campaign = new Chart(campaignCtx, {
            type: 'doughnut',
            data: {
                datasets: [{ data: [65, 35], backgroundColor: [colors.doughnutBg1, colors.doughnutBg2], borderColor: colors.doughnutBorder, borderWidth: 5, cutout: '80%' }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
        });

        // --- Grafic Vanzari (Sales Quantity Chart) ---
        const salesQuantityCtx = document.getElementById('salesQuantityChart').getContext('2d');
        const salesColors = {
            dark: ['#A07E69', '#E6A573', '#F7C480', '#FDECB0', '#ADDDC8', '#82CA9D'],
            light: ['#6C8EAD', '#82A0B9', '#99B2C6', '#B0C4D3', '#C7D6E0', '#DEE8EC']
        };
        const currentSalesColors = body.classList.contains('light-theme') ? salesColors.light : salesColors.dark;

        charts.sales = new Chart(salesQuantityCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [
                    { label: 'hot dog', data: [120, 50, 130, 120, 150, 180, 140], backgroundColor: currentSalesColors[0] },
                    { label: 'burger', data: [80, 40, 70, 80, 90, 110, 80], backgroundColor: currentSalesColors[1] },
                    { label: 'sandwich', data: [60, 30, 50, 60, 70, 80, 60], backgroundColor: currentSalesColors[2] },
                    { label: 'kebab', data: [40, 20, 30, 40, 50, 60, 40], backgroundColor: currentSalesColors[3] },
                    { label: 'fries', data: [30, 10, 20, 30, 40, 50, 30], backgroundColor: currentSalesColors[4] },
                    { label: 'donut', data: [90, 60, 80, 90, 110, 130, 100], backgroundColor: currentSalesColors[5] }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    x: { stacked: true, grid: { display: false }, ticks: { color: colors.textColor } },
                    y: { stacked: true, beginAtZero: true, grid: { color: colors.gridColor }, ticks: { color: colors.textColor } }
                },
                plugins: { legend: { position: 'right', labels: { color: colors.textColor, boxWidth: 10, usePointStyle: true, pointStyle: 'rect' } } }
            }
        });
    }

    // =================================================================
    // LOGICA PENTRU COMUTATORUL DE TEMA
    // =================================================================
    
    themeToggleBtn.addEventListener('click', () => {
        body.classList.toggle('light-theme');
        const isLight = body.classList.contains('light-theme');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = isLight ? 'light_mode' : 'dark_mode';
        
        // Asteptam putin pentru ca variabilele CSS sa se actualizeze inainte de a redesena graficele
        setTimeout(initializeOrUpdateCharts, 50);
    });

    // --- Incarcarea initiala ---
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = 'light_mode';
    } else {
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = 'dark_mode';
    }

    // Initializam graficele la incarcarea paginii
    initializeOrUpdateCharts();
});