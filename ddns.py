import requests
import json
import datetime
import argparse
import os

providers = ['porkbun', 'cloudflare']

DIRPATH = os.path.dirname(os.path.realpath(__file__))

PORKBUN_API_KEY = None
PORKBUN_API_SECRET = None
DOMAIN_NAME = None
CLOUDFLARE_TOKEN = None # api_token 
CLOUDFLARE_ZONE_ID = None
CLOUDFLARE_ACCOUNT_ID = None
CLOUDFLARE_EMAIL = None

config_file = DIRPATH +'/config.json'
assert os.path.exists(config_file), "config.json not found"

#get API key and secret from config.json
with open(config_file) as config_file:
    data = json.load(config_file)
    PORKBUN_API_KEY = data['PORKBUN_API_KEY']
    PORKBUN_API_SECRET = data['PORKBUN_API_SECRET']
    DOMAIN_NAME = data['DOMAIN']
    CLOUDFLARE_TOKEN = data['CLOUDFLARE_TOKEN']
    CLOUDFLARE_ZONE_ID = data['CLOUDFLARE_ZONE_ID']
    CLOUDFLARE_ACCOUNT_ID = data['CLOUDFLARE_ACCOUNT_ID']


# Get your current public IP address
def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    return ip

# Get A records Porkbun
def get_porkbuns_a_records():
    url = f'https://porkbun.com/api/json/v3/dns/retrieve/{DOMAIN_NAME}'
    headers = {'apikey':PORKBUN_API_KEY, 'secretapikey':PORKBUN_API_SECRET}
    response = requests.post(url, json=headers)
    records = response.json()['records']
    a_records = []
    for record in records:
        if record['type'] == 'A' and DOMAIN_NAME in record['name']  :
            a_records.append(record)
    if len(a_records) == 0:
        return None
    else:
        return a_records

# Update a Porkbun A record with the new IP
def update_porkbun_a_records_ip(new_ip, record):
     url = f'https://porkbun.com/api/json/v3/dns/edit/{DOMAIN_NAME}/{record["id"]}'
     data = {
     "secretapikey": PORKBUN_API_SECRET,
     "apikey": PORKBUN_API_KEY,
     "name": record["name"],
     "type": "A",
     "content": new_ip,
     "ttl": "300"
     }
     if(f".{DOMAIN_NAME}" in data["name"]):
         data["name"] = data["name"].replace(f".{DOMAIN_NAME}", "")
     elif (DOMAIN_NAME in data["name"]):
        data["name"] = data["name"].replace(DOMAIN_NAME, "")
     response = requests.post(url, json=data)
     if response.status_code == 200:
         print('A record updated successfully')
     else:
         print('Failed to update A record')

# Get A records from Cloudflare
def get_cloudflare_a_records():
    a_records = []
    url = f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records'
    headers = {
    'Authorization': f'Bearer {CLOUDFLARE_TOKEN}',
    }

    response = requests.request("GET", url, headers=headers)
    try:
        results = response.json()['result']
    except:
        print(response.json())
        raise Exception("Failed to get DNS records from Cloudflare")
    
    for record in results:
        if record['type'] == 'A' and DOMAIN_NAME in record['name']  :
            a_records.append(record)
    if len(a_records) == 0:
        return None
    else:
        return a_records
    pass

def get_a_records(provider):
    if args.provider == "porkbun":
        a_records = get_porkbuns_a_records()
    elif args.provider == "cloudflare":
        a_records = get_cloudflare_a_records()
    else:
        print("Invalid provider")
        return None
    
    return a_records
    

def update_cloudflare_a_records_ip(new_ip, record):
    url = f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record["id"]}'
    payload = {
        "content": new_ip,
        "name": record["name"],
        "proxied": True,
        "type": "A",
        "comment": "Last updated by DDNS " + str(datetime.datetime.now()),
        "ttl": 3600
    }
    headers = {
    'Authorization': f'Bearer {CLOUDFLARE_TOKEN}',
    }

    response = requests.request("PUT", url, json=payload, headers=headers)
    pass

def get_record_info(record, verbose):
    if(verbose):
        info = str(record)
    else:
        info = record['name'] +'\t' +record['content'] + '\t' + record['type']

    return info

def log(args, message, echo=True, timestamp=True):
    if echo:
        print(message)
    if args.log:
        if timestamp:
            timestamp = str(datetime.datetime.now()) + '\t'
        else:
            timestamp = ''
        with open(args.logf, 'a') as log_file:
            message = message.replace('\n', '\n' +timestamp)
            message = timestamp + message
            log_file.write(message + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update DNS records')
    parser.add_argument('--provider', type=str, help='DNS provider', default="cloudflare", choices=providers)
    parser.add_argument('--verbose', action='store_true', help='Show detailed record info')
    parser.add_argument('--log', action='store_true', help='Write logs to LOGF')
    parser.add_argument('--logf', type=str, help='Path to log file', default="/home/mason/documents/DDNS/ddns.log")
    parser.add_argument('--get-public-ip', action='store_true', help='Get public IP address')
    args = parser.parse_args()

    # If the log file was set, set log to True
    # if args.logf:
    #     args.log = True
    
    log(args, 'Starting update_dns.py', echo=False)
    log(args, f'Arguments: {args}', echo=False)

    if not(args.provider in providers):
        log(args, "Invalid provider")
        exit(1)

    public_ip = get_public_ip()
    log(args, f'Public IP: {public_ip}')

    if args.get_public_ip:
        print(public_ip)
        exit(0)
    
    a_records = get_a_records(args.provider)
    if a_records is None:
        log(args, 'No \'A\' records found')
        exit(1)
    log(args, f'Found {len(a_records)} \'A\' records')

    n = 1
    for record in a_records:
        info = get_record_info(record, args.verbose)
        
        if record['content'] == public_ip:
            log(args, f'{n}/{len(a_records)}.\tRecord up to date\n{info}')
        else:
            log(args, f'{n}/{len(a_records)}.\tRecord Out of date\n{info}')
            if args.provider == "porkbun":
                update_porkbun_a_records_ip(public_ip, record)
            elif args.provider == "cloudflare":
                update_cloudflare_a_records_ip(public_ip, record)
            else:
                log(args, "Invalid provider")
                exit(1)
            info = get_record_info(record, args.details)
            log(args, f'{n}/{len(a_records)}.\tRecord updated, see new record below\n{info}')
        n += 1
    
    log(args, '', echo=False, timestamp=False)