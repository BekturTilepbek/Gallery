from django.urls import path
from django.views.generic import RedirectView

from webapp.views import PhotoListView, CreatePhotoView, PhotoDetailView, UpdatePhotoView, DeletePhotoView, \
    GenerateAccessToken, PhotoFavoriteView, CreateAlbumView, AlbumDetailView, UpdateAlbumView, DeleteAlbumView, \
    AlbumFavoriteView

app_name = 'webapp'

urlpatterns = [
    path('photos/', PhotoListView.as_view(), name='photos'),
    path('', RedirectView.as_view(pattern_name='webapp:photos')),
    path('photos/create/', CreatePhotoView.as_view(), name='create_photo'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/<str:token>/', PhotoDetailView.as_view(), name='photo_detail_by_token'),
    path('photos/<int:pk>/update', UpdatePhotoView.as_view(), name='update_photo'),
    path('photos/<int:pk>/delete', DeletePhotoView.as_view(), name='delete_photo'),
    path('photos/<int:pk>/token/', GenerateAccessToken.as_view(), name='generate_token'),
    path('albums/create/', CreateAlbumView.as_view(), name='create_album'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('albums/<int:pk>/update', UpdateAlbumView.as_view(), name='update_album'),
    path('albums/<int:pk>/delete', DeleteAlbumView.as_view(), name='delete_album'),
    path('photos/<int:pk>/add-to-favorites/', PhotoFavoriteView.as_view(), name='photo_to_favorites'),
    path('albums/<int:pk>/add-to-favorites/', AlbumFavoriteView.as_view(), name='album_to_favorites')
]
