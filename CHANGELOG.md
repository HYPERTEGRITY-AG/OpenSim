# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2021-xx-xx
This release contains mainly 2 topics:
* **NGSI-LD Support** - Starting with this release the new Orion LD-server can be accessed with OpenSim.
* **Changes in Options** - This release has some changes in options in a way, that they become more generic in creating necessary headers. If you are familiar with the current options (in 1.0.0), here is, how to "migrate" to the new options:
  * **Bearer token** - In 1.0.0 you might have used the -b [--bearer] option like: `... -b BEARER_TOKEN ...`. With this new release you will have to use `-x Authorization "Bearer INSERT_BEARER_TOKEN_HERE"` instead.
  * **Tenant** - If you used the -t [--tenant] option like: `... -t MY_TENANT ...` to set the Fiware-service you have to switch to `-x Fiware-service MY_TENANT` now.
  * **X-Gravitee-Api-Key** - The -x [--x-api-key] option changed completely to -x [--header]. So if you used this option like: `... -x MY_API_KEY ...` you will have to use it like `-x X-Gravitee-Api-Key MY_API_KEY` now.

### Added
- NGSI-LD support.

### Deleted
- Removed options -b [--bearer] and -t [--tenant].

### Changed
- Made -x [--x-api-key] more generic (-x [--header])

## [1.0.0] - 2021-01-17
### Added
- Version- and Copyright-printout.
- CONTRIBUTION.md

### Deleted
- Nothing.

### Changed
- Nothing.
