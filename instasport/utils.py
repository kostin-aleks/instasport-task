"""

"""


def slugify_name(cls, name):
    """
    slugify name and check unique value
    """
    slug = slugify(name, to_lower=True)
    while cls.objects.filter(slug=slug).count():
        slug += '-1'
    return slug
