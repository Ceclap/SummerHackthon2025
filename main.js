document.addEventListener("DOMContentLoaded", function() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const body = document.body;
    let charts = {};

    // Function to get current theme colors from CSS variables
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

    // Function to initialize or update all charts
    function initializeOrUpdateCharts() {
        const themeColors = {
            light: {
                background: '#f8f9fa',
                cardBackground: '#ffffff',
                text: '#343a40',
                textSecondary: '#6c757d',
                primary: '#0d6efd',
                primaryLight: '#e7f0ff',
                expenses: '#dc3545',
                grid: '#e9ecef',
                border: '#dee2e6',
                barStack: ['#21436E', '#3A6BA5', '#6398D9', '#8FC2FF', '#BDE0FF']
            },
            dark: {
                background: '#121212',
                cardBackground: '#1e1e1e',
                text: '#e9ecef',
                textSecondary: '#adb5bd',
                primary: '#4dabf7',
                primaryLight: '#2c3e50',
                expenses: '#ff6b6b',
                grid: '#343a40',
                border: '#343a40',
                barStack: ['#A6C4E7', '#73A2D6', '#4A80C3', '#2E64A7', '#1A437A']
            }
        };
        const colors = body.classList.contains('light-theme') ? themeColors.light : themeColors.dark;

        // Destroy existing charts before redrawing
        Object.values(charts).forEach(chart => chart?.destroy());

        drawRevenueChart(colors);
        drawCampaignChart(colors);
        drawSalesQuantityChart(colors);
    }

    let revenueChartInstance = null;
    const drawRevenueChart = (themeColors) => {
        const colors = getThemeColors();

        // Destroy existing charts if they exist
        Object.values(charts).forEach(chart => chart.destroy());

        // --- Revenue Chart ---
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        if (charts.revenue) {
            charts.revenue.destroy();
        }

        const labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const venituriData = [10000, 18000, 14500, 22000, 17500, 23000, 19000, 22000, 21000, 25000, 24000, 28000];
        const cheltuieliData = [8000, 10500, 8500, 12000, 14000, 15000, 12000, 14000, 12500, 15500, 14500, 17000];

        const lang = localStorage.getItem('language') || 'ro';
        const venituriLabel = (typeof translations !== 'undefined' && translations[lang] && translations[lang].legend_income) || 'Venituri';
        const cheltuieliLabel = (typeof translations !== 'undefined' && translations[lang] && translations[lang].legend_expenses) || 'Cheltuieli';

        const data = {
            labels: labels,
            datasets: [
                {
                    label: venituriLabel,
                    data: venituriData,
                    borderColor: colors.lineColor1,
                    backgroundColor: colors.lineColor1 + '33', // a bit of transparent fill
                    fill: false,
                tension: 0.4,
                    pointBackgroundColor: colors.lineColor1,
                pointRadius: 5,
                pointHoverRadius: 7,
            },
            {
                    label: cheltuieliLabel,
                    data: cheltuieliData,
                    borderColor: colors.lineColor2,
                    backgroundColor: colors.lineColor2 + '33',
                    fill: false,
                tension: 0.4,
                    pointBackgroundColor: colors.lineColor2,
                pointRadius: 5,
                pointHoverRadius: 7,
                }
            ]
        };

        const options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        color: colors.textColor,
                        boxWidth: 15,
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('ro-RO', { style: 'currency', currency: 'MDL' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: colors.gridColor,
                        borderDash: [2, 4],
                    },
                    ticks: {
                        color: colors.textColor,
                        callback: function(value, index, values) {
                            if (value >= 1000) {
                               return 'MDL ' + value / 1000 + 'k';
                            }
                            return 'MDL ' + value;
                        }
                    }
                },
                x: {
                   grid: {
                        display: false
                    },
                    ticks: {
                        color: colors.textColor
                    }
                }
            }
        };

        charts.revenue = new Chart(revenueCtx, {
            type: 'line',
            data: data,
            options: options
        });
    };

    let campaignChartInstance = null;
    const drawCampaignChart = (themeColors) => {
        const ctx = document.getElementById('campaignChart')?.getContext('2d');
        if (!ctx) return;

        if (campaignChartInstance) {
            campaignChartInstance.destroy();
        }
        
        const data = {
            labels: ['Achieved', 'Remaining'],
            datasets: [{
                data: [75, 25], // Represents 75% progress
                backgroundColor: [themeColors.primary, themeColors.grid],
                borderWidth: 0,
                hoverBackgroundColor: [themeColors.primary, themeColors.grid]
            }]
        };

        const options = {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '80%',
            circumference: 270,
            rotation: -135,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        };

        campaignChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: options
        });
    };

    let salesQuantityChartInstance = null;
    const drawSalesQuantityChart = (themeColors) => {
        const ctx = document.getElementById('salesQuantityChart')?.getContext('2d');
        if (!ctx) return;

        if (salesQuantityChartInstance) {
            salesQuantityChartInstance.destroy();
        }
        
        const lang = localStorage.getItem('language') || 'ro';
        const labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul'];
        
        const getDataSetLabel = (key) => (typeof translations !== 'undefined' && translations[lang] && translations[lang][key]) || key;

        const datasets = [
                {
                label: getDataSetLabel('cat_servicii'),
                data: [120, 80, 100, 150, 180, 200, 150],
                backgroundColor: themeColors.barStack[0],
                },
                {
                label: getDataSetLabel('cat_marfuri'),
                data: [130, 60, 80, 120, 150, 180, 210],
                backgroundColor: themeColors.barStack[1],
                },
                {
                label: getDataSetLabel('cat_consultanta'),
                data: [80, 30, 50, 90, 100, 130, 100],
                backgroundColor: themeColors.barStack[2],
                },
                 {
                label: getDataSetLabel('cat_chirii'),
                data: [50, 20, 40, 60, 80, 90, 70],
                backgroundColor: themeColors.barStack[3],
                },
                 {
                label: getDataSetLabel('cat_altele'),
                data: [40, 20, 20, 30, 40, 50, 20],
                backgroundColor: themeColors.barStack[4],
                },
        ];

        const data = {
            labels: labels,
            datasets: datasets
        };

        const options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: themeColors.text
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: { display: false },
                    ticks: { color: themeColors.text }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    grid: { color: themeColors.grid },
                    ticks: { color: themeColors.text }
                    }
                }
        };

        salesQuantityChartInstance = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: options
        });
    };

    // --- Theme Switcher Logic ---
    themeToggleBtn.addEventListener('click', () => {
        body.classList.toggle('light-theme');
        const isLight = body.classList.contains('light-theme');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = isLight ? 'light_mode' : 'dark_mode';
        
        // Use a short timeout to allow CSS variables to update before redrawing charts
        setTimeout(initializeOrUpdateCharts, 50);
    });

    // --- Initial Load ---
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = 'light_mode';
    } else {
        themeToggleBtn.querySelector('.material-symbols-outlined').textContent = 'dark_mode';
    }

    initializeOrUpdateCharts();
});