import requests
import json
import sys

#INPUTS REQUIRED:

#Create and manage access keys - https://docs.prismacloud.io/en/classic/cspm-admin-guide/manage-prisma-cloud-administrators/create-access-keys#idb225a52a-85ea-4b0c-9d69-d2dfca250e16

#username = Access key ID
#password = Secret key
#prismaid = Prisma Cloud tenant ID
#prisma_base_api_url = the root API URL for your Prisma Cloud stack - see https://pan.dev/prisma-cloud/api/cspm/api-urls/

username = ''
password = ''
prismaid = ''
prisma_base_api_url = 'https://api0.prismacloud.io'

#Login and retrieve an auth token

#https://pan.dev/prisma-cloud/api/cspm/app-login/

url = prisma_base_api_url + '/login'
action = 'POST'

request_headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': 'application/json; charset=UTF-8'
}

request_body_json = {
  'password': password,
  'prismaId': prismaid,
  'username': username
}

response = requests.request(action, url, headers=request_headers, json=request_body_json)

api_response = json.loads(response.content)

authtoken = api_response.get('token')

if ( authtoken is None ):
    print ('auth failed')
    sys.exit('Exit with error: Auth failed')
else:
    print ('auth success')
    
#Retrieve a list of all cloud accounts

#https://pan.dev/prisma-cloud/api/cspm/get-cloud-accounts/

url = prisma_base_api_url + '/cloud'
action = 'GET'

request_headers = {
  'Accept': 'application/json; charset=UTF-8',
  'x-redlock-auth': authtoken
}

request_body_json = {}

response = requests.request(action, url, headers=request_headers, json=request_body_json)

cloud_accounts = json.loads(response.content)

#Iterate and build an array of accountIds

accountIds = []

for cloud_account in cloud_accounts:
    accountIds.append(cloud_account['accountId'])

if not accountIds:
    sys.exit('Exit with error: No cloud accounts found')
else:
    print('Account Ids: '.join(str(cloud_account) for cloud_account in accountIds))


#Retrive the license consumption details of identified accountIds

#https://pan.dev/prisma-cloud/api/cspm/license-usage-count-by-cloud-paginated-v-2/

#License API requires Time Range Model parameter - https://pan.dev/prisma-cloud/api/cspm/api-time-range-model/

url = prisma_base_api_url + '/license/api/v2/usage'
action = 'POST'

request_headers = {
    'Accept': 'application/json; charset=UTF-8',
    'Content-Type': 'application/json; charset=UTF-8',
    'x-redlock-auth': authtoken
}

request_body_json = {
    'accountIds': accountIds,
    'timeRange': {
        'type': 'relative',
        'value': {
            'amount': 24,
            'unit': 'hour'
            }
        }
    }

response = requests.request(action, url, headers=request_headers, json=request_body_json)

#api_response = json.loads(response.content)
api_response = json.dumps(response.json(), indent = 4)

print (api_response)
