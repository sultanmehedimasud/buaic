<p float="left">
  <img alt="HTML" src="https://img.shields.io/badge/HTML-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/>
  <img alt="CSS" src="https://img.shields.io/badge/CSS-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/>
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
  <img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"/>
  <img alt="Bootstrap" src="https://img.shields.io/badge/Bootstrap-%2302569B.svg?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
  <img alt="Apache" src="https://img.shields.io/badge/Apache-%23D42029.svg?&style=for-the-badge&logo=apache&logoColor=white"/>
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-%2300f.svg?&style=for-the-badge&logo=mysql&logoColor=white"/>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge"/>
</p>

# BUAIC: BRAC University AI Club 🤖

This is the final project of our CSE471 course (System Analysis and Design). The idea of the project is members can register on the website to become part of the club's online community. Once registered, members gain access to various features such as event management, resource allocation, and user profile customization.

We have used a modular approach to build the website, breaking down the system into smaller, manageable modules. Each module focuses on specific functionality, making it easier to develop, test, and maintain. This approach also promotes code reusability and scalability, allowing for future expansion and enhancements.

By adopting a modular approach, we have ensured that the website is well-organized, efficient, and easy to navigate. It also facilitates collaboration among team members, as each module can be developed independently and integrated seamlessly into the overall system.

Our goal with this project is to demonstrate our understanding of system analysis and design principles while delivering a robust and user-friendly website for the BRAC University AI Club.

## Featuers 🔍

**User Registration:** Members can register on the website by providing necessary information such as name, email, and password. Upon registration, users gain access to the club's online platform.

**Role-based Authorization:** Secure authentication mechanisms ensure that only registered users can access the website's features. Users can log in securely using their credentials.

**Dashboard:** Upon logging in, users are greeted with a personalized dashboard that provides an overview of club activities, upcoming events, and notifications.

**Event Management:** Administrators can create, manage, and promote events through the website. Members can view event details, RSVP, and participate in club activities.

**Resource Allocation:** Members can book rooms or allocate resources for club activities through the website. This feature streamlines the process of reserving club facilities.

**Polling System:** The website includes a polling system where members can participate in surveys, vote on club-related matters, and provide feedback.

**Notification System:** A notification system keeps users informed about important updates, event reminders, and announcements from the club administrators.

**Profile Management:** Users can customize their profiles, update personal information, and manage account settings through an intuitive profile management interface.

**Forgot Password:** In case users forget their passwords, they can initiate a password reset process by providing their registered email address. A reset link is sent to their email for password recovery.

**Data Export:** Administrators can export club data, membership lists, event details, and other information into various formats such as CSV files for analysis and reporting purposes.

**Attendance System:** Administrators can track and manage attendance for club events through the website. A dedicated attendance system allows event organizers to record attendance either manually or using an automated method such as RFID scanning. This feature helps in maintaining accurate attendance records and evaluating member participation in club activities.

## Contributions 🧑🏻‍💻

### Sabbir Bin Abdul Latif (21201200)

- [x] Dynamic Navbar
- [x] Dynamic Bar Chart
- [x] Popups/Modals
- [x] Email Sending
- [x] Search and Filter (Members)
- [x] Sorting (Members)
- [x] Attendance System
- [x] Notification Toast

### Sultan Mehedi Masud (22101071)

- [x] User Registration
- [x] Password Hashing
- [x] Polling System
- [x] Event Management
- [x] OTP
- [x] Data Export
- [x] Current Requests

### Susmita Biswas (22101380)

- [x] Dashboard
- [x] Login and Logout
- [x] Role-based Authorization
- [x] Change Password
- [x] Edit Profile
- [x] Forgot Password
- [x] Resource Allocation

