#!/usr/bin/env python
'''
    $ pip install flickrapi
    ....
    $ FLICKR_API_KEY=mykey ./flick.py tag1[,tag2,tag3...]
'''
 
# Flickr Keys
#api_key =  'xxxxxxxxxxxxxxxxxxxx'
api_key = 'xxxxxxxxxxxxxxxxxxxxxx'
#api_secret = 'xxxxxxxxxxxxxxxx'
api_secret = 'xxxxxxxxxxxxxxxxxx'

 
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
#(token, frob) = flickr.get_token_part_one(perms='write')
#flickr.get_token_part_two((token, frob))

#print flickr.photos_search( api_key = api_key, tages = 'Land')
#print url_for_photo(random.choice(flickr.photos_search(tags=sys.argv[0], per_page=20)[0]))
print url_for_photo(random.choice(flickr.photos_search(tags='Land', per_page=2)[0]))
#r = flickr.photos_search(user_id='48439369@N00', per_page='10')
#xml.etree.ElementTree.dump(r)