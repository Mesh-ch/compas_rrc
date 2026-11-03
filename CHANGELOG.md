# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

* A feedback parser that raises now resolves the pending `send`/`send_and_wait` future with an `InstructionException` naming the instruction (e.g. `WaitForDigital(gripper_closed)`) instead of leaving it unresolved forever.

### Removed


## [2.0.0] 2024-03-28

### Added

* Added `to_configuration` and `to_configuration_primitive` to `compas_rrc.ExternalAxes` and `compas_rrc.RobotJoints`

### Changed

* Update minimum requirements to `compas_fab > 1.x` and `compas > 2.x`

### Removed

## 1.1.0

### Added

* Prepared github actions for continuous integration
* Added compas plugin for automatic Rhino install

## 1.0.0

* Initial version
