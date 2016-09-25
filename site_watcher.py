import file_utils
import shutil
import os
import http_utils
import time


class SiteWatcher():
    url_dir = "urls"
    html_dir = "htmls"
    old_html_dir = "old_htmls"
    report_dir = "report"

    def prepare_dirs(self):
        if os.path.exists(self.old_html_dir):
            shutil.rmtree(self.old_html_dir)

        if os.path.exists(self.html_dir):
            os.renames(self.html_dir, self.old_html_dir)

        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def get_all_urls(self):
        return file_utils.get_url_tuples(self.url_dir)

    def save_file(self, file_path, value):
        with open(file_path, 'w') as f:
            f.write(value.decode("cp1251", "ignore"))

    def get_ready_file_name(self, dir_name, file_name):
        return dir_name + '/' + file_name + '.txt'

    def download_and_save_html(self, url_dict):
        for url_tuple in url_dict.items():
            try:
                value = http_utils.get_html(url_tuple[1])
                file_path = self.get_ready_file_name(self.html_dir, url_tuple[0])
                self.save_file(file_path, value=value)
            except Exception as e:
                print(e)

    def get_report_name(self):
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        return self.report_dir + '/' + timestr + '.html'

    def add_to_report(self, report_name, link_text, link):
        with open(report_name, 'a') as f:
            f.write('<a href=' + link + '/>' + link_text + '</a>' + '<br>' + '\n')

    def save_diffs(self):
        report_name = self.get_report_name()
        url_dict = file_utils.get_url_tuples(self.url_dir, postfix='.txt')
        file_list = file_utils.get_file_names(self.html_dir)

        filtred_dict = dict([(k, url_dict[k]) for k in file_list])

        for url_tuple in filtred_dict.items():
            if not file_utils.files_are_equal(url_tuple[0], self.old_html_dir, self.html_dir):
                self.add_to_report(report_name, link_text=url_tuple[0], link=url_tuple[1])

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
        # 1.
        if url_dict is None:
            url_dict = self.get_all_urls()

        # 2,3 and 4

        self.prepare_dirs()

        self.download_and_save_html(url_dict=url_dict)
        self.save_diffs()
