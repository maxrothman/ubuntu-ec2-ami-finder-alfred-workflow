from urllib2 import urlopen
from ast import literal_eval
from feedback import Feedback
import re, sys, os, time

CACHE_FILE = "ubuntu_ec2_instances.cache"
MAX_CACHE_AGE = 60 * 60 * 24 * 7  #1 week

def get_amis():
  if not os.path.isfile(CACHE_FILE) or time.time() - os.stat(CACHE_FILE).st_mtime > MAX_CACHE_AGE:
    data = urlopen('http://cloud-images.ubuntu.com/locator/ec2/releasesTable').read()
    open(CACHE_FILE, 'w').write(data)

  return open(CACHE_FILE).read()


fb = Feedback()
query = sys.argv[1:]
data = literal_eval(get_amis())['aaData']

for item in data:
  ami = re.search('ami-[a-f0-9]{8}', item[6]).group()

  matches = 0
  for q in query:
    matches = matches + 1 if any(q in i for i in item) else matches
  if matches == len(query):
    fb.add_item(
      subtitle = ami,
      title = ' '.join(item[:5] + [item[7]]),
      arg = ami
    )

print fb