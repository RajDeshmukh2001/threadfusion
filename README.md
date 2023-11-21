Project Name: ThreadFusion
- - - -

### Overview ###
_ThreadFusion_ is a dynamic and responsive forum website designed and implemented as the final project for CS50’s Web Programming with Python and JavaScript. It provides a platform for users to engage in discussions, ask questions, and explore topics of interest through a well-organized tagging system.
_ThreadFusion_ stands out through its meticulously organized project structure. Django powers the backend, while the frontend leverages JavaScript for dynamic content rendering and templating with HTML and SASS/CSS.

### Distinctiveness ###
* __User Interaction__: The forum provides a dynamic and interactive user experience. Users can not only ask questions but also actively participate in discussions, fostering a sense of community.

* __RichText Editor__: ThreadFusion incorporates the QuillField WYSIWYG editor, enhancing the user experience when composing questions and answers. This feature provides users with a _What You See Is What You Get (WYSIWYG)_ editing experience, allowing them to format text effortlessly. QuillField includes features such as rich text formatting, image and video embedding, adding hyperlinks, changing text color or background, aligning the text, inserting code snippets, and a user-friendly interface, making the process of creating and editing content more intuitive and enjoyable for users.

* __Tagging System__: The implementation of a tagging system adds a layer of organization, allowing users to explore content based on their interests. This feature enhances the user experience and distinguishes ThreadFusion from standard forum platforms.

* __Toast Messages and Deletion Confirmation Popup__: The use of toast messages for success and error notifications enhances user feedback. Additionally, the deletion confirmation popup ensures that critical actions, such as deleting questions and answers, are intentional.

### Complexity ###
The complexity of the project is evident in the implementation of features such as user authentication, dynamic content rendering, and the management of questions and answers. Additionally, the tagging system and search functionality contribute to the project's depth and sophistication.
- - - -

### File Structure ###
```
/ : represents folder
-- : represents files

/capstone - main project folder
    /capstone - Django main project folder
        --asgi.py - This file is used to deploy Django application using an ASGI (Asynchronous Server Gateway Interface) server.
        --settings.py - This file contains the configuration settings for Django project.
        --urls.py - This file contains the URL patterns for Django project. It maps URLs to views.
        --wsgi.py - This file is used for deploying your Django application using a WSGI (Web Server Gateway Interface) server.
    /threadfusion - Django forum website
        /static: A directory where you can store static files such as CSS, JavaScript, and images.
            /threadfusion - A subfolder for static
                --script.js - Javascript code
                --style.scss - SASS file
                --style.css - CSS file
                --style.css.map
        /templates - A directory for storing HTML templates used by your Django views.
            /threadfusion - A subfolder for templates
                --askquestion.html - Handles the submission of new questions.
                --contact.html -  Handles the submission of the contact form.
                --editanswer.html - Handles the editing of existing answers.
                --editquestion.html - Handles the editing of existing questions.
                --footer.html - Displays the footer of the website.
                --index.html - Displays the landing page of the website.
                --login.html - Handles user login.
                --navbar.html - Displays the navbar with logo and navigation links  of the website.
                --register.html - Handles user registration.
                --search.html - Displays questions based on search queries.
                --singlequestion.html - Displays a single question with its answers and comments and a quill-field to post answers.
                --tags.html - Displays questions filtered by tags.
        --admin.py - Admin settings for model view
        --apps.py - Contains configuration for the threadfusion app, including metadata such as the app's name and any application specific configuration.
        --forms.py - Defines threadfusion forms.
        --models.py - Defines the database models for threadfusion application.
        --urls.py - Defines how URLs are mapped to views.
        --views.py - Contains the view functions or classes that handle HTTP requests and return HTTP responses.
    --manage.py - A command-line utility that lets you interact with your Django project in various ways, such as running development servers, creating database tables, and more.
    --README.md - this file
    --requirements.txt - list of libraries needed to run
```

- - - - 

