import file_utils
import shutil
import os
import http_utils
import time
import logging
import logging.config

class SiteWatcher():
    logging.config.fileConfig('logging.conf')

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
        return file_utils.get_url_tuples(walk_dir=self.url_dir, filter=".url", postfix="")

    def save_file(self, file_path, value):
        with open(file=file_path, encoding='cp1251', mode='w') as f:
            f.write(value.decode('cp1251', 'ignore'))

    def get_ready_file_name(self, dir_name, file_name):
        res = dir_name + '/' + file_name + '.txt'
        return res

    def download_and_save_html(self, url_dict):
        if url_dict is not None:
            logging.info('total urls: ' + str(len(url_dict)))

        for url_tuple in url_dict.items():
            try:
                value = http_utils.get_html(url_tuple[1])
                file_path = self.get_ready_file_name(dir_name=self.html_dir, file_name=url_tuple[0])
                self.save_file(file_path=file_path, value=value)
                logging.debug('downloaded: ' + file_path)
            except Exception as e:
                logging.error("Can't write the file: " + file_path + ": Reason: " + str(e))

    def get_report_name(self):
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        return self.report_dir + '/' + timestr + '.html'

    def add_to_report(self, report_name, link_text, link):
        with open(report_name, 'a') as f:
            f.write('<a href=' + link + '/>' + link_text + '</a>' + '<br>' + '\n')

    def save_diffs(self):
        report_name = self.get_report_name()
        url_dict = file_utils.get_url_tuples(self.url_dir, filter=".url", postfix='.txt')
        file_list = file_utils.get_file_names(self.html_dir)

        for i in file_list:
            print(i)

        filtred_dict = dict([(k, url_dict[k]) for k in file_list])

        total_diff=0

        for url_tuple in filtred_dict.items():
            file_name=url_tuple[0]
            link=url_tuple[1]
            if not file_utils.files_are_equal(file_name=file_name, old_dir=self.old_html_dir, new_dir=self.html_dir):
                logging.debug('*** files ' + file_name + ' are not equal ***')
                total_diff = total_diff + 1
                self.add_to_report(report_name, link_text=file_name, link=link)
        logging.info('total diffs: ' + str(total_diff))

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
        logging.info("---")
        logging.info("START watching")
        logging.info("---")
        # 1.
        if url_dict is None or len(url_dict) == 0:
            url_dict = self.get_all_urls()

        # 2,3 and 4

        self.prepare_dirs()

        self.download_and_save_html(url_dict=url_dict)
        self.save_diffs()
