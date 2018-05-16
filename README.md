# Aporeto_challenge

Deployed link - http://git-contribution.us-east-2.elasticbeanstalk.com/

Rest API call - http://git-contribution.us-east-2.elasticbeanstalk.com/MyGitContributionsAPI?uname={GIT_Username}&access_code={Access Code of user}

Wiki page - https://github.com/ShyamKatta/Aporeto_challenge/wiki

Technical details for local run.
- Python must be installed 
- Replace host to localhost:3000, to test locally
- Need to install few additional packages before running python script

pip install requests, pip install pytz, pip install tzlocal. If running on windows should prepend "Python -m"

Navigation - A user needs to authorize with access to his repositories, on successful approval, user gets a chance to enter a git hub user id and date(optional). If user enters his/her GitHub user id, user would be able to see all contributions including private repos. If a user tries to check contributions for different user, the queried user's public contributions will be displayed.

However, the access token is not stored in any session/ database. Instead, generated from access code. The access code is prone to expire soon, so it is recommended to navigate from home page for complete contributions of self. Else, public contributions will be shown upon token expiry.
At times due to same request being sent, there might be 304 error(https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304). Hence, it is **_"recommended to navigate to home page and reauthorize from begining to see all contributions of yourself, including private/public"_**

Note - careful while dealing with date in python script, as the GIT displays contributions according to local date, Python date was handled to manage UTC to local time. See wiki for detailed implementation of date.
