from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
# INDEX ACTION METHOD
# RENDERS THE REGISTERATION AND LOGIN FORM


def index(request):
    return render(request, 'index.html')


def register(request):
    # check if post request
    if request.method == "POST":
        # check if register object is valid
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        # check to see if user email is already in use
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "email is already in use.",
                           extra_tags=email)
            return redirect('/')

        # Hash the password with bycrpt
        pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

        # Create User in database
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )

        # Put User Id into Session & Redirect
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')
    else:
        return redirect('/')


def login(request):
    # check if Post Request
    if request.method == "POST":
        # Validate the Login object
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        # check if email is in database
        user = User.objects.filter(email=request.POST['login_email'])
        if not user:
            messages.error(request, "Invalid Email/Password",
                           extra_tags="login")
            return redirect('/')
        # Check if passwords match
        if not bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
            messages.error(request, "Invalid Email/Password",
                           extra_tags="login")
            return redirect('/')
        # put user id into session & redirect
        request.session['user_id'] = user[0].id
        return redirect('/dashboard')
    else:
        return redirect('/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_poems': Poem.objects.all()
        }
        return render(request, 'dashboard.html', context)


def create_poemp(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'create_poem.html', context)


def create_poem(request):
    if request.method == "POST":
        errors = Poem.objects.poem_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
                return redirect('/create_poemp')

        Poem.objects.create(
            poem_title=request.POST['poem_title'],
            poem_poem=request.POST['poem_poem'],
            user=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/create_poemp')
    else:
        return redirect('/dashboard')


def like(request, poem_id, user_id):
    poeml = Poem.objects.get(id=poem_id)
    user = User.objects.get(id=user_id)

    poeml.likes.add(user)
    return redirect('/dashboard')


def edit_user(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'edit': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'edit_user.html', context)


def update_user(request):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
                return redirect('/edit_user')
        update = User.objects.get(id=request.session['user_id'])
        update.first_name = request.POST['edit_first_name']
        update.last_name = request.POST['edit_last_name']
        update.email = request.POST['edit_email']
        update.save()
        return redirect('/edit_user')
    else:
        return redirect('/logout')

# def edit_poem(request,poem_id):
#     poem = Poem.objects.get(id=poem_id)
#     context = {
#         "editp": Poem.objects.get(id=request.session['poem_id']),
#     }

#     if poem == poem_id:
#         pass
#     return render(request,'edit_poem.html',context)

# def update_poem(request):
#     if request.method == "POST":
#         errors = Poem.objects.editp_validator(request.POST)
#         if len(errors) > 0:
#             for key,value in errors.items():
#                 messages.error(request,value,extra_tags=key)
#                 return redirect('/edit_poem')
#         update = Poem.objects.get(id=request.session['poem_id'])
#         update.poem_title = request.POST['edit_poem_title']
#         update.poem_poem = request.POST['edit_poem_poem']
#         update.save()
#         return redirect('/edit_poem')
#     else:
#         return redirect('/logout')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')


def destroy(request, poem_id):
    destroy = Poem.objects.get(id=poem_id)
    destroy.delete()
    return redirect('/dashboard')
