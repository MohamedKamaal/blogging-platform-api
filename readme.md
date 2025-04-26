Medium-like Platform API
Django
DRF
PostgreSQL

A RESTful API for a Medium-like blogging platform with user profiles, articles, and social features.

Features
User Authentication

Email-based registration and login

JWT token authentication

Password reset functionality

Profile Management

User profiles with bio, profile pictures

Follow/unfollow system

Follower/following lists

Article System

Create, read, update, and delete articles

Article views tracking

Clapping system

Comments and ratings

Admin Interface

Custom Django admin interface

User and content management

API Documentation
Interactive API documentation available at:

Swagger UI: /swagger/

ReDoc: /redoc/

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/medium-like-api.git
cd medium-like-api
Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Configure environment variables:
Create a .env file based on .env.example and set your configuration.

Run migrations:

bash
python manage.py migrate
Create superuser:

bash
python manage.py createsuperuser
Run development server:

bash
python manage.py runserver
Project Structure
medium-like-api/
├── articles/              # Article-related functionality
├── profiles/              # User profile functionality
├── users/                 # Custom user model and auth
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md              # This file


Testing
Run tests with:

bash
python manage.py test




Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See LICENSE for more information.

