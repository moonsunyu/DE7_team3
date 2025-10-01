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
                backgroundColor: '#FFD700', // ✨ 색상 단일화 (원래 금색)
                borderColor: '#FFD700',
                borderWidth: 1,
                borderRadius: 3,
                
                categoryPercentage: 0.8, // 카테고리가 차지하는 공간 비율을 늘림 (막대 두께)
                barPercentage: 0.9      // 막대가 카테고리 공간에서 차지하는 비율을 늘림 (간격 감소)
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
                            size: 30,       // 글꼴 크기를 14px로 설정
                            weight: 'bold', // 글꼴을 굵게 설정
                        }
                    },
                    border: {
                        display: false
                    }
                } 
            },
            animation: false 
        }
    });
});