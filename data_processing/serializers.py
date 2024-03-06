# data_processing/serializers.py

from rest_framework import serializers

class OutcomeSerializer(serializers.Serializer):
    Player = serializers.CharField(max_length=100)
    Type = serializers.CharField(max_length=100)
    Game = serializers.IntegerField()
    Outcome = serializers.CharField(max_length=10)
