from flask import Flask, request, jsonify, session, Response
from constant import Constant
from utils import Utils
from copy import deepcopy
from random import randint
import json as simplejson
from aishoot import AIShoot

app = Flask(__name__)
app.secret_key="my secret key"


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/invite", methods=["POST"])
def invite():
    session_id = request.headers['X-SESSION-ID']
    token = request.headers['X-TOKEN']
    # get request value from game engine

    try:
        board_width = request.json["boardWidth"]
    except Exception:
        board_width = Constant.DEFAULT_BOARD_WIDTH


    try:
        board_height = request.json["boardHeight"]
    except Exception:
        board_height = Constant.DEFAULT_BOARD_HEIGHT

    ships = request.json["ships"]

    print(type(ships), ships)
    #TODO
    session.clear()

    # store init game informations to session
    session[Constant.SESSION_KEY_BOARD_WIDTH] = board_width
    session[Constant.SESSION_KEY_BOARD_HEIGHT] = board_height
    session[Constant.SESSION_KEY_INVITE_SHIPS] = ships
    # init ai stage shoot
    session[Constant.SESSION_KEY_AI_STAGE] = 1 # Random
    session["previous_status"] = -1
    session["current_direction"] = -1
    session["ship_hitting_position"] = []
    
    js = simplejson.dumps({"message": "successful"})

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['X-SESSION-ID'] = session_id
    resp.headers['X-TOKEN'] = token
    return resp

@app.route("/place-ships", methods=["POST"])
def place_ships():
    utils = Utils()
    session_id = request.headers['X-SESSION-ID']
    token = request.headers['X-TOKEN']

    # get information from request
    player1 = request.json["player1"]
    player2 = request.json["player2"]

    # get information from session
    board_width = session[Constant.SESSION_KEY_BOARD_WIDTH]
    board_height = session[Constant.SESSION_KEY_BOARD_HEIGHT]
    ships = session[Constant.SESSION_KEY_INVITE_SHIPS]
    print(type(ships), ships)

    #init board
    #TODO
    board = []
    for x in range(Constant.DEFAULT_BOARD_HEIGHT):
        board.append([Constant.OCEAN] * Constant.DEFAULT_BOARD_WIDTH)

    # store oppnent board
    opponent_board = deepcopy(board)
    session[Constant.SESSION_KEY_OPPONENT_BOARD] = opponent_board

    ret_ships = []
    for ship in ships:
        for quantity in range(ship["quantity"]):
            ret_ship = {}
            ret_ship["type"] = ship["type"]
            ret_ship["coordinates"] = []
            shipxy = utils.place_ship(ship, board)
            board = shipxy["board"]

            ret_ship["coordinates"] = shipxy["ship_coordinates"]
            print(ret_ship)
            ret_ships.append(ret_ship)

    # store ai board in session
    session[Constant.SESSION_KEY_AI_BOARD] = board

    js = simplejson.dumps({"ships": ret_ships})

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['X-SESSION-ID'] = session_id
    resp.headers['X-TOKEN'] = token
    return resp


@app.route("/shoot", methods=["POST"])
def shoot():
    utils = Utils()
    session_id = request.headers['X-SESSION-ID']
    token = request.headers['X-TOKEN']

    # ai_board = session[Constant.SESSION_KEY_AI_BOARD]
    opponent_board = session[Constant.SESSION_KEY_OPPONENT_BOARD]
    # counter for turn in session
    turn = request.json["turn"]
    session["turn"] = turn
    aishoot = AIShoot()

    try: 
        max_shots = request.json["maxShots"]
    except Exception:
        max_shots = 1

    ret_shots = []
    for i in range(max_shots):
        ai_stage = session[Constant.SESSION_KEY_AI_STAGE]
        print("SHOOT: ai_stage before shoot", ai_stage)
        previous_status = session["previous_status"]
        # when line shot miss then change ai to circle
        # if previous_status == Constant.SHOT_STATUS_MISS and ai_stage == Constant.AI_STAGE_LINE_SHOOT:
        #     print("change from line => circle")
        #     ai_stage == Constant.AI_STAGE_CIRCLE_SHOOT
        # Hunt mode
        if ai_stage == Constant.AI_STAGE_RANDOM_SHOOT:
            shoot_info = aishoot.random_shoot(opponent_board)

            guess_pos = shoot_info["guess_pos"]
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]
            session["previous_guess_x"] = guess_x
            session["previous_guess_y"] = guess_y
        elif ai_stage == Constant.AI_STAGE_CIRCLE_SHOOT: #circle
            # based on previous hit
            ship_postion = session["hit_ship_position"]
            target_x = ship_postion[0]
            target_y = ship_postion[1]

            pos = aishoot.circle_shoot(opponent_board, target_x, target_y)
            guess_pos = pos["guess_pos"]
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]

            #direction
            session["current_direction"] = pos["direction"]

            session["previous_guess_x"] = guess_x
            session["previous_guess_y"] = guess_y
            session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_CIRCLE_SHOOT
        elif ai_stage == Constant.AI_STAGE_LINE_SHOOT: #line shoot
            ship_postion = session["hit_ship_position"]
            target_x = ship_postion[0]
            target_y = ship_postion[1]
            
            current_direction = session["current_direction"]

            shoot_info = aishoot.line_shoot(opponent_board, target_x, target_y, current_direction)
            guess_pos = shoot_info["guess_pos"]
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]

            #session[Constant.SESSION_KEY_AI_STAGE] = shoot_info["ai_stage"]
            session["current_direction"] = shoot_info["direction"]

            session["previous_guess_x"] = guess_x
            session["previous_guess_y"] = guess_y
        elif ai_stage == Constant.AI_STAGE_OPPOSITE_SHOOT:
            ship_postion = session["hit_ship_position"]
            target_x = ship_postion[0]
            target_y = ship_postion[1]

            current_direction = session["current_direction"]

            shoot_info = aishoot.opposite_shoot(opponent_board, target_x, target_y, current_direction)
            guess_pos = shoot_info["guess_pos"]
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]

            session[Constant.SESSION_KEY_AI_STAGE] = shoot_info["ai_stage"]
            session["current_direction"] = shoot_info["direction"]
            session["previous_guess_x"] = guess_x
            session["previous_guess_y"] = guess_y
        elif ai_stage == Constant.AI_STAGE_SCAN_SHOOT:
            print("SHOT: SCAN SHOOT -------------- START ")
            ship_hitting_position = session["ship_hitting_position"]
            last_hit_postion = session["hit_ship_position"]
            print(ship_hitting_position,last_hit_postion)
            guess_direction = utils.guess_ship_orientation_v1(ship_hitting_position, last_hit_postion)
            print(guess_direction)

            print(session["previous_status"])

            shoot_info = aishoot.scan_shoot_v1(opponent_board, last_hit_postion[0], last_hit_postion[1], guess_direction,
                               ship_hitting_position, session["previous_status"])
            guess_pos = shoot_info["guess_pos"]
            print(guess_pos)
            guess_x = guess_pos[0]
            guess_y = guess_pos[1]
            session[Constant.SESSION_KEY_AI_STAGE] = shoot_info["ai_stage"]
            session["current_direction"] = shoot_info["direction"]
            session["previous_guess_x"] = guess_x
            session["previous_guess_y"] = guess_y
            print("SHOT: SCAN SHOOT -------------- END ")
        print("shooted: ", guess_x, guess_y)
        print("ai_state", ai_stage)
        print(session["current_direction"])
        ret_shot = [guess_x, guess_y]
        ret_shots.append(ret_shot)

    session[Constant.SESSION_KEY_OPPONENT_BOARD] = opponent_board
    #session[Constant.SESSION_KEY_AI_BOARD] = ai_board

    js = simplejson.dumps({"coordinates" : ret_shots})

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['X-SESSION-ID'] = session_id
    resp.headers['X-TOKEN'] = token
    return resp


