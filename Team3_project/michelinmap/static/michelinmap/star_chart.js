document.addEventListener("DOMContentLoaded", function() {
    const ratingDataElement = document.getElementById('star_ratio');
    if (!ratingDataElement) return;

    const ratingData = JSON.parse(ratingDataElement.textContent);

    const labels = ['★★★★★','★★★★☆','★★★☆☆','★★☆☆☆','★☆☆☆☆'];
    const data = [
        ratingData[5] || 0,
        ratingData[4] || 0,
        ratingData[3] || 0,
        ratingData[2] || 0,
        ratingData[1] || 0
    ];

    const ctx = document.getElementById('starChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels, 
            datasets: [{
                label: '별점 개수',
                data: data,
                backgroundColor: '#FFD700',
                borderColor: '#FFD700',
                borderWidth: 1,
                borderRadius: 10,
                borderSkipped: false,
                
                categoryPercentage: 0.6, 
                barPercentage: 0.8     
            }]
        },
        options: {
            indexAxis: 'y',
            
            responsive: false, 
            maintainAspectRatio: true, 
        
            hover: {
                mode: false 
            },
            
            plugins: { 
                legend: { display: false }, 
                tooltip: { enabled: false }
            },
            
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: 'transparent' }, 
                    display: false 
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'transparent',
                        drawOnChartArea: false
                    },
                    
                    ticks: {
                        drawTicks: false,
                        color: '#FFD700',
                        font: {
                            size: 25,     
                            weight: 'bold', 
                        },
                        padding: 5
                    },
                    border: {
                        display: false
                    },
                    offset: true
                } 
            },
            animation: false 
        }
    });
});
