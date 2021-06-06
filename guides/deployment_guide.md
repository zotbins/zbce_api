# ZBCE API Deployment Guides

There are multiple deployment options listed below. If you feel that there is a alternative deployment option that you would like to share feel free to make a pull request!

# 💡 LAMP Server Deployment

My instructions are based off of Tanner Crook's Blog, which is really well-written. If you would like more detail for any of the steps I don't explain well just follow his instructions here: [LAMP Stack with Flask](https://db.tannercrook.com/cit-225/lamp-stack-with-flask/). You can use PostgreSQL instead of MYSQL if you want.

This is the basic outline for deploying:

1. Setting up the LAMP server
2. Git Clone and Setting up the Environment
3. Create a `.env` File
4. Testing the Server

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
```bash
sudo apt install python3
sudo apt install python3-venv
sudo apt install python3-pip
```

### FTP (Optional but Recommended)
This step is optional, but is recommended for transferring files to or from the server.
```bash
sudo apt install vsftpd
sudo nano /etc/vsftpd.conf
```
uncomment the line: `write_enable=YES`

```bash
sudo service vsftpd restart
```

## 2 - Git Clone and Setting up the Environment
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

## 3 - Create a `.env` File
Now that you have the stack setup and your repository and your virtual environment. You want to create a `.env` file with the editor program of your choice or just use nano. This will allow you to store some variables that are supposed to be a secret like passwords, or usernames, etc. We will be using a `.env` to also store sensitive information.

0. In the project directory run: `sudo nano .env`
1. Add the following lines and replace the following portions as specified

    ```bash
    # change this to specify your MySQL Database
    SQLALCHEMY_DATABASE_URI=mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@localhost/zotbinsCE

    # this will be used for your flask app, change the following to a secure secret key
    SECRET_KEY=YOUR_HARD_TO_GUESSS_STRING

    # change this to specify where you want the image files to be uploaded to
    # for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
    UPLOAD_FOLDER=YOUR_UPLOAD_FOLDER_PATH

    # this is the base url used for the unit tests
    BASE_URL="http://127.0.0.1"
    ```
2. Close and save the file.
3. In `config.py` Turn off or turn on Debugging options. You should turn off debugging, when you want your server to run in production mode: `app.config['DEBUG'] = True # turn this off when not debugging.`

## 4 - Testing the Server
Alright, everything should be set now!
1. Reboot your server: `reboot`
2. Open the `unit_tests.py` file and change the following:
    ```bash
    BASEURL = "YOUR_URL"
    IPADDRESS = "YOUR_IP_ADDRESS"
    ```
3. Save and close the file
4. Run the unit tests
    ```bash
    su
    cd /var/www/app/app
    pytest -q unit_tests.py
    ```
5. If there are no error messages everything should be good!

# 🐪 LUMP Server Deployment

This solution stack uses Linux, Uvicorn, MySQL (or you could use PostgreSQL), and Python. Please refer to [Patrick's fork](https://github.com/patrickanguyen/zbce_api).

# PythonAnywhere deployment

[PythonAnywhere](https://www.pythonanywhere.com/) is a cloud service where you can host your Python website. It is very convenient since everything is already setup and there is a free plan as well.

*Warning: If you deploy it on PythonAnywhere it will be publicly available. Make sure to add tokens or password protect the webpage if you don't want strangers to access your information and add data to your database.* 😉



### 1. Create a new Web app

1. Make a [PythonAnywhere](https://www.pythonanywhere.com/) account and log in

   ![image-20210605122936959](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605122936959.png)

2. On the dashboard click **Open Web tab** on the middle right to navigate to the Web tab.

3. Click on **Add a new web app**  near the top left in the Web tab.

   ![image-20210605123116664](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605123116664.png)

4. Click **Next**.

   ![image-20210605123329199](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605123329199.png)

5. Click on **Manual configuration**

   ![image-20210605123438967](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605123438967.png)

6. Select **Python3.8** and then click **Next**

   ![image-20210605123515704](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605123515704.png)

7. Nice! Your web app should now be setup.

   ![image-20210605123611724](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605123611724.png)





   ## 2. Git Clone and Setting Up the Environment

   1. Go to **Consoles** and create a new **Bash** Console

      ![image-20210605124254142](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605124254142.png)

   2. In your bash terminal do a git clone and change directory.

      ```bash
      git clone https://github.com/zotbins/zbce_api.git
      cd zbce_api
      ```

   3. Create the python virtual environment:

       ```bash
       python3 -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt
       ```

   4. Create a folder for uploading your images and change the permissions

       ```bash
       mkdir <YOUR_UPLOAD_FOLDER_NAME>
       chmod 777 <YOUR_UPLOAD_FOLDER_NAME>
       ```

   ## 3. Create a .env Environment

   1. Find your MySQL database information in the **Databases** tab near the top right. Try to set a password for it.

      ![image-20210605131953424](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605131953424.png)

   3. Create your .env file

      ```bash
      # make sure you are in the same directory where
      # you cloned the git repo.
      nano .env
      ```

   3. Add the following lines and replace the following portions as specified.

      ```bash
      # change this to specify your MySQL Database
      SQLALCHEMY_DATABASE_URI=mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@YOUR_DATABASE_HOST_ADDRESS

      # this will be used for your flask app, change the following to a secure secret key
      SECRET_KEY="YOUR_HARD_TO_GUESSS_STRING"

      # change this to specify where you want the image files to be uploaded to
      # for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
      UPLOAD_FOLDER="YOUR_UPLOAD_FOLDER_PATH"

      # this is the base url used for the unit tests
      BASE_URL="http://<username>.pythonanywhere.com"
      ```

   4. Save the file using `ctrl + x`.

   5. Go back to the **Web** tab.

   6. Under the **Code** section, fill out the **Source code** path: `/home/<your_username>/zbce_api`

   7. Under the **Virtualenv** section fill out the path to your virtual environment:  `/home/<your_username>/zbce_api/venv`

   8. Edit the **WSGI configuration file** by clicking on the hyperlink next to it.

      ![image-20210605180326774](https://raw.githubusercontent.com/zotbins/zbce_api/formatted/guides/deployment_guide.assets/image-20210605180326774.png)

   9. Delete everything in the wsgi.py file and include the following lines. Make to include your PythonAnywhere username in place of `<YOUR_USERNAME`and your hard to guess string that you used in the `.env` file in place of `<YOUR_HARD_TO_GUESS_STRING>`.

      ```python
      import sys

      path = '/home/<YOUR_USERNAME>/zbce_api'
      if path not in sys.path:
          sys.path.append(path)

      from app import app as application  # noqa
      application.secret_key = '<YOUR_HARD_TO_GUESSS_STRING>'
      ```

   10. Save the file



   ## 4. Verify that Everything Works

   1. Open a PythonAnywhere bash terminal  

   2. Use `pytest` to verify that everything works

      ```bash
      # go into the repo directory if you aren't already
      cd zbce_api

      # activate the virutal environment if it isn't already activated
      source venv/bin/activate

      # run the unit_tests.py file
      pytest -q unit_tests.py      
      ```

   3. Yay! Congrats you got everything setup and running!🥳
