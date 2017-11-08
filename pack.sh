#!/bin/bash

rm incomingredirect -rf
mkdir incomingredirect

cp __init__.py  manifest.ini  incomingredirect.png  incomingredirect.py incomingredirect

zip -r incomingredirect.zip incomingredirect incomingredirect/*.py incomingredirect/*.png incomingredirect/manifest.ini
rm incomingredirect -rf
