from rest_framework import serializers


class TrustedLocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.IntegerField(default=500)

class CheckLocationSerializer(
    serializers.Serializer
):
    latitude = serializers.FloatField()

    longitude = serializers.FloatField()