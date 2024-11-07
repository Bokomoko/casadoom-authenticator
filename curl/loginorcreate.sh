#!/bin/bash
# logins into stytch if the user is old or creates a new user
curl --request POST \
  --url https://test.stytch.com/v1/magic_links/email/login_or_create \
  -u  "${STYTCH_PROJECT_ID}:${STYTCH_SECRET}" \
  -H 'Content-Type: application/json' \
  -d '{"email": "bokomoko+test@gmail.com", "login_magic_link_url": "http://localhost:3000/authenticate", "signup_magic_link_url": "http://localhost:3000/authenticate" }'