@app.route("/notify", methods=["POST"])
def notify():
    utils = Utils()
    session_id = request.headers['X-SESSION-ID']
    token = request.headers['X-TOKEN']

    player_id = request.json["playerId"]
    aishoot = AIShoot()
    print("Player: ", player_id)
    if player_id == Constant.MY_NAME:
        shots = request.json["shots"]

        opponent_board = session[Constant.SESSION_KEY_OPPONENT_BOARD]
        # analysis status shot
        for shot in shots:
            print(shot["coordinate"], shot["status"])
            coordinate = shot["coordinate"]
            status = shot["status"]
            session["previous_guess_x"] = coordinate[0]
            session["previous_guess_y"] = coordinate[1]

            # in case of have sunk ship
            sunk_ships = request.json["sunkShips"]

            if status == Constant.SHOT_STATUS_HIT:
                print('Good shot')
                session["previous_status"] = Constant.SHOT_STATUS_HIT
                # ship_position.extend(coordinate)
                session["hit_ship_position"] = coordinate

                session["ship_hitting_position"].append(coordinate)
                print(coordinate)
                # update HIT value into board
                opponent_board[coordinate[1]][coordinate[0]] = Constant.HIT

                # TODO determine next ai stage shoot
                ai_stage = session[Constant.SESSION_KEY_AI_STAGE]
                if ai_stage == Constant.AI_STAGE_RANDOM_SHOOT:
                    print("HIT: change random => circle")
                    session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_CIRCLE_SHOOT
                elif ai_stage == Constant.AI_STAGE_CIRCLE_SHOOT:
                    print("HIT: change circle => line")
                    session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_LINE_SHOOT
                elif ai_stage == Constant.AI_STAGE_SCAN_SHOOT:
                    # if kill ship then change shoot way else keep scan shoot
                    if len(sunk_ships) > 0:
                        print("HIT: change scan => line")
                        session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_LINE_SHOOT


                # analysis sunk ship
                # if has not sunk ship then not random
                if len(sunk_ships) > 0:
                    for sunk_ship in sunk_ships:
                        print("HIT: has sunk ship")
                        # session.pop("hit_ship_position", None)
                        # session.pop("ship_hitting_position", None)
                        session["hit_ship_position"] = []
                        session["ship_hitting_position"] = []
                        print(session["ship_hitting_position"])
                        # if ship is destroyed completely then reset ai_stage to random
                        session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_RANDOM_SHOOT

                        opponent_board = utils.update_board(sunk_ship["coordinates"], opponent_board)
                print(" HIT: ai_stage in session", session[Constant.SESSION_KEY_AI_STAGE])
            elif status == Constant.SHOT_STATUS_MISS:
                print('Oh no, miss shot. Try again')
                print(" MISS: ai_stage in session", session[Constant.SESSION_KEY_AI_STAGE])
                opponent_board[coordinate[1]][coordinate[0]] = Constant.FIRE
                session["previous_status"] = Constant.SHOT_STATUS_MISS

                ship_hitting_position = session["ship_hitting_position"]
                if len(ship_hitting_position) > 1:
                    if len(sunk_ships) == 0:
                        session[Constant.SESSION_KEY_AI_STAGE] = Constant.AI_STAGE_SCAN_SHOOT



    # return response to game engine
    js = simplejson.dumps({"message": "successful"})

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['X-SESSION-ID'] = session_id
    resp.headers['X-TOKEN'] = token
    return resp

@app.route("/game-over", methods=["POST"])
def game_over():
    return jsonify({"message": "game over !!!!"})


if __name__ == '__main__':
    app.run(debug=True)