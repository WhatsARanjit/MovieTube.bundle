import re
#import xml.etree.ElementTree as ET
from lxml import etree

NAME = 'MovieTube'
ICON = 'icon-default.png'
PREFIX = '/video/movietube'
XMLDIR = '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/MovieTube.bundle/Contents/Resources'

##########################################################################
def Start():

    ObjectContainer.title1 = NAME
    HTTP.CacheTime = CACHE_1HOUR
    DirectoryObject.thumb = R(ICON)
    EpisodeObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)

##########################################################################
@handler(PREFIX, NAME, thumb=ICON)
def MainMenu():

    oc = ObjectContainer()

    oc.add(DirectoryObject(key=Callback(InCinema), title=L('incinema')))

    return oc

##########################################################################
@route(PREFIX + '/incinema')
def InCinema():

    oc = ObjectContainer(title2=L('incinema'))
    parser = etree.XMLParser(recover=True)
    xml = '%s/incinema.xml' % XMLDIR
    list = etree.parse(xml, parser=parser).getroot()

    for result in list.xpath("//items/item"):
        try:
            title = result.xpath("./title/text()")[0]
            url = result.xpath("./video_url/text()")[0]
            thumb = result.xpath("./thumb/text()")[0]
            summary = result.xpath("./summary/text()")[0]

        except IndexError:
            Log.Debug(url)

        except Exception as error:
            Log.Exception(error)

        else:
            oc.add(EpisodeObject(
                title = title,
                url = url,
                thumb = thumb,
                summary = summary,
            ))

    return oc