🔗 [Live link of the Application](https://buaic.onrender.com/)

Although, if you want to run the application to your server you can do that too. To set up the Flask web application along with a MySQL database, you can follow these guidelines. I've included steps for setting up the application environment, installing dependencies from the requirements.txt file, and restoring a MySQL database backup. To run this app to your machine just download the repository and follow the steps.

## Setup Documentation 📑

#### Prerequisites

- Python installed on your system.
- MySQL Server installed and running.
- Flask application files on your machine (app.py and others).
- The requirements.txt file.

#### Step 1: Setting Up a Virtual Environment

It's a good practice to use a virtual environment for Python projects. This isolates your project's dependencies from the system's Python environment.

1. Navigate to the project's app directory in the command line.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

#### Step 2: Installing Dependencies

Install the required packages using the requirements.txt file.

1. Ensure your virtual environment is activated.
2. Run:
   ```
   pip install -r requirements.txt
   ```

#### Step 3: Setting Up MySQL Database

1. Open MySQL command-line client or a GUI tool like MySQL Workbench/ PHP My Admin.
2. Create a new database for the application with name `buaic` in your machine.

#### Step 4: Configuring Your Flask Application

1.  Create a `.env` at the root folder of the application.
2.  Copy the following code to the file:

    ```
    DATABASE_URL=YOUR_DATABASE_URL_HERE
    MAIL_USERNAME=YOUR_EMAIL_HERE
    MAIL_PASSWORD=YOUR_EMAIL_APP_PASSWORD_HERE
    MAIL_DEFAULT_SENDER=YOUR_EMAIL_HERE
    ```

    Replace the placeholders `YOUR_DATABASE_URL_HERE`, `YOUR_EMAIL_HERE`, and `YOUR_EMAIL_APP_PASSWORD_HERE` with your actual database URL, email address, and email application password respectively.
    
    **DATABASE_URL:** This is the connection URL for your MySQL database. It typically follows the format mysql://username:password@hostname/database_name.
    
    **MAIL_USERNAME:** This is your email address used for sending emails.
    
    **MAIL_PASSWORD:** This is the password generated for your email application. If you're using Gmail, you may need to generate an app password.
    
    **MAIL_DEFAULT_SENDER:** This is the default sender email address for outgoing emails.

3.  Save the .env file.

By setting up the .env file with the correct database and email credentials, your application will be able to establish connections to the database and send emails as needed.

#### Step 5: Running The Flask Application

1. In the command line, navigate to your project's directory.
2. Set the environment variable FLASK_APP to your main application file (usually app.py):

- On Windows:
```

set FLASK_APP=app.py

```
- On macOS/Linux:
```

export FLASK_APP=app.py

```

3. Run the Flask app:
```

flask run

````

#### Step 6: Accessing the Application

- Open a web browser and navigate to http://127.0.0.1:5000 (or the URL provided in the terminal).
- Register as a new user. Then make the user admin from the database to access admin actions.

##### Additional Notes

- Always ensure your virtual environment is activated when working on the project.
- If you encounter any errors during the setup, check the error messages for guidance and ensure all prerequisites are met.

## Contributors ✨

Thanks goes to these wonderful people

<table>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/sabbirosa"><img src="https://media.licdn.com/dms/image/D5603AQEXlYoou3obDw/profile-displayphoto-shrink_400_400/0/1711444280181?e=1722470400&v=beta&t=fXEic4lkqk_btvtACrnC7C6mjiAQ9yKra1IqUv6c3i8" width="100px;" alt=""/>
    <br />
    <sub><b>Sabbir Bin Abdul Latif</b></sub></a>
    </td>
    <td align="center"><a href="https://www.linkedin.com/in/sultan-mehedi-masud"><img src="https://media.licdn.com/dms/image/D4E03AQFfa-Q4crrt3g/profile-displayphoto-shrink_400_400/0/1699899673258?e=1722470400&v=beta&t=K09ADqeu80hJdNfNL-AScaRGGETHagUk8WaCIRhYNWQ" width="100px;" alt=""/>
    <br />
    <sub><b>Sultan Mehedi Masud</b></sub></a>
    </td>
    <td align="center"><a href="https://www.linkedin.com/in/susmita-biswas-01a5b7267"><img src="https://media.licdn.com/dms/image/D5603AQH2Z94IGgE2Pg/profile-displayphoto-shrink_400_400/0/1704562312536?e=1722470400&v=beta&t=mQTP3og1hr2SCKSmfdAkjg3DKP1MeRrtK6SQ-yFJBxY" width="100px;" alt=""/>
    <br />
    <sub><b>Susmita Biswas</b></sub></a>
    </td>
  </tr>
</table>

## [Licenses](LICENSE) 📃
