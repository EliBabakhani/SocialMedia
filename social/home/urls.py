from django.urls import path
from . import views

app_name='home'
urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('detail/<int:id>/<slug:slug>',views.PostDetailView.as_view(), name='detail'),
    path('post/delete/<int:id>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:id>', views.PostUpdateView.as_view(), name='post_update'),
]