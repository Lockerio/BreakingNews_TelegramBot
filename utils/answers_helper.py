from container import expectedMoveService


class AnswerHelper:
    @staticmethod
    def is_user_waiting_n(user_id):
        return expectedMoveService.get_one_by_user_id(user_id).is_waiting_n

    @staticmethod
    def update_user_waiting_n(user_id, is_waiting_n):
        mapping = {
            "user_id": user_id,
            "is_waiting_n": is_waiting_n
        }
        expectedMoveService.update(mapping)

    @staticmethod
    def format_news(news):

        message = f"""
<b>{news.title}</b>
    
{news.text}
    
Читайте полностью: <a href="{news.url}">{news.news_agency.beauty_url}</a>
        """
        return message
