from django.urls import path
from .views import new, detail, edit, delete

app_name = 'community'

urlpatterns = [
    path('new/', new, name='new'),
    path('<int:id>', detail, name='detail'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
]
