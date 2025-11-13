from django.db import models


class Test1Result(models.Model):
    email = models.EmailField()
    status = models.CharField(max_length=50)
    logs = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.status} ({self.created_at.isoformat()})"
