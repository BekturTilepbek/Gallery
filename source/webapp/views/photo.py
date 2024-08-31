from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Photo
from webapp.forms import PhotoForm


class PhotoListView(ListView):
    model = Photo
    template_name = "photo/photos_list.html"
    ordering = ['-created_at']
    context_object_name = 'photos'
    paginate_by = 5

    def get_queryset(self):
        return Photo.objects.filter(is_public=True).order_by('-created_at')


class CreatePhotoView(CreateView):
    template_name = "photo/create_photo.html"
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.album.is_public:
            form.instance.is_public = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})


class PhotoDetailView(DetailView):
    template_name = "photo/photo_detail.html"
    model = Photo


class UpdatePhotoView(UpdateView):
    template_name = "photo/update_photo.html"
    form_class = PhotoForm
    model = Photo

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})


class DeletePhotoView(DeleteView):
    template_name = "photo/delete_photo.html"
    model = Photo
    success_url = reverse_lazy("webapp:photos")

