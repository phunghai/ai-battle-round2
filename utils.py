from random import randint
from constant import Constant
from models import Carrier, Battleship, Cruiser, Destroyer, Oilrig


class Utils:
    def random_y(self, is_vertical, size, height, ship_type):
        if is_vertical == Constant.VERTICAL:
            if ship_type == Constant.SHIP_TYPE_CARRIER  or ship_type == Constant.SHIP_TYPE_OIL_RIG:
                return randint(0, Constant.DEFAULT_BOARD_HEIGHT - size)
            else:
                return randint(0, Constant.DEFAULT_BOARD_HEIGHT - 1)
        else:
            if ship_type == Constant.SHIP_TYPE_CARRIER  or ship_type == Constant.SHIP_TYPE_OIL_RIG :
                return randint(height - 1, Constant.DEFAULT_BOARD_HEIGHT - height)
            else:
                return randint(0, Constant.DEFAULT_BOARD_HEIGHT - size)


    def random_x(self, is_vertical, size, height, ship_type):
        if is_vertical == Constant.VERTICAL:
            if ship_type == Constant.SHIP_TYPE_CARRIER or ship_type == Constant.SHIP_TYPE_OIL_RIG:
                return randint(height - 1 , Constant.DEFAULT_BOARD_WIDTH - 1)
            else:
                return randint(0, Constant.DEFAULT_BOARD_WIDTH - size)
        else:
            if ship_type == Constant.SHIP_TYPE_CARRIER or ship_type == Constant.SHIP_TYPE_OIL_RIG:
                return randint(0 , Constant.DEFAULT_BOARD_WIDTH - size)
            else:
                return randint(size - 1, Constant.DEFAULT_BOARD_WIDTH - 1)

    def is_ocean(self, x, y, board):  # true if ocean
        if y < 0 or y >= Constant.DEFAULT_BOARD_HEIGHT:
            return 0
        elif x < 0 or x >= Constant.DEFAULT_BOARD_WIDTH:
            return 0

        if board[y][x] == Constant.OCEAN:
            return 1
        else:
            return 0

    def make_ship(self, ship_type):
        if ship_type == Constant.SHIP_TYPE_CARRIER:
            make_ship = Carrier()
        elif ship_type == Constant.SHIP_TYPE_BATTLE_SHIP:
            make_ship = Battleship()
        elif ship_type == Constant.SHIP_TYPE_CRUISER:
            make_ship = Cruiser()
        elif ship_type == Constant.SHIP_TYPE_DESTROYER:
            make_ship = Destroyer()
        elif ship_type == Constant.SHIP_TYPE_OIL_RIG:
            make_ship = Oilrig()
        else:
            make_ship = Carrier()

        return make_ship

    def place_ship(self, ship, board):
        """
        Placing a ship on game board
        :param ship:
        :param board:
        :return:
        """
        is_vertical = randint(0, 1) # vertical ship if true
        occupied = True
        ship_type = ship["type"]
        ship_info = Constant.SHIPS_INFO[ship_type]
        size = ship_info["width"]
        height = ship_info["height"]

        # making new ship based on ship type
        ship = self.make_ship(ship_type)

        ship_x = 0
        ship_y = 0
        while occupied:
            occupied = False
            ship_x = self.random_x(is_vertical, size, height, ship_type)
            ship_y = self.random_y(is_vertical, size, height, ship_type)

            if ship.can_place(ship_x, ship_y, board, is_vertical) is False:
                print('can not place', ship_x, ship_y)
                occupied = True

        print("ship_x", ship_x, "ship_y", ship_y)
        # place ship on game board
        ship_coordinates = ship.get_ship(ship_x, ship_y, is_vertical)

        for ship_coordinate in ship_coordinates:
            board[ship_coordinate[1]][ship_coordinate[0]] = ship_type

        print(board)
        return {"ship_coordinates": ship_coordinates, "board": board, "is_vertical": is_vertical}

    def update_board(self, ship_coordinates, board):
        # uppdate HIT in board
        for coordinate in ship_coordinates:
            x = coordinate[0]
            y = coordinate[1]
            board[y][x] = Constant.HIT

        return board

    def check_ship_orientation(self, direction):
        if direction == Constant.SHOOT_DIRECTION_ABOVE or direction == Constant.SHOOT_DIRECTION_RIGHT:
            return Constant.VERTICAL
        elif direction == Constant.SHOOT_DIRECTION_RIGHT or direction == Constant.SHOOT_DIRECTION_LEFT:
            return Constant.HORIZONTAL

        return -1 #unknow

    def guess_ship_orientation(self, hit_position):
        x_arr = []
        y_arr = []
        for position in hit_position:
            x_arr.append(position[0])
            y_arr.append(position[1])

        # check ascendining
        sort_x_arr_asc = sorted(x_arr, reverse=False)
        sort_x_arr_desc = sorted(x_arr, reverse=True)
        sort_y_arr_asc = sorted(y_arr, reverse=False)
        sort_y_arr_desc = sorted(y_arr, reverse=True)
        if sort_x_arr_asc == self.remove_duplicates(x_arr):
            # horizintal
            return 3 #EAST
        elif sort_x_arr_desc == self.remove_duplicates(x_arr):
            return 1
        elif sort_y_arr_asc == self.remove_duplicates(y_arr):
            return 0
        elif sort_y_arr_desc == self.remove_duplicates(y_arr):
            return 2
        return -1

    def guess_ship_orientation_v1(self, ship_hit_possion, last_hit_position):
        previous_hit = ship_hit_possion[len(ship_hit_possion) - 2]

        if last_hit_position[0] < previous_hit[0] and last_hit_position[1] == previous_hit[1]:
            return 3
        elif last_hit_position[0] > previous_hit[0] and last_hit_position[1] == previous_hit[1]:
            return 1
        elif last_hit_position[1] > previous_hit[1] and last_hit_position[0] == previous_hit[0]:
            return 2
        elif last_hit_position[1] < previous_hit[1] and last_hit_position[0] == previous_hit[0]:
            return 0

        return -1

    def remove_duplicates(self, lst):
        seen = set()
        res = []
        for x in lst:
            if x not in seen:
                res.append(x)
                seen.add(x)
        return res
