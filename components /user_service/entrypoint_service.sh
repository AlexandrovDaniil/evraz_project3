#!/bin/bash
set -e

gunicorn -b 0.0.0.0:1234 user.composites.user_api:app --reload