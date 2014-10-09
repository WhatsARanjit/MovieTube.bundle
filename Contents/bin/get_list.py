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

try:
    incinema = urllib.urlopen(MOVIES_SEARCH, INCINEMA_POST)
    results = re.findall(RE_SEARCH, incinema.read())
    f = open('movietube.xml', 'w')

    try:
        for result in results:
            id = re.findall(RE_ID, result) 
            url = MOVIES_HOST + '/watch.php?v=' + id[0]
            title = re.findall(RE_URL, result)
            thumb = re.findall(RE_THUMB, title[0])
            summary = re.findall(RE_SUMMARY, result)

            params = urllib.urlencode({
                'c':'result',
                'a':'getplayerinfo',
                'p':'{"KeyWord":"' + id[0] + '"}'
            })
            video = urllib.urlopen(MOVIES_SEARCH, params).read()

            video_url = video.find('vjplayer')
            print video_url

            data = "<item>\n\t<title>%s</title>\n\t<summary>%s</summary>\n\t<thumb>%s</thumb>\n\t<video_url>%s</video_url>\n</item>\n" % (title[1], summary[1], thumb[0], video)
            f.write(data)
    except:
        print id

    f.close()

except Exception as error:
    print type(error)
    print error.args
    print error
