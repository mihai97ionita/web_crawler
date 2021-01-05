import validators


def is_home(request):
    return request.method == "GET"


def is_submit(request):
    return 'bbsubmit' in request.form and request.method == 'POST'


def get_url_to_parse(request):
    if "url" in request.form:
        url = request.form["url"]
        return url
    else:
        return None


def get_info_to_display(request):
    info = []
    for i in request.form:
        if i.startswith("info_"):
            info.append(request.form[i])
    if not info:
        return None
    else:
        return info


def not_validate(url):
    if not validators.url(url):
        return True
    else:
        return False
