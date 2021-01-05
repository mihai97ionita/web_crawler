import os

from crawler.data.selectable_info import selectable_info
from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import NotFound, HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from crawler.functions.crawler_functions import crawler_and_parse, filter_by_info_selected
from crawler.functions.parse_functions import *
from crawler.functions.request_functions import *


class ServerEnvironment:
    def __init__(self):
        templates_path = os.path.join(os.path.dirname(__file__), '../../templates')
        self.jinja_env = Environment(loader=FileSystemLoader(templates_path), autoescape=True)

        self.url_map = Map([
            Rule('/', endpoint='home')
        ])

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def error_404(self):
        response = self.render_template('404.html')
        response.status_code = 404
        return response

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound:
            return self.error_404()
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def on_home(self, request):
        if is_home(request):
            return self.render_home()

        if is_submit(request):
            url = get_url_to_parse(request)
            info = get_info_to_display(request)
            if url is None or info is None or not_validate(url):
                alert_text = "Please enter a valid URL and choose information to display"
                return self.render_template('home.html', info=selectable_info, alert_text=alert_text)
            else:
                return self.render_parsed_data(url, info)

    def render_home(self):
        return self.render_template('home.html', info=selectable_info, alert_text=None)

    def render_parsed_data(self, url, selected_info):
        crawled_dict_info = crawler_and_parse(parse_page_by_url, url)
        filtered_crawled_dict_info = filter_by_info_selected(crawled_dict_info, selected_info)
        return self.render_template('crawl_info.html', info=filtered_crawled_dict_info)
