# Inspyre

### Create boldly. Share freely. Discover endlessly.

![Responsive Demo](./README/images/Am-I-Responsive.png)

#### Backend DRF API - for the frontend React app, [click here](https://github.com/MattMiles95/PP5_Inspyre_Frontend).

Inspyre is a modern content-sharing platform designed to empower creativity and connection. Whether you're a digital artist, writer, photographer, or passionate hobbyist, Inspyre gives you the tools to showcase your work, engage with a like-minded community, and discover new inspiration every day.

Powering a dynamic content-sharing platform, the Inspyre DRF API supports secure user authentication, image and text post management, customizable user profiles with tag associations, a simple yet robust profile following system and a built-in direct messaging system.

[Visit the deployed API](https://inspyre-api-6e178387b3cb.herokuapp.com/)

## Table of Contents

### [Design](#design-1)

### [Features & Logic](#features--logic-1)

- [Authorisation](#authorisation)
- [Posts](#posts)
- [Profiles](#profiles)
- [Likes & Trending Posts](#likes--trending-posts)
- [Follow System](#post-searchbar)
- [Comments](#comments)
- [Direct Messaging](#direct-messaging)

### [Testing](#testing-1)

### [Project Management - an Agile Approach](#project-management---an-agile-approach-1)

### [Technologies Used](#technologies-used-1)

- [Languages](#languages)
- [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used-1)

### [Local Development & Deployment](#local-development--deployment-1)

- [Deployment](#deployment)
- [Forking the GitHub Repository](#forking-the-github-repository)
- [Local Clone](#local-clone)
- [Code Institute PostgreSQL Database](#code-institute-postgresql-database)
- [Cloudinary](#cloudinary)

### [Credits](#credits-1)

- [Affiliations](#affiliations)
- [Code Credits](#code-credits)

<br>

## Design

<br>

## Features & Logic

<br>

### Authorisation

Inspyre implements a robust authorisation system using Django REST Auth and Django Allauth on the backend. This ensures secure authentication while streamlining user registration, login, and session management.

Behind the scenes, Jason Web Token (JWT) authentication is used to manage user sessions securely. Upon login, users are issued an authentication token that must be included with each API request requiring authorisation. Django REST Auth handles the issuing and validation of these tokens, ensuring only authenticated users can access protected endpoints.

Permissions are carefully scoped using Django REST Framework's built-in permission classes, along with custom logic. This ensures users can only perform actions they're authorised for - for example, editing their own posts, accessing their conversations, or managing their own profile - while preventing unauthorised access to other users' data or actions.

<br>

### Posts

<br>

### Profiles

<br>

### Likes & Trending Posts

<br>

### Follow System

<br>

### Comments

<br>

### Direct Messaging

<br>

## Testing

For manual testing and validator results, please head to my [TESTING](./TESTING.md) file.

<br>

## Project Management - an Agile Approach

<br>

### Agile Methodology

I used the Agile methodology to plan my project in terms of iterations. Tasks were created as segmented 'User Stories', each with their own acceptance criteria. These User Stories were prioritised using the MoSCoW method (see below) and worked through incrementally, allowing for an objective driven yet adaptable development process. User Stories were also categorised into separate Milestones (i.e., 'Direct Messaging'), to make it easier to track how far progressed I was with each feature group. Features I knew I wanted but wouldn't feasibly achieve by the project deadline were labelled as 'not required in this iteration'.

<br>

### MoSCoW Prioritisation

In order to prioritise my User Stories, I used MoSCoW Prioritisation to label each issue one of the following:

- Must Have - product requires this feature to be viable.

- Should Have - feature would add substantial value to product

- Could Have - feature could add value to the product.

- Won't Have - feature isn't required during this iteration (non-priority)

<br>

### GitHub Project - Kanban Board

I used GitHub Issues and Projects to manage the above-mentioned process. Each issue provided a User Story, which was placed on a Kanban board in my Inspyre Project. This board was separated into 4 columns: 'To Do', 'In Progress', 'Done' and 'Not Required This Iteration'. I linked both my frontend and backend repos to this project, which can be viewed [here](https://github.com/users/MattMiles95/projects/8/views/1)

<br>

## Technologies Used

### Languages

- [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>)

<br>

### Frameworks, Libraries & Programs Used

#### Frameworks

- [Django 4.2.20](https://www.djangoproject.com/) - Open-source Python framework.
- [Django Rest Framework 3.15.2](https://www.django-rest-framework.org/) - API framework for Django.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/) - Authentication library for Django REST Framework.
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/) - Authentication system for Django.
- [django-cloudinary-storage](https://github.com/klis87/django-cloudinary-storage) - Cloudinary integration for Django’s file storage.
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) - CORS handling for Django.
- [django-filter](https://django-filter.readthedocs.io/en/stable/) - Filtering library for Django REST Framework.
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - JWT authentication for Django REST Framework.

#### Libraries

- [asgiref](https://docs.djangoproject.com/en/stable/releases/3.0/#asgiref) - ASGI interface reference implementation.
- [cffi](https://cffi.readthedocs.io/en/latest/) - Foreign Function Interface for C code.
- [charset-normalizer](https://github.com/Ousret/charset_normalizer) - Encoding detection library.
- [cloudinary (Python SDK)](https://cloudinary.com/documentation/django_integration) - Media management SDK.
- [cryptography](https://cryptography.io/en/latest/) - Cryptographic operations for Python.
- [idna](https://pypi.org/project/idna/) - Internationalized domain names support.
- [oauthlib](https://oauthlib.readthedocs.io/en/latest/) - OAuth1 and OAuth2 support.
- [packaging](https://packaging.pypa.io/en/latest/) - Python package versioning utilities.
- [pillow](https://python-pillow.org/) - Image processing library for Python.
- [psycopg2 2.9.10](https://www.psycopg.org/) - PostgreSQL database adapter for Python.
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/) - JSON Web Token library for Python.
- [python3-openid](https://github.com/necaris/python3-openid) - OpenID authentication for Python.
- [pytz](https://pypi.org/project/pytz/) - World timezone definitions.
- [requests](https://docs.python-requests.org/en/latest/) - HTTP library for Python.
- [requests-oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/) - OAuth support for requests.
- [setuptools](https://setuptools.pypa.io/en/latest/) - Python package management and installation.
- [six](https://six.readthedocs.io/) - Python 2 and 3 compatibility utilities.
- [sqlparse](https://sqlparse.readthedocs.io/en/latest/) - SQL parser and formatter.
- [tzdata](https://pypi.org/project/tzdata/) - IANA timezone data for Python.
- [urllib3](https://urllib3.readthedocs.io/en/latest/) - HTTP client for Python.
- [webencodings](https://github.com/SimonSapin/python-webencodings) - Character encoding APIs.

#### Programs

- [gunicorn](https://gunicorn.org/) - WSGI HTTP server for Python web apps.
- [whitenoise](https://whitenoise.readthedocs.io/en/latest/) - Static file serving for Python web apps.
- [PostgreSQL](https://www.postgresql.org/) - Database system.

#### Tools & Utilities

- [Cloudinary](https://cloudinary.com/home) - Cloud-based file storage service.
- [Git](https://git-scm.com/) - Version control system.
- [GitHub](https://github.com/) - Online repository storage.
- [Heroku](https://www.heroku.com/home) - App deployment platform.
- [Lucid](https://lucid.app/documents#/documents?folder_id=home) - Logic diagram design app.
- [Visual Studio Code](https://code.visualstudio.com/) - IDE.

<br>

## Local Development & Deployment

This app was developed using VSCode and deployed via Heroku.

<br>

### Deployment

Prior to the below deployment process, enter the `pip freeze > requirements.txt` command in your Git Bash terminal to update your requirements.txt file. Once this has been done, you can deploy via Heroku using the following steps:

1. Login to [Heroku](https://dashboard.heroku.com/).

2. On the 'Dashboard', click **"New"** then **"Create new app"**.

3. Choose a unique app name for the backend (e.g., `inspyre-api`) and select your region.

4. Click **"Create app"**.

5. Under the **Settings** tab, locate **"Config Vars"**.

6. Click **"Reveal Config Vars"** and add the following variables:

- ALLOWED_HOSTS

- CLIENT_ORIGIN

- CLIENT_ORIGIN_DEV

- CLOUDINARY_URL (if required)

- DATABASE_URL

- SECRET_KEY

7. Under the **Deploy** tab:

- Select **GitHub** as the deployment method.
- Search for your backend repo and click **"Connect"**.
- Choose either **"Enable Automatic Deploys"** or **"Manual Deploy"**.
- Deploy the main branch.

8. Wait for the build and publish process. Once completed, test your API via the Heroku app link to ensure successful deployment.

<br>

### Code Institute PostgreSQL Database

1. Create a Code Institute PostgreSQL account.

2. Create a new instance.

3. Copy the database URL.

4. Add database to the **env.py** file in your IDE.

5. Add the database to your Heroku app's **Config Vars**.

<br>

### Cloudinary

1. Create an account with [Cloudinary](https://cloudinary.com/).

2. Add your Cloudinary API environment variable to your **env.py** and Heroku app's **Config Vars**.

3. In settings.py, add Cloudinary libraries to INSTALLED_APPS in the following order:

```
   'cloudinary_storage',
   'cloudinary',
```

4. Also in settings.py, configure Cloudinary to provide secure responses over HTTPS instead of HTTP:

```
cloudinary.config(
    secure=True
)
```

<br>

### Forking the GitHub Repository

Forking the repository creates a copy of the original, allowing us to view and change the repository without affecting the original. This can be done by following the below steps:

1. Open the GitHub repository - [PP5_Inspyre_Backend](https://github.com/MattMiles95/PP5_Inspyre_Backend).

2. Select the "Fork" button in the top-right section of the page.

A copy of the repository should now be in your own GitHub account.

<br>

### Local Clone

Cloning the repository allows you to copy the files into your own IDE for local development. This can be done by following the below steps:

1. Open the GitHub repository - [PP5_Inspyre_Backend](https://github.com/MattMiles95/PP5_Inspyre_Backend).

2. Navigate the 'Code' dropdown menu and select whether you wish to clone the code using HTTPS, SSH or GitHub CLI.

3. Open the a Git Bash terminal in your chosen IDE and navigate your working directory to the location you wish to clone the project.

4. Use the command 'git clone' followed by the link you copied from the repository.

<br>

## Credits

### Affiliations

Inspyre is a fictional brand I created for this project. I hold no copyright for the brand and am not affiliated with any persons, organisations or platforms.

<br>

### Code Credits

Both my frontend and backend projects were built using my Code Institute "Moments" walkthrough project as a foundation. Inspyre has evolved substantially from this foundation, but much of the core logic and naming conventions of that project persist within the bones of my final code. All other code featured in this project has been written by me, with the assistance of the Slack community, various forums, articles, YouTube videos, a great deal of coffee and the help from my mentor, Mitko Bachvarov.
