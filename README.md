# Lost and Found

## Overview
This project aims to provide Cornell students help with finding lost items.

## Setup
1. Clone this repository.
2. cd into src
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Start the server by running `python3 app.py`.

## Endpoints [SEE APP.PY]
#User
- GET "/api/users/" Get all Users
- GET "/api/users/<int:user_id>/" Get user by user Id
- POST "/api/signup/" Create a User
- POST "/api/users/<int:user_id>/" Update user By  user Id
- DELETE "/api/users/<int:user_id>/" Delete user by user ID
  
#Posts
- GET "/api/posts/" Get all posts
- GET "/api/posts/<int:post_id>/" Get post by id
- POST "/api/posts/<user_id>/" Create Post by user id
- POST "/api/posts/<int:post_id>/update/" Update post by id
- DELETE "/api/posts/<int:post_id>/" Delete post by id
  
#Comments
- GET "/api/comments/" Get all comments
- GET "/api/comments/<int:comment_id>/" Get comment by comment id
- POST "/api/comments/<int:user_id>/<int:post_id>/" Create comment by user and post id
- DELETE "/api/comments/<int:comment_id>/" Delete comment by comment id
- UPDATE "/api/comments/update/<int:comment_id>/" Update comment by comment id
  
#Other
- POST "/api/login/" Login user 
- POST "/api/upload/" Upload image
- GET "/api/upload/<string:image_name>/" Get image by image ID 

## Technologies Used
- Python
- Flask
- SQLAlchemy

## Contributors
- [David Valarezo]
- [Nathnael Tefsaw]

