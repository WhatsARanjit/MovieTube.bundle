#!/usr/local/bin/python
import httplib, urllib, re

MOVIES_HOST = 'http://www.movietubenow.com'
MOVIES_SEARCH = '%s/index.php' % MOVIES_HOST
HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
}
INCINEMA_POST = urllib.urlencode({
  'c':'song',
  'a':'retrieve',
  'p':'{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"Score"}'
})
RE_SEARCH = r'<tr.+?>.*?</tr>'
RE_ID = r'watch\.php\?v=([a-zA-Z0-9]+)'
RE_URL = r'<a.+?>(.*?)</a>'
RE_THUMB = r'src="(.+?)"'
RE_SUMMARY = r'<h3_light class="text"></h3_light><br/><h3_light class="text">(.+?)</h3_light>'
RE_DOCS = r'(?:content|src)="(https://docs\.google\.com/file/.*?/preview)">'

# Trying pulling the URL
try:
    print "=> Accessing search URL..."
    incinema = urllib.urlopen(MOVIES_SEARCH, INCINEMA_POST, HTTP_HEADERS)
    results = re.findall(RE_SEARCH, incinema.read())

except Exception as error:
    print "Could not request search URL"
    print type(error)
    print error.args
    print error

else:
    print "=> Opening file..."
    f = open('incinema.xml', 'w')

    for result in results:
        # Try finding all the elements
        try:
            id = re.findall(RE_ID, result) 
            url = MOVIES_HOST + '/watch.php?v=' + id[0]
            title = re.findall(RE_URL, result)
            thumb = re.findall(RE_THUMB, title[0])
            summary = re.findall(RE_SUMMARY, result)
            print "==> Finding metadata for " + title[1] + "..."

            print "==> Requesting URL page..."
            params = urllib.urlencode({
                'c':'result',
                'a':'getplayerinfo',
                'p':'{"KeyWord":"' + id[0] + '"}'
            })
            video = urllib.urlopen(MOVIES_SEARCH, params, HTTP_HEADERS).read()

            # See if there is a Google Docs URL
            try:
                gdocs = re.findall(RE_DOCS, video)[0]
            except:
                gdocs = ''

        except IndexError as error:
            print id

        except Exception as error:
            print "Could not POST for clip information"
            print type(error)
            print error.args
            print error

        else:
            print "==> Setting video_url..."
            if gdocs:
                video_url = gdocs
            elif video.find('vjplayer') > -1:
                expr = r'src="(.*?)"'
                video_url = re.findall(expr, urllib.unquote(video).decode('utf8'))[0]
            elif video.find('vkplayer') > -1:
                expr = r'data="(.*?)"'
                video_url = re.findall(expr, urllib.unquote(video).decode('utf8'))[0]
            elif video.find('uplayer') > -1:
                expr = r'src="(.*?)"'
                video_url = re.findall(expr, urllib.unquote(video).decode('utf8'))[0]
            else:
                video_url = video

            data = "<item>\n\t<title>%s</title>\n\t<summary>%s</summary>\n\t<thumb>%s</thumb>\n\t<video_url>%s</video_url>\n</item>\n" % (title[1], summary[1], thumb[0], video_url)
            print "==> Writing data to XML file..."
            f.write(data)

    print "=> Closing file..."
    f.close()
