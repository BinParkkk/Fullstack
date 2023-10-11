from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, reqparse
from Global import variable_file_load, Ai_admin_variable_file_error

login = Namespace(
    name='Auth',
    description='로그인 API'
)

auth_login_request_response = login.schema_model('authLogin',{
    'properties': {
        'code' : {'type' : 'integer','description': '결과코드', 'example' : 0},
        'message' : {'type' : 'string','description': '메시지', 'example' : '성공'},
        'result': { 'type': 'object', 
            'properties': {
                 'token': {'type': 'string', 'description': '로그인 성공', 'example':'로그인 성공'}
                } 
        }
    }, 
    'type': 'object',
})

auth_login_error = login.schema_model('authLoginError',{
    'properties': {
        'code' : {'type' : 'integer', 'description': '결과코드', 'example' : 1},
        'message' : {'type' : 'string', 'description': '메시지', 'example' : '아이디 또는 비밀번호를 확인해 주세요.'},
        'result': {'type': 'object', 
            'properties': {}}
    }, 
    'type': 'object',
})

auth_variable_error = login.schema_model('authVariableError', Ai_admin_variable_file_error)

auth_login_request = reqparse.RequestParser()
auth_login_request.add_argument('id', required=True, action='append', location='headers', type=str, help='아이디')
auth_login_request.add_argument('password', required=True, action='append', location='headers', type=str, help='패스워드')
auth_login_request.add_argument('email', required=False, action='append', location='headers', type=str, help='이메일주소')

@login.route('/login')
class AuthLogin(Resource):
    @login.expect(auth_login_request)
    @login.response(200, 'Success', auth_login_request_response)
    @login.response(1, '로그인 실패', auth_login_error)
    @login.response(2, '환경변수 파일이 존재하지 않습니다.', auth_variable_error)
    def get(self):
        ''' 로그인 및 토큰 발급 '''
        # request id, password 불러오기
        id = request.args.get('id')
        password = request.args.get('password')
        email = request.args.get('email')
        
        # 변수 파일에 저장되어 있는 id, password 불러오기
        admin = variable_file_load("login")
        admin_id = admin['id']
        admin_pwd = admin['password']
        
        # 아이디, 비밀번호 확인
        if admin_id != id or admin_pwd != password:
            return make_response(jsonify({'code' : 1, 'message' : '아이디 또는 비밀번호를 확인해 주세요.', 'result' : {}}), 401)
        elif admin_id == id and admin_pwd == password:
            return make_response(jsonify({'code' : 0, 'message' : '성공', 'result' : {}}), 200)