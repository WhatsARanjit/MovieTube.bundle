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

    return oc
