# Sask Wildfire Bot  
🤖 Bot to propogate #sk #wildfire information  
🔥 Data Source: https://saskatchewan.ca/fire  
⏰ Checks for updates every hour or so  
💻 Maintained by [@FeXd](https://github.com/FeXd)  
🐣 https://twitter.com/SaskWildfire  


## ⁉️ How & Why
**Sask Wildfire Bot** is a [Twitter bot](https://en.wikipedia.org/wiki/Twitter_bot) dedicated to **propogating Saskatchewan wildfire information**.  
It is written in [Python 3](https://www.python.org/) and uses the following packages:
- [urllib](https://docs.python.org/3/library/urllib.html) to pull information from the [Saskatchewan Public Safety Agency](https://saskatchewan.ca/fire)
- [pdf2image](https://github.com/Belval/pdf2image) to convert pdfs into jpg images
- [python-dotenv](https://github.com/theskumar/python-dotenv) to set environment variables from a `.env` file

_The Saskatchewan Public Safety Agency_ does a great job updating wildfire status information [here](https://www.saskpublicsafety.ca/emergencies-and-response/wildfire-status)... But most of the information including Active Wildfire Map, Current Fire Bans, Daily Fire Danger Map, and Fire Danger Map Tomorrow is stored in a _.pdf_ format.

This bot allows people to subscribe to notifications from [@SaskWildfire](https://twitter.com/SaskWildfire) for up to date wildfire information, rather than feeling the need to navigate to the [Wildfire Status]((https://www.saskpublicsafety.ca/emergencies-and-response/wildfire-status)) page and download _.pdf_ files daily.


## 💻 Dependencies & Installation
- [Python 3](https://www.python.org/) with [pip](https://pypi.org/project/pip/)
     - run `pip install -r requirements.txt`
- [Poppler](https://github.com/freedesktop/poppler)
     - run `brew install poppler` on macOS
     - (this is required for pdf conversion using pdf2image)
- Twitter Authentication Tokens via a [Twitter Developer Account](https://developer.twitter.com/)
     - Create a `.env` file with these tokens in the root of the directory
     - ([Tweepy](https://www.tweepy.org/) has good documentation on retrieving those [here](https://docs.tweepy.org/en/latest/auth_tutorial.html))
     - (`tweepy_setup.py` has also been provided to help set up tokens)
- Run Sask Wildfire main script
     - run `python main.py`

## 🐞 Bugs, Questions, & Comments
Please feel free to provide feedback through any of the below methods:
- open an [issue](https://github.com/FeXd/SaskWildfire/issues)  
- tweet [@FeXd](https://twitter.com/fexd) or [@SaskWildfire](https://twitter.com/SaskWildfire)  
- email <arlin@fexd.com>  

## 💡 Official Government Websites
This tool has been created independently and is not associated with the _Government of Saskatchewan_ or the _Saskatchewan Public Safety Agency_. Below are links to official websites for more information about wildfires in Saskatchewan:
- [https://saskatchewan.ca/fire](https://saskatchewan.ca/fire)
- [https://www.saskpublicsafety.ca/emergencies-and-response](https://www.saskpublicsafety.ca/emergencies-and-response)
- [https://www.saskpublicsafety.ca/emergencies-and-response/wildfire-status](https://www.saskpublicsafety.ca/emergencies-and-response/wildfire-status)
- [http://environment.gov.sk.ca/firefiles/activefires.pdf](http://environment.gov.sk.ca/firefiles/activefires.pdf)
- [http://environment.gov.sk.ca/firefiles/firestodate.pdf](http://environment.gov.sk.ca/firefiles/firestodate.pdf)
- [http://environment.gov.sk.ca/firefiles/MunicipalFireBans.pdf](http://environment.gov.sk.ca/firefiles/MunicipalFireBans.pdf)
- [http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/today_fwi.pdf](http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/today_fwi.pdf)
- [http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/tomorrow_fwi.pdf](http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/tomorrow_fwi.pdf)

## 📜 License
Copyright (c) 2021 Arlin Schaffel

Licensed under the MIT License, available here:
https://github.com/FeXd/SaskWildfire/blob/main/LICENSE.md
