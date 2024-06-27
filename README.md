![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/474b9cf0-bbfc-4d4f-9b56-68577453fcff)# Flask Blog with MySQL Integration

## Overview

This project is a fully-functional blog application built using Flask, Bootstrap, and MySQL. The blog features a mobile-friendly layout, a user login system, a dashboard for managing blog posts and image uploads, and a contact page where users can send inquiries directly to the blog owner.

## Screenshots
### Home Page
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/809d358b-df98-4005-a778-3c6ce6b99c9a)
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/4aa1bb0c-d779-4d51-959b-5d4ad6c24a74)
### About Me
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/cc33adfe-bcfa-42b9-a451-349c8794a1f9)

### Contact Page
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/e04c9407-af4f-4308-bbe8-0e432e8a2688)
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/977f25a8-309b-4919-8eb0-dcf59f472162)
### Admin login
![image](https://github.com/swagatx1/Blog-Webapp/assets/113201534/70f9a2ed-bffa-43db-aec5-10d1430f3f4c)


## Features

- **Mobile-Friendly Design**: Responsive layout using Bootstrap to ensure optimal user experience across various devices.
- **Secure User Authentication**: Allows users to log in and access a dashboard for managing blog posts.
- **Dashboard**: Users can add, edit, and delete blog posts from a user-friendly interface.
- **Image Uploads**: Users can upload images to be included in their blog posts.
- **Contact Page**: A dedicated page for users to send questions and inquiries, with the messages being emailed to the blog owner.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **Bootstrap**: A front-end framework for developing responsive and mobile-first websites.
- **MySQL**: A relational database management system used for storing blog posts and user information.
- **HTML/CSS**: Markup and styling for the blog pages.
- **Flask-Mail**: A Flask extension for sending emails.

## Where I Learned to Make This Blog Website

[YouTube Playlist](https://youtube.com/playlist?list=PLu0W_9lII9agAiWp6Y41ueUKx1VcTRxmf&si=BoI5LSL1teS5I80u)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/flask-blog.git
    cd flask-blog
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Ensure you have MySQL installed and running.
    - Create a database and a user with the appropriate privileges.
    - Update the `config.json` file with your database credentials.

5. **Configure the application**:
    - Fill in the required parameters in the `config.json` file, including email credentials for Flask-Mail.

6. **Initialize the database**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. **Run the application**:
    ```bash
    flask run
    ```

## Configuration

The `config.json` file should include the following parameters:

```json
{
    "param": {
        "secret_key": "your-secret-key",
        "gmail_user": "your-email@gmail.com",
        "gmail_password": "your-email-password",
        "local_server": true,
        "local_uri": "mysql://username:password@localhost/db_name",
        "prod_uri": "mysql://username:password@prod-db-host/db_name",
        "no_of_posts": 5,
        "admin_user": "admin",
        "admin_password": "admin-password",
        "upload_location": "path/to/upload/directory"
    }
}
