import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from channels.auth import login


class GameConsumer(WebsocketConsumer):

    def connect(self):

        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = "tictactoe_%s" % self.game_id

        async_to_sync(self.channel_layer.group_add)(self.game_group_name, self.channel_name)

        self.accept()

    

    def disconnect(self, close_code):
        
        response = Game.objects.get(id=self.game_id).manage_system("disconnect", self.scope["user"].username)
        self.send_message("all", response, "game_message")

        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )



    def receive(self, text_data):

        json_data = json.loads(text_data)
        message_category = json_data["message_category"]
        username = json_data["username"]
        
        if (message_category == "management"):
            
            async_to_sync(login)(self.scope, User.objects.get(username=username))
            self.scope["session"].save()

            response = Game.objects.get(id=self.game_id).manage_system("connect", self.scope["user"].username)
            self.send_message("all", response, "game_message")


        elif (message_category == "game"):
            col_id = json_data["col_id"]
            row_id = json_data["row_id"]
            response = Game.objects.get(id=self.game_id).process_one_turn(username, col_id, row_id)
            
            if (response["status"] == "error"):
                self.send_message("one", response)
            else:
                self.send_message("all", response, "game_message")
    

    def send_message(self, action_type: str, response: dict[str, str], message_type: str=""):
        if (action_type == "one"):
            self.send(text_data=json.dumps(response))

        elif (action_type == "all"):
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    "type": message_type,
                    "response": response
                }
            )


    def game_message(self, event):
        response = event["response"]
        self.send(text_data=json.dumps(response))