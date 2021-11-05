import os
from skyflow.Errors import SkyflowError
from skyflow.ServiceAccount import GenerateToken
from skyflow.Vault import Client, SkyflowConfiguration, RequestMethod, GatewayConfig

'''
This sample is for generating CVV using Skyflow Gateway with a third party integration such as VISA
'''

CREDENTIALS_PATH = os.getenv('CREDENTIALS_FILE_PATH')

def tokenProvider():
    token, _ = GenerateToken(CREDENTIALS_PATH)
    return token

try:
    config = SkyflowConfiguration('<VAULT_ID>', '<VAULT_URL>', tokenProvider)
    gatewayConfig = GatewayConfig('<GATEWAY_URL>', RequestMethod.POST,
    requestHeader={
                'Content-Type': 'application/json',
                'Authorization': '<GATEWAY_BASIC_AUTH>'
    },
    requestBody= # For third party integration
    {
        "expirationDate": {
            "mm": "12",
            "yy": "22"
        }
    },
    pathParams={'cardID': '<CARD_VALUE>'}) # param as in the example
    client = Client(config)

    response = client.invokeGateway(gatewayConfig)
    print('Response:', response)
except SkyflowError as e:
    print('Error Occured:', e)
