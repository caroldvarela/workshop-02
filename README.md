# Workshop # 2 ETL

# Introduction
This project demonstrates how to build an ETL (Extract, Transform, Load) pipeline using **Apache Airflow**. The ETL pipeline extracts information from three different data sources: a **CSV file**, and a **PostgreSQL database**. After performing transformations, the data is merged and stored into **Google Drive** as a CSV file and loaded in a database. The final step involves creating a **dashboard** to visualize the data stored in the database.

![image](https://github.com/caroldvarela/images/blob/main/workshop2.png)

## Data Sources
1. **Spotify Dataset 🎶🟩**: Data to be extracted, transformed, and loaded using Python and Apache Airflow.
2. **Grammys Dataset 🏆**: To be loaded into the database, read, transformed, and merged with the Spotify dataset using Airflow.

## Key Features

- **ETL Process**: Extracts data from multiple sources, performs transformations, and loads it into a database and CSV format.
- **Database Integration**: Data is stored in a **PostgreSQL** database for further visualization.
- **Dashboard**: Visualizes the processed data using charts. All data used in the reports is retrieved from the database, not from CSV files.

## Project Structure

```plaintext
├── dags
│   ├── dag.py
│   └── etl.py
├── data
│   ├── spotify_dataset.csv
│   └── the_grammy_awards.csv
├── db
│   └── db_connection.py
├── models
│   └── model.py
├── notebooks
│   ├── 000_data_migration_grammy.ipynb
│   ├── 001_EDA_spotify.ipynb
│   └── 002_EDA_grammy.ipynb
├── src
│   ├── extract
│   │   ├── read_grammy.py
│   │   └── read_spotify.py
│   ├── transform
│   │   ├── transform_grammy.py
│   │   └── transform_spotify.py
│   ├── merge
│   │   └── merge.py
│   ├── load
│   │   └── load_to_database.py
│   └── store
│       └── store.py
```

## Prerequisites

- **Python 3** 🐍
- **Apache Airflow** 🔄 
- **PostgreSQL** 🗃️
- **Virtual environment** 🌍

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/caroldvarela/workshop-02.git
   cd workshop-02
2. **Create a Virtual Environment**  
   Create a Python virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
3. **Install the Required Dependencies**  
   Run the following command to install the necessary packages:
   ```bash
   pip install -r requirements.txt

I will also give you a brief guide on how to install what you need!

## PostgresSQL
- **Set Up PostgreSQL**  
   Install and configure PostgreSQL:
   ```bash
   sudo apt update
   sudo apt-get -y install postgresql postgresql-contrib
   sudo service postgresql start
   sudo apt-get install libpq-dev python3-dev

- **Log in to PostgreSQL**  
   Run the following commands to log in:
   ```bash
   sudo -i -u postgres
   psql

- **Create a New Database and User**  
   Run the following SQL commands to create a new user and database:
   ```sql
   CREATE USER <your_user> WITH PASSWORD '<your_password>';
   ALTER USER <your_user> WITH SUPERUSER;
   CREATE DATABASE workshop2 OWNER <your_user>;
   
- **Configure PostgreSQL for External Access (Optional for PowerBI)**  
   The PostgreSQL configuration files are generally located in `/etc/postgresql/{version}/main/`
   Edit the `postgresql.conf` file to allow external connections
   
   ```bash
   listen_addresses = '*'
   ssl = off
   
-  **Edit the pg_hba.conf File**  
   Allow connections from your local IP by adding the following line:
   ```plaintext
   host    all             all             <your-ip>/32         md5

- **Set Up pgAdmin 4 (Optional)**  
   To install pgAdmin 4, run the following commands:
   ```bash
   sudo apt install curl
   sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
   sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
   sudo apt install pgadmin4


## Configure Google Drive API

- **Go to the Google Cloud Console:**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/).

- **Create a New Project:**
   - Click on the project dropdown and select "New Project."

- **Enable the Google Drive API:**
   - In the API Library, search for "Google Drive API" and enable it.

- **Create OAuth 2.0 Client IDs Credentials:**
   - Go to the "Credentials" tab and click on "Create Credentials."
   - Select "OAuth client ID."
   - Configure the consent screen if prompted, then choose "Desktop app" or the appropriate option for your use case.

- **Download the `credentials.json` File:**
   - Once created, download the credentials file and rename it to `service_account.json`.

- **Place the File in the Project Directory:**
   - Move the `service_account.json` file to your project directory.

- **Create a folder in your Drive and share it with your project’s service account as an editor:**  
   - In the link of the folder, you’ll find the `PARENT_FOLDER_ID`. 

   ![image](https://github.com/caroldvarela/images/blob/main/apidrive.png)
  

## Configuration of the .env File

- **Create a .env File**  
   Create a `.env` file with the following configuration:
   ```plaintext
   PGDIALECT=postgresql
   PGUSER=<your_user>
   PGPASSWD=<your_password>
   PGHOST=localhost
   PGPORT=5432
   PGDB=workshop2
   WORK_DIR=<your_working_directory>

   # Google Drive API
   SERVICE_ACCOUNT_FILE=./service_account.json
   PARENT_FOLDER_ID=<your_google_drive_folder_id>


## Airflow

 - **Create the Airflow Directory:**  
   ```bash
   mkdir airflow
   ```

 - **Set the Airflow Home Environment Variable:**  
   ```bash
   export AIRFLOW_HOME=~/airflow
   ```

 - **Configure the airflow.cfg File**  
   The `airflow.cfg` file is located in the directory specified by `AIRFLOW_HOME`. To modify the `dags_folder`, set it to the path of your `dag.py` file:
   ```ini
   dags_folder = /path/to/your/dag
   ```

 - **Initialize the Airflow Database:**  
   ```bash
   airflow db init
   ```

 - **Start Airflow:**  
   ```bash
   airflow standalone
   ```

You can now access the Airflow UI using the generated **credentials**.

5. **Run the Airflow DAG**  

   - Navigate to the **Airflow UI**, enable the DAG, and trigger it manually.
   
   - View the generated CSV files in **Google Drive** and the data in your **PostgreSQL** database.
   
   - Visualize the data using the dashboard created from the data stored in the database.

---

# Connect Power BI to PostgreSQL

Do you want to create your own dashboard? You’ll probably need to do this:

## Steps to Configure the Bridged Adapter

1. **Open VirtualBox:**
   - Start VirtualBox on your computer.

2. **Select the Virtual Machine:**
   - From the list of virtual machines, select the one you want to configure.

3. **Open Settings:**
   - Click the "Settings" button (the gear icon) at the top.

4. **Go to the Network Tab:**
   - In the settings window, select the "Network" tab.

5. **Enable the Adapter:**
   - Check the box "Enable Network Adapter."

6. **Select the Adapter Type:**
   - In the "Attached to" field, select "Bridged Adapter."



## Open Power BI

7. **Start Power BI Desktop** on your Windows machine.

8. **Get Data:**
   - On the home screen, click "Get Data."
     
   ![image](https://github.com/caroldvarela/images/blob/main/Dashboard_1.png)
9. **Select PostgreSQL:**
   - In the "Get Data" window, choose "PostgreSQL Database" and click "Connect."

   ![image](https://github.com/caroldvarela/images/blob/main/Dashboard_2.png)
10. **Configure the Connection:**
    - In the connection dialog, enter the following information:
      - **Server:** `server_ip:port` (by default, `localhost:5432` if connecting to your local machine).
      - **Database:** The name of the database you want to connect to.
   ![image](https://github.com/caroldvarela/images/blob/main/workshop2-1.png)

11. **Authentication:**
    - Select the authentication method "Database" and enter your PostgreSQL username and password.
   ![image](https://github.com/caroldvarela/images/blob/main/workshop2-2.png)
12. **Load Data:**
    - Click "Connect" and if the connection is successful, you will see the available tables in your database. Select the tables you want to import and click "Load."
