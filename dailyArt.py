# This gets kicked off by a cron job daily
# Picks a trending topic on Twitter (takes the world and US trending, then gets the common one) then uses that tag to grab a picture off flickr
# If there is no image, then goes back through the list until it does find an image
# Saves the image in the newImage directory

import twitter
import json
import urllib

CONSUMER_KEY = 'CiUUz9NABupYbIkPikPOI0UD7'
CONSUMER_SECRET = 'uWlnaxYbpx78hxzBbple3JZD6wvGmVxSdLayRhImqK1MWVtJdi'
OAUTH_TOKEN = '14630801-NQj7KzMd9bb97aBKpx4zzVj9KV0KPj8svj0HyJBse'
OAUTH_TOKEN_SECRET = 'BClcN1uDSlELw3ZFdQ4FppMCfpHH99ptyRyy5t8IjpPS5'

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
    urllib.urlretrieve( 'http://farm3.staticflickr.com/2903/14247445822_60c0f849e1_m.jpg', 'newImage/newImage.jpg')
    
#def main():
#    print( 'main')

    
#if __name__ == '__main__':
#    main()
    