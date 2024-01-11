from dataclasses import dataclass
from environs import Env
import os

@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    # db_host: str          # URL-адрес базы данных
    # db_user: str          # Username пользователя базы данных
    # db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    # admin_ids: list[int]  # Список id администраторов бота

@dataclass
class Yandex:
    link: str
    lookup_method: str
    getlangs_method: str
    api_key: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    yandex: Yandex


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)
    print(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            # admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            # db_host=env('DB_HOST'),
            # db_user=env('DB_USER'),
            # db_password=env('DB_PASSWORD')
            ),
        yandex=Yandex(link=env('YANDEX_LINK'),
                      lookup_method='lookup',
                      getlangs_method='getLangs',
                      api_key=env('YANDEX_API_KEY'))
        )

config: Config = load_config('/'.join(os.path.abspath(__file__).split('/')[:-1] + ['../.env']))
script_path = os.path.abspath(__file__)
main_data_base = script_path.split('/')[:-1] + ['..'] + [config.db.database]
main_data_base = '/'.join(main_data_base)
main_link = config.yandex.link
