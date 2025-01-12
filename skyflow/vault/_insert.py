import json

import requests
from requests.models import HTTPError
from skyflow.errors._skyflowerrors import SkyflowError, SkyflowErrorCodes, SkyflowErrorMessages
from skyflow._utils import InterfaceName

interface = InterfaceName.INSERT.value


def getInsertRequestBody(data, tokens: bool):
    try:
        records = data["records"]
    except KeyError:
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT,
                           SkyflowErrorMessages.RECORDS_KEY_ERROR, interface=interface)

    if not isinstance(records, list):
        recordsType = str(type(records))
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INVALID_RECORDS_TYPE.value % (
            recordsType), interface=interface)

    requestPayload = []
    insertTokenPayload = []
    for index, record in enumerate(records):
        tableName, fields = getTableAndFields(record)
        requestPayload.append({
            "tableName": tableName,
            "fields": fields,
            "method": "POST",
            "quorum": True})
        if tokens:
            insertTokenPayload.append({
                "method": "GET",
                "tableName": tableName,
                "ID": "$responses." + str(index) + ".records.0.skyflow_id",
                "tokenization": True
            })
    requestBody = {"records": requestPayload + insertTokenPayload}
    try:
        jsonBody = json.dumps(requestBody)
    except Exception as e:
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INVALID_JSON.value % (
            'insert payload'), interface=interface)

    return jsonBody


def getTableAndFields(record):
    try:
        table = record["table"]
    except KeyError:
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT,
                           SkyflowErrorMessages.TABLE_KEY_ERROR, interface=interface)

    if not isinstance(table, str):
        tableType = str(type(table))
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INVALID_TABLE_TYPE.value % (
            tableType), interface=interface)

    try:
        fields = record["fields"]
    except KeyError:
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT,
                           SkyflowErrorMessages.FIELDS_KEY_ERROR, interface=interface)

    if not isinstance(fields, dict):
        fieldsType = str(type(table))
        raise SkyflowError(SkyflowErrorCodes.INVALID_INPUT, SkyflowErrorMessages.INVALID_FIELDS_TYPE.value % (
            fieldsType), interface=interface)

    return (table, fields)


def processResponse(response: requests.Response, interface=interface):
    statusCode = response.status_code
    content = response.content.decode('utf-8')
    try:
        response.raise_for_status()
        try:
            return json.loads(content)
        except:
            raise SkyflowError(
                statusCode, SkyflowErrorMessages.RESPONSE_NOT_JSON.value % content, interface=interface)
    except HTTPError:
        message = SkyflowErrorMessages.API_ERROR.value % statusCode
        if response != None and response.content != None:
            try:
                errorResponse = json.loads(content)
                if 'error' in errorResponse and type(errorResponse['error']) == type({}) and 'message' in errorResponse['error']:
                    message = errorResponse['error']['message']
            except:
                message = SkyflowErrorMessages.RESPONSE_NOT_JSON.value % content
        if 'x-request-id' in response.headers:
            message += ' - request id: ' + response.headers['x-request-id']
        raise SkyflowError(statusCode, message, interface=interface)


def convertResponse(request: dict, response: dict, tokens: bool):
    responseArray = response['responses']
    records = request['records']
    recordsSize = len(records)
    result = []
    for idx, _ in enumerate(request):
        table = records[idx]['table']
        skyflow_id = responseArray[0]['records'][idx]['skyflow_id']
        if tokens:
            fieldsDict = responseArray[recordsSize + idx]['fields']
            fieldsDict['skyflow_id'] = skyflow_id
            result.append({'table': table, 'fields': fieldsDict})
        else:
            result.append({'table': table, 'skyflow_id': skyflow_id})
    return {'records': result}
