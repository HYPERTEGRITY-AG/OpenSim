# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-xx-xx
This release is about packaging and distributing.  
The package is renamed from _opensim_ to _oscsim_, since opensim is already taken on PyPI.

### Added
- Nothing

### Deleted
- Nothing

### Changed
- Nothing

## [1.1.0] - 2021-05-30
This release contains mainly 2 topics:
* **NGSI-LD Support (experimental)** - Starting with this release the experimental Orion LD-server (Version: post-v0.7) can be used with Open Smart City-Sim.
* **Changes in Options** - This release has some changes in options in a way, that there is now a more generic way for creating necessary headers. If you are familiar with the current options (in 1.0.0), here is, how to "migrate" to the new options:
  * **Bearer token** - In 1.0.0 you might have used the -b [--bearer] option like: `... -b BEARER_TOKEN ...`. With this new release you will have to use `-H Authorization "Bearer INSERT_BEARER_TOKEN_HERE"` instead.
  * **Tenant** - If you used the -t [--tenant] option like: `... -t MY_TENANT ...` to set the Fiware-service you have to switch to `-H Fiware-service MY_TENANT` now.
  * **X-Gravitee-Api-Key** - If you used the -x [--x-api-key] option to set an X-Gravitee-Api-Key, please use `-H X-Gravitee-Api-Key MY_API_KEY` now.

### Added
- NGSI-LD support (experimental).
- Option -H [--header] can be used to add header.

### Deleted
- Removed options -b [--bearer], -x [--x-api-key] and -t [--tenant].

### Changed
- Nothing

## [1.0.0] - 2021-01-17
### Added
- Version- and Copyright-printout.
- CONTRIBUTION.md

### Deleted
- Nothing.

### Changed
- Nothing.
