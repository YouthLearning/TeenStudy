import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel

from ...models.accuont import User
from ...utils.path import getConfig
from ...utils.utils import to_hash


class UserModel(BaseModel):
    user_id: int
    password: str
    role: bool


route = APIRouter()


@route.post('/login', response_class=JSONResponse)
async def login(user: UserModel):
    user_id = user.user_id
    password = await to_hash(user.password)
    role = user.role
    if role:
        result = getConfig()
        if result["SUPERUSER"] != user_id or result["PASSWORD"] != password:
            result = False
    else:
        result = await User.filter(user_id=user_id, password=password).count()
    if not result:
        return {
            'status': -100,
            'msg': '登录失败，请确认用户ID和密码无误'
        }
    token = await create_token(user_id=user.user_id, role=role)
    if role:
        return {
            'status': 0,
            'msg': '登录成功',
            'data': {
                'url': "admin",
                'role': role,
                'user_id': user_id,
                'token': token
            }
        }
    else:
        return {
            'status': 0,
            'msg': '登录成功',
            'data': {
                'url': f"/home?user_id={user_id}",
                'role': role,
                'user_id': user_id,
                'token': token
            }
        }


async def get_userInfo(token: str) -> dict:
    """
    返回用户信息
    :param token: token值
    :return:
    """
    result = getConfig()
    key = result["KEY"]
    algorithm = result["ALGORITHM"]
    payload = jwt.decode(token, key, algorithms=algorithm)
    return {
        "user_id": payload.get("user_id"),
        "role": payload.get("role")
    }


def admin_authentication():
    async def inner(token: Optional[str] = Header(...)):
        result = getConfig()
        key = result["KEY"]
        algorithm = result["ALGORITHM"]
        try:
            payload = jwt.decode(token, key, algorithms=algorithm)
            if not (user_id := payload.get('user_id')):
                raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
            else:
                try:
                    role = payload.get('role')
                    if role:
                        result = getConfig()
                        if result["SUPERUSER"] != user_id:
                            result = False
                        if not result:
                            raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
                    else:
                        raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
                except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
                    raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
        except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
            raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')

    return Depends(inner)


def authentication():
    async def inner(token: Optional[str] = Header(...)):
        result = getConfig()
        key = result["KEY"]
        algorithm = result["ALGORITHM"]
        try:
            payload = jwt.decode(token, key, algorithms=algorithm)
            if not (user_id := payload.get('user_id')):
                raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
            try:
                role = payload.get('role')
                if role:
                    result = getConfig()
                    if result['SUPERUSER'] != user_id:
                        result = False
                    if not result:
                        raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
                else:
                    result = await User.filter(user_id=user_id).count()
                    if not result:
                        raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
            except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
                raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')
        except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
            raise HTTPException(status_code=400, detail='登录验证失败或已失效，请重新登录')

    return Depends(inner)


async def create_token(user_id: int, role: bool):
    result = getConfig()
    key = result["KEY"]
    time = result["TOKEN_TIME"]
    algorithm = result["ALGORITHM"]
    data = {'user_id': user_id, 'role': role,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=time)}
    return jwt.encode(data, key, algorithm=algorithm)
