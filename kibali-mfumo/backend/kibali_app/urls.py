from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('permits/create/', views.create_permit, name='create_permit'),
    path('permits/', views.list_permits, name='list_permits'),
    path('permits/<int:permit_id>/', views.get_permit_detail, name='permit_detail'),
    path('permits/<int:permit_id>/download/', views.download_permit_pdf, name='download_permit_pdf'),
]
