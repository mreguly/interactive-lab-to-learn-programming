from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from pyexerciser.forms import UserRegisterForm, UserLoginForm


def index(request):
    return redirect('course:listing')


class UserFormView(View):
    form_class = UserRegisterForm
    template_name = 'register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # if authenticated
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/courses/')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        username = form['username'].value()
        password = form['password'].value()

        # # if authenticated
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/courses/')
        else:
            form.errors.clear()
            error = "Wrong username or password"
            return render(request, self.template_name, {'form': form, 'invalid': error})


def logout_user(request):
    logout(request)
    return redirect('/login/')
