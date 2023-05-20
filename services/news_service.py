from serializers.news_serializer import NewsSerializer


class NewsService:
    def __init__(self, serializer: NewsSerializer):
        self.serializer = serializer

    def get_one(self, news_id):
        return self.serializer.get_one(news_id)

    def get_one_by_title(self, title):
        return self.serializer.get_one_by_title(title)

    def get_newest_agency_news(self):
        return self.get_newest_agency_news()

    def get_all(self):
        return self.serializer.get_all()

    def assert_news_create(self, data):
        if self.get_one_by_title(data["title"]):
            return False
        self.serializer.create(data)
        return True

    def update(self, data):
        news_id = data.get("id")
        news = self.get_one(news_id)
        news.title = data.get("title")
        news.text = data.get("text")
        news.url = data.get("url")
        return self.serializer.update(news)

    def delete(self, news_id):
        self.serializer.delete(news_id)
