from domain.service.user_service import UserService
from domain.service.jwt_provider import JwtProvider
from domain.model.jwt_response import JwtResponse
from domain.model.refresh_jwt_request import RefreshJwtRequest
from datasource.model.user_table import UserTable
from datasource.mapper.mapper import DataMapper
import uuid
import base64

class AuthorizationService(UserService, JwtProvider):
    def __init__(self, repository):
         self.repository = repository

    def registration(self, sign_up_request):
        new_user = UserTable(id_user = uuid.uuid4(), login = sign_up_request.login, password = sign_up_request.password, count_games = 0, count_wins = 0, count_lose = 0)
        
        result = self.repository.add_user(new_user)
        
        return result

    def authorization(self, jwt_request):
        new_accessToken = None
        new_refreshToken = None
    
        user = self.repository.find_user_by_login(jwt_request.login)
        if user is not None and user.password == jwt_request.password:
            new_accessToken = self.generating_access_token(str(user.id_user))
            new_refreshToken = self.generating_refresh_token(str(user.id_user))
            
        result = JwtResponse(new_accessToken, new_refreshToken)
        
        return result 

    def get_info_user_by_id(self, id_user):
        return DataMapper.user_table_to_user(self.repository.find_user_by_id(id_user))
        
    def get_info_user_by_login(self, login_user):
        return DataMapper.user_table_to_user(self.repository.find_user_by_login(login_user))

    def refresh_access_token(self, refresh_request: RefreshJwtRequest):
        if not self.refresh_token_validation(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        user_uuid = self.get_uuid_from_token(refresh_request.refreshToken)
        
        user = self.get_info_user_by_id(user_uuid)
        
        if not user:
            raise ValueError("User not found")
        
        new_access_token = self.generating_access_token(str(user.id_user))
        return JwtResponse(new_access_token, refresh_request.refreshToken)

    def refresh_refresh_token(self, refresh_request: RefreshJwtRequest):
        if not self.refresh_token_validation(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        user_uuid = self.get_uuid_from_token(refresh_request.refreshToken)
        
        user = self.get_info_user_by_id(user_uuid)
        
        if not user:
            raise ValueError("User not found")
            
        new_refresh_token = self.generating_refresh_token(str(user.id_user))
        new_access_token = self.generating_access_token(str(user.id_user))
        return JwtResponse(new_access_token, new_refresh_token)