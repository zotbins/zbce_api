# ZBCE API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a proof-of-concept API repository that allows users to store waste related metrics such as bin fullness, waste weight, bin usage, and waste images. Thank you to everyone who contributed! 🙌

![GitHub Contributors Image](https://contrib.rocks/image?repo=zotbins/zbce_api)


# 📔 Table of Contents
- [ZBCE API](#zbce-api)
- [📔 Table of Contents](#-table-of-contents)
- [📰 Deployment](#-deployment)
    + [Prerequisites](#prerequisites)
    + [Deployment Guides](#deployment-guides)
- [🔨 Development](#-development)
    + [Cloning ZBCE Repository](#cloning-zbce-repository)
    + [Setting up Python](#setting-up-python)
    + [Installing MySQL](#installing-mysql)
    + [Creating a '.env' file](#creating-a--env--file)
    + [Creating Tables in Database](#creating-tables-in-database)
    + [Running the Server](#running-the-server)
- [📚 Database Interface Tool](#-database-interface-tool)
- [🤝 Contributing](#-contributing)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# 📰 Deployment
If you have the Prerequisites listed below you can fully deploy this project. Since we use an ORM (Object-relational Mapping), you can use different SQL databases such as PostgreSQL or MySQL. If you only wish to just work on a development version, please refer to the [Development](#-development) section below.

### Prerequisites
- [Ubuntu 20.04 Operating System](https://ubuntu.com/)
    - other versions might be alright, but have not been tested
- Basic understanding of the Linux Command Line

### Deployment Guides

If you're ready to deploy please follow this [deployment guide](https://github.com/zotbins/zbce_api/blob/formatted/guides/deployment_guide.md).

The [deployment guide](https://github.com/zotbins/zbce_api/blob/formatted/guides/deployment_guide.md) has instructions for the following:

- Self-Hosted LAMP (Linux, Apache, MySQL, Python)
- Self-Hosted LUMP (Linux, Uvicorn, PostgreSQL, Python)
- PythonAnywhere Deployment

# 🔨 Development
This section is for setting up the development environment only, which takes less steps and does not require Ubuntu. However, development should not be used in a production environment. For a more deployed solution, please refer to the [Deployment](#-deployment) section above.  

This is the basic outline for setting up your development environment:
1. Cloning Repo in Workspace
2. Setting up Python
3. Installing MySQL
4. Creating a '.env' file
5. Creating Tables in Database
6. Running the Server

### Cloning ZBCE Repository
Following the instructions listed, you will be able to clone the ZBCE Repository; however, if you would like a more thorough guide/step-by-step, visit the GitHub Docs guide for cloning a repository: https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository.

1. Open an empty folder (or the folder you would like to clone the repo into) and navigate to that folder using a terminal
2. In your terminal, type in `git clone` add a space then paste https://github.com/zotbins/zbce_api.git (Note: you can also find the repo's HTTP URL yourself by clicking the green "Code" button on the top right corner of the ZBCE repo)
3. Run the command

After these steps, you should be able to access the ZBCE repo from your computer.

### Setting up Python
1. Download the appropriate Python version for your OS from https://www.python.org/downloads/
2. Unzip the python file and follow the Python's setup instructions given

Once Python is downloaded on your device, you will need to create a virtual environment. For a more in depth explanation of creating a virtual Python environment, visit https://docs.python.org/3/tutorial/venv.html

1. In your terminal type and run `python3 -m venv venv`
2. Activate the virtual environment
   For Windows type and run `venv\Scripts\activate.bat`
   For MacOS or Linux type and run `source venv/bin/activate`
3. Install packages within the virtual environment with `pip install -r requirements.txt`

### Installing MySQL
1. Download the MySQL workbench and server DB for your OS using https://dev.mysql.com/downloads/workbench/
2. Unzip the msi files and follow the setup instructions as given

Once MySQL is installed (workbench and server), you will have to connect to the ZBCE Database.
1. Open MySQL and ‘Start MySQL Server’
2. Open MySQLWorkbench
3. Create a new MySQL Connection
   Connection Name: zotbinsCE
   Hostname: 127.0.0.1
   Port: 3306
   Username: root
   Hit ok and connect to this server
4. Create a new SQL tab:
5. Run this query once to create the database (click on lightning bolt to run):
   CREATE DATABASE zotbinsCE;

### Creating a '.env' file
1. Create an .env file in the same directory
2. Input this into the .env file and change the parameters to match your username and password
    ```bash
    # change this to specify your MySQL Database
    SQLALCHEMY_DATABASE_URI=mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@localhost/zotbinsCE

    # this will be used for your flask app, change the following to a secure secret key
    SECRET_KEY=YOUR_HARD_TO_GUESSS_STRING

    # change this to specify where you want the image files to be uploaded to
    # for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
    UPLOAD_FOLDER=YOUR_UPLOAD_FOLDER_PATH

    # this is the base url used for the unit tests
    BASE_URL="http://127.0.0.1" # replace with your server name
    ```
3. Save your changes

### Creating Tables in Database
1. Create the tables in your database by running `python create_tables.py`
2. If set up successfully, you should see new tables added in mySQL Workbench

### Running the Server
1. Type and run `python app.py` into your terminal
2. Check where to access your API by looking at “Running on” section on the command line
3. Use Postman for further tests if desired

Congratulations you successfully set up your development environment! 🥳

# 📚 Database Interface Tool

The database interface tool is the python file called `db_interface_tool.py` that lets users interact with a simple command line interface to drop and recreate tables. It also lets users add bins to the Bin Info table in the database as seen in the database schema image below.

![Database Schema](https://user-images.githubusercontent.com/33404602/104277024-ef173f00-545a-11eb-8776-26567a18be8c.png)

Run the script to use the tool:

```bash
# You need to make sure that either your development or deployment environment is already setup
# make sure you activate your virtual environment first
source venv/bin/activate

# run script
python db_interface_tool.py
```

# 🤝 Contributing

Here are some following ways you can contribute:

- Make a pull request!
- Join our [Discord](https://discord.gg/mGKVVpxTPr) server and contribute to our growing community
- Submit bugs by opening an issue on our [Github](https://github.com/zotbins). Please make sure that bugs are reported in detail and is reproducible.
- Write some documentation for a repository and we can add it to our GitHub Wiki Page
- Look for open issues on our repositories
- Suggest new features in our Discord Server
- Contribute to our crowd-sourcing projects. Occasionally, we will have certain projects that require crowd-sourced data, and would love people to help.
- Submit user feedback through feedback forms or polls in our Discord community
- Lookout for more requests for help on our Discord server
