
from app.utils.randomize import get_random_name

def icon_image_upload(instance, filename):
    """
    Returns location to saved into. Relative to MEDIA_ROOT folder in settings.
    Location format = <executor> / <randomfilename>.
    """
    y = get_random_name()
    extension = filename.split(".")[-1]

    return f"{y}.{extension}"