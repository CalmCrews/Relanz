from django.urls import path
from .views import new, detail, edit, delete, communityHome, like
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('communityHome/<int:challenge_id>', communityHome, name='communityHome'),
    path('<int:challenge_id>/<int:article_id>', detail, name='detail'),
    path('<int:challenge_id>/new', new, name='new'),
    path('edit/<int:challenge_id>/<int:article_id>', edit, name='edit'),
    path('delete/<int:challenge_id>/<int:article_id>', delete, name='delete'),
    path('<int:article_id>/like/', like, name='like')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)