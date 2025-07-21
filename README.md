# Commplete Authentication System

This is a full-stack web application built using **Python Django** for the backend, **React.js** for the frontend, and **MySQL** as the database. The application provides essential user functionalities like sign up, sign in, password reset with OTP, Google login, and JWT-based token authentication for secure user sessions.

## Features

- **User Authentication**:
  - **Sign Up**: Users can create a new account by providing their email, username, and password.
  - **Sign In**: Users can sign in to their account using their credentials (email and password).
  - **Password Reset (OTP)**: Users can reset their password by receiving a One-Time Password (OTP) to their email.
  - **Google Login**: Users can sign in using their Google account.
  - **JWT Authentication**: Secure authentication using JSON Web Tokens (JWT) for maintaining user sessions.

## Tech Stack

- **Frontend**:
  - **React.js**: A JavaScript library for building user interfaces.
  - **Material-UI (MUI)**: A popular React component library for building modern and responsive UIs with pre-built components.
  - **Axios**: For making API calls to the backend.
  - **React Router**: For managing client-side routing.

- **Backend**:
  - **Python Django**: A powerful web framework for building robust and secure web applications.
  - **Django Rest Framework (DRF)**: For building RESTful APIs.
  - **JWT Authentication**: For securely handling user authentication and session management.

- **Database**:
  - **MySQL**: A relational database management system for storing user data and application information.

## Installation

### Backend (Django)

. Clone the repository:
   ```bash
   git clone https://github.com/K9TX/Complete_Auth

Navigate to the backend directory:
cd project-name/backend

Set up a virtual environment:
python -m venv venv

Activate the virtual environment:
.\venv\Scripts\activate

Install the required Python dependencies:
pip install -r requirements.txt

Set up the MySQL database:
Create a MySQL database and update the DATABASES configuration in settings.py with your database credentials.

Apply database migrations:
python manage.py migrate

Create a superuser (optional for accessing the admin panel):
python manage.py createsuperuser

Start the Django development server:
python manage.py runserver


Frontend (React.js)
Navigate to the frontend directory:

npm install

Install Material-UI (MUI):

npm install @mui/material @emotion/react @emotion/styled

Install other required dependencies like Axios and React Router:

npm install axios react-router-dom

Start the React development server:

npm start
This will start the frontend on http://localhost:5173.
