import logging

from view.display_html import DisplayHtml


class HelpPage:
    def __init__(self):
        super().__init__()
        logging.debug('in HelpPage')
        display_html = DisplayHtml("html/help.html", "Help for Find Words", 400, 300)
        display_html.display()
