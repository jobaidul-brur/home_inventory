from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('new/', views.create_item, name='new'),
    path('list/', views.show_item_list, name='list'),
    path('list/?message=<str:message>', views.show_item_list, name='list'),
    path('edit/<int:item_id>/', views.edit_item, name='edit'),
    path('delete/<int:item_id>/', views.delete_item, name='delete'),
]
