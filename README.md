# ZBCE API

# Prerequisites:
- [Ubuntu 20.04 Operating System](https://ubuntu.com/)
    - other versions might be alright, but have not been tested
- Basic understanding of the Linux Command Line

# Getting Started
These are the basic steps to get started:
1. Setting up the LAMP Server
2. Installing MySQL
3. Git Clone and Setup
4. Create a `.env` File
5. Testing the Server

My instructions are based off of Tanner Crook's Blog, which is really well-written. If you would like more detail for any of the steps I don't explain well just follow his instructions here: [LAMP Stack with Flask](https://db.tannercrook.com/cit-225/lamp-stack-with-flask/)

## 1 - Setting up the LAMP Server
#### Linux
Make sure your server is up to date by running the following commands
```
sudo apt update
sudo apt upgrade
```
#### Apache
```
sudo apt install apache2
```

#### MySQL
Follow these instructions if you would like more detail: [How to Install MySQl on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)

1. `sudo apt update`
2. `sudo apt install mysql-server`
3. `sudo mysql_secure_installation`
4. Set password for root user from the step above
5. Create a dedicated MySQL User and Grant Privileges using the steps below.
6. `sudo mysql`
7. In the MySQL console run the following commands:
    ```sql
    CREATE USER 'YOURUSERNAME'@'localhost' IDENTIFIED BY 'YOURPASSWORD';
    ```
8. Now grant your permissions
    ```sql
    GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'YOURUSERNAME'@'localhost' WITH GRANT OPTION;
    ```
9. You can now log in with your new user and password `mysql -u u YOURUSERNAME -p`
10. Create your database using the SQL command: `CREATE DATABASE zotbinsCE`;
11. Exit the MySQL shell: `exit`
11. Remember your username and password 😉

#### Python
```
sudo apt install python3
sudo apt install python3-venv
sudo apt install python3-pip
```

### FTP (Optional but Recommended)
This step is optional, but is recommended for transferring files to or from the server.
```
sudo apt install vsftpd
sudo nano /etc/vsftpd.conf
```
uncomment the line: `write_enable=YES`

```
sudo service vsftpd restart
```

## 3 - Git Clone and Setting up the Environment
*Following these instructions will be more convenient if you are in superuser mode `su`*

1. Follow these instructions to set up your Apache and WSGI Configuration: [https://db.tannercrook.com/building-a-flask-foundation/](https://db.tannercrook.com/building-a-flask-foundation/)
2. After the step above you should have a working LAMP Stack w/ Flask
3. Now we're going to clone the ZBCE API. So we need to replace the app folder with the repository we are cloning by running the following:
    ```bash
    mv /var/www/app/app /var/www/app/app.bak
    cd /var/www/app
    git clone https://github.com/zotbins/zbce_api
    mv zbce_api app
    ```
4. Now build the virtual environment.
    ```bash
    cd app
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt  
    ```
5. Create a folder for uploading your images and change the permissions.
    ```bash
    cd /var/www/app/app
    mkdir YOUR_UPLOAD_FOLDER_NAME
    chmod 777 YOUR_UPLOAD_FOLDER_NAME
    ```

## 4 - Create a `.env` File
Now that you have the stack setup and your repository and your virtual environment. You want to create a `.env` file with the editor program of your choice or just use nano. This will allow you to store some variables that are supposed to be a secret like passwords, or usernames, etc. We will be using a `.env` to also store sensitive information.

0. `sudo nano .env`
1. Add the following lines and replace the following portions as specified

    ```bash
    # change this to specify your MySQL Database
    SQLALCHEMY_DATABASE_URI=mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@localhost/zotbinsCE

    # this will be used for your flask app, change the following to a secure secret key
    SECRET_KEY=YOUR_HARD_TO_GUESSS_STRING

    # change this to specify where you want the image files to be uploaded to
    # for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
    UPLOAD_FOLDER=YOUR_UPLOAD_FOLDER_PATH
    ```
1. Change the variable: `UPLOAD_FOLDER = 'YOUR_UPLOAD_FOLDER_NAME'`
2. Modify your secret key: `app.config['SECRET_KEY'] = 'YOUR_HARD_TO_GUESSS_STRING'`
3. Specify your MySQL Database: `app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@localhost/zotbinsCE'`
4. Turn off or turn on Debugging options. You should turn off debugging, when you want your server to run in production mode: `app.config['DEBUG'] = True # turn this off when not debugging.`

## 5 - Testing the Server
Alright, everything should be set now!
1. Reboot your server: `reboot`
2. Open the `unit_tests.py` file and change the following:
    ```
    BASEURL = "YOUR_URL"
    IPADDRESS = "YOUR_IP_ADDRESS"
    ```
3. Save and close the file
4. Run the unit tests
    ```
    su
    cd /var/www/app/app
    pytest -q unit_tests.py
    ```
5. If there are no error messages everything should be good!
