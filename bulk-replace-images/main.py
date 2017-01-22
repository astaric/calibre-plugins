import os

from PyQt5.QtWidgets import QAction

from calibre.ebooks.oeb.polish.cover import is_raster_image
from calibre.gui2.tweak_book.boss import Boss
from calibre.gui2.tweak_book.plugin import Tool
from calibre.gui2 import choose_dir


class BulkReplaceImagesTool(Tool):
    name = 'bulk-replace-images'

    allowed_in_toolbar = True

    allowed_in_menu = True

    def create_action(self, for_toolbar=True):
        ac = QAction("Bulk Replace Images", self.gui)
        ac.triggered.connect(self.bulk_replace)
        return ac

    def bulk_replace(self):
        dir = choose_dir(self.gui, "select dir", "select dir title")
        if not dir:
            return

        boss = self.boss
        assert isinstance(boss, Boss)

        before = self.current_container
        boss.add_savepoint("Before: Bulk Replace Images")

        book_images = {}
        for filename in self.current_container.manifest_items_of_type(is_raster_image):
            name, _ = os.path.splitext(filename)
            book_images[name] = filename

        os.chdir(dir)
        mapping = {}
        for filename in sorted((f for f in os.listdir(dir) if os.path.isfile(f)), key=os.path.getmtime):
            name, ext = os.path.splitext(filename)
            if name in book_images:
                mapping[book_images[name]] = os.path.join(dir, filename)

        for name, path in mapping.items():
            print(name, path)
            nname = os.path.basename(path)
            nname, ext = nname.rpartition('.')[0::2]
            nname = nname + '.' + ext.lower()
            self.boss.replace_requested(name, path, nname, False)

        boss.show_current_diff(to_container=before)




