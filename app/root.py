import app
import config
from app.web_parser import Parser

parser = Parser()

print(parser.get_content(config.Parser.URL)[0]['name'])
