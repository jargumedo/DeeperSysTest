# DeeperSysTest

# User Management Project

This project consists of a user management application that utilizes a backend in Python with Flask and a user interface in Vue.js. The goal is to allow the creation, viewing, editing, and deletion of users in a simple and efficient manner.

## Prerequisites

Before you begin, ensure that you have the following components installed on your machine:

- Python 3.x
- Node.js and npm (Node Package Manager)
- MongoDB (local or in the cloud, such as MongoDB Atlas)

## Project Structure

The project is divided into two main parts:

- **Backend**: This is the REST API that handles operations with the database.
- **Frontend**: This is the user interface that interacts with the backend.

## Installation and Setup

### 1. Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_NAME>

```

### 2. Set Up the Backend

a. Navigate to the Backend Directory

Go to the directory where the backend code is located:

```bash
cd api

```


b. Install Dependencies
Install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

c. Configure MongoDB Connection
Make sure to have the correct configuration file to connect your application to MongoDB. Review the connection code in parser.py and adjust the connection URL if necessary.

d. Run the Backend
Finally, run the backend server with the following command:

```bash
python app.py
```

The backend should be running at http://localhost:4000.

3. Set Up the Frontend
   a. Navigate to the Frontend Directory
   Go to the directory where the frontend code is located:

```bash
cd frontdeeper
```

b. Install Dependencies
Install the necessary dependencies using npm:

```bash
npm install
```
c. Run the Frontend
Run the frontend server with the following command:

```bash
npm run serve
```

The frontend should be running at http://localhost:8080.

# Using the Application
Access the User Interface: Open your browser and go to http://localhost:8080.
Create a User: Click on the "Create User" button to open the user creation form.
View Users: The list of users will automatically display. You can click on a user's name to see more details.
Update or Delete Users: Use the "Update" and "Delete" buttons in the table to modify or remove users.