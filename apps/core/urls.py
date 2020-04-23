from django.urls import path

from apps.core.views import list_item, create_item, detail_item, update_item, delete_item, add_to_cart, remove_from_cart


urlpatterns = [
    path('', list_item, name='list_item'),
    path('create_item/', create_item, name='create_item'),
    path('item/<int:id>/', detail_item, name='detail_item'),
    path('item/<int:id>/update/', update_item, name='update_item'),
    path('item/<int:id>/delete/', delete_item, name='delete_item'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),

]