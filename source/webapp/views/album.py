from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Album, Photo
from webapp.forms import AlbumForm


class CreateAlbumView(CreateView):
    template_name = "album/create_album.html"
    form_class = AlbumForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:album_detail", kwargs={"pk": self.object.pk})


class AlbumDetailView(DetailView):
    template_name = "album/album_detail.html"
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(album=self.object)
        return context


class UpdateAlbumView(UpdateView):
    template_name = "album/update_album.html"
    form_class = AlbumForm
    model = Album

    def get_success_url(self):
        return reverse("webapp:album_detail", kwargs={"pk": self.object.pk})


class DeleteAlbumView(DeleteView):
    template_name = "album/delete_album.html"
    model = Album
    success_url = reverse_lazy("webapp:photos")

