## COVIDwebApp 
This is CSE3310 UTA project (#COVIDwebApp)

###Getting Started
Before you start make sure you have the Python 3.8 or higher installed in you operating system.<br/>

###Initial Setup 
* Clone the COVIDwebApp repo:
    * To clone the repo run ```git clone https://github.com/ujjwalbgn/COVIDwebApp ```
* Navigate into the repository  ```cd COVIDwebApp```
* Install all the requirements listed in requirements.txt using ```pip install requirements.txt ```      


###Running the Application
By default, the configuration uses SQLite, so migrate models to database follow the steps listed below: <br/>
 * Make sure with in the repo for COVIDwebApp, now run ```python COVIDwebApp\manage.py makemigrations``` followed by ```python COVIDwebApp\manage.py migrate```
 * Now the Database is set, so to create a superuser run ```python COVIDwebApp\manage.py createsuperuser```
    *System wil prompt you for username, email and password
 * You can now login to backend of th application at ```http://127.0.0.1:8000/admin/``` 
    * After logging as Super User create two user groups 'staff' and 'patient'.
    * Assign the Super User to the staff group. 
 * Now all new users who register will be marked as 'patient'
 * For Healthcare providers assign them to 'staff' group in order to grant them access to Patient Details
 
 
          

