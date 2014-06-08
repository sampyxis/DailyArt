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
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart




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
    url =  url_for_photo(random.choice(flickr.photos_search(tags='contestation', per_page=2)[0]))
    
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
    
    #now - kick off the processing job
    # need to change director for the local server - will put into a yaml file
    os.system("processing-java --sketch=..\..\..\..\GitHub\DailyArt\DailyArt --output=..\..\..\..\GitHub\DailyArt\DailyArtBuild --force --run")
    
    # now send the email to Tumblr
    # email set up
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    #Next, log in to the server
    server.login(user_name, user_pass)

    #Send the mail
    #msg = "\nHello!" # The /n separates the message from the headers
    #server.sendmail("you@gmail.com", "target@example.com", msg)
    # Create the container (outer) email message.
   
    msg = MIMEMultipart()
    msg['Subject'] = 'DailyArt Post'
    me = "sampyxis@gmail.com"
    msg['From'] = me
    msg['To'] = tumblr_email
    msg.preamble = '#dailyart #generative #generativeart' 

    img = MIMEImage(open('DailyArt/newImage/newImageChanged.jpg',"rb").read(), _subtype="jpeg")
    img.add_header('Content-Disposition', 'attachment; filename="newImageChanged.jpg"')
    msg.attach(img)
    
    # Assume we know that the image files are all in PNG format
    #filename = 'DailyArt/newImage/newImageChanged.jpg';
    #fp = open(filename, 'rb')
    #img = MIMEImage(fp.read(), 'jpeg')
    #fp.close()
    #msg.attach(img)
    
    # Send the email via our own SMTP server.
    #s = smtplib.SMTP('localhost')
    server.sendmail(me, tumblr_email, msg.as_string())
    server.quit()    
    
    
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
    