from django.db import models
from django.db.models import Sum
from accounts.models import User
from courses.models import Course

# =========================
# TRAINER MODEL
# =========================
class Trainer(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="trainer_profile"
    )

    def __str__(self):
        return self.user.username

# =========================
# TOPIC MODEL
# =========================
class Topic(models.Model):
    name = models.CharField(max_length=200)
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="topics"
    )

    def __str__(self):
        return self.name

# =========================
# ASSIGNMENT MODEL
# =========================
class Assignment(models.Model):
    TEST_TYPES = (
        ("mcq", "MCQ"),
        ("pdf", "PDF"),
        ("gform", "Google Form"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Relationships
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Settings
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default="mcq")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    duration = models.PositiveIntegerField(default=30) # In minutes
    
    # Selection-based Scoring (Used for ALL test types)
    # Trainer/Admin enters these (e.g., Max: 20, Pass: 15)
    total_marks = models.PositiveIntegerField(default=100) 
    pass_marks = models.PositiveIntegerField(default=40)  

    # File/Link Support
    pdf_file = models.FileField(upload_to="assignments/pdfs/", null=True, blank=True)
    google_form_link = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_marks(self):
        """
        For MCQ: Recalculates total based on question weights.
        For PDF/GForm: Keeps the manual total_marks set by Trainer/Admin.
        """
        if self.test_type == "mcq":
            total = self.questions.aggregate(Sum('marks'))['marks__sum'] or 0
            if total > 0:
                self.total_marks = total
                self.save()

    def __str__(self):
        return self.title

# =========================
# QUESTION MODEL (For MCQ only)
# =========================
class Question(models.Model):
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    text = models.TextField() 
    marks = models.PositiveIntegerField(default=1) 
    
    #New filed added about time for each qns
    time_limit = models.IntegerField("Time in seconds")
    #def __str__(self):
       # return self.question_text
    
    def __str__(self):
        return self.text

# =========================
# OPTION MODEL (For MCQ only)
# =========================
class Option(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# =========================
# SUBMISSION MODEL
# =========================
class Submission(models.Model):
    SUBMISSION_STATUS = (
        ("started", "Started"),     
        ("submitted", "Submitted"), 
        ("graded", "Graded"),       
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Proof for PDF/Google Form types
    pdf_answer = models.FileField(upload_to="submissions/pdfs/", null=True, blank=True)
    
    # Results
    # This score is auto-filled for MCQ and manually filled for PDF/GForm
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default="started")
    submitted_at = models.DateTimeField(null=True, blank=True)

    @property
    def percentage(self):
        """Standardized percentage regardless of test type."""
        if self.assignment.total_marks > 0:
            return (self.score / self.assignment.total_marks) * 100
        return 0

    @property
    def is_passed(self):
        """
        The Universal Rule:
        Works for MCQ (Auto), PDF (Manual Grade), and GForm (Manual Grade).
        Example: If Admin set Pass Marks to 15, and Score is 14 -> FAIL.
        """
        return self.score >= self.assignment.pass_marks

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

# =========================
# ANSWER MODEL (Only for MCQ choice tracking)
# =========================
class Answer(models.Model):
    submission = models.ForeignKey(
        Submission, 
        on_delete=models.CASCADE, 
        related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Ans: {self.submission.student.username} - {self.question.id}"