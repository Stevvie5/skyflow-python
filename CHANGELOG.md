# Changelog

All notable changes to this project will be documented in this file.

## [1.6.0] - 2022-04-12

### Added

- support for application/x-www-form-urlencoded and multipart/form-data content-type's in connections.

## [1.5.1] - 2022-03-29

### Added

- Validation to token obtained from `tokenProvider`

### Fixed

- Request headers not getting overriden due to case sensitivity

## [1.5.0] - 2022-03-22

### Changed

- `getById` changed to `get_by_id`
- `invokeConnection`changed to `invoke_connection`
- `generateBearerToken` changed to `generate_bearer_token`
- `generateBearerTokenDromCreds` changed to `generate_bearer_token_from_creds`
- `isExpired` changed to `is_expired`
- `setLogLevel` changed to `set_log_level`

### Removed

- `isValid` function
- `GenerateToken` function

## [1.4.0] - 2022-03-15

### Changed

- deprecated `isValid` in favour of `isExpired`

## [1.3.0] - 2022-02-24

### Added

- Request ID in error logs and error responses for API Errors
- Caching to accessToken token
- `isValid` method for validating Service Account bearer token

## [1.2.1] - 2022-01-18

### Fixed

- `generateBearerTokenFromCreds` raising error "invalid credentials" on correct credentials

## [1.2.0] - 2022-01-04

### Added

- Logging functionality
- `setLogLevel` function for setting the package-level LogLevel
- `generateBearerTokenFromCreds` function which takes credentials as string

### Changed

- Renamed and deprecated `GenerateToken` in favor of `generateBearerToken`
- Make `vaultID` and `vaultURL` optional in `Client` constructor

## [1.1.0] - 2021-11-10

### Added

- `insert` vault API
- `detokenize` vault API
- `getById` vault API
- `invokeConnection`

## [1.0.1] - 2021-10-26

### Changed

- Package description

## [1.0.0] - 2021-10-19

### Added

- Service Account Token generation
