import re
#import xml.etree.ElementTree as ET
from lxml import etree

NAME = 'MovieTube'
ICON = 'icon-default.png'
PREFIX = '/video/movietube'
XMLDIR = Prefs['xmldir']
HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
}

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

    oc.add(DirectoryObject(key=Callback(Section, section='incinema'), title=L('incinema')))
    oc.add(DirectoryObject(key=Callback(Section, section='whatsnew'), title=L('whatsnew')))

    return oc

##########################################################################
@route(PREFIX + '/section')
def Section(section):

    oc = ObjectContainer(title2=L(section))
    parser = etree.XMLParser(recover=True)
    xml = '%s/movietube.xml' % XMLDIR
    list = etree.parse(xml, parser=parser).getroot()

    xsection = "//items/item[section='%s']" % section
    for result in list.xpath(xsection):
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
            oc.add(VideoClipObject(
                url = url,
                title = title,
                thumb = thumb,
                summary = summary,
            ))

    oc.http_headers = HTTP_HEADERS
    return oc
