import requests
import json
import sys
#imports for date conversion
import datetime
import pytz
from tzlocal import get_localzone
from pytz import timezone		# need to install pytz by running pip install pytz

#import set

inp = sys.argv
if len(inp)!=2:
	print "please input in format -> python trials.py 'Github username'"
	exit()
iter = 1
uname = inp[1]	#"harshakanamanapalli"
url = "https://api.github.com/users/"+uname+"/events?page="+str(iter)+"&per_page=100"
#data = '{  "platform": {    "login": {      "userName": "shyamkatta",      "password": "xx"    }}}'
mycounts = {}
totalcount = 0
mylist = []

from tzlocal import get_localzone
local_tz = get_localzone()
utc = pytz.timezone('UTC')
year_back_date = ((utc.localize(datetime.datetime.now()).astimezone(get_localzone()))-datetime.timedelta(days=365))
#print year_back_date
#print local_tz

final_result= {}

while(1):
	r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj:
			type = i['type']
			repo_id = i['repo']['name']
			mytuple = (type,repo_id)
			mylist.append(mytuple)
			# if type in mycounts.keys():
				# mycounts[type]+=1
			# else:
				# mycounts[type]=1
			totalcount+=1
		iter+=1
		url = "https://api.github.com/users/"+uname+"/events?page="+str(iter)+"&per_page=100"
	else:
		break

# get user npn forked repositories
iter=1
url = "https://api.github.com/search/repositories?q=user:"+uname+"&per_page=100"
#https://api.github.com/search/repositories?q=user:shyamkatta
					

# url = "api.github.com/users/"+uname+"/repos"
r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
jsonobj = r.json()
if r.status_code==200  or r.status_code == 304:
	for i in jsonobj['items']:
		repo_id = i['full_name']
		mytuple = ("user_repo",repo_id)
		mylist.append(mytuple)
		# get the created time of this repository and add it as a contribution
		utc_date = datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ")
		# add the timezone for this as UTC
		utc_date = utc.localize(utc_date)
		local_date = utc_date.astimezone(get_localzone())
		#local_date = utc_date.astimezone(timezone(local_tz))
		#print utc_date#+" is utc date"
		#print local_date#+" is local date"

		#print date.strftime('%x')
		if local_date.strftime('%x') in final_result.keys():
			final_list = final_result[local_date.strftime('%x')]
			final_list[3]+=1		# increment the pull req count of the date by 1
		elif (local_date<year_back_date):
			if year_back_date.strftime('%x') in final_result.keys():
				final_list = final_result[year_back_date.strftime('%x')]
				final_list[3]+=1
			else:
				final_result[year_back_date.strftime('%x')] = [0,0,0,1]
		else:
			final_list=[0,0,0,1]
			final_result[local_date.strftime('%x')]=final_list


# users organizations 
# https://api.github.com/users/Dogild/orgs
# assuming user would not be in >100 organizations
url = "https://api.github.com/users/"+uname+"/orgs?per_page=100"
orgs_repo_url=[]

r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
jsonObj = r.json()
if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
	for orgs in jsonObj:
		orgs_repo_url.append(orgs['repos_url'])

#print orgs_repo_url

if(len(orgs_repo_url)!=0):
	for orgs in orgs_repo_url:
		# iterate for all pages
		iter=1
		while(1):
			url = orgs+"?page="+str(iter)+"&per_page=100"
			r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
			jsonObj = r.json()
			#print url
			if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
				#print len(jsonObj)
				for i in jsonObj:
					if(not i['fork']):
						repo_id = i['full_name']
						mytuple = ("org_repo",repo_id)
						mylist.append(mytuple)
				iter+=1
			else:
				break

#print("====================================")
#print mylist
#print("====================================")
# add issues
# https://api.github.com/search/issues?q=type:apr+state:closed+author:shyamkatta&per_page=100&page=1
iter = 1
# 0-commits, 1-issues, 2-pull-requests, 3-created
# str.split('T')[0]
# date = datetime.datetime.strptime(<date_string>, "%Y-%m-%dT%H:%M:%SZ")
url = "https://api.github.com/search/issues?q=type:pr+author:"+uname+"&per_page=100"

