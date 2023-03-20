from rest_framework import serializers
from .models import *


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("board_size", "creator", "current_turn")



class SquareSerializer(serializers.Serializer):
    username = serializers.CharField()
    class Meta:
        model = Square
        fields = ("col_id", "row_id")