import os.path
from pathlib import Path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, '.env'))


class TelegramBotConfig(object):
    TOKEN = os.environ.get('BOT_TOKEN')


class ParserConfig(object):
    HOST = 'https://bb.usurt.ru/'
    URL = 'https://bb.usurt.ru/webapps/cmsmain/webui/institution/' \
          '%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5/' \
          '?action=frameset&subaction=view&uniq=-a7wbkh'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    FILE_FORMATS = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.jpg', '.png', '.jpeg']


class SaveConfig(object):
    SAVE_PATH = Path(os.path.dirname(os.path.abspath(__file__))).joinpath('app/temp')
