import logging

from view.display_html import DisplayHtml


class AboutPage:
    def __init__(self):
        super().__init__()
        logging.debug('in AboutPage')
        display_html = DisplayHtml("html/about.html", "About FindWords", 400, 300)
        display_html.display()
