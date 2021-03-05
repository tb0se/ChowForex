# ChowForex Blog

## Getting Started
1. Clone this repository.
### Make sure you are in the root directory, then:
1. Create a virtual environment: `$ virtualenv env`
2. Activate the virtual environment: `$ source env/bin/activate`
3. Install the required packages: `$ pip install -r requirements.txt`

## To Run
1. Create environment variables:
    - `FLASK_APP=app`
    - `FLASK_ENV`
    - `EMAIL_USER` valid Gmail credentials
    - `EMAIL_PASS` valid Gmail credentials
    - `ADMIN_EMAIL`
    - `ADMIN_PASS`
2. Start the Flask application:
    - `flask init-db`
    - `flask db upgrade`
    - `flask create-user admin`
    - `flask run`