
class Notifier:

    def __init__(self, board_status: dict[str, str]):
        self.board_status = board_status


    def add_board_status(get_notification):

        def wrapper(self, *args, **kwargs):
            notification_with_board_status = get_notification(*args, **kwargs).copy()
            notification_with_board_status["data"]["board_status"] = self.board_status
            return notification_with_board_status

        return wrapper



    def get_default_notification(self) -> dict[str, str]:
        notification = {"status": "default", "type": "game_system", "data": {"category": "unknown_action"}}
        return notification


    @add_board_status
    def get_player_join_notification(username: str) -> dict[str, str]:
        notification = {"status": "success", "type": "game_system", "data": {"message": "Websocket sucessfully connected", "category": "game_join", "username": username}}
        return notification


    @add_board_status
    def get_player_leave_notification(username: str) -> dict[str, str]:
        notification = {"status": "success", "type": "game_system", "data": {"message": "Websocket sucessfully disconnected", "category": "game_leave", "username": username}}
        return notification


    def get_waiting_opponent_notification(self) -> dict[str, str]:
        notification = {"status": "error", "type": "in_game", "data": {"category": "waiting_opponent"}}
        return notification


    def get_game_over_notification(self) -> dict[str, str]:
        notification = {"status": "error", "type": "in_game", "data": {"category": "game_over"}}
        return notification


    def get_wrong_turn_notification(self) -> dict[str, str]:
        notification = {"status": "error", "type": "in_game", "data": {"category": "wrong_turn"}}
        return notification


    def get_square_taken_notification(self) -> dict[str, str]:
        notification = {"status": "error", "type": "in_game", "data": {"category": "square_taken"}}
        return notification


    @add_board_status
    def get_game_winner_notification(col_id: int, row_id: int, player_symbol: str) -> dict[str, str]:
        notification = {"status": "success", "type": "in_game", "data": {"category": "is_winner", "col_id": col_id, "row_id": row_id, "value": player_symbol}}
        return notification


    @add_board_status
    def get_game_draw_notification(col_id: int, row_id: int, player_symbol: str) -> dict[str, str]:
        notification = {"status": "success", "type": "in_game", "data": {"category": "is_draw", "col_id": col_id, "row_id": row_id, "value": player_symbol}}
        return notification


    @add_board_status
    def get_turn_change_notification(col_id: int, row_id: int, player_symbol: str) -> dict[str, str]:
        notification = {"status": "success", "type": "in_game", "data": {"category": "turn_change", "col_id": col_id, "row_id": row_id, "value": player_symbol}}
        return notification