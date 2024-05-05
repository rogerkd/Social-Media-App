from django.urls import path
from chat import views
from chat.views import Room, RoomList, Private

urlpatterns = [

    path('', RoomList.as_view(), name='room_list'),
    path('<str:room_name>/', Room.as_view(), name='room'),
    path('private/<int:user_id>/', Private.as_view(), name='private'),
    path("join_room/<str:room>/", views.join_room, name='join_room'),
    path("leave_room/<str:room>/", views.leave_room, name="leave_room"),
    path('save', views.Save, name='save'),
    path("remove/<str:room>/", views.Remove, name='remove_room'),
]