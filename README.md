# RESTful_Microservices 
The goal of this project is to develop 4 micro services for a blog using Python Flask.

## Microservices
There are 4 microservies, each having appropriate JSON data formats, HTTP methods, URL endpoints, and HTTP status codes for each service.
- Articles microservice
Each article consists of text, a title or headline, an author, and timestamps for article’s creation and the last time the article was modified.

- Tags microservice
Each article can be have one or more tags associated with it. Since this API is exposed separately from the Articles API, individual articles are referred to by URL.

- Comments microservice
Users can post comments on each article. As with the tags microservice, individual articles are referred to by URL. Each comment has an author and a date.

- Users microservice
Each user has a display name shown to other users, an email address (used as a username when logging in), and a hashed password.

# The Project Team
## Team Members
- Shekhar Palit
- Rohan Bedarkar
- Akshay Bhor
## Project Technologies
- Programming Language - Python
- Web Frame Work - Flask
- DataBase - SQLite3
