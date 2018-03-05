from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from models import *
import bcrypt 

# Create your views here.
def index(request):
	return render(request, 'reviews/index.html')

def success(request, num):
	query_recent = []
	query_compare = []
	query_old = []
	context = {
		'reviews': Review.objects.all().order_by('-created_at'),
		'query_recent': query_recent,
		'query_old': query_old,
	}
	id_start = len(Review.objects.all())
	id_end = len(Review.objects.all())
	reviews = Review.objects.all().order_by('-created_at')
	count = 1
	for objects in reviews:
		if count < 4:
			query_recent.append(objects)
			query_compare.append(objects.book_reviewed.title)
			count += 1
	for objects in reviews:
		if objects.book_reviewed.title not in query_compare:
			query_compare.append(objects.book_reviewed.title)
			query_old.append(objects)
	return render(request, 'reviews/success.html', context)

def add(request):
	context = {
		'authors': Author.objects.all()
	}
	return render(request, 'reviews/add.html', context)

def profile(request, num):
	context = {
		'user': User.objects.get(id = num),
		'reviews': Review.objects.filter(reviewed_by = num),
		'reviews_len': len(Review.objects.filter(reviewed_by = num))
	}
	return render(request, 'reviews/profile.html', context)

def login(request):
	match = User.objects.login_validator(request.POST)
	if len(match):
		for tag, error in match.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		user = User.objects.filter(email = request.POST['login_email'])
		request.session['id'] = user[0].id
		request.session['name'] = user[0].name
		return redirect('/success/' + str(request.session['id']))

def register(request):
	errors = User.objects.register_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		name = request.POST['name']
		alias = request.POST['alias']
		email = request.POST['email']
		password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(name = name, alias = alias, email = email, password = password)
		request.session['name'] = name
		request.session['id'] = User.objects.get(email = request.POST['email']).id
		return redirect('/success/' + str(request.session['id']))
	# password = request.POST['password']

def logout(request):
	request.session.pop('id')
	request.session.pop('name')
	return redirect('/')

def create(request):
	book = Review.objects.book_validator(request.POST)
	if len(book):
		for tag, error in book.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/add')
	else:
		title = request.POST['title']
		name_new = request.POST['author_new']
		name_old = request.POST['author_old']
		review = request.POST['review']
		rating = request.POST['rating']
		user = User.objects.get(id = request.session['id'])
		Book.objects.create(title = title)
		if len(name_new) == 0:
			Author.objects.create(name = name_old, books_written = Book.objects.all().last())
		else:
			Author.objects.create(name = name_new, books_written = Book.objects.all().last())
		Review.objects.create(review = review, rating = rating, reviewed_by = user, book_reviewed = Book.objects.all().last())
		return redirect('success/' + str(request.session['id']))

def review_page(request, num, num2):
	context = {
		'book': Book.objects.get(id = num2),
		'author': Author.objects.get(books_written = num2),
		'review': Review.objects.filter(book_reviewed = num2)
	}
	return render(request, 'reviews/review_page.html', context)

def add_review(request, num, num2):
	review = Review.objects.review_validator(request.POST)
	if len(review):
		for tag, error in review.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/review_page/' + str(request.session['id']) + '/' + str(Book.objects.get(id =num2).id))
	else:
		new_review = request.POST['new_review']
		new_rating = request.POST['new_rating']
		Review.objects.create(review = new_review, rating = new_rating, book_reviewed = Book.objects.get(id = num2), reviewed_by = User.objects.get(id = num))
		return redirect('/review_page/' + str(request.session['id']) + '/' + str(Book.objects.get(id =num2).id))

def delete(request, num, num2):
	b = Review.objects.get(id = num)
	b.delete()
	if len(Review.objects.filter(book_reviewed = num2)) == 0:
		d = Book.objects.get(id = num2)
		d.delete()
		return redirect('/success/' + str(request.session['id']))
	return redirect('/review_page/' + str(request.session['id']) + '/' + str(Book.objects.get(id = num2).id))

























