# Changelog
[![Build Status](https://avatars1.githubusercontent.com/u/35299314?s=200&v=4)](https://github.com/balemessenger)

## [1.5.11] - 2018-12-23
### Added
- added validator parameter to filters as a callable function to validate the inputs
- added text field among with text_message filed to template response message for unifying
 with other classes text field
### fixed
- state holder problem at stop

## [1.4.10] - 2018-12-23
### Added
- Quoted Message Handler
- default action and value for template_message_button
- group_shield to config for preventing bot to handle updates from group_peer
- saving bot state_machine to redis db through state_holder and redis configs in config
- template_message, location_message and contact_message load_from_json

### fixed
- bot.send_document


## [1.3.9] - 2018-12-05
### Added
- get_response method in response class
- IPG payment message
- healthy socket connection
 
## [1.2.8] - 2018-09-30
### Added
- Send photo message easier than the past.
- Send Document message easier than the past.


### fixed
- network connection


