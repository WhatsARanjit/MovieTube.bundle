import re

NAME = 'MovieTube'
ICON = 'icon-default.png'
PREFIX = '/video/movietube'
MOVIES_HOST = 'http://www.movietubenow.com'
MOVEIES_CINEMA = '%s/search.php?QuickSelectType=4|Score' % MOVIES_HOST
MOVIES_SEARCH = '%s/index.php' % MOVIES_HOST

HTTP_HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25'}
RE_SEARCH = r'<tr.+?>.*?</tr>'
RE_ID = r'watch\.php\?v=([a-zA-Z0-9]+)'
RE_URL = r'<a.+?>(.*?)</a>'
RE_THUMB = r'src="(.+?)"'
RE_SUMMARY = r'<h3_light class="text"></h3_light><br/><h3_light class="text">(.+?)</h3_light>'

##########################################################################
def Start():

    ObjectContainer.title1 = NAME
    HTTP.CacheTime = CACHE_1HOUR
    DirectoryObject.thumb = R(ICON)
    EpisodeObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)

##########################################################################
@handler(PREFIX, NAME, art=ART, thumb=THUMB)
def MainMenu():

    oc = ObjectContainer()

    oc.add(DirectoryObject(key=Callback(InCinema), title=L('incinema')))

    return oc

##########################################################################
@route(PREFIX + '/incinema')
def InCinema():

    oc = ObjectContainer(title2=L('incinema'))
    req = HTTP.Request(MOVIES_SEARCH, headers=HTTP_HEADERS, values=dict(
        c='song',
        a='retrieve',
        p='{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"Score"}'
    ))
    results = re.findall(RE_SEARCH, req.content)

    #oc.add(EpisodeObject(
    #    url = 'http://www.movietubenow.com/watch.php?v=4xGNPihcAf8',
    #    title = 'This Is Where I Leave You (2014)',
    #    summary = results[0]
    #))

    for result in results:

        try:
            id = re.findall(RE_ID, result) 
            url = MOVIES_HOST + '/watch.php?v=' + id[0]
            title = re.findall(RE_URL, result)
            thumb = re.findall(RE_THUMB, title[0])
            summary = re.findall(RE_SUMMARY, result)

            oc.add(VideoClipObject(
                url = url,
                title = title[1],
                thumb = thumb[0],
                summary = summary[1],
            ))
        except:
            #raise Ex.MediaNotAvailable
            Log(id)

    return oc
