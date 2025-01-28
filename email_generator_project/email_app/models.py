from django.db import models

# Create your models here.

class Email(models.Model):
    incoming_email = models.TextField()
    email_type = models.CharField(max_length=50)
    tone = models.CharField(max_length=50)
    generated_subject = models.CharField(max_length=255)
    generated_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.generated_subject