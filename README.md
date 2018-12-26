WordPress AJAX Action Fuzz Tester
---------------------------------

This script can:

1) Attempt (naive) AJAX action discovery in given source (plugin) directory. This is done by inspecting the PHP files for lines containing `wp_ajax(_nopriv?)_` and extracting those. Only the literal actions are extracted - meaning, no fancy stuff such as string interpolation, `sprintf`s and the like.
2) Given a domain, attempt a series of requests (POST and GET) with some data payloads.
3) Given username and password, the script will attempt login first and issue both authenticated and unauthed requests.
4) The script will report successful requests by default. In addition to `200 OK` HTTP response status header, the successful responses are checked against the standard `wp_send_json_error` format: if the response is JSON, _and_ if it has `success` property, _and_ it's `false` - the request is a failure regardless of the response status header.
