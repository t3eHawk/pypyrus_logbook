# logbook
Built-in Python logging module is a powerful tool to provide your programs with high quality logs.
This project is conception continue and alternative for native python logging.

*Logbook* is not a rework and even not based on python logging objects but it is a rethink totally written from zero (honestly with use similar names and tricks for easier migration and use).
We chose this path when found out that python logging is not enough functional and not enough flexible when we speak about integration with other our products.

With logbook you can:
* Generate and customize log file.
* Use existing file instead of creating new.
* Write messages into console instead of file.
* Generate customizable header with basic information about application, system or log.
* Log information, success and debug messages.
* Log errors with different levels (error, warning, critical).
* Abort program when high level error occurs.
* Or log messages in any desired record type.
* Separate different log blocks with border.
* Customize and design records of any type.
* Configure the default or add new record types, messages, patterns and forms.
* Manage log parameters during or after initialization.
* Reset log to default parameters.
* Close or reopen current log.
* Limit log by size or day.

## Getting Started
### Requirements
Operation systems: Windows, Linux, Mac OS.

Python version: 3.7.1.

### Installation
To install just download the latest release of *[logbook](https://github.com/tm7tai/logbook/releases)* and copy src/logbook folder to your/python/folder/Lib/site-packages/.

## How to Use
To start just declare log class instance:
```
import pypyrus_logbook as logbook

log = logbook.getlogger()
```
