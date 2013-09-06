from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.name


class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	post_date = models.DateTimeField('date published', auto_now_add=True)
	content = models.TextField()
	tag = models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.title


class Comment(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	post = models.ForeignKey(Post)