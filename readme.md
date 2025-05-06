
# Blogging Rest API
A blogging REST API that enables users to register, log in, and interact with articles by viewing, creating, rating, commenting, clapping, and bookmarking them. Additionally, users can follow others, view their followers and following lists, and engage in a community of bloggers.



## Features

- **User Registration and Authentication**  
  Users can register with their email, set a password, and log in to access the platform. JWT tokens are used for secure authentication.

- **User Profile Management**  
  Each user has a profile with their first name, last name, and email. Users can update their profile information.

- **Article Management**  
  - **View Articles**: Users can browse articles posted by others.
  - **Create Articles**: Authenticated users can create new blog posts, including titles, content, and optional tags.
  - **Edit/Delete Articles**: Users can edit or delete their own articles.

- **Interaction with Articles**  
  - **Rate Articles**: Users can give a rating to articles.
  - **Clap for Articles**: Users can "clap" for articles they like, showing appreciation.
  - **Bookmark Articles**: Users can bookmark articles for easy access later.
  - **Comment on Articles**: Users can leave comments on articles to interact with the content.

- **User Interaction**  
  - **Follow/Unfollow Users**: Users can follow others to see their articles in their feed.
  - **Followers and Following Lists**: Users can view who is following them and who they are following.

- **Admin Features**  
  - **Manage Users and Articles**: Admins can manage users and articles, including the ability to delete inappropriate content or block malicious users.

- **Rate Limiting**  
  The API uses rate throttling to limit the number of requests a user can make in a given time frame, helping prevent abuse and ensuring system stability.

- **Unit Tests**  
  Comprehensive unit tests are included, leveraging tools like **pytest** and **Factory Boy** for mock data and efficient testing of API endpoints and user interactions.

- **Pagination**  
  Articles, comments, and user lists are paginated to improve performance when handling large datasets.


## Tech Stack

**Backend:**
- Django Rest Framework
- JWT
- PostgreSQL
- pytest
- Factory Boy

**Deployment:**
- Render

## Installation

Follow these steps to get the project running locally:

### 1. Clone the repository

```bash
git clone https://github.com/MohamedKamaal/blogging-platform-api
cd blog
pip install -r requirements.txt
```

### 2. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 3. Run the development server
```bash
python manage.py runserver
```
### 4. Access API documentation
```bash
http://localhost:8000/redoc/
```
## Running Tests

To run tests, run the following command

```bash
  pytest 
```


## Demo

Insert gif or link to demo

