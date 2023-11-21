## First clone the git repository
git clone https://github.com/ezefernandez94/wa-bot.git

## Then create conda env out of requirements.txt

## This has to be done on the same folder of requirements.txt file
## If not, path ath the end of the line is incorrect (!)

conda create --name [env_name] --file ./requirements.txt

## Activate conda environment
conda activate [env_name]

## Run script bot.py
python3 bot.py

## To check that is working
In any browser go to: http://127.0.0.1:5000/welcome
If working you'll se a message that says: "Vos sos de la B"

## Set a Meta Developers Account
Steps:
    - Create an account
    - Create an Application ("Other")
        - Buiseness
        - Complete Form
    - Configure "WhatsApp"
    - Configure "WhatsApp API"

## For local development testing, Postman is needed.

url for testing: http://127.0.0.1:5000/webhook
POST request, JSON application type
Examples of JSON messages are in Meta Developer Docs


## For "production", glitch.com is used
Steps:
    - Import project from github.
    - Changes to requirements.txt --> remove Flask and erkzeug versions and change urllib3 version to 1.26.6
    - Add start.sh file with the following content:
        
        #!/bin/bash

        ## Exit early in errors
        set -eu

        ## Python buffer stdout
        export PYTHONUNBUFFERED=true

        python3 -m pip install -U pip

        ## Install requirements
        python3 -m pip install -r requirements.txt

        ## Run server
        python3 bot.py
