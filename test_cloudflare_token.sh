# Use this script to test your Cloudflare Token before using it in the DDNS script
SECRET_TOKEN=""

# Test Cloudflare Token
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer $SECRET_TOKEN" \
     -H "Content-Type:application/json"