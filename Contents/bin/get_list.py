#!/usr/local/bin/python
import urllib,urllib2, re, os

CWD = '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/MovieTube.bundle/Contents/Resources'

#MOVIES_HOST = 'http://www.movietubenow.com'
MOVIES_HOST = 'http://www.movietube.cc'
MOVIES_SEARCH = '%s/index.php' % MOVIES_HOST
HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
}

RE_SEARCH = r'<tr.+?>.*?</tr>'
RE_ID = r'watch\.php\?v=([a-zA-Z0-9\-]+)'
RE_URL = r'<a.+?>(.*?)</a>'
RE_THUMB = r'src="(.+?)"'
RE_SUMMARY = r'<h3_light class="text"></h3_light><br/><h3_light class="text">(.+?)</h3_light>'
RE_DOCS = r'(?:content|src)="(https://docs\.google\.com/file/.*?/preview)">'

POST = {
  'incinema': {
      'c':'song',
      'a':'retrieve',
      'p':'{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"Score"}'
  },
  'whatsnew': {
      'c':'song',
      'a':'retrieve',
      'p':'{"Page":"1","NextToken":"","VideoYoutubeType":"English","Genere":"","Year":"","Sortby":"ReleaseDate"}'
  }
}

# Begin in Resources directory
print "=> Change directory to " + CWD + "..."
os.chdir(CWD)
print "=> Opening file..."
f = open('movietube.xml', 'w')
f.write("<?xml version=\"1.0\"?>\n<items>\n")

for section in POST:
    print "=> Starting " + section + " section..."

    # Trying pulling the URL
    try:
        print "==> Accessing search URL..."
        req = urllib2.Request(MOVIES_SEARCH, urllib.urlencode(POST[section]), HTTP_HEADERS)
        incinema = urllib2.urlopen(req)
        results = re.findall(RE_SEARCH, incinema.read())

    except Exception as error:
        print "Could not request search URL"
        print type(error)
        print error.args
        print error
        raise

    else:
        
        for result in results:
            # Try finding all the elements
            try:
                id = re.findall(RE_ID, result) 
                url = MOVIES_HOST + '/watch.php?v=' + id[0]
                title = re.findall(RE_URL, result)
                thumb = re.findall(RE_THUMB, title[0])
                summary = re.findall(RE_SUMMARY, result)
                print "===> Finding metadata for " + title[1] + "..."

                print "====> Requesting URL page..."
                params = urllib.urlencode({
                    'c':'result',
                    'a':'getplayerinfo',
                    'p':'{"KeyWord":"' + id[0] + '"}'
                })
                req2 = urllib2.Request(MOVIES_SEARCH, params, HTTP_HEADERS)
                video = urllib2.urlopen(req2).read()

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
                print "====> Setting video_url..."
                if gdocs:
                    video_url = gdocs
                    source = 'Google Docs'
                elif video.find('vjplayer') > -1:
                    expr = r'src="(https?://.*?)"'
                    video_url = re.findall(expr, urllib2.unquote(video).decode('utf8'))[0]
                    source = 'VJ Player'
                elif video.find('vkplayer') > -1:
                    expr = r'data="(https?://.*?)"'
                    video_url = re.findall(expr, urllib2.unquote(video).decode('utf8'))[0]
                    source = 'VK Player'
                elif video.find('uplayer') > -1:
                    expr = r'src="(https?://.*?)"'
                    video_url = re.findall(expr, urllib2.unquote(video).decode('utf8'))[0]
                    source = 'U Player'
                else:
                    video_url = video
                    source = 'None'

                try:
                    data = "\t<item>\n\t\t<title>%s</title>\n\t\t<summary>%s</summary>\n\t\t<thumb>%s</thumb>\n\t\t<video_url>%s</video_url>\n\t\t<source>%s</source>\n\t\t<section>%s</section>\n\t</item>\n" % (title[1], summary[1], thumb[0], video_url, source, section)
                    print "====> Writing data to XML file..."
                    f.write(data)
                except:
                    print "====> Skipping because of weird URL..."

            print "===> Done"

    print "=> Ending section " + section

print "=> Closing file..."
f.write("</items>\n")
f.close()
