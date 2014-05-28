#!/usr/bin/env python
'''
    $ pip install flickrapi
    ....
    $ FLICKR_API_KEY=mykey ./flick.py tag1[,tag2,tag3...]
'''
 
# http://www.flickr.com/services/api/flickr.photos.search.html
api_key =  '22b38b315def19e4aa077020eb33cbc6'
api_secret = 'ec2c4f409b7332dd'

 
import flickrapi
import os
import sys
import random
#api_key = os.environ['22b38b315def19e4aa077020eb33cbc6']
url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'
 
def url_for_photo(p):
    return url_template % {
        'server_id': p.get('server'),
        'farm_id': p.get('farm'),
        'photo_id': p.get('id'),
        'secret': p.get('secret'),
    }
    
 
flickr = flickrapi.FlickrAPI(api_key, api_secret)
print url_for_photo(random.choice(flickr.photos_search(tags=sys.argv[0], per_page=20)[0]))