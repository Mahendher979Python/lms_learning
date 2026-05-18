
const trainers = JSON.parse(document.getElementById('trainers-data').textContent);
const students = JSON.parse(document.getElementById('students-data').textContent);
const courses = JSON.parse(document.getElementById('courses-data').textContent);

/* =========================
   1. USERS PIE CHART
========================= */
new Chart(document.getElementById('userChart'), {
    type: 'pie',
    data: {
        labels: ['Trainers', 'Students', 'Courses'],
        datasets: [{
            data: [trainers, students, courses],
            backgroundColor: ['#2563eb', '#16a34a', '#f59e0b']
        }]
    }
});

/* =========================
   2. TRAINERS vs STUDENTS
========================= */
new Chart(document.getElementById('roleChart'), {
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

/* =========================
   3. COURSES CHART
========================= */
new Chart(document.getElementById('courseChart'), {
    type: 'doughnut',
    data: {
        labels: ['Courses'],
        datasets: [{
            data: [courses],
            backgroundColor: ['#f59e0b']
        }]
    }
});

/* =========================
   4. WEEKLY GROWTH (STATIC SAMPLE)
========================= */
new Chart(document.getElementById('growthChart'), {
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
