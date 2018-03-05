from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
from time import gmtime, strftime, time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z .]+$')
RATING_REGEX = re.compile(r'^[1-5]+$')
REVIEW_REGEX = re.compile(r'^[a-zA-Z0-9 .]+$')


class CourseManager(models.Manager):
	def register_validator(self, postData):
		errors = {}
		if len(postData['name']) < 2 and not NAME_REGEX.match(postData['name']):
			errors["name"] = "Name must be longer than 2 characters and no numbers"
		if len(postData['alias']) < 2 and not NAME_REGEX.match(postData['alias']):
			errors["alias"] = "Alias must be longer than 2 characters."
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Email must be a valid email."
		if len(postData['password']) < 8:
			errors["password"] = "Password must be longer than 8 characters and no numbers."
		if postData['password'] != postData['confirm_password']:
			errors['confirm_password'] = "Password must match confrim password"
		email_val = User.objects.filter(email = postData['email'])
		if len(email_val) != 0:
			errors['wrong_password'] = "email already taken"

		return errors

	def login_validator(self, postData):
		match = {}
		user_email = User.objects.filter(email = postData['login_email'])
		if len(postData['login_email']) < 1 or len(postData['login_password']) < 1:
			match['empty'] = "Login fields cannot be blank!"
		if not EMAIL_REGEX.match(postData['login_email']):
			match["email"] = "Email must be a valid email."
		elif len(user_email) == 0:
			match['address'] = "Email not in system"
		elif not bcrypt.checkpw(postData['login_password'].encode(), user_email[0].password.encode()):
			match['wrong'] = "Password not correct"
		return match
class ReviewManager(models.Manager):
	def book_validator(self, postData):
		book = {}
		query_compare = []
		author = Author.objects.all()
		if len(postData['title']) < 1 or len(postData['review']) < 1:
			book['empty'] = "Items cannot be blank"
		if len(postData['author_old']) < 1 and len(postData['author_new']) < 1:
			book['empty_author'] = "Must select or add author"
		if len(postData['author_old']) > 0 and len(postData['author_new']) > 0:
			book['double'] = "Cannot input new and old author"
		if len(postData['author_new']) > 0:
			if not NAME_REGEX.match(postData['author_new']):
				book['author'] = "New author cannot contain letters"
		if len(postData['author_old']) > 0:
			for objects in author:
				query_compare.append(objects.name)
				print query_compare
			if postData['author_old'] not in query_compare:
				book['hack'] = "STOP TRYING TO HACK MY SITE"

		if not RATING_REGEX.match(postData['rating']):
			book['wrong_rating'] = "Invalid rating"

		return book
	def review_validator(self, postData):
		review = {}
		if len(postData['new_review']) < 1 or not REVIEW_REGEX.match(postData['new_review']):
			review['empty'] = "Review cannot be blank"

		if not RATING_REGEX.match(postData['new_rating']):
			review['wrong_rating'] = "Invalid rating"	

		return review



class User(models.Model):
	name = models.CharField(max_length = 255)
	alias = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = CourseManager()

class Book(models.Model):
	title = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()

class Author(models.Model):
	name = models.CharField(max_length = 255)
	books_written = models.ForeignKey(Book, related_name = 'written_by')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()

class Review(models.Model):
	review = models.TextField()
	rating = models.IntegerField()
	reviewed_by = models.ForeignKey(User, related_name = 'reviewed_books')
	book_reviewed = models.ForeignKey(Book, related_name = 'have_reviews')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()


