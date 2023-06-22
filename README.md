# Scissor API  

 This repository provides access to the functionality of the URL shortener, allowing users to create, manage, and track short URLs. The API provides endpoints for creating new short URLs, retrieving information about existing short URLs, and tracking the number of visitors for each short URL.

 API Documentation  For detailed information about the Flask and how to use them, please refer to the [API Documentation](https://flask.palletsprojects.com/en/2.3.x/)

## Installation  
Follow the instructions below to set up and run the Scissor API on your local machine.  

### Prerequisites  - Flask (version 2.3.2) - Python (version ^3.9)  


### Getting Started  


1. Clone the repository:     

    ` git clone https://github.com/stardev1/scissor`

2.  Install the dependencies:
    
    `pip install -r requirements`
    
3.  Start the development server:
    
    
    `python3 -m app`
    
4.  The server will be running at `http://localhost:5000`

## Scissor Website

This website provides an API for shortening URLs. The API documentation is available for reference.

Web Version endponts
--------------------

The web version of the app is available at `localhost:5000`. It provides the following endpoints:

- `/`: Generates a new short URL from a long URL.
- `/custom`: Creates a custom short URL based on your website name and interests.
- `/history`: Shows all generated URLs.
- `/history/{url}/stats`: Shows statistics for the specified URL.
- `/history/{url}/edit`: Allows editing of the specified URL and its redirection address.
- `/history/{url}/delete`: Allows removal of unwanted URLs from the history page.


    

API Usage
---------

### Authentication

*   To authenticate a user, use the following endpoint:
    
    *   `POST /api/login`: Authenticate user using email and password
*   To register a new user, use the following endpoint:
    
    *   `POST /api/signup`: Register new user

### User Operations

*   To get user information, use the following endpoint:
    
    *   `GET /api/users`: Get User Info
*   To create a new user, use the following endpoint:
    
    *   `POST /api/user`: Create a new user with the provided information
*   To get current user information, use the following endpoint:
    
    *   `GET /api/user`: Get Current User
*   To update user information, use the following endpoint:
    
    *   `PATCH /api/user/edit`: Update user info
*   To delete the authenticated user, use the following endpoint:
    
    *   `DELETE /api/user/delete`: Delete Auth user

### URL Operations

*   To get all URLs created by the current authenticated user, use the following endpoint:
    
    *   `GET /api/`: Get all URLs
*   To fetch URL details, use the following endpoint:
    
    *   `GET /api/{url}`: Fetch URL details
*   To fetch the number of visitors for a specific short URL, use the following endpoint:
    
    *   `GET /api/{url}/visitors`: Fetch all Visitors
*   To generate a new short URL for a long URL, use the following endpoint:
    
    *   `POST /api/generate`: Generate new URL
*   To update a short URL with new information, use the following endpoint:
    
    *   `PATCH /api/{url}/edit`: Update URL
*   To delete a short URL, use the following endpoint:
    
    *   `DELETE /api/{url}/delete`: Delete short URL

### Visitors

*   To get all visitors for a specific short URL, use the following endpoint:
    *   `GET /api/{url}/visitors/`: Get all visitors

Contributing
------------

Contributions are welcome! If you find any issues or want to enhance the API, feel free to submit a pull request.

License
-------

[MIT License](LICENSE)
