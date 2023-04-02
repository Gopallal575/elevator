from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer


class ElevatorViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()

    def retrieve(self, request, *args, **kwargs):
        elevator = self.get_object()
        serializer = self.get_serializer(elevator)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        elevator = self.get_object()
        serializer = self.get_serializer(elevator, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def assign_elevator(self, request):
        try:
            floors = request.data['floors']
        except KeyError:
            return Response({'error': 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)

        elevator = Elevator.assign_elevator(floors)
        if elevator is None:
            return Response({'error': 'No elevators available'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(elevator)
        return Response(serializer.data)


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            floor = request.data['floor']
            direction = request.data['direction']
        except KeyError:
            return Response({'error': 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)

        elevator = Elevator.get_elevator(floor, direction)
        if elevator is None:
            return Response({'error': 'No elevators available'}, status=status.HTTP_404_NOT_FOUND)

        request = Request(floor=floor, direction=direction, elevator=elevator)
        request.save()

        serializer = self.get_serializer(request)
        return Response(serializer.data)
