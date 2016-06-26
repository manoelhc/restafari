# restafari [![Build Status](https://travis-ci.org/manoelhc/restafari.svg?branch=master)](https://travis-ci.org/manoelhc/restafari) [![Python Support](https://img.shields.io/badge/restafari-3.3%2C%203.4%2C%203.5-yellow.svg)
Restafari is a simple REST test tool.

## Features
Basically the features are:
 * Type check
 * Conditional validation
 * Test combination and dependencies, like: execute login test before and finally execute logout test.
 * HTTP status check


## Test example

You can create simple requests validation with some conditional features, like:

```yaml
  - id : ping
    weight : 20
    executable : true
    exec_before : []
    exec_after : []
    desc : "This is the ping"
    format : "json"
    path :  "/files/simple_comparison"
    method : GET
    expect:
      http: 200
      data:
        time :
          $and:
             $or :
               $type : Number
               $gt : 10000
          $or :
             $lt : 2000
             $gt : 100

```

Some values are default and another way to write this test is:

```yaml
  - id : ping
    desc : "This is the ping"
    path :  "/files/simple_comparison"
    expect:
      data:
        time :
          $and:
             $or :
               $type : Number
               $gt : 10000
          $or :
             $lt : 2000
             $gt : 100

```


## Syntax

Restafary sintax is pretty simple:

```bash
usage: restafari.py [-h] [--hostname HOSTNAME] [--protocol PROTOCOL]
                    [--port PORT] [--exec-before EXEC_BEFORE]
                    [--exec-success EXEC_SUCCESS] [--debug DEBUG]
                    [N [N ...]]

Restafari REST API tester

positional arguments:
  N                     The test file(s) to be used

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME, -s HOSTNAME
                        The hostname of the web service
  --protocol PROTOCOL, -p PROTOCOL
                        The protocol which will be used (HTTP/HTTPS)
  --port PORT, -P PORT  The port number
  --exec-before EXEC_BEFORE, -B EXEC_BEFORE
                        Execute a single command-line/script before starting
                        the REST test. It's useful to prepare the environment
                        for the tests.
  --exec-success EXEC_SUCCESS, -S EXEC_SUCCESS
                        Execute a single command-line/script when all tests
                        were done successfully.
  --debug DEBUG, -D DEBUG
                        Enable debug mode

```
