# ThreadFusion - A Forum Website

***ThreadFusion*** is a dynamic and responsive forum website designed and implemented as the final project for CS50’s Web Programming with Python and JavaScript. 

It provides a platform for users to engage in discussions, ask questions, and explore topics of interest through a well-organized tagging system.
The application uses Django for the backend and HTML, SASS/CSS, and JavaScript for the frontend.

---

## Tech Stack
**Backend**
- Python
- Django
- Django ORM

**Frontend**
- HTML
- SASS/CSS
- JavaScript
- Quill WYSIWYG Editor

**Database & Storage**
- Neon PostgreSQL — Production database
- Cloudinary — User-uploaded media storage

**Deployment**
- Docker — Application containerization
- Gunicorn — Production WSGI server
- Render — Application hosting
- WhiteNoise — Static file serving

---
## How to run
1. Clone the repository using:
   ```bash
   git clone https://github.com/RajDeshmukh2001/threadfusion.git
   ```
2. Navigate into the project directory:
   ```bash
   cd threadfusion
   ```
3. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   ```
   Windows:
   ```bash
   .venv\Scripts\activate
   ```

4. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root and configure the required environment variables:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_URL=your_neon_database_connection_string
   CLOUDINARY_URL=your_cloudinary_url
   ```
6. Apply the existing database migrations:
   ```bash
   python manage.py migrate
   ```
7. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
8. Open the application in your browser:
   ```bash
   http://localhost:8000/
   ```

9. Optional: Django Admin - Create a superuser if you want to access Django Administration:
    ```bash
   python manage.py createsuperuser
   ```

### Docker
1. Build the Docker image:
   ```bash
   docker build -t threadfusion .
   ```

2. Run the container:
   ```bash
   docker run --rm --name threadfusion-app --env-file .env -p 8000:8000 -e PORT=8000 threadfusion
   ```

3. Then open:
   ```bash
   http://localhost:8000/
   ```

### Deployment

ThreadFusion is deployed using:
- Docker for containerization
- Render for application hosting
- Neon PostgreSQL for the production database
- Cloudinary for persistent media storage
- Gunicorn as the production WSGI server
- WhiteNoise for static files

>Production secrets and database credentials are configured through environment variables.

---
## Features

* __User Authentication__: Registration, login, logout, password validation, and authenticated user actions.
* __Questions & Answers__: Users can ask questions and post detailed answers using a rich-text editor.
* __Rich-Text Editing__: Quill WYSIWYG editor for formatting questions and answers, including code snippets, links, images, and other formatting options.
* __Comments__: Users can comment on answers and participate in discussions.
* __Tags & Search__: Questions can be categorized using tags and searched by title, description, or tags.
* __User Profiles__: Users can create and update profiles with profile images and social links.
* __Follow System__: Users can follow other users and view their activity.
* __Likes__: Users can like answers.
* __Pagination__: Large collections of questions, answers, and comments are paginated for better usability.
* __User Feedback__: Toast notifications and confirmation dialogs provide feedback for important actions.