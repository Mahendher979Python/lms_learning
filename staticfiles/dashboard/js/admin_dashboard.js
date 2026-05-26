document.addEventListener("DOMContentLoaded", function () {
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

    /* ================= CHARTS ================= */
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

    // Users Overview Chart
    const adminUserChartEl = document.getElementById('adminUserChart');
    if (adminUserChartEl) {
        new Chart(adminUserChartEl, {
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
                    borderWidth: 3,
                    borderColor: '#071028'
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

    // Trainers vs Students Chart
    const adminRoleChartEl = document.getElementById('adminRoleChart');
    if (adminRoleChartEl) {
        new Chart(adminRoleChartEl, {
            type: 'bar',
            data: {
                labels: ['Trainers', 'Students'],
                datasets: [{
                    label: 'Count',
                    data: [trainers, students],
                    backgroundColor: [
                        '#3b82f6',
                        '#10b981'
                    ],
                    borderRadius: 12
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
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    y: {
                        ticks: { color: '#d1d5db' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    }
                }
            }
        });
    }

    // Courses Chart
    const adminCourseChartEl = document.getElementById('adminCourseChart');
    if (adminCourseChartEl) {
        new Chart(adminCourseChartEl, {
            type: 'doughnut',
            data: {
                labels: ['Active Courses'],
                datasets: [{
                    data: [courses, Math.max(0, 30 - courses)],
                    backgroundColor: [
                        '#f59e0b',
                        'rgba(245, 158, 11, 0.15)'
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
                        display: false
                    }
                }
            }
        });
    }
});
