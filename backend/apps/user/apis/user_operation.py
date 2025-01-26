from ninja import Router, Schema, ModelSchema, Field

router = Router()

"""
注册
"""
class RegisterOut(Schema):
    status_code: int
    message: str
    user_id: int

class RegisterSchema(Schema):
    email: str = Field(description='邮箱')
    nick_name: str = Field(description='昵称')
    password: str = Field(description='密码')
    password_repeat: str = Field(description='重复密码')

@router.post('/register', response=RegisterOut)
def register(request, payload: RegisterSchema):
    return {'status_code': 200, 'message': '注册成功', 'user_id': 1}

"""
登录 
"""
class LoginSchema(Schema):
    username: str = Field(None, alias='username')
    password: str = Field(None, alias='password')

class Out(Schema):
    token: str

@router.post('/login', response=Out, auth=None)
def login(request, data: LoginSchema):
    return {'status': 'ok', 'token': '123132'}





