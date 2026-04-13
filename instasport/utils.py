"""

"""

from slugify import slugify


def slugify_name(cls, name):
    """
    slugify name and check unique value
    """
    slug = slugify(name, lowercase=True)
    while cls.objects.filter(slug=slug).count():
        slug += '-1'
    return slug
