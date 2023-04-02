from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'elevators', views.ElevatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('elevator_requests/', views.ElevatorRequests.as_view()),
    path('elevator_destination/<int:elevator_id>/', views.ElevatorDestination.as_view()),
    path('elevator_direction/<int:elevator_id>/', views.ElevatorDirection.as_view()),
    path('add_request/', views.AddRequest.as_view()),
    path('maintenance/<int:elevator_id>/', views.Maintenance.as_view()),
    path('open_door/<int:elevator_id>/', views.OpenDoor.as_view()),
    path('close_door/<int:elevator_id>/', views.CloseDoor.as_view()),
]
