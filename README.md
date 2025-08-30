# 🌱 Community Mangrove Watch

A Django web app to report and track threats to mangrove forests.

## 🚀 How to Run

- Download and extract the project  
- Create a virtual environment:  
  `python -m venv venv`  
- Activate it:  
  - Windows: `venv\Scripts\activate`  
  - Mac/Linux: `source venv/bin/activate`  
- Install packages:  
  `pip install -r requirements.txt`  
- Run database setup:  
  `python manage.py migrate`  
- Create an admin:  
  `python manage.py createsuperuser`  
- Start the server:  
  `python manage.py runserver`  
- Open in browser: **http://localhost:8000**

## 🌍 Features

- Easy signup/login  
- Report incidents with location  
- Map view with reports  
- Points & badges for users  
- Dashboard for users & admins  
- Works on mobile & desktop  

## 🔑 Admin

Go to `/admin` to manage users, reports, and badges.
