from django.urls import path
from . import views

app_name = 'farewell'

urlpatterns = [
    path('', views.farewell_index, name='index'),
    path('squad-cards/', views.squad_cards, name='squad_cards'),
    path('add/', views.add_friend, name='add_friend'),
    path('delete/<int:pk>/', views.delete_friend, name='delete_friend'),
    path('friend/<int:pk>/', views.friend_detail, name='friend_detail'),
    path('friend/<int:pk>/edit/', views.edit_friend, name='edit_friend'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/<int:pk>/', views.event_detail_view, name='event_detail'),
    path('gallery/add/', views.add_event, name='add_event'),
    path('gallery/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('gallery/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('gallery/<int:pk>/upload/', views.add_photos, name='add_photos'),
    path('photo/<int:pk>/delete/', views.delete_photo, name='delete_photo'),
    path('timeline/add/', views.add_milestone, name='add_milestone'),
    path('timeline/edit/<int:pk>/', views.edit_milestone, name='edit_milestone'),
    path('timeline/delete/<int:pk>/', views.delete_milestone, name='delete_milestone'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('awards/', views.awards_view, name='awards'),
    path('newspaper/', views.newspaper, name='newspaper'),
]
