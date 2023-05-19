from container import agencyService


def fill_db():
    agencies = [
        {
            "name": "Байкал Daily",
            "description": "Новости Бурятии и Улан-Удэ в реальном времени.",
            "beauty_url": "baikal-daily.ru"
        },
        {
            "name": "IRK.RU",
            "description": "Новости Иркутска.",
            "beauty_url": "irk.ru"
        },
        {
            "name": "Norilsk city",
            "description": "ОФИЦИАЛЬНЫЙ САЙТ ГОРОДА НОРИЛЬСКА.",
            "beauty_url": "norilsk-city.ru"
        },
    ]

    for agency in agencies:
        agencyService.create(agency)


if __name__ == '__main__':
    fill_db()
