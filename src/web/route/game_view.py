from flask import Blueprint, render_template, request, current_app, jsonify

from flask_jwt_extended import get_jwt_identity
import json
import uuid

from web.mapper.mapper import WebMapper
from datasource.service.authorization_service import AuthorizationService

game_view = Blueprint('game_view', __name__)

@game_view.route('/get_user_uuid')
@AuthorizationService.access_token_validation()
def get_user_uuid():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    return jsonify(current_user=jwt_identity["uuid_user"]), 200
    
@game_view.route('/list_games')
def list_games():
    return render_template('list_games.html')
    
@game_view.route('/get_list_games', methods=['get'])
@AuthorizationService.access_token_validation()
def get_list_games():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    
    service = current_app.config["container"].service
    
    result = service.get_list_id_games_for_user(current_user)
    
    return jsonify(list_games=result), 200
        
@game_view.route('/game/<id_game>', methods=["GET"])
def game(id_game):
    id_game = uuid.UUID(id_game)
    service = current_app.config["container"].service
        
    status_game = service.get_status_game(id_game)
    
    if status_game in ["waiting players", "move X", "move O"]:
        return render_template('game.html')
    else:
        return render_template('end_game.html', result_game = status_game)
        
@game_view.route('/game_info/<id_game>', methods=['get', 'post'])
@AuthorizationService.access_token_validation()
def game_info(id_game):
    id_game = uuid.UUID(id_game)
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service
    

    if request.method == "POST":
        i = request.json.get("i", None)
        j = request.json.get("j", None)

        if i is None or j is None:
            return jsonify({"error": "Invalid move"}), 400
        
        service.make_move(current_user, id_game, i, j)
        
        return jsonify({"result": "OK"}), 200
        
    
    this_game = service.get_game(id_game)
    web_game = WebMapper.current_game_to_web_current_game(this_game)

    icon_user = "uninitialized"
    if web_game.creator.id_user == current_user:
        icon_user = web_game.type_creator
    else:
        icon_user = "X" if web_game.type_creator == "O" else "O"
        
    if web_game.enemy is not None:
        web_game.enemy.password = ""
        web_game.enemy = web_game.enemy.__dict__
    web_game.field = web_game.field.__dict__
    web_game.creator.password = ""
    web_game.creator = web_game.creator.__dict__

    return jsonify({"game": web_game.__dict__, "type_player": icon_user}), 200      

@game_view.route('/join_game/<id_game>')
@AuthorizationService.access_token_validation()
def join_game(id_game):
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service
    
    result_join = service.join_to_game(current_user, id_game)

    if result_join:
        return jsonify({"new_url": "/game/" + id_game}), 200 
    else:
        return jsonify({"new_url": "/list_games"}), 200 
    
@game_view.route('/new_game')
def new_game():
    return render_template('new_game.html')
    
@game_view.route('/create_new_game/<is_online>')
@AuthorizationService.access_token_validation()
def create_new_game(is_online):
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service
    
    bool_is_online = False
    
    if is_online.lower() == 'true':
        bool_is_online = True
    
    new_id_game = service.create_game(current_user, bool_is_online)
    
    if new_id_game:
        return jsonify({"new_url": "/game/" + str(new_id_game)}), 200 
    else:
        return jsonify({"new_url": "/list_games"}), 200 
    
@game_view.route('/profile/<id_user>')
def profile(id_user):
    
    return render_template('profile.html', id_user = id_user)
    
@game_view.route('/profile_info/<id_user>')
@AuthorizationService.access_token_validation()
def profile_info(id_user):
    service = current_app.config["container"].service
    
    user = service.get_user_info(id_user)
    web_user = WebMapper.user_to_user_authenticator(user)
    web_user.password = ""
    
    return jsonify({"user_info": web_user.__dict__}), 200
    
    
    
    
@game_view.route('/history_games')
def history_games():
    return render_template('history_games.html')
    
@game_view.route('/get_history_games')
@AuthorizationService.access_token_validation()
def get_history_games():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    
    service = current_app.config["container"].service
    
    result = service.get_history_games_for_user(current_user)
    
    return jsonify(list_games=result), 200    

    
    
@game_view.route('/list_leaders')
def list_leaders():
    return render_template('list_leaders.html')
    
@game_view.route('/get_list_leaders/<count_leaders>')
@AuthorizationService.access_token_validation()
def get_list_leaders(count_leaders):
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    current_user = uuid.UUID(jwt_identity["uuid_user"])
    
    service = current_app.config["container"].service
    
    result = service.get_list_leaders(count_leaders)
    
    return jsonify(list_leaders=result), 200    