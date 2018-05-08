import requests

uname="shyamkatta"
url = "https://api.github.com/search/issues?q=type:pr+author:"+uname+"&per_page=2"

r = requests.get(url+"&page=1",auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})#('shyamkatta','shyam1993'),headers={"Content-Type": "application/json"})
jsonObj  = r.json()
if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
	url = jsonObj['items'][0]['repository_url']
	print url
	split = url.rsplit('/')
	print '/'.join([split[-2], split[-1]])
else:
	print "failure" # add the timezone for this as UTC
	