# 🌱 Community Mangrove Watch

A Django web app to report and track threats to mangrove forests.

<img width="1895" height="1079" alt="Screenshot 2026-03-14 164003" src="https://github.com/user-attachments/assets/4a7a1c21-52ad-4321-8b6c-5a1b290b32f2" />

<img width="1889" height="598" alt="Screenshot 2026-03-14 164022" src="https://github.com/user-attachments/assets/3f52784c-ef25-41dc-9463-21643c04d173" />

<img width="1895" height="1079" alt="Screenshot 2026-03-14 164126" src="https://github.com/user-attachments/assets/3e5cf9a6-3f42-417c-93e6-c207a234260d" />


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
