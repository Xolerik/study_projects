from django.urls import path
from .views import index, product_type, AMDVideoView, video_cards

urlpatterns = [
    path("<int:product_id>/", product_type, name="producttype"),
    path ('', index, name="index"),
    path("create/", AMDVideoView.as_view(), name="create"),
    path("video_cards/", video_cards, name="video_cards")
]