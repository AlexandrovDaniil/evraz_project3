#!/bin/bash
set -e

gunicorn -b 0.0.0.0:1235 book.composites.book_api:app --reload