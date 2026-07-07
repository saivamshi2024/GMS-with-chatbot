# Grocery Management System with AI Chatbot

## 📌 Description
This project is a web-based Grocery Management System developed using Django. It allows users to browse products, manage categories, add products to the cart, and efficiently manage grocery inventory. The system also includes an AI-powered chatbot that assists users by answering product-related queries and providing information about the grocery store.

---

## 🚀 Features
- User Login & Authentication
- Product Management
- Category Management
- Product Search
- Shopping Cart Functionality
- Order Management
- Admin Dashboard
- Image Upload for Products
- AI Chatbot Integration (Groq API)
- Responsive User Interface

---

## 🛠 Tech Stack
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Python, Django
- **Database:** SQLite3
- **AI Integration:** Groq API (LLM)

---

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/saivamshi2024/GMS.git
```

### 2. Navigate to the project directory

```bash
cd GMS
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Add Groq API Key

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_api_key_here
```

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

### 9. Open in Browser

```
http://127.0.0.1:8000/
```

---

## 📁 Folder Structure

```
grocery/
├── grocery/
│
├── .venv/                         # Python virtual environment
│
├── grocery_app/                   # Main Django application
│   ├── management/                # Custom management commands
│   ├── migrations/                # Database migrations
│   ├── static/                    # CSS, JS, Images
│   ├── templates/                 # HTML templates
│   │   ├── chatbot.html
│   │   └── ...
│   │
│   ├── chatbot/                   # AI Chatbot Module
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── database.py
│   │   ├── prompts.py
│   │   ├── utils.py
│   │   └── config.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── forms.py
│
├── grocery_system/                # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
│   ├── categories/
│   └── products/
│
├── static/
│   ├── css/
│   │   └── chatbot.css
│   ├── js/
│   │   └── chatbot.js
│   └── images/
│
├── .env                           # Environment Variables
├── requirements.txt
├── db.sqlite3
└── manage.py

```

---

## 🤖 AI Chatbot Workflow

```
User
   │
   ▼
chatbot.html
   │
   ▼
chatbot.js
   │
   ▼
views.py
   │
   ▼
chatbot.py
   │
   ├── database.py
   │       │
   │       ▼
   │   SQLite Database
   │
   ▼
Groq API
   │
   ▼
AI Response
   │
   ▼
views.py
   │
   ▼
chatbot.js
   │
   ▼
chatbot.html
```

---

## 📸 Screenshots

### Home Page

(Add Screenshot Here)

### Product Management

(Add Screenshot Here)

### Shopping Cart

(Add Screenshot Here)

### AI Chatbot

(Add Screenshot Here)

---

## 👨‍💻 Author

**Sai Vamshi**

- GitHub: https://github.com/saivamshi2024
- Project: Grocery Management System with AI Chatbot
## 📸 Screenshots
<img width="1849" height="871" alt="image" src="https://github.com/user-attachments/assets/99f65287-2883-41f5-9460-1acccaf5aa48" />
<img width="1834" height="869" alt="image" src="https://github.com/user-attachments/assets/70063d26-2ea0-44c4-a263-028cb183eb0b" />
<img width="1844" height="740" alt="image" src="https://github.com/user-attachments/assets/d696e32f-31c5-49f2-a027-bfb9c19b4c73" />


---

## 👨‍💻 Author
Nidhish Kamboj
