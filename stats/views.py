from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm
from django.contrib import messages
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Login feito com sucesso.')
            else:
                return HttpResponse('Conta inexistente')
        else:
            return HttpResponse('Login Inválido')
    else:
        form = LoginForm()

    return render(request, 'stats/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'stats/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Cria um objeto mas não salva
            new_user = user_form.save(commit=False)
            #Define a senha escolhida
            new_user.set_password(user_form.cleaned_data['password'])
            #Salva o objeto
            new_user.save()
            return render(request, 'stats/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'stats/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Usuário editado com sucesso')
        else:
            messages.error(request, 'Erro ao salvar')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'stats/edit.html', {'user_form': user_form})
