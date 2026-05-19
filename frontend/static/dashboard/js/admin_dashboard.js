document.addEventListener("DOMContentLoaded", function() {
    const trainersDataEl = document.getElementById('trainers-data');
    const studentsDataEl = document.getElementById('students-data');
    const coursesDataEl = document.getElementById('courses-data');

    let trainers = 0;
    let students = 0;
    let courses = 0;

    if (trainersDataEl) {
        try {
            trainers = JSON.parse(trainersDataEl.textContent);
        } catch (e) {
            console.error('Error parsing trainers data:', e);
        }
    }

    if (studentsDataEl) {
        try {
            students = JSON.parse(studentsDataEl.textContent);
        } catch (e) {
            console.error('Error parsing students data:', e);
        }
    }

    if (coursesDataEl) {
        try {
            courses = JSON.parse(coursesDataEl.textContent);
        } catch (e) {
            console.error('Error parsing courses data:', e);
        }
    }

    const isDark = document.body.classList.contains('dark');
    const textColor = isDark ? '#f8fafc' : '#1e293b';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                color: textColor,
                font: {
                family: 'Segoe UI',
                size: 13,
                weight: '600'
            }
            }
        }
    };

    /* =========================
       1. USERS PIE CHART (3D Style)
    ========================= */
    const userChartEl = document.getElementById('userChart');
    if (userChartEl) {
        new Chart(userChartEl, {
            type: 'pie',
            data: {
                labels: ['Trainers', 'Students', 'Courses'],
                datasets: [{
                    data: [trainers, students, courses],
                    backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b'
                    ],
                    borderColor: isDark ? '#1e293b' : '#ffffff',
                    borderWidth: 3,
                    hoverOffset: 12,
                    borderRadius: 8
                }]
            },
            options: {
                ...chartOptions,
                plugins: {
                    ...chartOptions.plugins,
                    legend: {
                    position: 'bottom',
                    labels: {
                        ...chartOptions.plugins.legend.labels,
                        padding: 20
                    }
                }
            }
        });
    }

    /* =========================
       2. TRAINERS vs STUDENTS (Bar)
    ========================= */
    const roleChartEl = document.getElementById('roleChart');
    if (roleChartEl) {
        new Chart(roleChartEl, {
            type: 'bar',
            data: {
                labels: ['Trainers', 'Students'],
                datasets: [{
                    label: 'Count',
                    data: [trainers, students],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.9)',
                        'rgba(16, 185, 129, 0.9)'
                    ],
                    borderColor: [
                        '#3b82f6',
                        '#10b981'
                    ],
                    borderWidth: 3,
                    borderRadius: 12,
                    borderSkipped: false
                }]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                    beginAtZero: true,
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: textColor
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: textColor,
                        font: {
                            weight: '600'
                        }
                    }
                }
            }
        });
    }

    /* =========================
       3. COURSES CHART (Doughnut 3D)
    ========================= */
    const courseChartEl = document.getElementById('courseChart');
    if (courseChartEl) {
        new Chart(courseChartEl, {
            type: 'doughnut',
            data: {
                labels: ['Active Courses'],
                datasets: [{
                    data: [courses, Math.max(0, 20 - courses)],
                    backgroundColor: [
                        '#f59e0b',
                        'rgba(245, 158, 11, 0.15)'
                    ],
                    borderColor: isDark ? '#1e293b' : '#ffffff',
                    borderWidth: 3,
                    cutout: '65%',
                    hoverOffset: 8
                }]
            },
            options: {
                ...chartOptions,
                plugins: {
                    ...chartOptions.plugins,
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    /* =========================
       4. WEEKLY GROWTH (Premium Line)
    ========================= */
    const growthChartEl = document.getElementById('growthChart');
    if (growthChartEl) {
        new Chart(growthChartEl, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    {
                        label: 'Students',
                        data: [12, 19, 15, 25, 22, 30, 35],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.15)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 6,
                        pointHoverRadius: 10,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: isDark ? '#0f172a' : '#ffffff',
                        pointBorderWidth: 3
                    },
                    {
                        label: 'Trainers',
                        data: [3, 5, 4, 6, 8, 7, 10],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.15)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 6,
                        pointHoverRadius: 10,
                        pointBackgroundColor: '#10b981',
                        pointBorderColor: isDark ? '#0f172a' : '#ffffff',
                        pointBorderWidth: 3
                    }
                ]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                    beginAtZero: true,
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: textColor
                    }
                },
                    x: {
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: textColor
                    }
                }
            }
        });
    }
});
