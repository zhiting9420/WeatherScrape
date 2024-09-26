// 气温走势图
function createTemperatureChart() {
    var ctx = document.getElementById('temperatureChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: '最高气温 (°C)',
                data: chartData.maxTemperatures,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            },
            {
                label: '最低气温 (°C)',
                data: chartData.minTemperatures,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: '温度 (°C)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '月度气温走势图'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        title: function(context) {
                            return '日期: ' + context[0].label;
                        },
                        label: function(context) {
                            var label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.parsed.y + '°C';
                            }
                            return label;
                        }
                    }
                },
                crosshair: {
                    line: {
                        color: '#808080',
                        width: 1
                    },
                    sync: {
                        enabled: true,
                        group: 1,
                        suppressTooltips: false
                    },
                    zoom: {
                        enabled: false
                    },
                    snap: {
                        enabled: true
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index',
            },
        }
    });
}

// 天气统计柱状图
function createWeatherChart() {
    var weatherCtx = document.getElementById('weatherChart').getContext('2d');
    new Chart(weatherCtx, {
        type: 'bar',
        data: {
            labels: chartData.weatherTypes,
            datasets: [{
                label: '天数',
                data: chartData.weatherCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '天数'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '月度天气类型统计'
                },
                crosshair: false
            }
        }
    });
}

// 表格动画
function animateTable() {
    gsap.from("table tr", {
        duration: 0.5,
        opacity: 0,
        y: 20,
        stagger: 0.05,
        ease: "power1.out",
        delay: 0.5
    });
}

// 初始化函数
function initCharts() {
    createTemperatureChart();
    createWeatherChart();
    animateTable();
}

// 当 DOM 加载完成后初始化图表
document.addEventListener('DOMContentLoaded', initCharts);