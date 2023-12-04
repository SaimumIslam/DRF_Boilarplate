#!/bin/sh
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
purple=`tput setaf 4`
pink=`tput setaf 5`
aqua=`tput setaf 6`
white=`tput setaf 7`
reset=`tput sgr0`

echo "${yellow}  - create virtual environment (venv) and activate ${reset}"
python3 -m venv venv
source venv/bin/activate

echo "${pink} install required packages from requirements: ${reset}"
pip install -r requirements.txt

echo "${aqua} Run migrations: ${reset}"
python manage.py makemigrations
python manage.py migrate

echo "${green} Run server: ${reset}"
python manage.py runserver

echo "${reset} completed successfully! run staging server shell"
