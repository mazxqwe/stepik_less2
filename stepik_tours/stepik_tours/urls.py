from django.urls import path
from django.contrib import admin
from tours import views


urlpatterns = [
    path('', views.MainView.as_view()),
    path('departure/<str:departure>/', views.DepView.as_view()),
    path('tour/<int:tour_id>', views.TourView.as_view()),
    path('admin/', admin.site.urls),
]
