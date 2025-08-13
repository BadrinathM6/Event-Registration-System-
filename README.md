# Event Registration System

A **Django-based event registration system** that allows users to create events, register attendees, and manage event capacity with comprehensive filtering and sorting capabilities.

---

## 🚀 Features

- **Event Management**: Create, view, and cancel events
- **Registration System**: Attendee registration with duplicate email validation
- **Capacity Management**: Automatic capacity checking and waitlist functionality
- **Filtering & Sorting**: Search, filter by status, and sort events
- **Statistics Dashboard**: View event statistics and registration data
- **Responsive UI**: Mobile-friendly Bootstrap interface
- **Pagination**: Efficient event browsing
- **Validation**: Comprehensive form and model validation

---

## 🛠 Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+
- `pip`

### 1️⃣ Clone the Repository
```
git clone <repository-url>
cd event_registration_system
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run Development Server
```bash
python manage.py runserver
```

### Access the Application
- **Main Application**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📌 Usage Examples

### Creating an Event
1. Navigate to **"Create Event"** from the navigation
2. Fill in event details with a **future date**
3. Set capacity (**minimum 1**)
4. Submit the form

### Filtering Events
- **Search**: Use the search box to find events by title, description, or location
- **Status Filter**: Filter by Active, Cancelled, or Completed events
- **Sorting**: Sort by date, title, or capacity (ascending/descending)

### Registering for Events
1. Click **"View Details"** on any active event
2. Click **"Register Now"** if spots are available
3. Fill in attendee information
4. Submit registration

### Event Statistics
- View overall statistics dashboard
- See registration rates and event performance
- Monitor capacity utilization

---

## ✅ Key Features Demonstrated
- Event Creation: Future date validation
- Filtering & Sorting: Multiple filter options with persistence
- Registration System: Duplicate email prevention and capacity management
- Event Cancellation: Prevents new registrations
- Statistics View: Comprehensive event analytics
- Responsive Design: Mobile-friendly interface
- Pagination: Efficient data browsing
- Form Validation: Client and server-side validation

---

## 📂 Project Structure
```
event_registration_system/
├── event_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── base.html
│   └── events/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📌 Assumptions
- Events with past dates cannot accept registrations
- Cancelled events block all new registrations
- One registration per email per event
- Waitlist functionality when capacity is exceeded
- Bootstrap and Font Awesome loaded via CDN
- SQLite database for development simplicity

---

## 🔮 Future Enhancements
- Email notifications for registrations
- Payment integration
- Event categories and tags
- Advanced reporting and analytics
- REST API endpoints
- User authentication system
