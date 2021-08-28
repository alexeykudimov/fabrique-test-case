from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Polls-TestCase API",
      default_version='v1',
      description="Docs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('polls/', views.GetActivePollsListView.as_view({'get': 'list'})),

    path('polls/<int:pk>/', views.PollViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('polls/create/', views.PollViewSet.as_view({'post': 'create'})),

    path('questions/<int:pk>/', views.QuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('questions/create/', views.QuestionViewSet.as_view({'post': 'create'})),

    path('polls/pass/', views.PassPollViewSet.as_view({'post': 'create'})),

    path('user/<int:pk>/', views.UserPollsViewSet.as_view({'get': 'list'})),

    re_path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
