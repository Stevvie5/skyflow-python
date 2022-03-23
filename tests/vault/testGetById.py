import unittest
import os
from skyflow.errors._skyflowerrors import SkyflowError, SkyflowErrorCodes, SkyflowErrorMessages
from skyflow.vault import Client, Configuration, RedactionType
from skyflow.service_account import generate_bearer_token
from dotenv import dotenv_values
import warnings


class TestGetById(unittest.TestCase):

    def setUp(self) -> None:
        self.envValues = dotenv_values(".env")
        self.dataPath = os.path.join(os.getcwd(), 'tests/vault/data/')

        def tokenProvider():
            token, type = generate_bearer_token(
                self.envValues["CREDENTIALS_FILE_PATH"])
            return token

        config = Configuration(
            self.envValues["VAULT_ID"], self.envValues["VAULT_URL"], tokenProvider)
        self.client = Client(config)
        warnings.filterwarnings(
            action="ignore", message="unclosed", category=ResourceWarning)
        return super().setUp()

    def getDataPath(self, file):
        return self.dataPath + file + '.json'

    def testGetByIdNoRecords(self):
        invalidData = {"invalidKey": "invalid"}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.RECORDS_KEY_ERROR.value)

    def testGetByIdRecordsInvalidType(self):
        invalidData = {"records": "invalid"}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.INVALID_RECORDS_TYPE.value % (str))

    def testGetByIdNoIds(self):
        invalidData = {"records": [
            {"invalid": "invalid", "table": "pii_fields", "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.IDS_KEY_ERROR.value)

    def testGetByIdInvalidIdsType(self):
        invalidData = {"records": [
            {"ids": "invalid", "table": "pii_fields", "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.INVALID_IDS_TYPE.value % (str))

    def testGetByIdInvalidIdsType2(self):
        invalidData = {"records": [
            {"ids": ["123", 123], "table": "pii_fields", "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.INVALID_ID_TYPE.value % (int))

    def testGetByIdNoTable(self):
        invalidData = {"records": [
            {"ids": ["id1", "id2"], "invalid": "invalid", "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.TABLE_KEY_ERROR.value)

    def testGetByIdInvalidTableType(self):
        invalidData = {"records": [
            {"ids": ["id1", "id2"], "table": ["invalid"], "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.INVALID_TABLE_TYPE.value % (list))

    def testGetByIdNoRedaction(self):
        invalidData = {"records": [
            {"ids": ["id1", "id2"], "table": "pii_fields", "invalid": "invalid"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.REDACTION_KEY_ERROR.value)

    def testGetByIdInvalidRedactionType(self):
        invalidData = {"records": [
            {"ids": ["id1", "id2"], "table": "pii_fields", "redaction": "PLAIN_TEXT"}]}
        try:
            self.client.get_by_id(invalidData)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.INVALID_REDACTION_TYPE.value % (str))

    def testGetByIdSuccess(self):
        data = {"records": [
            {
                "ids": [self.envValues["SKYFLOW_ID1"], self.envValues["SKYFLOW_ID2"], self.envValues["SKYFLOW_ID3"]],
                "table": "pii_fields",
                "redaction": RedactionType.PLAIN_TEXT
            }
        ]}
        try:
            response = self.client.get_by_id(data)
            self.assertIsNotNone(response["records"][0]["fields"])
            self.assertIsNotNone(
                response["records"][0]["fields"]["skyflow_id"])
            self.assertEqual(response["records"][0]["table"], "pii_fields")
            self.assertIsNotNone(response["records"][1]["fields"])
            self.assertIsNotNone(
                response["records"][1]["fields"]["skyflow_id"])
            self.assertEqual(response["records"][1]["table"], "pii_fields")
        except SkyflowError as e:
            self.fail('Should not throw an error')

    def testDetokenizePartialSuccess(self):
        data = {"records": [
            {
                "ids": [self.envValues["SKYFLOW_ID1"], self.envValues["SKYFLOW_ID2"], self.envValues["SKYFLOW_ID3"]],
                "table": "pii_fields",
                "redaction": RedactionType.PLAIN_TEXT
            },
            {
                "ids": ["invalid id"],
                "table": "pii_fields",
                "redaction": RedactionType.PLAIN_TEXT
            }]}
        try:
            self.client.get_by_id(data)
            self.fail('Should have thrown an error')
        except SkyflowError as e:
            errors = e.data['errors']
            self.assertEqual(e.code, SkyflowErrorCodes.PARTIAL_SUCCESS.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.PARTIAL_SUCCESS.value)
            self.assertIsNotNone(e.data["records"][0]["fields"])
            self.assertIsNotNone(e.data["records"][0]["fields"]["skyflow_id"])
            self.assertEqual(e.data["records"][0]["table"], "pii_fields")
            self.assertIsNotNone(e.data["records"][1]["fields"]["skyflow_id"])
            self.assertIsNotNone(e.data["records"][1]["fields"])
            self.assertEqual(e.data["records"][1]["table"], "pii_fields")
            self.assertEqual(e.data["errors"][0]["error"]["code"], 404)
            self.assertTrue(e.data["errors"][0]["error"]
                            ["description"].find("No Records Found") != -1)