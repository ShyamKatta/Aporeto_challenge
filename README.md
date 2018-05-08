# Aporeto_challenge

Deployed link - http://contrib.us-east-2.elasticbeanstalk.com/

Rest API call - http://contrib.us-east-2.elasticbeanstalk.com/MyGitContributionsAPI?uname={GIT_Username}

Wiki page - https://github.com/ShyamKatta/Aporeto_challenge/wiki

Technical details for local run.
- Python must be installed 
- Replace host to localhost:3000, to test locally
- Need to install few additional packages before running python script

pip install requests, pip install pytz, pip install tzlocal. If running on wondows should prepend "Python -m"

Note - careful while dealing with date in python script, as the GIT displays contributions according to local date, Python date was handled to manage UTC to local time. See wiki for detailed implementation of date.
