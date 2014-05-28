#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import datetime,random,urllib2,re

def getInterestingFlickrImage(filename=None):
    ''' Returns a random "interesting" image from Flickr.com.
        The image is saved in current directory.
        
        In case the image is not valid (eg.photo not available, etc.)
        the image is not saved and None is returned.
    
        Input:
            filename (string): An optional filename.
                 If filename is not provided, a name will be automatically provided.
            None
        
        Output:
            (string) Name of the file.
                     None if the image is not available.
    '''
    # Get a random "interesting" page from Flickr:
    print 'Getting a random "interesting" Flickr page...'
    # Choose a random date between the beginning of flickr and yesterday.
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    flickrStart = datetime.datetime(2004,7,1)
    nbOfDays = (yesterday-flickrStart).days
    randomDay = flickrStart + datetime.timedelta(days=random.randint(0,nbOfDays))
    # Get a random page for this date.
    url = 'http://flickr.com/explore/interesting/%s/page%d/' % (randomDay.strftime('%Y/%m/%d'),random.randint(1,20))
    urlfile = urllib2.urlopen(url)
    html = urlfile.read(500000)
    urlfile.close()
    print(url)
    
    # Extract images URLs from this page
    re_imageurl = re.compile('src="(http://farm\d+.static.flickr.com/\d+/\d+_\w+_m.jpg)"',re.IGNORECASE|re.DOTALL)
    
    urls = re_imageurl.findall(html)
    if len(urls)==0:
        raise ValueError,"Oops... could not find images URL in this page. Either Flickr has problem, or the website has changed."
    urls = [url.replace('_m.jpg','_o.jpg') for url in urls]
    
    # Choose a random image
    url = random.choice(urls)

    # Download the image:        
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
        filename = url[url.rindex('/')+1:]
    fileout = open(filename,'w+b')
    fileout.write(image)
    fileout.close()
    
    return filename

if __name__ == '__main__':
    print getInterestingFlickrImage()