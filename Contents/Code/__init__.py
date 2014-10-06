NAME = 'MovieTube'
MOVIES_HOST = 'http://www.movietubenow.com/'
MOVEIES_CINEMA = '%s/search.php?QuickSelectType=4|Score' % MOVIES_HOST

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
@route('/video/movietube/incinema', allow_sync=True)
def InCinema():

    oc = ObjectContainer(title2=('incinema'))
    req = HTTP.Request(MOVIES_CINEMA, values=dict(
        c = 'song',
        a = 'retrieve',
        p = '{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"Score"}'
    ))
    page = req.content
    Log(page)

    for result in page.xpath("//*[@id='list_content']/table[@class='list_table']/tbody//tr"):

        oc.add(EpisodeObject(
            #url = MOVIES_HOST + result.xpath("*//a")[0].get('href')
            #title = result.xpath("*//a/text()")[0]
            url = 'http://www.movietubenow.com/watch.php?v=4xGNPihcAf8',
            title = 'This Is Where I Leave You (2014)'
        ))

    return oc
