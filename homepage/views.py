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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;
        700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg mb-4">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">🏢 Коммуналка</a>
            <div class="d-flex">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/meters/">Счётчики</a>
                <a class="nav-link" href="/payments/">Платежи</a>
            </div>
        </div>
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
    <div class="mb-4">
        <h1 class="fw-bold">Главная панель</h1>
        <p class="text-muted">Управление коммунальными показаниями</p>
    </div>

    <div class="row g-4 mb-5">
        <div class="col-md-4">
            <a href="/meters/" class="text-decoration-none">
                <div class="dashboard-card bg-purple">
                    <div>
                        <h5>Счётчики</h5>
                        <p>Управление приборами учёта</p>
                    </div>
                    <div class="text-end fs-1 opacity-25">📊</div>
                </div>
            </a>
        </div>
        <div class="col-md-4">
            <a href="/payments/" class="text-decoration-none">
                <div class="dashboard-card bg-orange">
                    <div>
                        <h5>Платежи</h5>
                        <p>Расчёт стоимости услуг</p>
                    </div>
                    <div class="text-end fs-1 opacity-25">💳</div>
                </div>
            </a>
        </div>
        <div class="col-md-4">
            <a href="/admin/" class="text-decoration-none">
                <div class="dashboard-card bg-teal">
                    <div>
                        <h5>Админ-панель</h5>
                        <p>Служебные данные Django</p>
                    </div>
                    <div class="text-end fs-1 opacity-25">⚙️</div>
                </div>
            </a>
        </div>
    </div>
    """
    return HttpResponse(page("Коммунальные показания", content))
