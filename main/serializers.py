from rest_framework import serializers
from django.db.models import Count
from .models import (
    Wing, Fuselage, Tail, Avionics,
    Aircraft, UsedWing, UsedFuselage, UsedTail, UsedAvionics
)


# Wing Serializer with Count
class WingSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wing
        fields = '__all__'

    def get_count(self, obj):
        return Wing.objects.filter(wing_type=obj.wing_type).count()


# Fuselage Serializer with Count
class FuselageSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Fuselage
        fields = '__all__'

    def get_count(self, obj):
        return Fuselage.objects.filter(fuselage_type=obj.fuselage_type).count()


# Tail Serializer with Count
class TailSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tail
        fields = '__all__'

    def get_count(self, obj):
        return Tail.objects.filter(tail_type=obj.tail_type).count()


# Avionics Serializer with Count
class AvionicsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Avionics
        fields = '__all__'

    def get_count(self, obj):
        return Avionics.objects.filter(avionics_type=obj.avionics_type).count()


# Aircraft Serializer with Nested Components
class AircraftSerializer(serializers.ModelSerializer):
    wing_id = WingSerializer(read_only=True)
    fuselage_id = FuselageSerializer(read_only=True)
    tail_id = TailSerializer(read_only=True)
    avionics_id = AvionicsSerializer(read_only=True)

    class Meta:
        model = Aircraft
        fields = '__all__'


# UsedWing Serializer with Count
class UsedWingSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UsedWing
        fields = '__all__'

    def get_count(self, obj):
        return UsedWing.objects.filter(wing=obj.wing).count()


# UsedFuselage Serializer with Count
class UsedFuselageSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UsedFuselage
        fields = '__all__'

    def get_count(self, obj):
        return UsedFuselage.objects.filter(fuselage=obj.fuselage).count()


# UsedTail Serializer with Count
class UsedTailSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UsedTail
        fields = '__all__'

    def get_count(self, obj):
        return UsedTail.objects.filter(tail=obj.tail).count()


# UsedAvionics Serializer with Count
class UsedAvionicsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UsedAvionics
        fields = '__all__'

    def get_count(self, obj):
        return UsedAvionics.objects.filter(avionics=obj.avionics).count()



# Shared Part Serializer for Availability
class PartAvailabilitySerializer(serializers.Serializer):
    part_type = serializers.CharField()
    total = serializers.IntegerField()
    used = serializers.IntegerField()
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        return obj['total'] - obj['used']