### How to run ###
1. Download the zip file or Clone the repository using this command in your terminal.
2. In your terminal, cd into the capstone directory.
3. Run `python manage.py makemigrations threadfusion` to make migrations for the threadfusion website.
4. Run `python manage.py migrate` to apply migrations to your database.
5. Run `python manage.py createsuperuser` to create a superuser for Django Administration.
6. Run `pip install django-quill-editor` to install Rich Text editor (QuillField). 
7. Run `python manage.py runserver` to start up the Django web server, and visit the website in your browser.

### Features ###
* __User Authentication__: It ensures a secure and user-friendly experience for users, offering both login and registration functionalities with necessary validation and error handling.Both login and registration forms include CSRF tokens for security. Appropriate redirections are implemented to ensure a smooth user experience. Error messages are displayed when there are issues with authentication or registration. The code includes measures to enforce password complexity and prevent username duplication.
	* __Registration__: Attempts to create a new user with the provided information.
	* __Login__: Attempts to authenticate the user using the provided username and password.
	* __Logout__: Logs out the currently authenticated user.

* __Index Page__: The index page of ThreadFusion serves as the main landing page for users. It features a hero section with a compelling headline and an invitation to ask questions.
	* __Top Questions__: Each question is displayed as a clickable link, leading to its detailed page. For each question, the number of answers is presented, along with associated tags for categorization. The date of posting and, if applicable, the date of the last edit are also included. Users can easily navigate to specific questions or explore topics through tags 

* __Ask Question__: It allows authenticated users to submit new questions through a dedicated form. Users are presented with a set of forum rules and community guidelines before submitting a question.
	* __Form__: The form incorporates two TextFields dedicated to capturing the question's title and tags, along with a QuillField for providing a detailed description of the question. Each field is accompanied by a help text that provides guidance on how to complete the respective fields.
	* __Authentication Check__: Authenticated users can seamlessly post their questions, while non-authenticated users are prompted to log in before contributing.  


* __Singlequestion Page__: The singlequestion page in the ThreadFusion forum displays a detailed view of a specific question and its answers.
	* __Question__:  It includes title and description of the question, tags associated with the question for categorization and user details who posted the question, along with the date it was asked and last edited.
	* __Answers Section__: Displays all answers to the question, including user details, timestamps, and an option to edit or delete the answer (if the current user is the answer's author).
	* __Comments Section__: Displays comments for each answer, with commenter's username and a timestamp.
	* __Commenting__: Includes a TextField with 'Add' button that allows users to add comments to answers.
	* __Answer Form__: It allows authenticated users (other than the question's author) to submit their answers using a QuillField and a 'Post your answer' button and if the user is not authenticated, a link to a login page encourages them to log in to contribute answers. 
	* __Restrictions for Question Author__: If the authenticated user is the author of the question, they are informed that they cannot answer their own question. Instead, they are encouraged to update the question with a solution.

* __Edit and Delete Question and Answer__: 
	* __Edit Question__: Upon accessing the "Edit Question" page, users are presented with a form pre-filled with the existing question details. They can make necessary modifications and save the changes.
	* __Edit Answer__: Upon accessing the "Edit Answer" page, users are presented with a form that includes a single field, QuillField, pre-filled with the existing answer content. They can make necessary modifications and save the changes.
	* __Delete Question__: Clicking the Delete button triggers a confirmation popup, asking the current user(author of the question) if they are sure about deleting the question. If confirmed, the question and its associated answers are permanently deleted. The deletion process cannot be undone.
	* __Delete Answer__: Clicking the Delete button triggers a confirmation popup, asking the current user(author of the Answer) if they are sure about deleting the answer because the deletion process cannot be undone. If confirmed, the answer and its associated comments are permanently deleted.

* __Search Questions__: It allows users to search for relevant questions based on their titles, descriptions, or tags. The results are displayed on the search page, showcasing a list of questions that match the search criteria. Each result includes information such as the question itself, associated tags, and the count of answers to provide users with a quick overview of the relevant content.

* __Tags__: Each question is associated with one or more tags, which are displayed in a list. Users can click on a tag to view a filtered list of questions related to that specific topic.

* __Contact Us__: The contact form allows users to submit feedback and queries to the site administrators related to the website. The form includes TextFields for the user's full name and email, and a Textarea for message. Additionally, there are social media icons (non-functional for now) just providing a visual enhancement to the UI.