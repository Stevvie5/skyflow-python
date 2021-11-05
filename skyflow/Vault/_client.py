import requests
from ._insert import getInsertRequestBody, processResponse, convertResponse
from ._config import SkyflowConfiguration
from ._config import InsertOptions, GatewayConfig
from ._gateway import createRequest
from ._detokenize import sendDetokenizeRequests, createDetokenizeResponseBody
from ._getById import sendGetByIdRequests, createGetByIdResponseBody
import asyncio
from skyflow.Errors._skyflowErrors import SkyflowError, SkyflowErrorCodes, SkyflowErrorMessages   

class Client:
    def __init__(self, config: SkyflowConfiguration):
        if config.vaultID == None:
            raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INIT_FAILED.value%('Vault ID'))
        if config.vaultURL == None:
            raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INIT_FAILED.value%('Vault URL'))
        if config.tokenProvider == None:
            raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INIT_FAILED.value%('Token Provider'))

        self.vaultID = config.vaultID
        self.vaultURL = config.vaultURL.rstrip('/')
        self.tokenProvider = config.tokenProvider

    def insert(self, data: dict, options: InsertOptions = InsertOptions()):
        jsonBody = getInsertRequestBody(data, options.tokens)
        requestURL = self.vaultURL + "/v1/vaults/" + self.vaultID
        token = self.tokenProvider()
        headers = {
            "Authorization": "Bearer " + token
        }
        response = requests.post(requestURL, data=jsonBody, headers=headers)
        processedResponse = processResponse(response)
        return convertResponse(data, processedResponse, options.tokens)

    def invokeGateway(self, config: GatewayConfig):
        session = requests.Session()
        token = self.tokenProvider()
        request = createRequest(config)
        request.headers['X-Skyflow-Authorization'] = token
        response = session.send(request)
        session.close()
        return processResponse(response)

    def detokenize(self, data):
        token = self.tokenProvider()
        url = self.vaultURL + "/v1/vaults/" + self.vaultID + "/detokenize"
        responses = asyncio.run(sendDetokenizeRequests(data, url, token))
        result, partial = createDetokenizeResponseBody(responses)
        if partial:
            raise SkyflowError(SkyflowErrorCodes.PARTIAL_SUCCESS ,SkyflowErrorMessages.PARTIAL_SUCCESS, result)
        else:
            return result
    
    def getById(self, data):
        token = self.tokenProvider()
        url = self.vaultURL + "/v1/vaults/" + self.vaultID
        responses = asyncio.run(sendGetByIdRequests(data, url, token))
        result, partial = createGetByIdResponseBody(responses)
        if partial:
            raise SkyflowError(SkyflowErrorCodes.PARTIAL_SUCCESS ,SkyflowErrorMessages.PARTIAL_SUCCESS, result)
        else:
            return result
        


