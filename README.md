# tlsa-ovh
Script for renew TLSA records.

The script will look for your TLSA records in the specified zone name and then regenerate them with the available certificate. It's convenient especially with Let's Encrypt which obliges us to renew our certificates every 3 months.

Requirements:
* python3
* ovh-api python
* hash-slinger

Instalation:
* apt install hash-slinger python3-pip python3-setuptools python3-wheel 
* pip install ovh

Configuration:
* rename conf.ini.default in conf.ini
* replace with your value

```ini
[default]
endpoint=ovh-eu
zoneName=exemple.com
subDomains=_443._tcp.www,_443._tcp.git

[ovh-eu]
application_key=my_app_key
application_secret=my_application_secret
consumer_key=my_consumer_key
```
If you don't have credentials : https://eu.api.ovh.com/createApp/

The subDomains list, is usefull if you want create new TLSA records.

Run:
* python3 tlsa-ovh.py
