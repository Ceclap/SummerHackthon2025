document.addEventListener("DOMContentLoaded", function() {
    
    // Chart.js Global Settings
    Chart.defaults.font.family = 'Poppins';
    Chart.defaults.color = '#A0A0A0';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';

    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    const revenueChart = new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Venituri',
                data: [12000, 19000, 15000, 18000, 22000, 25000, 23000, 24000, 20000, 21000, 26000, 28000],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Cheltuieli',
                data: [8000, 9500, 11000, 9000, 13000, 15000, 16000, 14500, 12000, 14000, 17000, 18000],
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        borderDash: [5, 5]
                    },
                    ticks: {
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
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                     labels: {
                        usePointStyle: true,
                        pointStyle: 'rect'
                    }
                }
            }
        }
    });

    // Campaign Chart
    const campaignCtx = document.getElementById('campaignChart').getContext('2d');
    const campaignChart = new Chart(campaignCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [65, 35],
                backgroundColor: ['#4A90E2', '#50D1AA'],
                borderColor: ['#141414', '#141414'],
                borderWidth: 3,
                cutout: '80%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });


    // Sales Quantity Chart
    const salesQuantityCtx = document.getElementById('salesQuantityChart').getContext('2d');
    const salesQuantityChart = new Chart(salesQuantityCtx, {
        type: 'bar',
        data: {
            labels: ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM'],
            datasets: [
                {
                    label: 'hot dog',
                    data: [120, 50, 130, 120, 150, 180, 140],
                    backgroundColor: '#A07E69',
                },
                {
                    label: 'burger',
                    data: [80, 40, 70, 80, 90, 110, 80],
                     backgroundColor: '#E6A573',
                },
                {
                    label: 'sandwich',
                    data: [60, 30, 50, 60, 70, 80, 60],
                    backgroundColor: '#F7C480',
                },
                 {
                    label: 'kebab',
                    data: [40, 20, 30, 40, 50, 60, 40],
                    backgroundColor: '#FDECB0',
                },
                 {
                    label: 'fries',
                    data: [30, 10, 20, 30, 40, 50, 30],
                    backgroundColor: '#ADDDC8',
                },
                {
                    label: 'donut',
                    data: [90, 60, 80, 90, 110, 130, 100],
                    backgroundColor: '#82CA9D',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true,
                     grid: {
                        display: false
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        stepSize: 50
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                         boxWidth: 10,
                         usePointStyle: true,
                         pointStyle: 'rect'
                    }
                }
            }
        }
    });

});