from pytz import timezone
while(1):
	r = requests.get(url+"&page="+str(iter),auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj['items']:
			# add the timezone for this as UTC
			
			utc_date = datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ")
			utc_date = utc.localize(utc_date)
			local_date = utc_date.astimezone(get_localzone())
			#datetime_obj_local = timezone('US/Eastern').localize(date)		#local_tz
			#print datetime_obj_local.strftime("%Y-%m-%d %H:%M:%S %Z%z")+ "is changed new time "
			#print date
			#print date.replace(pytz.timezone('US/Eastern'))
			#print date.strftime('%x')

			# add pull req repo to repos collection  -> change this
			repo_url = i['repository_url']
			split = repo_url.rsplit('/')
			repo_url = '/'.join([split[-2], split[-1]])
			mytuple = ("pull_repo",repo_url)
			mylist.append(mytuple)
			if local_date.strftime('%x') in final_result.keys():
				final_list = final_result[local_date.strftime('%x')]
				final_list[2]+=1		# increment the pull req count of the date by 1
			elif (local_date<year_back_date):
				if year_back_date.strftime('%x') in final_result.keys():
					final_list = final_result[year_back_date.strftime('%x')]
					final_list[2]+=1
				else:
					final_result[year_back_date.strftime('%x')] = [0,0,1,0]
			else:
				final_list=[0,0,1,0]
				final_result[local_date.strftime('%x')]=final_list
		iter+=1
	else:
		break

#print final_result
#print "after issues"

# 0-commits, 1-issues, 2-pull-requests, 3-created
iter=1
url = "https://api.github.com/search/issues?q=type:issue+author:"+uname+"&per_page=100"
while(1):
	r = requests.get(url+"&page="+str(iter),auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj['items']:
#			date = i['created_at'].split('T')[0]
			utc_date = datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ")
			utc_date = utc.localize(utc_date)
			local_date = utc_date.astimezone(get_localzone())		
			if local_date.strftime('%x') in final_result.keys():
				final_list = final_result[local_date.strftime('%x')]
				final_list[1]+=1		# increment the pull req count of the date by 1
			elif (local_date<year_back_date):
				if year_back_date.strftime('%x') in final_result.keys():
					final_list = final_result[year_back_date.strftime('%x')]
					final_list[1]+=1
				else:
					final_result[year_back_date.strftime('%x')] = [0,1,0,0]
			else:
				final_list=[0,1,0,0]
				final_result[local_date.strftime('%x')]=final_list
		iter+=1
	else:
		break


#print final_result


# repoList = []
# for currtuple in mylist:
	# name,repoName = currtuple
	# repoList.append(repoName)

# uniqueRepoList = set(repoList)
# conflictList = []
# for currreponame in uniqueRepoList:
	# currrepouser,reponame = split(currreponame,'/')
	# repouserlist = re.search('(.*)/'+reponame)
	# if(len(repouserlist)>1):
		# conflictList.append((repouserlist))



uniqueRepoEventSet = set(mylist)
#forkset = set()
forklist = []
uniqueRepoEventList = list(uniqueRepoEventSet)
repoList =  [x[1] for x in uniqueRepoEventList]
uniqueRepoSet = set(repoList)

for repo in uniqueRepoSet:
	#event, repo = repoEvent
	url = "https://api.github.com/repos/"+repo
	r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	if r.status_code==200 or r.status_code == 304:
		jsonObj = r.json()
		if jsonObj['fork']:
			forklist.append(repo)
	
#FinalRepoEventList = list(uniqueRepoEventSet.difference(forkset))
FinalRepoEventList = []
for repoEvent in uniqueRepoEventList:
	event,repo = repoEvent
	if repo not in forklist:
		FinalRepoEventList.append(repoEvent)


#print(len(uniqueRepoEventSet))		
#print len(forkset)			
#print len(forklist)
temp_new_list = set([x[1] for x in FinalRepoEventList])
#print len(FinalRepoEventList)
#print mycounts
#print totalcount

temp_list = set([x[0] for x in  FinalRepoEventList])
# print temp_list

#uname = "harshakanamanapalli"
for i in temp_new_list:
	if (1):#i[0]=="org_repo" or i[0]=="user_repo"):
		# get the user commits from this repo
		url = "https://api.github.com/repos/"+i+"/commits?author="+uname	#:owner/:repo/
		iter=0
		while(1):
			iter+=1
			#print url+"&page="+str(iter)+"&per_page=100"
			r = requests.get(url+"&page="+str(iter)+"&per_page=100",auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
			jsonObj  = r.json()
			if (r.status_code==200 or r.status_code == 304) and (len(jsonObj)!=0):
				for res in jsonObj:
					# if res['commit']['author']['name']==uname:
					#print res['commit']['author']['date']
					utc_date = datetime.datetime.strptime(res['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
					utc_date = utc.localize(utc_date)
					local_date = utc_date.astimezone(get_localzone())
					if local_date.strftime('%x') in final_result.keys():
						final_list = final_result[local_date.strftime('%x')]
						final_list[0]+=1		# increment the pull req count of the date by 1
					elif (local_date<year_back_date):
						if year_back_date.strftime('%x') in final_result.keys():
							final_list = final_result[year_back_date.strftime('%x')]
							final_list[0]+=1
						else:
							final_result[year_back_date.strftime('%x')] = [1,0,0,0]
					else:
						final_list=[1,0,0,0]
						final_result[local_date.strftime('%x')]=final_list
			else:
				break

#print sorted(final_result.items())
formated_list=[]

for key in sorted(final_result.keys()):
	temp_list = { "date": key,  "commits":final_result[key][0], "pull_requests":final_result[key][1], "issues":final_result[key][2], "create_repo":final_result[key][3] }
	formated_list.append(temp_list)

import json
print json.dumps(formated_list)
#print formated_list
