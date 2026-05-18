from django.db import models
from django.conf import settings


# =========================
# SUBJECT
# =========================
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =========================
# TRAINER
# =========================
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name


# =========================
# ASSIGNMENT
# =========================
class Assignment(models.Model):
    EXAM_TYPE = (
        ('mcq', 'MCQ'),
        ('gform', 'Google Form'),
        ('pdf', 'PDF Upload'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    test_type = models.CharField(max_length=20, choices=EXAM_TYPE, default='mcq')

    # Optional fields based on type
    google_form_link = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='assignments/', blank=True, null=True)

    total_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=40)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_assignments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# QUESTION (MCQ ONLY)
# =========================
class Question(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
        ]
    )

    marks = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.assignment.title} - Q{self.id}"


# =========================
# SUBMISSION
# =========================
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ('started', 'Started'),
            ('submitted', 'Submitted'),
            ('evaluated', 'Evaluated'),
        ],
        default='started'
    )

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    # 🔥 IMPORTANT FIX → prevent duplicate submissions
    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student} - {self.assignment}"


# =========================
# ANSWER
# =========================
class Answer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_option = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
        ]
    )

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.student} - Q{self.question.id}"