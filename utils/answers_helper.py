from container import expectedMoveService


class AnswerHelper:
    @staticmethod
    def is_user_waiting_n(user_id):
        """
        Ждет ли пользователь изменения количества новостей для получения.
        :param user_id: Id пользователя.
        :return: True - да, ждет. False - нет, ждет.
        """
        return expectedMoveService.get_one_by_user_id(user_id).is_waiting_n

    @staticmethod
    def update_user_waiting_n(user_id, is_waiting_n):
        """
        Обновить количество новостей для получения.
        :param user_id: Id пользователя.
        :param is_waiting_n: Количество новостей для получения.
        """
        mapping = {
            "user_id": user_id,
            "is_waiting_n": is_waiting_n
        }
        expectedMoveService.update(mapping)

    @staticmethod
    def update_user_amount_of_read_news(user_id, amount_of_read_news):
        """
        Обновить количество прочитанных новостей.
        :param user_id: Id пользователя.
        :param amount_of_read_news: Количество прочитанных новостей.
        """
        mapping = {
            "user_id": user_id,
            "amount_of_read_news": amount_of_read_news
        }
        expectedMoveService.update(mapping)

    @staticmethod
    def format_news(news):
        """
        Отформатировать новость.
        :param news: Новость.
        :return: Отформатированная новость.
        """

        message = f"""
<b>{news.title}</b>
    
{news.text}
    
Читайте полностью: <a href="{news.url}">{news.news_agency.beauty_url}</a>
        """
        return message
