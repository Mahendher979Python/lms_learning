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

    /* =========================
       1. USERS PIE CHART
    ========================= */
    const userChartEl = document.getElementById('userChart');
    if (userChartEl) {
        new Chart(userChartEl, {
            type: 'pie',
            data: {
                labels: ['Trainers', 'Students', 'Courses'],
                datasets: [{
                    data: [trainers, students, courses],
                    backgroundColor: ['#2563eb', '#16a34a', '#f59e0b']
                }]
            }
        });
    }

    /* =========================
       2. TRAINERS vs STUDENTS
    ========================= */
    const roleChartEl = document.getElementById('roleChart');
    if (roleChartEl) {
        new Chart(roleChartEl, {
            type: 'bar',
            data: {
                labels: ['Trainers', 'Students'],
                datasets: [{
                    label: 'Users',
                    data: [trainers, students],
                    backgroundColor: ['#2563eb', '#16a34a']
                }]
            }
        });
    }

    /* =========================
       3. COURSES CHART
    ========================= */
    const courseChartEl = document.getElementById('courseChart');
    if (courseChartEl) {
        new Chart(courseChartEl, {
            type: 'doughnut',
            data: {
                labels: ['Courses'],
                datasets: [{
                    data: [courses],
                    backgroundColor: ['#f59e0b']
                }]
            }
        });
    }

    /* =========================
       4. WEEKLY GROWTH (STATIC SAMPLE)
    ========================= */
    const growthChartEl = document.getElementById('growthChart');
    if (growthChartEl) {
        new Chart(growthChartEl, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Growth',
                    data: [5, 10, 8, 15, 20, 18, 25],
                    borderColor: '#2563eb',
                    tension: 0.4
                }]
            }
        });
    }
});
