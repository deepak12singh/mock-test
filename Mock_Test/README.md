<<<<<<< HEAD
Here's your full `README.md` content, ready to copy and paste directly:

---

````markdown
# 🎓 Exam Prep Site – Your Gateway to Exam Success

An all-in-one Django-based web platform designed for students preparing for **CUET UG/PG** and other competitive exams. It offers centralized access to **mock tests**, **syllabus info**, **notifications**, **FAQs**, and **university links**, helping learners streamline their preparation and boost performance.

---

## 👨‍💻 Author

**Deepak Singh**  
📧 Email: [deepak12singh92@gmail.com](mailto:deepak12singh92@gmail.com)  
🔗 GitHub: [@deepak12singh](https://github.com/deepak12singh)
=======
Thanks for the schema! Based on the provided models (`User`, `Profile`, `QuestionUG`, `QuestionPG`, `ResultAnswer`, `ResultNotAttempt`, etc.), here’s a professional and complete `README.md` for your **Mock Test** Django project:

---

```markdown
# 🧠 Mock Test Platform

A Django-based online testing system designed to conduct **UG/PG level multiple-choice exams**, track attempts, evaluate answers, and generate performance reports. Ideal for students, institutions, and developers building educational tools.
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908

---

## 🚀 Features

<<<<<<< HEAD
- 🧠 CUET UG & PG focused mock test system
- 📚 Subject-wise syllabus and categorized question bank
- 🔔 Real-time notifications and exam updates
- 📊 User performance tracking and analytics
- 🔗 Direct university links and exam tips
- ✅ OTP-based user verification
- 📱 Mobile-friendly, responsive design
- 🛡️ Admin panel for full control and test management
=======
- 🔐 User registration, login, and OTP-based verification
- 🎓 UG and PG question sets with subject categorization
- ✅ Automatic evaluation of answers
- 📊 Result tracking with detailed reports (attempted, not attempted, score)
- 🧾 Admin log and session management
- 🖼️ Profile management with avatar upload
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908

---

## 🛠️ Tech Stack

<<<<<<< HEAD
| Layer           | Tech Used            |
|----------------|----------------------|
| Frontend       | HTML5, CSS3, JavaScript |
| Backend        | Python, Django (MVT) |
| Database       | SQLite (can scale to PostgreSQL/MySQL) |
| Hosting        | Google Cloud / Any cloud-compatible host |
| Version Control| Git & GitHub         |
=======
- **Backend**: Django (Python)
- **Database**: Default (SQLite/PostgreSQL supported)
- **Auth**: Django's AbstractUser with OTP and verification
- **Media**: Image support via `ImageField` for avatars

---

## 📂 Project Structure

```

Mock\_Test/
├── manage.py
├── Mock\_Test/            # Project settings and URLs
├── exam/                 # Main app with models, views, templates
│   ├── models.py         # User, Profile, Questions, Results
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
└── static/               # CSS/JS assets

````
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/deepak12singh/mock-test.git
cd mock-test/Mock_Test

<<<<<<< HEAD
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
=======
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908

# Install dependencies
pip install -r requirements.txt

<<<<<<< HEAD
# Migrate the database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start the server
=======
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908
python manage.py runserver
````

---

<<<<<<< HEAD
## 👨‍🎓 How It Works

1. 📝 **Register/Login**
   Users can register, verify OTP, and log in to access mock tests.

2. 🎯 **Select Exam Type (UG/PG)**
   Navigate between CUET UG & PG sections.

3. ❓ **Take Mock Tests**
   Attempt subject-wise MCQs. Results are calculated instantly.

4. 📊 **Track Progress**
   Dashboard shows attempted questions, skipped ones, and scores.

5. 🛠️ **Admin Features**
   Add/edit/delete questions, users, and control content via Django admin panel.

---

## 📁 Folder Structure

```
Mock_Test/
├── exam/               # Django app with models/views/templates
│   ├── models.py       # UG/PG questions, results, profile
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
├── static/             # CSS/JS/assets
├── media/              # Uploaded avatars, images
├── Mock_Test/          # Django project settings
└── manage.py
```

---

## 📊 Database Schema (Major Models)

* `User` (custom AbstractUser)
* `Profile` – Avatar, Bio, OTP, Verified
* `QuestionUG` / `QuestionPG` – MCQs with options & correct answers
* `ResultAnswer` – Stores attempted answers & score
* `ResultNotAttempt` – Stores skipped questions
* `Session`, `Permissions`, `Groups` – Auth modules

---

## 🔍 Sample Features in Action

* **Mock Test Page**: Subject-wise timed test interface
* **Progress Tracker**: Tracks previous scores and unattempted questions
* **Admin Panel**: Add/manage questions and view user progress
* **Syllabus Page**: Structured CUET UG/PG syllabus
* **Exam Tips**: Smart advice for test preparation
* **FAQ & Notification Pages**: Quick answers and updates

---

## 📌 Future Enhancements

* Support for **SSC**, **UPSC**, **Banking**, **MBA** exams
* Role-based dashboards for admin vs student
* Dynamic question generator with difficulty filter
* Integrated PDF download of performance reports
=======
## 👥 Models Overview

### 🧑 User & Profile

* Custom user model with `email`, `username`, `is_verified`
* Linked `Profile` with avatar, bio, OTP

### ❓ Questions

* `QuestionUG` and `QuestionPG` for different exam levels
* 4 options (`A`, `B`, `C`, `D`) and correct answer field

### 📝 Results

* `ResultAnswer`: For attempted questions
* `ResultNotAttempt`: For skipped/unattempted questions
* Marks, index, exam name, and subject tracking

---

## 🧪 Sample Usage

1. User signs up, verifies OTP
2. Selects exam (UG/PG and subject)
3. Answers MCQs
4. Submission evaluates:

   * Correct answers → `ResultAnswer`
   * Skipped → `ResultNotAttempt`
5. Result summary shown at end

---

## 🖼️ Screenshots (Optional)

*Add screenshots of test page, result page, profile, etc.*
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908

---

## 📜 License

<<<<<<< HEAD
MIT License © 2025 [Deepak Singh](https://github.com/deepak12singh)

---

## 🙌 Contributing

Contributions are welcome! Fork the repo and submit a pull request.

---

## 📸 Screenshots (Optional)

You can include these under `/docs/screenshots`:

* Home Page
* Mock Test Interface
* Result Tracker
* Admin Panel
* CUET UG/PG Pages

=======
This project is licensed under the **MIT License**.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.

```bash
# Fork the repo
# Make your changes
# Submit a PR 🚀
>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908
```

---

<<<<<<< HEAD
Let me know if you'd like this saved as a file, or want to include badges, deploy instructions, or Notion/portfolio formatting.
```
=======
## 👨‍💻 Author

**Deepak Singh**
📬 [GitHub](https://github.com/deepak12singh)

---


>>>>>>> ab980aa0514651d26dfdbc39289869b0a09dd908
