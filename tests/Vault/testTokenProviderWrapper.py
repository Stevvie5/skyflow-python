import unittest

import dotenv
from skyflow.Vault._token import tokenProviderWrapper
from skyflow.ServiceAccount import generateBearerToken
from skyflow.Errors._skyflowErrors import *


class TestTokenProviderWrapper(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def testInvalidStoredToken(self):
        env_values = dotenv.dotenv_values('.env')

        def tokenProvider():
            newerToken, _ = generateBearerToken(
                env_values['CREDENTIALS_FILE_PATH'])
            return newerToken

        try:
            tokenProviderWrapper('invalid', tokenProvider, "Test")
            self.fail('Should have thrown invalid jwt error')
        except SkyflowError as e:
            self.assertEqual(e.code, SkyflowErrorCodes.INVALID_INPUT.value)
            self.assertEqual(
                e.message, SkyflowErrorMessages.JWT_DECODE_ERROR.value)

    def testNoStoredToken(self):
        env_values = dotenv.dotenv_values('.env')
        self.newToken = ''

        def tokenProvider():
            self.newerToken, _ = generateBearerToken(
                env_values['CREDENTIALS_FILE_PATH'])
            return self.newToken

        try:
            newerToken = tokenProviderWrapper('', tokenProvider, "Test")
            self.assertEqual(newerToken, self.newToken)
        except SkyflowError:
            self.fail('Should have decoded token')

    def testStoredTokenNotExpired(self):
        env_values = dotenv.dotenv_values('.env')
        self.newerToken = ''

        def tokenProvider():
            self.newerToken, _ = generateBearerToken(
                env_values['CREDENTIALS_FILE_PATH'])
            return self.newerToken

        try:
            newToken = tokenProviderWrapper(
                tokenProvider(), tokenProvider, "Test")
            self.assertEqual(newToken, self.newerToken)
        except SkyflowError:
            self.fail('Should have decoded token')
