import site_watcher

if __name__ == '__main__':
    watcher = site_watcher.SiteWatcher()
    tst_dict=dict()
    tst_dict['апогода.url'] = 'http://meteoinfo.ru/hazardsbull'
    #tst_dict['Избирательная комиссия Ставропольского края.url'] = 'http://stavizbirkom.ru'
    #tst_dict['Авиакомпания Донавиа - Новости.url'] = 'http://www.aeroflot-don.ru/news.aspx'
    #tst_dict['Агентство инвестиционного развития Ростовской области.url'] = 'http://www.ipa-don.ru/'


    watcher.start(url_dict=tst_dict)
