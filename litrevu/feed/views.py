from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import CharField
from django.db.models import Value
from django.urls import reverse_lazy
from itertools import chain
from feed.models import Ticket
from feed.models import Review
from feed.forms import TicketForm
from feed.forms import ReviewForm


class FeedView(LoginRequiredMixin, View):
    template_name = "feed/feed.html"
    
    def get_reviewed_ticket_ids(self, user):
        #  IDs of tickets reviewed by user
        return Review.objects.filter(user=user).values_list('ticket_id', flat=True)
    
    def get_users_viewable_reviews(self, user):
        #  Reviews from users followed by user
        followed_users = list(user.following.values_list('followed_user', flat=True))
        followed_users.append(user.id)
        return Review.objects.filter(user_id__in=followed_users)
    
    def get_users_viewable_tickets(self, user):
        #  Tickets from users followed by user
        followed_users = list(user.following.values_list('followed_user', flat=True))
        followed_users.append(user.id)
        return Ticket.objects.filter(user_id__in=followed_users)
    
    def get(self, request, *args, **kwargs):
        # Retrieve and annotate reviews and tickets visible to the user
        reviews = self.get_users_viewable_reviews(request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = self.get_users_viewable_tickets(request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Get IDs of tickets reviewed by the user
        reviewed_ticket_ids = self.get_reviewed_ticket_ids(request.user)
        
        # Remember previous page
        previous_url = request.META.get('HTTP_REFERER', None)
        
        # Merge and sort posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

        # Render user's feed content
        return render(request, self.template_name,
                      context={
                      'posts': posts,
                      'reviewed_ticket_ids': reviewed_ticket_ids,
                      'previous_url': previous_url
                      })


class PostView(LoginRequiredMixin, View):
    template_name = "feed/posts.html"

    def get(self, request):
        # Retrieve tickets created by the user, ordered by creation time
        user_tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')

        # Retrieve reviews created by the user, ordered by creation time
        user_reviews = Review.objects.filter(user=request.user).order_by('-time_created')
        
        # Remember previous page
        previous_url = request.META.get('HTTP_REFERER', None)
        
        # Render the page with the fetched tickets and reviews
        return render(request, self.template_name, 
                      context={
                      'user_tickets': user_tickets,
                      'user_reviews': user_reviews,
                      'previous_url': previous_url
                      })


class TicketCreateView(LoginRequiredMixin, FormView):
    template_name = "feed/ticket_create.html"
    form_class = TicketForm
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        # Save form data into a ticket instance without committing to the database yet
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
            raise PermissionDenied("You do not have permission to edit this ticket.")
        return ticket

    def form_valid(self, form):
        # Save the form and redirect to the success URL
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "feed/ticket_delete.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        # Retrieve the ticket instance
        ticket = super().get_object(queryset)

        # Validate that the user requesting the deletion is the ticket's creator
        if ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this ticket.")
        return ticket
    
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
        context = super().get_context_data(**kwargs)
        context['ticket'] = get_object_or_404(Ticket, pk=self.kwargs.get('ticket_id'))
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context

    def form_valid(self, form):
        # Assign the requesting user and related ticket to the form instance
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs.get('ticket_id'))

        # Proceed to default form_valid behavior (save and redirect)
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
            raise PermissionDenied("You do not have permission to edit this review")
        return review

    def form_valid(self, form):
        # Assign the requesting user to the form instance user
        form.instance.user = self.request.user
        # Proceed to default form_valid behavior (save and redirect)
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        review = self.get_object()
        context['ticket'] = review.ticket
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "feed/review_delete.html"
    success_url = reverse_lazy("posts")

    # Retrieve the review instance
    def get_object(self, queryset=None):
        review = super().get_object(queryset)

        # Validate that the user requesting the deletion is the review's creator
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review")
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
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.POST or None)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', None)
        return context

    def form_valid(self, form):
        # Create, but don't save the new ticket instance yet
        ticket = form.save(commit=False)

        # Assign the current user to the new ticket instance
        ticket.user = self.request.user

        # Save the ticket instance
        ticket.save()

        # Manually validate the second form
        form2 = self.second_form_class(self.request.POST)

        # Check the validity of the second form
        if form2.is_valid():

            # Create, but don't save the new review instance yet
            review = form2.save(commit=False)

            # Assign the current user and associated ticket to the new review instance
            review.ticket = ticket
            review.user = self.request.user

            # Save the review instance
            review.save()

            # Redirect to the success URL
            return super().form_valid(form)
        else:
            # If the second form is invalid, re-render the forms with the data
            return self.form_invalid(form)
