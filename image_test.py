

from PIL import Image
import urllib2
import StringIO
from httplib2 import Http
import urllib

# retrieve image
http = Http()
request, content = http.request('http://farm3.staticflickr.com/2903/14247445822_60c0f849e1_m.jpg')
urllib.urlretrieve( 'http://farm3.staticflickr.com/2903/14247445822_60c0f849e1_m.jpg', 'newImage/newImage.jpg')

#print(StringIO.StringIO(content))
#im = Image.open(StringIO.StringIO(content))
#fname = "newImage.bmp"
#im.save(fname, "BMP")

#img = urllib2.urlopen('http://farm3.staticflickr.com/2903/14247445822_60c0f849e1_m.jpg')
#fname = "newImage.jpg"
#print(StringIO.StringIO(img))

try:
    #print(StringIO.StringIO(img))
    #im = Image.open(StringIO.StringIO(img))
    #im = Image.open(img)
    im.verify()
    #im.save(fname)
    im.show()
except Exception, e:
    print("Image is not valid")
    print(e)

#urllib2.uimg, fname)
    
    