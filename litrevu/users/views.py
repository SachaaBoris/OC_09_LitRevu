from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from users import forms
from users.models import UserFollows, CustomUser
from django.conf import settings


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

    # def dispatch(self, request, *args, **kwargs):
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


class FollowedUsersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Obtenir tous les suivis de l'utilisateur
        followed_users = UserFollows.objects.filter(user=user)

        # Créer une liste des utilisateurs suivis (pour faciliter la
        # vérification)
        followed_user_ids = followed_users.values_list(
            'followed_user_id', flat=True)

        # Créer un contexte avec les utilisateurs suivis
        context = {
            'followed_users': followed_users,
            'followed_user_ids': followed_user_ids
        }

        if settings.ALLOW_USER_SEE_ALL_USERS:
            CustomUser = get_user_model()
            all_users = CustomUser.objects.filter(
                is_superuser=False).exclude(
                id=user.id).order_by('username')
            context['all_users'] = all_users

        # Rendre la page avec le contexte
        return render(request, 'users/followed_users.html', context)


class FollowUserView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        # Retrieve the username to follow from the POST data.
        username_to_follow = request.POST.get('username_to_follow')

        # Check if the user is trying to follow themselves.
        if username_to_follow == request.user.username:
            messages.error(request, "You cannot follow yourself.")
            return redirect('subscriptions')

        try:
            # Retrieve the user to follow from the database.
            user_to_follow = CustomUser.objects.get(
                username=username_to_follow)

            # Hide superUsers
            if user_to_follow.is_superuser:
                messages.error(request, "You cannot follow a superuser.")
                return redirect('subscriptions')

            # Check if the follow relationship already exists
            if UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_follow).exists():
                messages.error(
                    request, f"You are already following {username_to_follow}!")
            else:
                # Create a new follow relationship.
                UserFollows.objects.create(
                    user=request.user, followed_user=user_to_follow)
                messages.success(
                    request, f"You are now following {
                        user_to_follow.username}!")

        except CustomUser.DoesNotExist:
            # Send an error message if the user to follow does not exist.
            messages.error(
                request, f"The user {username_to_follow} does not exist.")
        except IntegrityError:
            # Send an error message if the following relationship already
            # exists.
            messages.error(
                request, f"You are already following {username_to_follow}!")
        # Redirect the user back to the 'abonnements' page.
        return redirect('subscriptions')


class UnfollowUserView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, pk, *args, **kwargs):
        follow = UserFollows.objects.filter(
            user=request.user, followed_user_id=pk).first()
        # Check if the following relationship is found.
        if follow:
            # Save the followed user's username for use in the message.
            followed_username = follow.followed_user.username

            # Delete the following relationship.
            follow.delete()

            # Send a success message to the user.
            messages.success(
                request, f"You have unfollowed {followed_username}.")
        else:
            # If the relationship is not found, send an error message to the
            # user.
            messages.error(request, "User not found.")

        # Redirect the user back to the 'abonnements' page.
        return redirect('subscriptions')
