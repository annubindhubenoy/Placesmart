from django.db import models
from django.contrib.auth.models import User
class CustomUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords

    def __str__(self):
        return self.email



from django.db import models
from django.contrib.auth.models import User

class ExamResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    selected_option = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    mark_weightage = models.IntegerField(default=1)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.question_text[:20]}..."

from django.db import models

class test1(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # A, B, C, or D
    mark_weightage = models.IntegerField(default=1)
    level = models.IntegerField(default=1)  # Difficulty level
    subtopic_id = models.IntegerField()  # 1=Quantitative, 2=Quantitative etc.
    topic_id=models.IntegerField()
    def __str__(self):
        return f"{self.question[:50]}..."
