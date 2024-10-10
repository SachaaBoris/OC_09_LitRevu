from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import CharField
from django.db.models import Value
from django.urls import reverse_lazy, reverse
from itertools import chain
from feed.models import Ticket
from feed.models import Review
from feed.forms import TicketForm
from feed.forms import ReviewForm


class FeedView(LoginRequiredMixin, View):
    template_name = "feed/feed.html"

    def get_reviewed_ticket_ids(self, user):
        #  IDs of tickets reviewed by user
        if user.is_superuser:
            return Review.objects.values_list(
                'ticket_id', flat=True).distinct()
        else:
            # IDs des tickets reviewés par l'utilisateur
            reviewed_by_user = Review.objects.filter(
                user=user).values_list(
                'ticket_id', flat=True)

            # IDs des tickets créés par l'utilisateur qui ont été reviewés
            user_tickets = Ticket.objects.filter(
                user=user).values_list(
                'id', flat=True)
            reviewed_user_tickets = Review.objects.filter(
                ticket_id__in=user_tickets).values_list(
                'ticket_id', flat=True)

            # Convertir les querysets en sets et combiner
            combined_ticket_ids = set(
                reviewed_by_user) | set(reviewed_user_tickets)

            # Retourner la liste combinée des IDs de tickets
            return list(combined_ticket_ids)

    def get_users_viewable_reviews(self, user):
        if user.is_superuser:
            # Return all reviews if the user is a superuser
            return Review.objects.all()
        else:
            # IDs of users followed by the user
            followed_users = list(
                user.following.values_list(
                    'followed_user', flat=True))
            followed_users.append(user.id)  # Add the user themselves

            # Get reviews from users the current user follows
            reviews_from_followed_users = Review.objects.filter(
                user_id__in=followed_users)

            # Get tickets posted by the user and users followed by the user
            followed_users_tickets = Ticket.objects.filter(
                user_id__in=followed_users).values_list(
                'id', flat=True)

            # Get reviews linked to the user's tickets and tickets posted by
            # followed users
            reviews_on_followed_users_tickets = Review.objects.filter(
                ticket_id__in=followed_users_tickets)

            # Combine reviews from followed users and reviews on followed
            # users' tickets
            combined_reviews = reviews_from_followed_users | reviews_on_followed_users_tickets

            return combined_reviews.distinct()

    def get_users_viewable_tickets(self, user):
        if user.is_superuser:
            # Return all tickets if the user is a superuser
            return Ticket.objects.all()
        else:
            # Return tickets from users followed by the user
            followed_users = list(
                user.following.values_list(
                    'followed_user', flat=True))
            followed_users.append(user.id)

            # Get tickets that have been reviewed
            reviewed_ticket_ids = Review.objects.values_list(
                'ticket_id', flat=True)

            # Filter tickets from followed users excluding the reviewed tickets
            return Ticket.objects.filter(user_id__in=followed_users).exclude(
                id__in=reviewed_ticket_ids)

    def get(self, request, *args, **kwargs):
        user = request.user

        # Retrieve and annotate reviews and tickets visible to the user
        reviews = self.get_users_viewable_reviews(request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = self.get_users_viewable_tickets(request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Get IDs of tickets that have been reviewed
        reviewed_ticket_ids = self.get_reviewed_ticket_ids(user)

        # Remember previous page
        previous_url = request.META.get('HTTP_REFERER', None)

        # Merge and sort posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

        # Render user's feed content
        return render(request, self.template_name, context={
            'page': "feed",
            'posts': posts,
            'reviewed_ticket_ids': reviewed_ticket_ids,
            'previous_url': previous_url
        })


class PostView(LoginRequiredMixin, View):
    template_name = "feed/posts.html"

    def get(self, request):
        # Retrieve tickets created by the user, ordered by creation time
        user_tickets = Ticket.objects.filter(
            user=request.user).order_by('-time_created')

        # Retrieve reviews created by the user, ordered by creation time
        user_reviews = Review.objects.filter(
            user=request.user).order_by('-time_created')

        # Remember previous page
        previous_url = request.META.get('HTTP_REFERER', None)

        # Render the page with the fetched tickets and reviews
        return render(request, self.template_name, context={
            'page': "posts",
            'user_tickets': user_tickets,
            'user_reviews': user_reviews,
            'previous_url': previous_url
        })


class TicketCreateView(LoginRequiredMixin, FormView):
    template_name = "feed/ticket_create.html"
    form_class = TicketForm
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        # Save form data into a ticket instance without committing to the
        # database yet
        ticket = form.save(commit=False)

        # Associate the current user as the ticket's creator
        ticket.user = self.request.user

        # Finalize saving the ticket instance to the database
        ticket.save()

        # Redirect to the success URL
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        context['page'] = "create-ticket"
        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "feed/ticket_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        # Retrieve the ticket instance from the database
        ticket = super().get_object(queryset)

        # Check that the user requesting the update is the ticket creator
        if ticket.user != self.request.user:
            return None
        return ticket

    def get(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket is None:
            # Redirect to posts if the user does not have permission
            return redirect('posts')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the form and redirect to the success URL
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        context['page'] = "update-ticket"
        return context


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "feed/ticket_delete.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        # Retrieve the ticket instance
        ticket = super().get_object(queryset)

        # Validate that the user requesting the deletion is the ticket's
        # creator
        if ticket.user != self.request.user:
            return None
        return ticket

    def get(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket is None:
            # Redirect to posts if the user does not have permission
            return redirect('posts')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "feed/review_create.html"
    success_url = reverse_lazy("posts")

    def get_context_data(self, **kwargs):
        rating_range = range(6)
        context = super().get_context_data(**kwargs)
        ticket = get_object_or_404(
            Ticket, pk=self.kwargs.get('ticket_id'))

        context = super().get_context_data(**kwargs)
        context['ticket'] = ticket
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        context['page'] = "review-response"
        context['rating_range'] = rating_range
        return context

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(
            Ticket, pk=self.kwargs.get('ticket_id'))

        # Vérifier si le billet a déjà été critiqué avant de continuer
        if Review.objects.filter(ticket=ticket).exists():
            return redirect(reverse('feed'))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ticket = get_object_or_404(
            Ticket, pk=self.kwargs.get('ticket_id'))
        
        # Assigner l'user et le ticket à l'instance
        form.instance.user = self.request.user
        form.instance.ticket = ticket

        # Save and redirect
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "feed/review_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        # Retrieve the review instance
        review = super().get_object(queryset)
        # Validate that the user requesting the update is the review's creator
        if review.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this review")
        return review

    def form_valid(self, form):
        # Assign the requesting user to the form instance user
        form.instance.user = self.request.user
        # Proceed to default form_valid behavior (save and redirect)
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        review = self.get_object()
        rating_range = range(6)
        context['ticket'] = review.ticket
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        context['page'] = "review-update"
        context['rating_range'] = rating_range
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "feed/review_delete.html"
    success_url = reverse_lazy("posts")

    # Retrieve the review instance
    def get_object(self, queryset=None):
        review = super().get_object(queryset)

        # Validate that the user requesting the deletion is the review's
        # creator
        if review.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this review")
        return review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context


class CreateTicketAndReviewView(LoginRequiredMixin, FormView):
    template_name = 'feed/ticket_and_review_create.html'
    form_class = TicketForm
    second_form_class = ReviewForm
    success_url = reverse_lazy('feed')

    def get_context_data(self, **kwargs):
        rating_range = range(6)
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(
                self.request.POST or None)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        context['page'] = "review-create"
        context['rating_range'] = rating_range
        return context

    def form_valid(self, form):
        # Valider manuellement le deuxième formulaire (review)
        form2 = self.second_form_class(self.request.POST)

        # Vérifier si les deux formulaires sont valides
        if form.is_valid() and form2.is_valid():
            with transaction.atomic():
                # Créer, mais ne pas encore enregistrer l'instance du ticket
                ticket = form.save(commit=False)
                ticket.user = self.request.user
                ticket.save()

                # Créer, mais ne pas encore sauvegarder la review
                review = form2.save(commit=False)
                review.ticket = ticket
                review.user = self.request.user
                review.save()

                # Rediriger vers la success URL si tout est correct
                return super().form_valid(form)
        else:
            # Si l'un des formulaires est invalide, réafficher les formulaires avec les erreurs
            return self.form_invalid(form)
