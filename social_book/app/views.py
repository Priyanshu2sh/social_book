from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from .serializers import UploadedFileSerializer
from django.core.mail import send_mail

# Create your views here.
class UploadedFileList(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

class UploadedFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

def register(request):
    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        gender = request.POST.get('gender', '')
        date_of_birth_str = request.POST['date_of_birth']
        city = request.POST['city']
        state = request.POST['state']
        public_visibility = request.POST.get('public_visibility') == 'true'

        if '' in (email, username, password, full_name, gender, date_of_birth_str, city, state, public_visibility):
            messages.error(request, "All Fields are required!")
            return redirect('register')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address")
            return redirect('register')

        # check email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists !')
            return redirect('register')

        # check username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Sorry, that username's taken. Try another?")
            return redirect('register')
        
        date_of_birth = datetime.strptime(date_of_birth_str, '%d %B %Y').date()

        user = CustomUser(email=email, username=username, full_name=full_name, gender=gender, date_of_birth=date_of_birth, city=city, state=state, public_visibility=public_visibility)
        user.set_password(password)
        user.save()
        login(request, user)
        messages.success(request, 'Registered Successfully !')
        return redirect('home')
    else:
        return render(request, 'app/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully !')

            send_mail(
                'Log In',
                'You successfully logged in the Social Book. Thank You',
                'pksharma6160752@gmail.com',
                [email],
                fail_silently=False,
            )

            return redirect('home')
        else:
            if 'next' in request.GET:
                messages.error(request, 'Please login first.')
            messages.error(request, 'Invalid credentials')
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'app/login.html')

@login_required
def home(request):
    context = {'user': request.user}
    return render(request, 'app/home.html',context)

@login_required
def authors(request):
    users = CustomUser.objects.filter(public_visibility=True)
    context = {'users': users, 'user': request.user}
    return render(request, 'app/authors.html',context)

@login_required
def my_books(request):
    books = UploadedFile.objects.filter(author = request.user)
    if books:
        context = {'user': request.user, 'books':books}    
        return render(request, 'app/my_books.html',context)
    else:
        messages.error(request, 'You haven\'t uploaded any books yet.')
        return redirect('upload_books')

@login_required
def upload_books(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        visibility = request.POST.get('visibility') == 'true'
        cost = request.POST['cost']
        year_published = request.POST['year_published']
        file = request.FILES['file']
        author = request.user
        
        uploaded_file = UploadedFile(title=title, author=author, description=description, visibility=visibility, cost=cost, year_published=year_published, file=file)
        uploaded_file.save()
        return redirect('my_books')
    else:
        context = {'user': request.user}
        return render(request, 'app/upload_books.html',context)