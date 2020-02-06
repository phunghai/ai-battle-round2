from random import randint

from constant import Constant
from utils import Utils


class AIShoot:
    def random_shoot(self, board):
        utils = Utils()
        guess_x = randint(0, Constant.DEFAULT_BOARD_WIDTH - 1)
        guess_y = randint(0, Constant.DEFAULT_BOARD_HEIGHT - 1)
        while not utils.is_ocean(guess_x, guess_y, board):
            guess_x = randint(0, Constant.DEFAULT_BOARD_WIDTH - 1)
            guess_y = randint(0, Constant.DEFAULT_BOARD_HEIGHT - 1)
        guess_pos = [guess_x, guess_y]
        return {"guess_pos": guess_pos, "direction": -1, "ai_stage": Constant.AI_STAGE_RANDOM_SHOOT}

    def circle_shoot(self, board, start_x, start_y):
        utils = Utils()
        # 0: above, 1: right, 2: bottom, 3: left
        directions = [Constant.SHOOT_DIRECTION_ABOVE, Constant.SHOOT_DIRECTION_RIGHT,
                      Constant.SHOOT_DIRECTION_BOTTOM, Constant.SHOOT_DIRECTION_LEFT]

        if start_x == 0:
            directions.remove(Constant.SHOOT_DIRECTION_LEFT)  # can not shot at left side
        elif not utils.is_ocean(start_x - 1, start_y, board):
            directions.remove(Constant.SHOOT_DIRECTION_LEFT)

        if start_x == Constant.DEFAULT_BOARD_WIDTH - 1:
            directions.remove(Constant.SHOOT_DIRECTION_RIGHT)
        elif not utils.is_ocean(start_x + 1, start_y, board):
            directions.remove(Constant.SHOOT_DIRECTION_RIGHT)

        if start_y == 0:
            directions.remove(Constant.SHOOT_DIRECTION_ABOVE)
        elif not utils.is_ocean(start_x, start_y - 1, board):
            directions.remove(Constant.SHOOT_DIRECTION_ABOVE)

        if start_y == Constant.DEFAULT_BOARD_HEIGHT - 1:
            directions.remove(Constant.SHOOT_DIRECTION_BOTTOM)
        elif not utils.is_ocean(start_x, start_y + 1, board):
            directions.remove(Constant.SHOOT_DIRECTION_BOTTOM)

        direction = -1
        guess_x = start_x
        guess_y = start_y

        if directions:
            guess_spot = randint(0, len(directions) - 1)
            direction = directions[guess_spot]

        # base on shoot direction to guess next position
        if direction == Constant.SHOOT_DIRECTION_ABOVE:
            guess_y = start_y - 1
        elif direction == Constant.SHOOT_DIRECTION_RIGHT:
            guess_x = start_x + 1
        elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
            guess_y = start_y + 1
        elif direction == Constant.SHOOT_DIRECTION_LEFT:
            guess_x = start_x - 1

        if not utils.is_ocean(guess_x, guess_y, board):
            shoot_info = self.random_shoot(board)
            return {"guess_pos": shoot_info["guess_pos"], "direction": shoot_info["direction"],
                    "ai_stage": Constant.AI_STAGE_RANDOM_SHOOT}

        return {"guess_pos": [guess_x, guess_y], "direction": direction}

    def line_shoot(self, board, start_x, start_y, direction):  # checkeds
        utils = Utils()
        guess_x = start_x
        guess_y = start_y

        if direction == Constant.SHOOT_DIRECTION_ABOVE:
            guess_y = start_y - 1
        elif direction == Constant.SHOOT_DIRECTION_RIGHT:
            guess_x = start_x + 1
        elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
            guess_y = start_y + 1
        elif direction == Constant.SHOOT_DIRECTION_LEFT:
            guess_x = start_x - 1

        if guess_x < 0 or guess_x > Constant.DEFAULT_BOARD_WIDTH \
                or guess_y < 0 or guess_y > Constant.DEFAULT_BOARD_HEIGHT:
            shoot_info = self.random_shoot(board)
            return {"guess_pos": shoot_info["guess_pos"], "direction": shoot_info["direction"],
                    "ai_stage": shoot_info["ai_stage"]}
        elif not utils.is_ocean(guess_x, guess_y, board):
            shoot_info = self.circle_shoot(board, start_x, start_y)
            return {"guess_pos": shoot_info["guess_pos"], "direction": shoot_info["direction"],
                    "ai_stage": Constant.AI_STAGE_CIRCLE_SHOOT}

        guess_pos = [guess_x, guess_y]
        return {"guess_pos": guess_pos, "direction": direction, "ai_stage": 4}

    def opposite_shoot(self, board, start_x, start_y, direction):
        guess_x = 0
        guess_y = 0

        line_x = start_x
        line_y = start_y

        if direction == Constant.SHOOT_DIRECTION_ABOVE:
            guess_y = start_y + 1
            line_y += 1
        elif direction == Constant.SHOOT_DIRECTION_RIGHT:
            guess_x = start_x - 1
            line_x -= 1
        elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
            guess_y = start_y - 1
            line_y -= 1
        elif direction == Constant.SHOOT_DIRECTION_LEFT:
            guess_x = start_x + 1
            line_x += 1

        if guess_x < 0 or guess_x > Constant.DEFAULT_BOARD_WIDTH \
                or guess_y < 0 or guess_y > Constant.DEFAULT_BOARD_HEIGHT:
            guess_pos = self.random_shoot(board)
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]
        elif board[guess_y][guess_x] == Constant.FIRE:
            guess_pos = self.random_shoot(board)
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]

        return [guess_x, guess_y]

    def scan_shoot_v1(self, board, last_hit_x, last_hit_y, direction, ship_hitting_postion, hit_status):
        utils = Utils()
        guess_x = last_hit_x
        guess_y = last_hit_y

        last_hit_len = len(ship_hitting_postion)
        if hit_status == Constant.SHOT_STATUS_HIT:
            guess_x, guess_y = self._scan_shoot_for_hit_success(last_hit_x, last_hit_y, last_hit_len, direction)
        else:
            # shoot opposite
            guess_x, guess_y = self._scan_shoot_for_hit_fail(last_hit_x, last_hit_y, last_hit_len, direction)

        if guess_x < 0 or guess_x > Constant.DEFAULT_BOARD_WIDTH \
                or guess_y < 0 or guess_y > Constant.DEFAULT_BOARD_HEIGHT:
            shoot_info = self.random_shoot(board)
            return {
                "guess_pos": shoot_info["guess_pos"],
                "direction": shoot_info["direction"],
                "ai_stage": shoot_info["ai_stage"]
            }
        elif not utils.is_ocean(guess_x, guess_y, board):
            shoot_info = self.circle_shoot(board, last_hit_x, last_hit_y)
            return {
                "guess_pos": shoot_info["guess_pos"],
                "direction": shoot_info["direction"],
                "ai_stage": Constant.AI_STAGE_CIRCLE_SHOOT
            }

        guess_pos = [guess_x, guess_y]
        return {"guess_pos": guess_pos, "direction": direction, "ai_stage": Constant.AI_STAGE_SCAN_SHOOT}

    def _scan_shoot_for_hit_success(self, last_hit_x, last_hit_y, last_hit_len, direction):
        """ Guess new position for next shoot after hit success"""
        guess_x = last_hit_x
        guess_y = last_hit_y
        if last_hit_len < 4:
            if direction == Constant.SHOOT_DIRECTION_ABOVE:
                guess_y = last_hit_y - 1
            elif direction == Constant.SHOOT_DIRECTION_RIGHT:
                guess_x = last_hit_x + 1
            elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
                guess_y = last_hit_y + 1
            elif direction == Constant.SHOOT_DIRECTION_LEFT:
                guess_x = last_hit_x - 1
        return guess_x, guess_y

    def _scan_shoot_for_hit_fail(self, last_hit_x, last_hit_y, last_hit_len, direction):
        """ Guess new position for next shoot after hit failure"""
        guess_x = last_hit_x
        guess_y = last_hit_y

        if last_hit_len < 4:
            if direction == Constant.SHOOT_DIRECTION_ABOVE:
                guess_y = last_hit_y + last_hit_len
            elif direction == Constant.SHOOT_DIRECTION_RIGHT:
                guess_x = last_hit_x - last_hit_len
            elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
                guess_y = last_hit_y - last_hit_len
            elif direction == Constant.SHOOT_DIRECTION_LEFT:
                guess_x = last_hit_x + last_hit_len
        elif last_hit_len == 4:  # CV
            if direction == Constant.SHOOT_DIRECTION_ABOVE:
                guess_x = last_hit_x - 1
                guess_y = last_hit_y + 1
            elif direction == Constant.SHOOT_DIRECTION_RIGHT:
                guess_x = last_hit_x - 2
                guess_y = last_hit_y - 1
            elif direction == Constant.SHOOT_DIRECTION_BOTTOM:
                guess_x = last_hit_x - 1
                guess_y = last_hit_y - 2
            elif direction == Constant.SHOOT_DIRECTION_LEFT:
                guess_x = last_hit_x + 1
                guess_y = last_hit_y - 1
        return guess_x, guess_y
