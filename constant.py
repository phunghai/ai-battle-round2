class Constant:
    SHIP_TYPE_CARRIER = "CV"
    SHIP_TYPE_BATTLE_SHIP = "BB"
    SHIP_TYPE_CRUISER = "CA"
    SHIP_TYPE_DESTROYER = "DD"
    SHIP_TYPE_OIL_RIG = "OR"
    SHOT_STATUS_HIT = "HIT"
    SHOT_STATUS_MISS = "MISS"
    DEFAULT_BOARD_WIDTH = 20
    DEFAULT_BOARD_HEIGHT = 8
    # session key
    SESSION_KEY_BOARD_WIDTH = "SESSION_KEY_BOARD_WIDTH"
    SESSION_KEY_BOARD_HEIGHT = "SESSION_KEY_BOARD_HEIGHT"
    SESSION_KEY_INVITE_SHIPS = "SESSION_KEY_INVITE_SHIPS"
    SESSION_KEY_AI_BOARD = "SESSION_KEY_AI_BOARD"
    SESSION_KEY_OPPONENT_BOARD = "SESSION_KEY_OPPONENT_BOARD"
    SESSION_KEY_AI_STAGE = "SESSION_KEY_AI_STAGE"

    # stage of shoot
    AI_STAGE_RANDOM_SHOOT = 1
    AI_STAGE_CIRCLE_SHOOT = 2
    AI_STAGE_LINE_SHOOT = 3
    AI_STAGE_OPPOSITE_SHOOT = 4
    AI_STAGE_SCAN_SHOOT = 5

    # value on board game
    OCEAN = "O"
    FIRE = "X"
    HIT = "*"

    # ship info: ship type is one of 5 type: CV, BB, CA, DD, OR
    SHIPS_INFO = {"CV": {"width": 4, "height": 2},
                  "BB": {"width": 4, "height": 1},
                  "CA": {"width": 3, "height": 1},
                  "DD": {"width": 2, "height": 1},
                  "OR": {"width": 2, "height": 2}}
    VERTICAL = 0
    HORIZONTAL = 1
    MY_NAME = "calisthenis"

    # direction of shoot
    SHOOT_DIRECTION_ABOVE = 0
    SHOOT_DIRECTION_RIGHT = 1
    SHOOT_DIRECTION_BOTTOM = 2
    SHOOT_DIRECTION_LEFT = 3

    DEFAULT_MINE_TYPE = 'application/json'

