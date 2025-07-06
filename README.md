# Three-Tier Contact Form App

This is a simple full-stack contact form web application deployed on an AWS EC2 instance. It demonstrates a three-tier architecture:

- **Frontend**: HTML form (`index.html`) for users to enter name, email, and message.
- **Backend**: Python Flask API (`app.py`) to receive data, validate it, send email via AWS SES, and store it in a SQLite database.
- **Database**: SQLite database (`contact.db`) to persist contact form submissions.

## 🛠 Features
- Input validation
- Email delivery using AWS SES
- Database storage
- Built and deployed on an EC2 instance
- Source code tracked with GitHub

## 💻 Tech Stack
- Python 3
- Flask
- SQLite
- HTML
- AWS EC2
- AWS SES

## 📁 Project Structure
three-tier-contact-app/
├── app.py
├── contact.db
└── templates/
└── index.html


## 🚀 How to Run Locally
```bash
python3 app.py
