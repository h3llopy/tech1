# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.13] - 2020-07-03

### Fixed
- Reset password attempt passing the limit


## [1.0.12] - 2020-07-02

### Fixed
- After logout superuser shown logged in


## [1.0.11] - 2020-07-01

### Added
- Bulk terminate server action
- Search session by name of user

### Fixed
- Generate token error with active_model
- Error when another session not allowed


## [1.0.10] - 2020-06-30

### Fixed
- Mail template email_from


## [1.0.9] - 2020-06-25

### Changed
- Maximum failed login lockout based on user_id with failed login count field


## [1.0.8] - 2020-06-23

### Changed
- Maximum failed login lockout based on user_id rather than ip address


## [1.0.7] - 2020-06-18

### FIxed
- Error when quotation sent by mail


## [1.0.6] - 2020-06-11

### Fixed
- Redirect to reset_password error when 'website' installed.


## [1.0.5] - 2020-06-09

### Fixed
- Update session store access timestamp error
- Error on changing db from db with the module installed
- Login error if multiple sessions not allowed even if no other sessions exist


## [1.0.4] - 2020-06-02

### Fixed
- Database selected when logged out due to termination
- Terminate sessions on successful logout if multiple sessions not allowed

### Changed
- Known users' id stored in cookies


## [1.0.3] - 2020-06-02

### Fixed
- Installation error due to config_parameter
- Dashboard JS error

### Changed
- Login controller method


## [1.0.2] - 2020-05-30

### Fixed
- Incorrect username login error


## [1.0.1] - 2020-05-30

### Fixed
- In settings, invalid values (eg. negative values)


## [1.0.07] - 2020-05-29

### Changed
- Module name to 'User Login Security'

### Fixed
- Raise AccessDenied Exception On failed authentication
