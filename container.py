from sqlalchemy.orm import Session

from database import engine
from serializers.action_serializer import ActionSerializer
from serializers.expectedMove_serializer import ExpectedMoveSerializer
from serializers.user_serializer import UserSerializer
from services.action_service import ActionService
from services.expectedMove_service import ExpectedMoveService

from services.user_service import UserService


session = Session(bind=engine)

userSerializer = UserSerializer(session)
actionSerializer = ActionSerializer(session)
expectedMoveSerializer = ExpectedMoveSerializer(session)


userService = UserService(userSerializer)
actionService = ActionService(actionSerializer)
expectedMoveService = ExpectedMoveService(expectedMoveSerializer)

if __name__ == '__main__':
    pass
