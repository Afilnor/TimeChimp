# TimeChimp

## Description
- SDK to interact with TimeChimp API
- Can return a converted response to JSON and check for errors.
- Log HTTP method, url, params and headers
- Hide access_token in the logs

## How to install
`pip3 install timechimp`

## Source structure
- _endpoint.py: contain the source endpoints.
- _env_variables.py: env variables names holding the auth value (eg API token).
- api sub-package contains the functions to call

## How to use

- access token is retrieved through env variables TIMECHIMP_ACCESS_TOKEN

### Get the requests response object
```
import timechimp

response = timechimp.api.users.get_all()
```

### Convert the response object to json
```
import timechimp

users = timechimp.api.users.get_all(to_json=True)
```
- When setting to_json to True, will automatically raise an error if an error key is detected.
- So you don't have to worry about this in your application.


## Test
`pytest`