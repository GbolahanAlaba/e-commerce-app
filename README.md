
# **E-commerce App**

## **Overview**

This eCommerce project provides a seamless shopping experience with a set of essential features, including user authentication, product browsing, cart management, and payment integration. Here's a detailed description of the project:

## **Prerequisites**

- `Python 3.11.3`
- `Django 5.1.1`
- `Django Rest Framework (DRF) 3.15.2`
- `SQLite or any other preferred database`


## **Installation**
Clone the Repository


git clone https://github.com/GbolahanAlaba/ecommerce-app

cd ecommerce-app


## **Create Virtual Environment**

It's recommended to use a virtual environment to manage dependencies:


`python -m venv venv`

## **Activate Virtual Environment**

MAC `source venv/bin/activate`

Windows `venv/Scripts/activate`

## **Install Dependencies**

Install the required dependencies using pip:

`pip install -r requirements.txt`


## **Run Migrations**

Apply the migrations to set up your database schema:

`python manage.py makemigrations`

`python manage.py migrate`


## **Run the Development Server**
Start the development server to verify everything is set up correctly:

`python manage.py runserver`
You should now be able to access the application at http://127.0.0.1:8000/api

## **API Endpoints**
Base URL - `http://127.0.0.1:8000/`

- `POST /auth/signin/`: Signin as a user or admin.
- `POST /auth/signup/`: Signup an account.


## **API Implementation**


#### POST /create-applicant/

- **Request Body**:

  ```json
  {
    "email_or_phone": "admin@gmail.com" or "09073832843",
    "password": "pass"
  }

- **Response**:

  ```json
  {
    "status": "success",
    "message": "signin successfully",
    "data": {
        "user_id": "7ee38ad4-f0eb-42b1-87c4-175ce6ae467b",
        "first_name": "",
        "last_name": "",
        "email": "admin@gmail.com",
        "phone": "08011112222",
        "address": "Your address",
        "state": "Your state",
        "lga": "Your LGA",
        "residential": "",
        "gender": true,
        "referral_code": "",
        "is_staff": true
    },
    "token": "96cdda6bfec57d759752590ca3aef9359fa6684f79d409ad1822df69e18bc90e"
  }

`200 OK` on success.

`404 Not Found` on not found error.

`403 Forbidden` on forbidden error.

`509 Internal Server Error` on server error.



## **Testing**
Run a tests to ensure the API endpoints work as expected.

`py manage.py test`