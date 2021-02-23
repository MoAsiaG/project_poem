from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('create_poemp', views.create_poemp),
    path('create_poem', views.create_poem),
    path('destroy/<int:poem_id>', views.destroy),
    path('like/<int:poem_id>/<int:user_id>', views.like),
    path('edit_user', views.edit_user),
    path('update_user', views.update_user),
    # path('edit_poem/<int:poem_id>', views.edit_poem),
]
