# restafari 

[![Build Status](https://travis-ci.org/manoelhc/restafari.svg?branch=master)](https://travis-ci.org/manoelhc/restafari) [![Python Support](https://img.shields.io/badge/python-3.3%2C%203.4%2C%203.5-green.svg)]() [![Coverage Status](https://coveralls.io/repos/github/manoelhc/restafari/badge.svg?branch=master)](https://coveralls.io/github/manoelhc/restafari?branch=master) [![Issue Count](https://codeclimate.com/github/manoelhc/restafari/badges/issue_count.svg)](https://codeclimate.com/github/manoelhc/restafari) [![Code Climate](https://codeclimate.com/github/manoelhc/restafari/badges/gpa.svg)](https://codeclimate.com/github/manoelhc/restafari)
[![Test Coverage](https://codeclimate.com/github/manoelhc/restafari/badges/coverage.svg)](https://codeclimate.com/github/manoelhc/restafari/coverage) [![codecov](https://codecov.io/gh/manoelhc/restafari/branch/master/graph/badge.svg)](https://codecov.io/gh/manoelhc/restafari)


Restafari is a simple REST test tool. It provides a simple framework to describe and run tests and validations around your REST api.

## Features

 * Type check
 * Conditional validation
 * Test combination and dependencies, like: execute login test before and finally execute logout test.
 * HTTP status check
 * More to come...

## Getting Started (just 2 minutes)

To get yourself into Restafari, this is a 2-minutes getting started. First you need a machine with Python3 and PIP3 properly installed. You have to install Restafari as root user. 
 
```bash
 # On Ubuntu
 sudo su - root
 
 # On RHEL/CentOS
 su - root
```
 
Now, let's install Restafari from PYPI (the Python Package Index):
  
```bash
pip3 install restafari
```

After that, check if restafari was properly installed. Using your regular user, run:

```bash
restafari --version
```

You should see something like:

```bash
restafari 0.1.4
```

If your installation failed, try to install again. If it does not work, please open an ticket telling what happened. Restafari is a new product, not stable and it could happen anytime. 

All right, so if you Restafari installation is done, let's write our first test. For this test we will take a public API from http://jsonplaceholder.typicode.com/:
The service is http://jsonplaceholder.typicode.com/posts/1 which returns something similar to this:
 
```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```


Create a file called simple-test.rest and add this content:
```yaml
tests:
- id: check-post
  path: /posts/1
  expect:
    http: 200
    data:
      userId:
        $type: Number
```

Easy, hmm? Now let's run this test:

```shell
restafari --s jsonplaceholder.typicode.com  simple-test.rest
```

You should see:

```
Loading files
[/tmp/simple.rest]
-- Loading Test id: check-post test
Checking test dependencies
-- Test id: check-post request (jsonplaceholder.typicode.com,GET,/posts/1,)
 ---> [200] {  "userId": 1,  "id": 1,  "title": "sunt aut facere repella...
 [TEST] ['userId'] Comparing (Value $type Number) -> (From API)  the value must be Number (expect value) 
 [PASS]  Validation passed
```

So, this is your first test. Congratulations! Now you can improve your tests by checking other elements and adding a description for that:

```yaml
tests:
- id: check-post
  desc: Check Post
  path: /posts/1
  expect:
    http: 200
    data:
      userId:
        $type: Number
      id:
        $type: Number
      body:
        $type: String
      title:
        $type: String
```


Run Restafari with --help for further details. We are working to delivary a better documentation as well. :)
