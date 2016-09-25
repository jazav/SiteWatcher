import site_watcher

if __name__ == '__main__':
    watcher = site_watcher.SiteWatcher()
    tst_dict=dict()
    tst_dict['апогода.url'] = 'http://meteoinfo.ru/hazardsbull'
    watcher.start(url_dict=tst_dict)