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
    const coursesDataEl = document.getElementById('courses-data');
    const topicsDataEl = document.getElementById('topics-data');
    const assignmentsDataEl = document.getElementById('assignments-data');
    const studentsCountDataEl = document.getElementById('students-count-data');

    let courses = 0;
    let topics = 0;
    let assignments = 0;
    let students_count = 0;

    if (coursesDataEl) {
        try {
            courses = JSON.parse(coursesDataEl.textContent);
        } catch (e) {
            console.error('Error parsing courses data:', e);
        }
    }

    if (topicsDataEl) {
        try {
            topics = JSON.parse(topicsDataEl.textContent);
        } catch (e) {
            console.error('Error parsing topics data:', e);
        }
    }

    if (assignmentsDataEl) {
        try {
            assignments = JSON.parse(assignmentsDataEl.textContent);
        } catch (e) {
            console.error('Error parsing assignments data:', e);
        }
    }

    if (studentsCountDataEl) {
        try {
            students_count = JSON.parse(studentsCountDataEl.textContent);
        } catch (e) {
            console.error('Error parsing students count data:', e);
        }
    }

    /* ================= TRAINER CHART ================= */
    const trainerChartEl = document.getElementById('trainerChart');
    if (trainerChartEl) {
        new Chart(trainerChartEl, {
            type: 'bar',
            data: {
                labels: ['Courses', 'Topics', 'Assignments', 'Students'],
                datasets: [{
                    label: 'Analytics',
                    data: [courses, topics, assignments, students_count],
                    backgroundColor: [
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#8b5cf6'
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

    /* ================= STUDENT CHART ================= */
    const studentChartEl = document.getElementById('studentChart');
    if (studentChartEl) {
        new Chart(studentChartEl, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Progress',
                    data: [20, 35, 45, 65, 80, 95],
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
