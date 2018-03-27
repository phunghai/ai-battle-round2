from random import randint
from constant import Constant
from ships import *

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

    def is_ocean(self, x, y, b):  # true if ocean
        if y < 0 or y >= Constant.DEFAULT_BOARD_HEIGHT:
            return 0
        elif x < 0 or x >= Constant.DEFAULT_BOARD_WIDTH:
            return 0
        if b[y][x] == Constant.OCEAN:
            return 1
        else:
            return 0

    def make_ship(self, ship_type):
        if ship_type == Constant.SHIP_TYPE_CARRIER:
            make_ship = Carrier()
        if ship_type == Constant.SHIP_TYPE_BATTLE_SHIP:
            make_ship = Battleship()
        if ship_type == Constant.SHIP_TYPE_CRUISER:
            make_ship = Cruiser()
        if ship_type == Constant.SHIP_TYPE_DESTROYER:
            make_ship = Destroyer()
        if ship_type == Constant.SHIP_TYPE_OIL_RIG:
            make_ship = Oilrig()

        return make_ship


    def place_ship(self, ship, board):
        is_vertical = randint(0, 1) # vertical ship if true
        occupied = True
        ship_type = ship["type"]
        ship_info = Constant.SHIPS_INFO[ship_type]
        size = ship_info["width"]
        height = ship_info["height"]
        print("is_vertical=", is_vertical)
        print("shiptype=", ship_type)

        #TODO
        if ship_type == Constant.SHIP_TYPE_CARRIER:
            make_ship = Carrier()
        if ship_type == Constant.SHIP_TYPE_BATTLE_SHIP:
            make_ship = Battleship()
        if ship_type == Constant.SHIP_TYPE_CRUISER:
            make_ship = Cruiser()
        if ship_type == Constant.SHIP_TYPE_DESTROYER:
            make_ship = Destroyer()
        if ship_type == Constant.SHIP_TYPE_OIL_RIG:
            make_ship = Oilrig()

        while occupied:
            occupied = False
            ship_x = self.random_x(is_vertical, size, height, ship_type)
            ship_y = self.random_y(is_vertical, size, height, ship_type)

            if make_ship.canPlace(ship_x, ship_y, board, is_vertical) is False:
                print('can not place', ship_x, ship_y)
                occupied = True

        print("ship_x", ship_x, "ship_y", ship_y)
        #Place ship on boards
        ship_coordinates = make_ship.getShip(ship_x, ship_y, is_vertical)

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
        if direction == 0 or direction == 1:
            return Constant.VERTICAL
        elif direction == 1 or direction == 3:
            return Constant.HORIZONAL

        return -1 #unknow

    def guess_ship_orientation(self, hit_possion):
        x_arr = []
        y_arr = []
        for postion in hit_possion:
            x_arr.append(postion[0])
            y_arr.append(postion[1])

        print(x_arr,y_arr)
        # check ascendining
        sort_x_arr_asc = sorted(x_arr, reverse=False)
        sort_x_arr_desc = sorted(x_arr, reverse=True)
        sort_y_arr_asc = sorted(y_arr, reverse=False)
        sort_y_arr_desc = sorted(y_arr, reverse=True)
        if sort_x_arr_asc == self.remove_duplicates(x_arr):
            #horizinal
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

        # x_arr = []
        # y_arr = []
        # for postion in ship_hit_possion:
        #     x_arr.append(postion[0])
        #     y_arr.append(postion[1])

        


        # print(x_arr,y_arr)
        # # check ascendining
        # sort_x_arr_asc = sorted(x_arr, reverse=False)
        # sort_x_arr_desc = sorted(x_arr, reverse=True)
        # sort_y_arr_asc = sorted(y_arr, reverse=False)
        # sort_y_arr_desc = sorted(y_arr, reverse=True)
        # if sort_x_arr_asc == self.remove_duplicates(x_arr):
        #     #horizinal
        #     return 3 #EAST
        # elif sort_x_arr_desc == self.remove_duplicates(x_arr):
        #     return 1
        # elif sort_y_arr_asc == self.remove_duplicates(y_arr):
        #     return 0
        # elif sort_y_arr_desc == self.remove_duplicates(y_arr):
        #     return 2
        # return -1

    def remove_duplicates(self, lst):
        seen = set()
        res = []
        for x in lst:
            if x not in seen:
                res.append(x)
                seen.add(x)
        return res
