#!/bin/bash

git secret reveal
mv get_token.py web
mv management.py web
mv config.ini web
mv sub-scripts web

chown -R $(USER):www-data web/*