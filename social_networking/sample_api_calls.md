# Sample API Calls

## Signup

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/signup/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email_id": "sam@gmail.co.in",
    "password": "Test@g123"
}'
```

## Login

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email_id": "sam@gmail.co.in",
    "password": "Test@g123"
}'
```

## Search users

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/search_users?search_key=sam' \
--header 'Authorization: Bearer VGf6pbHdgcIxbM7deapgD7aZGwEeik'

```


## Friends List

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/get_friends/' \
--header 'Authorization: Bearer b1xEQaQysLnOAjDUiksy6vQfQcYokt'
```

## Pending Requests

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/get_pending_request/' \
--header 'Authorization: Bearer VGf6pbHdgcIxbM7deapgD7aZGwEeik'
```

## Sending/Accepting/Rejecting Friend Requests

```commandline
curl --location 'http://127.0.0.1:8000/friends/api/v1/get_pending_request/' \
--header 'Authorization: Bearer VGf6pbHdgcIxbM7deapgD7aZGwEeik'
```