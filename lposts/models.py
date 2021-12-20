from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=64)
    scraped_date = models.DateTimeField(auto_now_add=True)
    article_date = models.DateTimeField()
    excerpt = models.CharField(max_length=1024, blank=True)
    img_link = models.CharField(max_length=512, blank=True)
    source = models.CharField(max_length=2, choices = (
        ('TC', 'TechCrunch'), ('ME', 'Medium'),
    ))

    def __str__(self):
        return self.title
