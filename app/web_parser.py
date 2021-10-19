import requests
from bs4 import BeautifulSoup
from config import ParserConfig


class Parser:
    def _get_html(self, url):
        html = requests.get(url, headers=ParserConfig.HEADERS)
        if self._server_is_respond(html):
            return html
        else:
            raise ConnectionError('Status code = {code}'.format(code=html.status_code))

    def _create_url(self, text):
        if self._url_for_file(text):
            return text  # nothing to change, url is for file (full url)
        else:
            return ParserConfig.HOST + text  # adding HOSTNAME

    @staticmethod
    def _server_is_respond(html):
        return True if html.status_code == 200 else False

    @staticmethod
    def _url_for_file(url):
        return True if 'https://' in url else False  # directories url not contains https:// (starts with /webapps)

    def get_content(self, url):
        try:
            soup = BeautifulSoup(self._get_html(url).text, 'html.parser')
        except ConnectionError:
            return "Can't Parse!"

        table = soup.find('table', attrs={'class': 'inventory sortable $wrappingTableClass'})
        table_body = table.find('tbody')
        lines = table_body.find_all('tr')
        lines_list = list()

        for line in lines:
            lines_list.append(
                {
                    'name': line.find('a').get_text(strip=True),
                    'link': self._create_url(line.find('a').get('href')),
                    'format': self._define_format(line.find('a').get_text(strip=True))
                }
            )
        return lines_list

    @staticmethod
    def _define_format(name) -> str:
        for format in ParserConfig.FILE_FORMATS:
            if format in name:
                return format
        return 'directory'
