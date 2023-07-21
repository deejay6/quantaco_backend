## Quantaco Backend

This application is running on python3.9 and Django 3.2. This application 
contains middleware i.e. all requests are authenticated with valid session id.
Public routes are exempted like login, register and logout.

#### API Collection
https://documenter.getpostman.com/view/2502898/2s946k6AaX

### Application setup without docker

1. Clone this application.
2. Install python3.9 on your system if required.
3. Create virtual environment

    ``virtualenv -p python3.9 venv``
4. Activate virtual environment 
    
    ``source venv/bin/activate``
5. Install requirements

    ``pip install -r requirement.txt``
6. Run migrations
    
    ``python manage.py migrate``
7. Run server

    ``python manage.py runserver``

    Access the server at http://127.0.0.1:8000

### Application setup with docker
1. Install docker if required
2. Build Image

    ``docker build -t quantaco_backend .``
3. Run Image

    ``docker run -p 8000:8000 quantaco_backend``
4. Access server at http://127.0.0.1:8000