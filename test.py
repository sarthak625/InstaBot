import urllib2
url = "https://s-media-cache-ak0.pinimg.com/originals/19/a3/a3/19a3a3f32d8601abe0cf7dad0b49293a.jpg"

f = urllib2.urlopen(url)
file_name = url.split('/')[-1]
with open(file_name, "wb") as code:
    code.write(f.read())