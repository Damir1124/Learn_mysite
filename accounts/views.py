from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, LoginForm
from django.contrib import messages

class SingUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    initial = None

    # Перенаправит на домашнюю страницу, если пользователь попытается
    # получить доступ к странице регистрации после авторизации
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(SingUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember')

        if not remember:
            # Установим время истечения сеанса равным 0 секундам.
            # Таким образом, он автоматически закроет сеанс после
            # закрытия браузера. И обновим данные.
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        # В противном случае сеанс браузера будет таким же как время сеанса
        # cookie "SESSION_COOKIE_AGE", определенное в settings.py
        return super(CustomLoginView, self).form_valid(form)
