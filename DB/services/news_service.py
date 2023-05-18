from DB.serializers.news_serializer import NewsSerializer


class NewsService:
    def __init__(self, serializer: NewsSerializer):
        self.serializer = serializer

    def get_one(self, news_id):
        return self.serializer.get_one(news_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        return self.serializer.create(data)

    def update(self, data):
        news_id = data.get("id")
        news = self.get_one(news_id)
        news.title = data.get("title")
        news.text = data.get("text")
        news.url = data.get("url")
        return self.serializer.update(news)

    def delete(self, news_id):
        self.serializer.delete(news_id)