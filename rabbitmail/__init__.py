import site

from .conf import rel
site.addpackage(rel(), "apps.pth", known_paths=set())
