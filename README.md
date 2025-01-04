🚀 UAV Management System
A Django-based UAV (Unmanned Aerial Vehicle) Management System for managing and assembling UAV components, including wings, fuselages, tails, and avionics. This project utilizes PostgreSQL as its database and is containerized using Docker and Docker Compose.

📑 Table of Contents
Overview
Tech Stack
Setup Instructions
Environment Variables
Usage
Deployment
Future Improvements
Author
📊 Overview
This system allows:

📦 Management of UAV components: Wings, Fuselages, Tails, and Avionics.
🛠️ Assembly of UAVs from available components.
📊 Detailed insights and availability status for each component.
🔒 Role-based access control to manage permissions effectively.
The project supports both development and production environments with Docker Compose for easy deployment.

💻 Tech Stack
Backend: Django, Django REST Framework
Database: PostgreSQL
Frontend: HTML, CSS, Bootstrap
Containerization: Docker, Docker Compose
🛠️ Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/ecegozutok/UAV.git
cd UAV/website
2. Build and Run Docker Containers
bash
Copy code
docker-compose up --build
This will:

Create and run PostgreSQL and Django containers.
Apply database migrations.
Collect static files.
3. Access the Application
Open your browser and navigate to: http://localhost:8000
⚙️ Database Configuration
The database settings are pre-configured in settings.py:

python
Copy code
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "uavdb",
        "USER": "uavuser",
        "PASSWORD": "uavpassword",
        "HOST": "db",
        "PORT": "5432",
    }
}
Database Name: uavdb
Username: uavuser
Password: uavpassword
Host: db (Docker service name)
Port: 5432
Make sure these match your docker-compose.yml file.

🚀 Usage
1. Access Django Admin
URL: http://localhost:8000/admin
Default credentials: (create a superuser if needed)
bash
Copy code
docker-compose exec web python manage.py createsuperuser
2. API Endpoints
/api/wing_counts/: Check wing availability.
/api/fuselage_counts/: Check fuselage availability.
/api/tail_counts/: Check tail availability.
/api/avionics_counts/: Check avionics availability.
3. Stop the Containers
bash
Copy code
docker-compose down
📦 Static Files
Static files are collected in the /staticfiles directory inside the container:

Static Root: /app/staticfiles
In production, ensure a web server like Nginx serves these static files efficiently.

🚀 Deployment
1. Build the Docker Image
bash
Copy code
docker-compose build
2. Run Containers in Detached Mode
bash
Copy code
docker-compose up -d
3. Access Application
Open: http://localhost:8000
