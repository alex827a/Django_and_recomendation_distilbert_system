from django.urls import path
from.import views 
from.views import detail, add_review, edit_review_view
from .views import edit_review

app_name='item'

urlpatterns=[
    path('',views.items,name='items'),
    path('new/',views.new,name='new'),
    path('<int:pk>/',views.detail,name='detail'),
    path('<int:pk>/delete/',views.delete,name='delete'),
    path('<int:pk>/edit/',views.edit,name='edit'),
    path('item/<int:pk>/', detail, name='item_detail'),
    path('item/<int:pk>/add_review/', add_review, name='add_review'),
    path('review/edit/<int:pk>/', edit_review_view, name='edit_review_view'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),  
    path('items/', views.items, name='items'),
]