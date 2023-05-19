from sqlalchemy.orm import Session

from database import engine

from serializers.action_serializer import ActionSerializer
from serializers.agency_serializer import AgencySerializer
from serializers.expectedMove_serializer import ExpectedMoveSerializer
from serializers.favorites_serializer import FavoritesSerializer
from serializers.news_serializer import NewsSerializer
from serializers.user_serializer import UserSerializer

from services.action_service import ActionService
from services.agency_service import AgencyService
from services.expectedMove_service import ExpectedMoveService
from services.favorites_services import FavoritesService
from services.news_service import NewsService
from services.user_service import UserService


session = Session(bind=engine)

userSerializer = UserSerializer(session)
actionSerializer = ActionSerializer(session)
expectedMoveSerializer = ExpectedMoveSerializer(session)
agencySerializer = AgencySerializer(session)
newsSerializer = NewsSerializer(session)
favoritesSerializer = FavoritesSerializer(session)


userService = UserService(userSerializer)
actionService = ActionService(actionSerializer)
expectedMoveService = ExpectedMoveService(expectedMoveSerializer)
agencyService = AgencyService(agencySerializer)
newsService = NewsService(newsSerializer)
favoritesService = FavoritesService(favoritesSerializer)


if __name__ == '__main__':
    pass
