document.addEventListener("DOMContentLoaded", function () {
    /* ================= PROGRESS ================= */
    document.querySelectorAll('.premium-progress-fill').forEach(fill => {
        const progress = fill.dataset.progress;
        setTimeout(() => {
            fill.style.width = progress + '%';
        }, 300);
    });

    /* ================= COUNTER ================= */
    document.querySelectorAll('.premium-stat-card-value').forEach(counter => {
        const final = parseInt(counter.innerText);
        let current = 0;
        const increment = final / 50;
        counter.innerText = '0';

        const timer = setInterval(() => {
            current += increment;
            if (current >= final) {
                counter.innerText = final;
                clearInterval(timer);
            } else {
                counter.innerText = Math.floor(current);
            }
        }, 30);
    });

    /* ================= DATA ================= */
    const progressDataEl = document.getElementById('progress-data');
    let progress_percent = 0;

    if (progressDataEl) {
        try {
            progress_percent = JSON.parse(progressDataEl.textContent);
        } catch (e) {
            console.error('Error parsing progress data:', e);
        }
    }

    /* ================= PROGRESS CHART ================= */
    const studentProgressChartEl = document.getElementById('studentProgressChart');
    if (studentProgressChartEl) {
        new Chart(studentProgressChartEl, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Pending'],
                datasets: [{
                    data: [progress_percent, 100 - progress_percent],
                    backgroundColor: [
                        '#3b82f6',
                        'rgba(59,130,246,0.15)'
                    ],
                    borderWidth: 3,
                    borderColor: '#071028',
                    cutout: '65%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                }
            }
        });
    }

    /* ================= PERFORMANCE CHART ================= */
    const studentPerformanceChartEl = document.getElementById('studentPerformanceChart');
    if (studentPerformanceChartEl) {
        new Chart(studentPerformanceChartEl, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Progress',
                    data: [20, 35, 45, 65, progress_percent, progress_percent + 10, progress_percent + 15],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59,130,246,0.2)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#d1d5db' },
                        grid: { color: 'rgba(255,255,255,0.05)' }
                    },
                    y: {
                        ticks: { color: '#d1d5db' },
                        grid: { color: 'rgba(255,255,255,0.05)' }
                    }
                }
            }
        });
    }
});
