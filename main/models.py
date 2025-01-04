from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wing(models.Model) :
    class WingType(models.TextChoices):
        TB2 = 'TB2'
        TB3 = 'TB3'
        AKINCI = 'AKINCI'
        KIZILELMA = 'KIZILELMA'

    class Meta:
        permissions = [
            ("create_wing", "Can create a wing"),
            ("view_create_wing_page", "Can view create wing page"),
        ]
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    wing_type = models.CharField(max_length=20, choices=WingType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Fuselage(models.Model) :
    class FuselageType(models.TextChoices):
        TB2 = 'TB2'
        TB3 = 'TB3'
        AKINCI = 'AKINCI'
        KIZILELMA = 'KIZILELMA'

    class Meta:
        permissions = [
            ("create_fuselage", "Can create a fuselage"),
            ("view_create_fuselage_page", "Can view create fuselage page"),
        ]

    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fuselage_type = models.CharField(max_length=20, choices=FuselageType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Tail(models.Model) :
    class TailType(models.TextChoices):
        TB2 = 'TB2'
        TB3 = 'TB3'
        AKINCI = 'AKINCI'
        KIZILELMA = 'KIZILELMA'

    class Meta:
        permissions = [
            ("create_tail", "Can create a tail"),
            ("view_create_tail_page", "Can view create tail page"),
        ]
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tail_type = models.CharField(max_length=20, choices=TailType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Avionics(models.Model) :
    class AvionicsType(models.TextChoices):
        TB2 = 'TB2'
        TB3 = 'TB3'
        AKINCI = 'AKINCI'
        KIZILELMA = 'KIZILELMA'
    class Meta:
        permissions = [
            ("create_avionics", "Can create avionics"),
            ("view_create_avionics_page", "Can view create avionics page"),
        ]
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    avionics_type = models.CharField(max_length=20, choices=AvionicsType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Aircraft(models.Model):
    class AircraftType(models.TextChoices):
        TB2 = 'TB2'
        TB3 = 'TB3'
        AKINCI = 'AKINCI'
        KIZILELMA = 'KIZILELMA'
    class Meta:
        permissions = [
            ("create_aircraft", "Can create aircraft"),
            ("view_create_aircraft_page", "Can view create aircraft page"),
        ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    aircraft_type = models.CharField(max_length=20, choices=AircraftType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    wing_id = models.ForeignKey(Wing, on_delete=models.CASCADE)
    fuselage_id = models.ForeignKey(Fuselage, on_delete=models.CASCADE)
    tail_id = models.ForeignKey(Tail, on_delete=models.CASCADE)
    avionics_id = models.ForeignKey(Avionics, on_delete=models.CASCADE)

class UsedWing(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='used_wings')
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE, related_name='used_by_aircraft')
    aircraft_type = models.CharField(max_length=20)

    def __str__(self):
        return f"UsedWing: {self.wing.id} for Aircraft {self.aircraft.id}"


class UsedFuselage(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='used_fuselages')
    fuselage = models.ForeignKey(Fuselage, on_delete=models.CASCADE, related_name='used_by_aircraft')
    aircraft_type = models.CharField(max_length=20)

    def __str__(self):
        return f"UsedFuselage: {self.fuselage.id} for Aircraft {self.aircraft.id}"


class UsedTail(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='used_tails')
    tail = models.ForeignKey(Tail, on_delete=models.CASCADE, related_name='used_by_aircraft')
    aircraft_type = models.CharField(max_length=20)

    def __str__(self):
        return f"UsedTail: {self.tail.id} for Aircraft {self.aircraft.id}"


class UsedAvionics(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='used_avionics')
    avionics = models.ForeignKey(Avionics, on_delete=models.CASCADE, related_name='used_by_aircraft')
    aircraft_type = models.CharField(max_length=20)

    def __str__(self):
        return f"UsedAvionics: {self.avionics.id} for Aircraft {self.aircraft.id}"