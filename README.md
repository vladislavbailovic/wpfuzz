WordPress AJAX Action Fuzz Tester
=================================

Brute-attempt WP AJAX action endpoints and see what sticks.

This script can:

1) Attempt (naive) AJAX action discovery in given source (plugin) directory. This is done by inspecting the PHP files for lines containing `wp_ajax(_nopriv?)_` and extracting those. Only the literal actions are extracted - meaning, no fancy stuff such as string interpolation, `sprintf`s and the like.
2) Given a domain, attempt a series of requests (POST and GET) with some data payloads.
3) Given username and password, the script will attempt login first and issue both authenticated and unauthed requests.
4) The script will report successful requests by default. In addition to `200 OK` HTTP response status header, the successful responses are checked against the standard `wp_send_json_error` format: if the response is JSON, _and_ if it has `success` property, _and_ it's `false` - the request is a failure regardless of the response status header.
5) The script by default reports successful requests, as defined previously. It can additionally/alternatively report failures and rejected requests, or both, or neither. Rejected requests are the ones not handled by WP AJAX at all - i.e. with `400` status header and `0` in response body. The failures are pretty much any non-successful requests that aren't a success, or explicitly rejected.


Fixed data requests
-------------------

It is possible to send out requests with fixed data, by creating a `fuzzdata.json` file and specifying `fixdata` data source. Like this:

`cat '[{"key1": "val1"}]' > fuzzdata.json && wpfuzz http://example.com -a test -f fixdata`


Usage examples
--------------

- List actions in current directory: `wpfuzz list -d $(pwd)`
- Make a quick pass for actions from current plugin on example.org:
	- Visitors only: `wpfuzz example.org -d=$(pwd) -i 1 -f basic`
	- Auth and visitors: `wpfuzz example.org -d $(pwd) -i 1 -f basic -u <user> -p <pass>`


Expected results
----------------

Unless the project is explicitly listening to visitors requests, noauth requests should remain silent in output (either rejected, or failed). The same goes for auth requests with lesser-privileged user (e.g. admin actions with author-level user creds).
