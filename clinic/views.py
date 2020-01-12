from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import DoctorLoginForm, DoctorRegisterForm, LoginForm, UserRegistrationForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, ListView
from .models import Doctor, Clinic
from django.contrib.auth.models import User
import random
import string


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class HomePageView(TemplateView):
    template_name = 'home.html'


def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home.html', {'user': user})
            else:
                return HttpResponse(' NO SUCH ACCOUNT')

    else:
        form = DoctorLoginForm()
    return render(request, 'account/login.html', {'form': form})


def doctor_logout(request):
    logout(request)
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        user_form = DoctorRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            name = user_form.cleaned_data['name']
            surname = user_form.cleaned_data['surname']
            clinic_id = user_form.cleaned_data['clinic']
            # clinic = user_form.cleaned_data['clinic']
            # new_user.set_password(user_form.cleaned_data['password'])
            # new_user.save()
            login(request, new_user)
            Doctor.objects.create(name=name, surname=surname, slug=rand_slug(), clinic_id=clinic_id)
            User.objects.create(username=username,password=user_form.password, first_name=name, last_name=surname, email=None).save()
                                  # clinic_id=clinic, slug=rand_slug()).save()
            return render(request,
                          'home.html',
                          {'new_user': new_user})
    else:
        user_form = DoctorRegisterForm()
    return render(request,
                  'account/register.html',
                  {'form': user_form})


class ClinicsListView(ListView):
    model = Clinic
    template_name = 'clinics.html'
    context_object_name = 'clinics'


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'


def test(request):
    return render(request, 'Doctors.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active():
                    login(request, user)
                    return HttpResponse('Авторизация прошла успешно!')
                else:
                    return HttpResponse('Неверный логин или пароль, попробуйте еще раз!')
        else:
            return HttpResponse('Неверный логин')
    else:
        form = LoginForm()
    return render(request, 'account/user_login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.satestve(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'account/user_register_done.html',
                          {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/user_register.html', {'user_form': user_form})


class AboutView(TemplateView):
    template_name = 'about.html'


def user_detail(request):
    user = get_object_or_404(User)
    comments = user.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = user
            new_comment.save()
    else:
        comment_form = CommentForm()
#
    return render(request, 'comment.html', {'user': user,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})




