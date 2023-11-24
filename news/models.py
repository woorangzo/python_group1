from django.db import models


class Issue(models.Model):
    issue_date = models.DateField()
    issue_keyword = models.CharField(max_length=100)
    issue_size = models.FloatField()
    issue_groupid = models.CharField(max_length=5)


class Article(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_office = models.CharField(max_length=10)
    news_title = models.CharField(max_length=100)
    news_time = models.DateTimeField()
    news_writer = models.CharField(max_length=100)
    news_content = models.TextField()

