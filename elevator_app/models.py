from django.db import models

class Elevator(models.Model):
    id = models.IntegerField(primary_key=True)
    current_floor = models.IntegerField(default=0)
    direction = models.CharField(max_length=10, default="up")
    is_operational = models.BooleanField(default=True)

    def __str__(self):
        return f"Elevator {self.id}"

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
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    elevator = e

        return elevator

    def move(self):
        if self.direction == "up":
            self.current_floor += 1
        else:
            self.current_floor -= 1

        if self.current_floor == 0:
            self.direction = "up"
        elif self.current_floor == 9:
            self.direction = "down"

        self.save()
