# 🎓 Exam Prep Site – Your Gateway to Exam Success

**Live Demo:** [https://mocktest.deepaksingh.space](https://mocktest.deepaksingh.space)
**Source Code:** [GitHub Repository](https://github.com/deepak12singh/mock-test)

---

## 📚 Overview

**Exam Prep Site** is an advanced web-based platform for conducting mock tests and online examinations for both undergraduate (UG) and postgraduate (PG) students. It allows users to attempt time-bound multiple-choice exams with features like:

* User authentication
* Exam question randomization
* Result tracking
* Dashboard with attempt history
* Admin panel for managing exams, results, and questions

---

## ✨ Features

* 🧠 UG & PG mock test support
* 🔐 Secure login & session-based exam attempts
* 📊 Auto-evaluated results with performance analysis
* 📝 Admin portal to manage questions and users
* 💾 Saves code answers and MCQ choices in real-time (for coding exams)
* ☁️ Deployed using Docker, Traefik, and Let's Encrypt for HTTPS

---

## 🛠️ Technologies Used

* **Backend**: Django 5.x
* **Frontend**: HTML, Bootstrap, jQuery
* **Database**: PostgreSQL
* **Auth**: Django’s built-in authentication
* **Containerization**: Docker & Docker Compose
* **Reverse Proxy & SSL**: Traefik v3 + Let's Encrypt
* **Deployment**: Ubuntu 24.04 server (GCP VM)

---

## 📂 Project Structure

```
mock-test/
├── Mock_Test/                # Django project
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                     # Main app: exams, models, views
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── static/
├── media/                    # Uploaded files (if any)
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🧪 Local Setup

### 🔧 Requirements

* Python 3.10+
* Docker & Docker Compose
* PostgreSQL or SQLite (local)

### 🐳 Run with Docker

```bash
git clone https://github.com/deepak12singh/mock-test.git
cd mock-test

cp .env.example .env  # create your own environment config

# Run docker containers
docker-compose up --build
```

Visit `http://localhost` (or your server IP/domain) to view the site.

### 🐍 Run Locally (No Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 🔐 Admin Access

Go to: `https://mocktest.deepaksingh.space/admin`
To create superuser:

```bash
python manage.py createsuperuser
```

---

## 📌 Environment Configuration

`.env` file example:

```env
DEBUG=False
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=mocktest.deepaksingh.space,localhost,127.0.0.1
POSTGRES_DB=mocktest_db
POSTGRES_USER=mockuser
POSTGRES_PASSWORD=strongpassword
```

---

## 🌐 Deployment Architecture

```
[ Internet ]
     |
     v
[ Traefik (HTTPS) ]
     |
     v
[ Docker Containers ]
 ├── Django App
 └── PostgreSQL DB
```

* **Traefik** handles SSL (Let's Encrypt) and routing
* Auto-renewal of HTTPS certificates
* Dockerized and isolated services

---

## 📊 Future Enhancements

* Add timer-based question-by-question autosave
* Code editor integration for coding sections
* Google/GitHub social login
* Student performance analytics dashboard

---

## 🤝 Contribution

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -m 'Add xyz feature'`)
4. Push to the branch (`git push origin feature/xyz`)
5. Open a Pull Request

---

## 🧑‍💻 Author

**Deepak Singh**
📧 [deepak12singh92@gmail.com](mailto:deepak12singh92@gmail.com)
🌐 [GitHub: deepak12singh](https://github.com/deepak12singh)

---

## ⚖️ License

This project is licensed under the [MIT License](https://github.com/deepak12singh/mock-test/blob/main/LICENSE).
