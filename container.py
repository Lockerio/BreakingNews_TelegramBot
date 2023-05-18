from sqlalchemy.orm import Session

from database import engine
from serializers.action_serializer import ActionSerializer
from serializers.user_serializer import UserSerializer
from services.action_service import ActionService

from services.user_service import UserService


session = Session(bind=engine)

userSerializer = UserSerializer(session)
actionSerializer = ActionSerializer(session)


userService = UserService(userSerializer)
actionService = ActionService(actionSerializer)

if __name__ == '__main__':
    pass
