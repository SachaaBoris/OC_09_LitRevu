from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from users import forms


class LoginView(View):
    form_class = forms.LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        context = {
                "form": form,
                "message": message,
                "hide_navbar": True
            }
        return render(request, self.template_name, context)

    @method_decorator(require_POST)
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            message = ''
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                )
                if user is not None:
                    login(request, user)
                    return redirect('feed')
                else:
                    message = "Invalid credentials."
            context = {
                "form": form,
                "message": message,
                "hide_navbar": True
            }
            return render(request, self.template_name, context)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("login")
    
    #def dispatch(self, request, *args, **kwargs):
    #    messages.add_message(request, messages.SUCCESS, "Vous avez été déconnecté.")
    #    return super().dispatch(request, *args, **kwargs)


class SignupView(FormView):
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    # success_url = settings.LOGIN_REDIRECT_URL
    success_url = reverse_lazy("feed")

    def form_valid(self, form):

        # Create a new user instance and save it to the database.
        user = form.save()

        # Log the user in.
        login(self.request, user)

        # Redirect to the URL specified as the login destination in settings.
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Obtenir le contexte par défaut du FormView
        context = super().get_context_data(**kwargs)

        # Ajouter la variable hide_navbar pour cacher la navbar
        context['hide_navbar'] = True

        return context