# This gets kicked off by a cron job daily
# Picks a trending topic on Twitter (takes the world and US trending, then gets the common one) then uses that tag to grab a picture off flickr
# If there is no image, then goes back through the list until it does find an image
# Saves the image in the newImage directory

import twitter
import json
import urllib
import flickrapi
import os
import sys
import random
import urllib2

CONSUMER_KEY = 'xxxxxxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OAUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OAUTH_TOKEN_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxx'

# Flickr Keys
#api_key =  'xxxxxxxxxxxxxxxxxxxx'
api_key = 'xxxxxxxxxxxxxxxxxxxxxx'
#api_secret = 'xxxxxxxxxxxxxxxx'
api_secret = 'xxxxxxxxxxxxxxxxxx'
url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'

def getTwitterTrends():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    #print twitter_api

    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977

    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    us_trends = twitter_api.trends.place(_id=US_WOE_ID)

    print json.dumps(world_trends, indent=1)
    print 
    print json.dumps(us_trends, indent=1)

    # intersection of trends
    world_trends_set = set([trend['name']
                            for trend in world_trends[0]['trends']])
    us_trends_set = set([trend['name']
                            for trend in us_trends[0]['trends']])                      
    common_trends = world_trends_set.intersection(us_trends_set)

    print 'Common Trends**********************'
    print common_trends                        

def getImage():
    # gets this image - need to randomize which image it uses
    #urllib.urlretrieve( 'http://farm3.staticflickr.com/2903/14247445822_60c0f849e1_m.jpg', 'newImage/newImage.jpg')
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    # Replace some of these call tags with some randomness
    url =  url_for_photo(random.choice(flickr.photos_search(tags='totem', per_page=2)[0]))
    
    # Download the image:
    filename = None
    print 'Downloading %s' % url
    filein = urllib2.urlopen(url)
    try:
        image = filein.read(5000000)
    except MemoryError: # I sometimes get this exception. Why ?
        return None
        
    filein.close()
        # Check it.
    if len(image)==0:
        return None  # Sometimes flickr returns nothing.
    if len(image)==5000000:
        return None  # Image too big. Discard it.        
    if image.startswith('GIF89a'):
        return None # "This image is not available" image.
    
    # Save to disk.
    if not filename:
        filename = 'newImage/newImage.jpg' #url[url.rindex('/')+1:]
    fileout = open(filename,'w+b')
    fileout.write(image)
    fileout.close()
    
    
def url_for_photo(p):
    return url_template % {
        'server_id': p.get('server'),
        'farm_id': p.get('farm'),
        'photo_id': p.get('id'),
        'secret': p.get('secret'),
    }
    
    
def main():
    print( 'main')
    getImage()

    
if __name__ == '__main__':
    main()
    