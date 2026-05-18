import os
import pathlib
import re

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")
django.setup()

from django.conf import settings
from django.urls import NoReverseMatch, reverse


def main():
    project_root = pathlib.Path(settings.BASE_DIR).parent
    frontend_root = project_root / "frontend"
    template_root = frontend_root / "templates"
    template_paths = list(template_root.rglob("*.html"))

    url_re = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
    static_re = re.compile(r"{%\s*static\s+['\"]([^'\"]+)['\"]")

    missing_urls = set()
    missing_static = set()

    for p in template_paths:
        txt = p.read_text(encoding="utf-8", errors="ignore")

        for name in url_re.findall(txt):
            try:
                reverse(name)
            except NoReverseMatch as e:
                msg = str(e)
                if "is not a valid view function or pattern name" in msg:
                    missing_urls.add(f"{name} in {p.relative_to(project_root)}")

        for asset in static_re.findall(txt):
            if not (frontend_root / "static" / asset).exists():
                missing_static.add(f"{asset} in {p.relative_to(project_root)}")

    print(f"MISSING_URLS {len(missing_urls)}")
    for x in sorted(missing_urls):
        print(x)

    print(f"MISSING_STATIC {len(missing_static)}")
    for x in sorted(missing_static):
        print(x)


if __name__ == "__main__":
    main()
