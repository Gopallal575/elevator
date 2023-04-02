from django.db import models


class Elevator(models.Model):
    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'
    DIRECTION_CHOICES = [
        (DIRECTION_UP, 'Up'),
        (DIRECTION_DOWN, 'Down'),
    ]

    name = models.CharField(max_length=50, unique=True)
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES, default=DIRECTION_UP)
    current_floor = models.PositiveIntegerField(default=1)
    is_operational = models.BooleanField(default=True)

    @classmethod
    def assign_elevator(cls, floors):
        available_elevators = cls.objects.filter(is_operational=True)
        if not available_elevators.exists():
            return None

        min_distance = None
        selected_elevator = None
        for elevator in available_elevators:
            distance = abs(elevator.current_floor - floors[0])
            for floor in floors[1:]:
                distance += abs(elevator.current_floor - floor)
            if min_distance is None or distance < min_distance:
                min_distance = distance
                selected_elevator = elevator

        return selected_elevator

    @classmethod
    def get_elevator(cls, floor, direction):
        available_elevators = cls.objects.filter(is_operational=True)
        if not available_elevators.exists():
            return None

        elevator = None
        min_distance = None
        for e in available_elevators:
            if (e.direction == direction and e.current_floor <= floor) or \
                    (e.direction != direction and e.current_floor >= floor):
                distance = abs(e.current_floor - floor)
                if min_distance is None or
