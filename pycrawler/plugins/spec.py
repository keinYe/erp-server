
from pluggy import HookspecMarker

spec = HookspecMarker('pycrawler')


@spec
def hook_load_blueprints(app):
    """Hook for registering blueprints.

    :param app: The application object.
    """
