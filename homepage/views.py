from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Единый HTML-каркас для всех страниц проекта."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav mb-3 px-3 pt-3">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/meters/">Счётчики</a>
        <a class="nav-link" href="/payments/">Платежи</a>
    </nav>
    <main class="container pb-5">
        {content}
    </main>
</body>
</html>"""


def page_not_found(request, exception):
    """Страница 404. Вызывается Django автоматически при DEBUG = False."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )


def index(request):
    content = """
    <h1 class="display-4">Коммунальные показания</h1>
    <p class="lead">Сервис учёта коммунальных показаний.</p>
    <p>Основные разделы:</p>
    <a href="/meters/" class="btn btn-primary me-2">Счётчики</a>
    <a href="/payments/" class="btn btn-secondary">Платежи</a>
    """
    return HttpResponse(page("Коммунальные показания", content))
