import requests

# Enter your Porkbun API key and secret here
API_KEY = 'pk1_0dbedc4ceb8178ddc7e781d20f055d65157e62719a5ba56708c924791e76e530'
API_SECRET = 'sk1_eeb4bf79938b780c89f1928a1db4d4fdba133b4b7e2f3d7a8e301c4adf68952d'

# Enter your domain name and A record name here
DOMAIN_NAME = 'dill.digital'

# Get your current public IP address
def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    return ip

# Get the current A record IP from Porkbun DNS
def get_current_a_record():
    url = f'https://porkbun.com/api/json/v3/dns/retrieve/{DOMAIN_NAME}'
    headers = {'apikey':API_KEY, 'secretapikey':API_SECRET}
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

# U date the A record IP in Porkbun DNS
def update_a_record_ip(new_ip, record):
     url = f'https://porkbun.com/api/json/v3/dns/edit/{DOMAIN_NAME}/{record["id"]}'
     data = {
     "secretapikey": API_SECRET,
     "apikey": API_KEY,
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

# Main script
if __name__ == '__main__':
    a_records = get_current_a_record()    
    public_ip = get_public_ip()

    if a_records is None:
        print('No records found')
    for record in a_records:
        if record['content'] == public_ip:
            print('A record is already up to date')
        else:
            print(f'A record is outdated. Updating to {public_ip}')
            update_a_record_ip(public_ip, record)