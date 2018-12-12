from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


PAPER_ID_REGEX = '[a-zA-Z0-9:\.]+'


class PaperIdConverter(RegexConverter):
    def __init__(self, url_map):
        super(PaperIdConverter, self).__init__(url_map, PAPER_ID_REGEX)
