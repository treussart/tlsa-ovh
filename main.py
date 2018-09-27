#!/usr/bin/env python3
import configparser
import subprocess
import ovh
import os


def set_records(list_tlsa, zoneName):
    for value in list_tlsa:
        # usage 2 for SMTP and IMAP else 0
        port, proto, subDomain = value['subDomain'].replace('_','').split(".")
        if subDomain == 'mail' or subDomain == 'smtp' or subDomain == 'imap':
            cmd = "tlsa --create --only-rr --protocol " + proto + \
                  " --port " + port + " --usage 3 --selector 0 "\
                  + subDomain + "." + zoneName
        else:
            cmd = "tlsa --create --only-rr --protocol " + proto + \
                  " --port " + port + " --usage 0 --selector 0 "\
                  + subDomain + "." + zoneName
        exitcode, output = subprocess.getstatusoutput(cmd)
        if exitcode:
            print("Error: " + output)
            exit(exitcode)
        target = ""
        for line in output.splitlines():
            if line.startswith("_"):
                start = line.find("TLSA")
                end = line.__len__()
                target = line[start + 5:end]
                if not target:
                    print("Error: Target null for " + line)
                    exit(1)
        if value['id'] == 0:
            client.post('/domain/zone/{zoneName}/record'.format(zoneName=zoneName),
                        fieldType="TLSA", subDomain=value['subDomain'], target=target)
        else:
            client.put('/domain/zone/{zoneName}/record/{id}'.format(zoneName=zoneName, id=value['id']), target=target)


# execute only if run as a script
if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    config = configparser.ConfigParser()
    config.read(current_path + 'conf.ini')
    endpoint = config['default']['endpoint']
    zoneName = config['default']['zoneName']
    list_subDomain = config['default']['subDomains'].split(",")

    # Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
    # to get your credentials
    client = ovh.Client(
        endpoint=endpoint,
        application_key=config[endpoint]['application_key'],
        application_secret=config[endpoint]['application_secret'],
        consumer_key=config[endpoint]['consumer_key'],
    )
    results = client.get("/domain/zone/{zoneName}/record".format(zoneName=zoneName))
    list_tlsa = []
    list_tlsa_subDomains = []

    for i in results:
        result = client.get('/domain/zone/{zoneName}/record/{id}'.format(zoneName=zoneName, id=i))
        if result["fieldType"] == "TLSA":
            list_tlsa.append(result)
            list_tlsa_subDomains.append(result['subDomain'])

    diff_subDomains = set(list_subDomain).difference(list_tlsa_subDomains)
    list_diff_subDomains = []
    for item in diff_subDomains:
        list_diff_subDomains.append({'id': 0, 'subDomain': item})

    set_records(list_tlsa, zoneName)
    set_records(list_diff_subDomains, zoneName)
    exit(0)
