import urllib.request
from parser import HTMLTableParser

target = 'http://tibia.wikia.com/wiki/Achievements/DPL'

# get website content
req = urllib.request.Request(url=target)
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')

# instantiate the parser and feed it
p = HTMLTableParser()
p.feed(xhtml)
#print(p.tables)

achtab = p.tables

achtab = achtab[0][1:]
achdata = []
it = 0
for achie in achtab:
    achdata.append([it] + achie[0:3])
    it+=1

print(len(achdata))
print(achdata)
