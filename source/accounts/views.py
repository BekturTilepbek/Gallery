from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import RegistrationForm
from webapp.models import Album, Photo

User = get_user_model()


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "register.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:photos')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object == self.request.user:
            albums = Album.objects.filter(author=self.object)
            photos = Photo.objects.filter(album=None, author=self.object)
        else:
            albums = Album.objects.filter(is_public=True)
            photos = Photo.objects.filter(album=None, is_public=True)

        context['albums'] = albums
        context['photos'] = photos

        return context
