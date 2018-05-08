import requests
import json
import sys
#imports for date conversion
import datetime
import pytz
from tzlocal import get_localzone
from pytz import timezone		# need to install pytz by running pip install pytz

inp = sys.argv
if len(inp)!=2:
	print "please input in format -> python trials.py 'Github username'"
	exit()
iter = 1
uname = inp[1]	#"harshakanamanapalli"

mycounts = {}
totalcount = 0
mylist = []
final_result= {}

from tzlocal import get_localzone
local_tz = get_localzone()
utc = pytz.timezone('UTC')
year_back_date = ((utc.localize(datetime.datetime.now()).astimezone(get_localzone()))-datetime.timedelta(days=365))

# Fetch all 300 events for the requested user through github API
url = "https://api.github.com/users/"+uname+"/events?page="+str(iter)+"&per_page=100"
while(1):
	r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj:
			type = i['type']
			repo_id = i['repo']['name']
			mytuple = (type,repo_id)
			mylist.append(mytuple)
			totalcount+=1
		iter+=1
		url = "https://api.github.com/users/"+uname+"/events?page="+str(iter)+"&per_page=100"
	else:
		break

# Fetch user personal repositories, public 
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


# Fetch user organizations 
# https://api.github.com/users/Dogild/orgs
# assuming user would not be in >100 organizations, we do not iterate through pages as we did in previous API calls
url = "https://api.github.com/users/"+uname+"/orgs?per_page=100"
orgs_repo_url=[]

r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
jsonObj = r.json()
if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
	for orgs in jsonObj:
		orgs_repo_url.append(orgs['repos_url'])

# If there are organizations for user, iterate through each organization repositories and add them to repos array
if(len(orgs_repo_url)!=0):
	for orgs in orgs_repo_url:
		# iterate for all pages
		iter=1
		while(1):
			url = orgs+"?page="+str(iter)+"&per_page=100"
			r = requests.get(url,auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
			jsonObj = r.json()
			if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
				for i in jsonObj:
					if(not i['fork']):
						repo_id = i['full_name']
						mytuple = ("org_repo",repo_id)
						mylist.append(mytuple)
				iter+=1
			else:
				break

# The following notations will be used when storing in the dictionary
# 0-commits, 1-issues, 2-pull-requests, 3-created

# Fetch issues of user which are pull requests, add to contributions if the repo is not forked
iter = 1
url = "https://api.github.com/search/issues?q=type:pr+author:"+uname+"&per_page=100"

while(1):
	r = requests.get(url+"&page="+str(iter),auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj['items']:
			# add the timezone for this as UTC
			utc_date = datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ")
			utc_date = utc.localize(utc_date)
			local_date = utc_date.astimezone(get_localzone())
			# add pull req repo to repos collection
			repo_url = i['repository_url']
			split = repo_url.rsplit('/')
			repo_url = '/'.join([split[-2], split[-1]])
			mytuple = ("pull_repo",repo_url)
			mylist.append(mytuple)
			# if the date of contribution is older than 1 year, add it to date exactly one year behind, same logic followed in sub sequent similar calculations
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

# Fetch issues of user which are issues, add to contributions if the repo is not forked
iter=1
url = "https://api.github.com/search/issues?q=type:issue+author:"+uname+"&per_page=100"
while(1):
	r = requests.get(url+"&page="+str(iter),auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
	jsonObj  = r.json()
	if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
		for i in jsonObj['items']:
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

uniqueRepoEventSet = set(mylist)
forklist = []
uniqueRepoEventList = list(uniqueRepoEventSet)
repoList =  [x[1] for x in uniqueRepoEventList]
uniqueRepoSet = set(repoList)

# get uniques repos, to prevent duplicate API calling on same repo
for repo in uniqueRepoSet:
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

temp_new_list = set([x[1] for x in FinalRepoEventList])
temp_list = set([x[0] for x in  FinalRepoEventList])

# for the unique repos obtained earlier, fetch all commits as contributions if the commit is performed by current user 
for i in temp_new_list:
	if (1):#i[0]=="org_repo" or i[0]=="user_repo"):
		# get the user commits from this repo
		url = "https://api.github.com/repos/"+i+"/commits?author="+uname	#:owner/:repo/
		iter=0
		while(1):
			iter+=1
			r = requests.get(url+"&page="+str(iter)+"&per_page=100",auth = ('shyamkatta','f49cb7f4e110672f4ddc22657b4886f04dad2e40'),headers={"Content-Type": "application/json"})
			jsonObj  = r.json()
			if (r.status_code==200 or r.status_code == 304) and (len(jsonObj)!=0):
				for res in jsonObj:
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

formated_list=[]

# Convert the same to JSON compatible strings
for key in sorted(final_result.keys()):
	temp_list = { "date": key,  "commits":final_result[key][0], "pull_requests":final_result[key][1], "issues":final_result[key][2], "create_repo":final_result[key][3] }
	formated_list.append(temp_list)

# Convert to JSON format and print the same, Node applciation will consume this printed json from stdout 
import json
print json.dumps(formated_list)
