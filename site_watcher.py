import file_utils
import shutil
import os


class SiteWatcher():
    url_dir = "urls"
    html_dir = "htmls"
    old_html_dir = "old_htmls"
    diff_dir = "diffs"
    old_diff_dir = "old_diffs"

    def start(self, url_dict=None):
        """
        !!!WARNING: url_dict must be Pair<<name>,<url>>

        1. If url_dict is None we collect all urls from url_dir files to url_dict: ['File name', 'url']
        2. Delete old_html_dir
        3. Delete old_diff_dir and rename diff_dir to old_diff_dir
        4. Rename html_dir to old_html_dir
        5. Loop for all url_dict items to download html from sites to files in html_dir ("File name".html)
        6. Loop for every new html file to compare new htmls (html_dir) and old htmls (old_html_dir)
        7. Write diff in diff_dir like a plain text
        """
        #1.
        if url_dict is None:
            url_dict = file_utils.get_files_names(self.url_dir)
            print(url_dict)

        if os.path.exists(self.old_html_dir):
            shutil.rmtree(self.old_html_dir)
        if os.path.exists(self.old_diff_dir):
            shutil.rmtree(self.old_diff_dir)
        os.renames(self.html_dir, self.old_html_dir)


