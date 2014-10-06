NAME = 'MovieTube'
MOVIES_HOST = 'http://www.movietubenow.com'
MOVEIES_CINEMA = '%s/search.php?QuickSelectType=4|Score' % MOVIES_HOST
MOVIES_SEARCH = '%s/index.php' % MOVIES_HOST

HTTP_HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25'}
RE_SEARCH = Regex('(<tr.*</tr>$)')

##########################################################################
def Start():

    ObjectContainer.title1 = NAME
    HTTP.CacheTime = CACHE_1HOUR

##########################################################################
@handler('/video/movietube', NAME)
def MainMenu():

    oc = ObjectContainer()

    oc.add(DirectoryObject(key=Callback(InCinema), title=L('incinema')))

    return oc

##########################################################################
@route('/video/movietube/incinema')
def InCinema():

    Log("TEST")
    oc = ObjectContainer(title2=L('incinema'))
    req = HTTP.Request(MOVIES_SEARCH, values=dict(
        c='song',
        a='retrieve',
        p='{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"Score"}'
    ))
    #page = RE_SEARCH.search(req.content)[0]

    oc.add(EpisodeObject(
        url = 'http://www.movietubenow.com/watch.php?v=4xGNPihcAf8',
        title = 'This Is Where I Leave You (2014)'
    ))

    #for result in page.xpath("//*[@id='list_content']/table[@class='list_table']/tbody//tr"):

    #    oc.add(EpisodeObject(
    #        #url = MOVIES_HOST + result.xpath("*//a")[0].get('href')
    #        #title = result.xpath("*//a/text()")[0]
    #        url = 'http://www.movietubenow.com/watch.php?v=4xGNPihcAf8',
    #        title = 'This Is Where I Leave You (2014)'
    #    ))

    return oc
