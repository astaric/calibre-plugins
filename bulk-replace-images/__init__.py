from calibre.customize import EditBookToolPlugin


class DemoPlugin(EditBookToolPlugin):
    name = 'Bulk Replace Images'
    version = (1, 0, 0)
    author = 'Anze Staric'
    supported_platforms = ['windows', 'osx', 'linux']
    description = 'Bulk replace images in book'
    minimum_calibre_version = (1, 46, 0)
