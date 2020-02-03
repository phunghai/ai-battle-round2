from constant import Constant


class BaseShip:
	def __init__(self):
		self.num_col = Constant.DEFAULT_BOARD_WIDTH
		self.num_row = Constant.DEFAULT_BOARD_HEIGHT
		
	def can_push(self, pos_x, pos_y, board):
		if pos_x < 0 or pos_x >= self.num_col:
			return False
		elif pos_y < 0 or pos_y >= self.num_row:
			return False
		if board[pos_y][pos_x] == Constant.OCEAN:
			return True
		return False
		
	def can_place(self, start_x, start_y, board, orientation_type=Constant.HORIZONTAL):
		ship = self.get_ship(start_x, start_y, orientation_type)
		
		for i in range(len(ship)):
			pos_x = ship[i][0]
			pos_y = ship[i][1]
			if self.can_push(pos_x, pos_y, board) is False:
				print("can not push", pos_x, pos_y)
				return False
			else:
				print("CAN PUSH", pos_x, pos_y)

		return True


class Carrier(BaseShip):
	def __init__(self):
		BaseShip.__init__(self)

	def get_ship(self, start_x, start_y, orientation):
		if orientation == Constant.VERTICAL:
			return [
				[start_x,start_y],
				[start_x, start_y + 1],
				[start_x - 1, start_y + 1],
				[start_x, start_y + 2],
				[start_x, start_y + 3]
			]
		elif orientation == Constant.HORIZONTAL:
			return [
				[start_x, start_y],
				[start_x + 1, start_y],
				[start_x + 1, start_y - 1],
				[start_x + 2, start_y],
				[start_x + 3, start_y]
			]


class Battleship(BaseShip):
	def __init__(self):
		BaseShip.__init__(self)

	def get_ship(self, start_x, start_y, orientation):
		if orientation == Constant.VERTICAL:
			return [
				[start_x, start_y],
				[start_x, start_y + 1],
				[start_x, start_y + 2],
				[start_x, start_y + 3]
			]
		elif orientation == Constant.HORIZONTAL:
			return [
				[start_x, start_y],
				[start_x + 1, start_y],
				[start_x + 2, start_y],
				[start_x + 3, start_y]
			]


class Oilrig(BaseShip):
	def __init__(self):
		BaseShip.__init__(self)

	def get_ship(self, start_x, start_y, orientation):
		return [
				[start_x, start_y],
				[start_x, start_y + 1],
				[start_x - 1, start_y],
				[start_x - 1, start_y + 1]]


class Destroyer(BaseShip):
	def __init__(self):
		BaseShip.__init__(self)

	def get_ship(self, start_x, start_y, orientation):
		if orientation == Constant.VERTICAL:
			return [
				[start_x, start_y],
				[start_x, start_y + 1]
			]
		elif orientation == Constant.HORIZONTAL:
			return [
				[start_x, start_y],
				[start_x + 1, start_y]
			]


class Cruiser(BaseShip):
	def __init__(self):
		BaseShip.__init__(self)

	def get_ship(self, start_x, start_y, orientation):
		if orientation == Constant.VERTICAL:
			return [
				[start_x, start_y],
				[start_x, start_y + 1],
				[start_x, start_y + 2]
			]
		elif orientation == Constant.HORIZONTAL:
			return [
				[start_x, start_y],
				[start_x + 1, start_y],
				[start_x + 2, start_y]
			]			