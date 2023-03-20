from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

from user_handler.models import User


class LobbyView(APIView):

    def get(self, request, username):
        available_games: dict[str, dict[int, str]] = {"available_games": [{ "id": game.pk, "created_by": game.creator.username } for game in Game.get_available_game(username)]}
        available_games["unfinished_games"] = [{ "id": game.pk, "created_by": game.creator.username } for game in Game.get_unfinished_player_involved_game(username)]
        return JsonResponse(available_games)


    def post(self, request, username):        
        
        if request.data.get("method") == "new":

            board_size: int = request.data.get("board_size")
            creator: User = User.objects.get(username=username)
            serializer = GameSerializer(data={"board_size": board_size, "creator": creator.pk, "current_turn": creator.pk})

            if serializer.is_valid():
                obj = serializer.save().pk
                response_data = serializer.data
                response_data["game_id"] = obj

                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif request.data.get("method") == "join":

            id: int = request.data.get("id")
            player: User = User.objects.get(username=username)
            does_game_exist: bool = (Game.objects.filter(id=id, creator=player.pk) | Game.objects.filter(id=id, opponent=player.pk)).exists()
            if (does_game_exist):
                print("ça existe donc on ne fait que join")
                return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
            else:
                print("ici")
                Game.objects.get(pk=id).register_opponent(username)

            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)



def GameView(request, pk):
    return render(request, "tictactoe/control_panel.html", {"game_id": pk})