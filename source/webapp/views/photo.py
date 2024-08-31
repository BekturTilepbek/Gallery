from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View

from webapp.models import Photo
from webapp.forms import PhotoForm


class PhotoListView(ListView):
    model = Photo
    template_name = "photo/photos_list.html"
    ordering = ['-created_at']
    context_object_name = 'photos'
    paginate_by = 4

    def get_queryset(self):
        return Photo.objects.filter(access='public').order_by('-created_at')


class CreatePhotoView(LoginRequiredMixin, CreateView):
    template_name = "photo/create_photo.html"
    form_class = PhotoForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].queryset = form.fields['album'].queryset.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album:
            if form.instance.album.access == 'private':
                form.instance.access = 'private'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})


class PhotoDetailView(LoginRequiredMixin, DetailView):
    template_name = "photo/photo_detail.html"
    model = Photo

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        if token:
            photo = get_object_or_404(Photo, access_token=token)
            return render(request, self.template_name, {'photo': photo})
        return super().dispatch(request, *args, **kwargs)


class UpdatePhotoView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "photo/update_photo.html"
    form_class = PhotoForm
    model = Photo
    permission_required = "webapp.change_photo"

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album:
            if form.instance.album.access == 'private':
                form.instance.access = 'private'
        return super().form_valid(form)

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})


class DeletePhotoView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = "photo/delete_photo.html"
    model = Photo
    success_url = reverse_lazy("webapp:photos")
    permission_required = "webapp.delete_photo"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class GenerateAccessToken(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        if self.request.user == photo.author:
            photo.generate_access_token()
        return redirect('webapp:photo_detail', pk=photo.pk)


class PhotoFavoriteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        user = self.request.user

        if user in photo.favorite_users.all():
            photo.favorite_users.remove(user)
            in_favorites = False
        else:
            photo.favorite_users.add(user)
            in_favorites = True

        return JsonResponse({'in_favorites': in_favorites})
