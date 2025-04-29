
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GetStoryDots

urlpatterns = format_suffix_patterns([
    path('get_story_dots', GetStoryDots.as_view(), name='get_story_dots')
])
