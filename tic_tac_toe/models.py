from django.db import models
from django.db.models import Q
from user_handler.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .notifier import *


class Game(models.Model):

    board_size = models.IntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(5)])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opponent", blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    draw = models.BooleanField(default=False)
    current_turn = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_player")
   

    # Overriding Model class save() method in order to generate a new GameCell class (X times X class) at class creation
    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            super(Game, self).save(*args, **kwargs)
            self.create_board()
        else:        
            super(Game, self).save(*args, **kwargs)


    def manage_system(self, action: str, username: str) -> dict[str, str]:

        notifier: Notifier = Notifier(board_status=Game.get_board_status(pk=self.pk))

        if (action == "connect"):
            response: dict[str, str] = notifier.get_player_join_notification(username)
        elif (action == "disconnect"):
            response: dict[str, str] = notifier.get_player_leave_notification(username)
        else:
            response: dict[str, str] = notifier.get_default_notification() 

        return response

    
    def process_one_turn(self, username: str, col_id: int, row_id: int) -> dict[str, str]:
        
        notifier: Notifier = Notifier(board_status=Game.get_board_status(pk=self.pk))

        # Start game if there are two players
        if (self.opponent is None):
            response: dict[str, str] = notifier.get_waiting_opponent_notification()
        else:
            # Play the game until there is a winner
            if (self.is_finished):
                response: dict[str, str] = notifier.get_game_over_notification()
            else:
                # Check if this is the current player turn
                if (self.current_turn.username != username):
                    response: dict[str, str] = notifier.get_wrong_turn_notification()
                else:
                    # Check if the square is free to be used
                    if (self.get_square_value(col_id, row_id) != ''):
                        response: dict[str, str] = notifier.get_square_taken_notification()
                    # If all conditions are passed, the move can be registered
                    else:
                        self.update_square_value(username, col_id, row_id)
                        player_symbol: str = self.get_player_symbol(username)

                        if (self.check_if_win()):
                            self.winner = self.current_turn
                            self.save()
                            self.end_game()
                            notifier.board_status = Game.get_board_status(pk=self.pk)
                            response: dict[str, str] = notifier.get_game_winner_notification(col_id, row_id, player_symbol)
                        elif (self.check_if_draw()):
                            self.draw = True
                            self.save()
                            self.end_game()
                            notifier.board_status = Game.get_board_status(pk=self.pk)
                            response: dict[str, str] = notifier.get_game_draw_notification(col_id, row_id, player_symbol)
                        else:
                            self.next_player_turn()
                            notifier.board_status = Game.get_board_status(pk=self.pk)
                            response: dict[str, str] = notifier.get_turn_change_notification(col_id, row_id, player_symbol)

        return response



    def create_board(self) -> None:
        for row in range(self.board_size):
            for col in range(self.board_size):
                Square.objects.create(game=self, col_id=col, row_id=row, value='')



    def get_player_symbol(self, username: str) -> str:
        if (username == self.creator.username):
            player_symbol: str = 'X'
        elif (username == self.opponent.username):
            player_symbol: str = 'O'
        else:
            player_symbol: str = ''

        return player_symbol



    def register_opponent(self, username: str):
        player_to_register: User = User.objects.get(username=username)
        self.opponent = player_to_register
        self.save()
                        


    def update_square_value(self, username: str, col_id: int, row_id: int) -> None:
        player_symbol: str = self.get_player_symbol(username)
        Square.objects.filter(game=self.pk, col_id=col_id, row_id=row_id).update(value=player_symbol)



    def get_square_value(self, col_id: int, row_id: int) -> str:       
        return Square.objects.get(game=self.pk, col_id=col_id, row_id=row_id).value



    def get_column_values(self) -> list[list[str]]:
        column_values: list[list[str]] = []
        for i in range(self.board_size):
            one_column_values: list[str] = [cell["value"] for cell in Square.objects.filter(game=self.pk, col_id=i).values()]
            column_values.append(one_column_values)
        
        return column_values
    


    def get_row_values(self) -> list[list[str]]:
        row_values: list[list[str]] = []
        for i in range(self.board_size):
            one_row_values: list[str] = [cell["value"] for cell in Square.objects.filter(game=self.pk, col_id=i).values()]
            row_values.append(one_row_values)
        
        return row_values



    def get_diagonal_values(self) -> list[list[str]]:
        left_diagonal_values: list[str] = [Square.objects.get(game=self.pk, col_id=i, row_id=i).value for i in range(self.board_size)]
        right_diagonal_values: list[str] = [Square.objects.get(game=self.pk, col_id=self.board_size-1-i, row_id=i).value for i in range(self.board_size)]
        diagonal_values: list[list[str]] = [left_diagonal_values, right_diagonal_values]

        return diagonal_values



    def get_all_values(self) -> list[str]:
        all_values: list[str] = []
        all_values = [Square.objects.get(game=self.pk, col_id=j, row_id=i).value for i in range(self.board_size) for j in range(self.board_size)]
        return all_values



    def check_if_win(self) -> bool:
        
        all_values: list[list[str]] = self.get_column_values() + self.get_row_values() + self.get_diagonal_values()
        for values in all_values:
            is_not_initial_status: bool = (values[0] != '')
            is_same_value: bool = all(cell_value == values[0] for cell_value in values)
            is_win: bool = is_not_initial_status & is_same_value

            if is_win:
                return is_win

        return False



    def check_if_draw(self) -> bool:

        is_draw: bool = all(i != "" for i in self.get_all_values())
        if is_draw:
            return is_draw

        return False



    def next_player_turn(self) -> None:
        self.current_turn = self.creator if self.current_turn == self.opponent else self.opponent
        self.save()


    def end_game(self) -> None:
        self.is_finished = True
        self.save()


    @staticmethod
    def get_available_game(username: str):
        player_pk: int = User.objects.get(username=username).pk
        return Game.objects.filter(~Q(creator=player_pk), opponent=None)
    


    @staticmethod
    def get_unfinished_player_involved_game(username: str):
        player_pk: int = User.objects.get(username=username).pk
        return Game.objects.filter(creator=player_pk, is_finished=False) | Game.objects.filter(opponent=player_pk, is_finished=False)



    @staticmethod
    def get_board_status(pk: int):
        game: Game = Game.objects.get(pk=pk)
        board_status: dict[str, str] = {"creator": game.creator.username,
                                        "opponent": None if game.opponent is None else game.opponent.username,
                                        "current_player": game.current_turn.username,
                                        "is_finished": game.is_finished,
                                        "winner": None if game.winner is None else game.winner.username,
                                        "draw": game.draw,
                                        "board_size": Game.objects.get(pk=pk).board_size,
                                        "board_status": 
                                            [{"col_id": square.col_id, 
                                              "row_id": square.row_id, 
                                              "value": square.value} 
                                              for square in Square.objects.filter(game=pk)
                                        ]}
        return board_status





class Square(models.Model):

    POTENTIAL_CELL_VALUE: tuple[tuple[str, str]] = (
        ('', ''),
        ('X', 'X'),
        ('O', 'O')
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    col_id = models.IntegerField()
    row_id = models.IntegerField()
    value = models.CharField(max_length=1, choices=POTENTIAL_CELL_VALUE)