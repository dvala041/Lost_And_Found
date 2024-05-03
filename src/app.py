import json
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename 

from db import db, User, Post, Comment, Image
from flask import Flask, request, Response

app = Flask(__name__)
db_filename = "lost.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

def hash_password(password):
    # Use SHA256 to hash the password
    hasher = hashlib.sha256()
    password_bytes = password.encode()
    hasher.update(password_bytes)
    password_hash = hasher.hexdigest()

    return password_hash


"""USER ROUTES"""

#GET ALL USERS
@app.route("/api/users/")
def get_users():
    """Get all Users"""
    users = [u.serialize() for u in User.query.all()]
    return success_response(users)

#GET USER BY ID
@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """Get a user given its id"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found")
    
    return success_response(user.serialize())
@app.route("/")
def base():
    return "hello"

#CREATE USER; SIGN UP A USER
@app.route("/api/signup/", methods=["POST"])
def create_user():
    """Create a new user"""
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")
    username = body.get("username")
    password = body.get("password")

    if name is None or email is None or username is None or password is None:
        return failure_response("Body is missing field", 400)
    
    hashed_password = hash_password(password)
    new_user = User(name = name, email = email,username = username, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    user = new_user.simple_serialize()

    return success_response(user, 201)

#UPDATE USER
@app.route("/api/users/<int:user_id>/", methods=["POST"])
def update_user(user_id):
    """Updates all the fields of a given user"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found")
    
    ser = user.simple_serialize()
    body = json.loads(request.data)
    name = body.get("name", ser.get("name"))
    email = body.get("email", ser.get("email"))
    username = body.get("username", ser.get("username"))
    bio = body.get("bio", ser.get("bio"))
    profile_img_url = body.get("profile_img_url", ser.get("profile_image_url"))
    
    user.name = name 
    user.email = email
    user.username = username
    user.bio = bio
    user.profile_img_url = profile_img_url
    db.session.commit()
    return success_response(user.serialize())
    
#DELETE USER BY ID
@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """Delete user by id"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


    
"""COMMENTS ROUTES"""

#GET ALL COMMENTS
@app.route("/api/comments/")
def get_comments():
    """Get all Comments"""
    comments = [c.serialize() for c in Comment.query.all()]
    return success_response(comments)


#GET COMMENT BY ID
@app.route("/api/comments/<int:comment_id>/")
def get_comment(comment_id):
    """Get a comment given its id"""
    comment = Comment.query.filter_by(id=comment_id).first()

    if comment is None:
        return failure_response("Comment not found")
    
    return success_response(comment.serialize())

#CREATE COMMENT
@app.route("/api/comments/<int:user_id>/<int:post_id>/", methods=["POST"])
def create_comment(user_id,post_id):
    """Create a comment given a user_id and post_id"""
    user = User.query.filter_by(id=user_id).first()
    post = Post.query.filter_by(id= post_id).first()
    
    if user is None:
        return failure_response("User not found")
    if post is None:
        return failure_response("Post not found")
    
    body = json.loads(request.data)
    comment = body.get("comment")

    if comment is None:
        return failure_response("Body is missing field", 400)
    
    new_comment = Comment(comment = comment, post_id = post_id, user_id = user_id)
    db.session.add(new_comment)
    db.session.commit()

    return success_response(new_comment.serialize(), 201)

#DELETE COMMENT
@app.route("/api/comments/<int:comment_id>/", methods=["DELETE"])
def delete_comment(comment_id):
    """Delete comment by id"""
    comment = User.query.filter_by(id=comment_id).first()

    if comment is None:
        return failure_response("Comment not found")
    db.session.delete(comment)
    db.session.commit()
    return success_response(comment.serialize())

#UPDATE COMMENT
@app.route("/api/comments/update/<int:comment_id>/", methods=["POST"])
def update_comment(comment_id):
    """Updates a field of a given comment"""
    comment = Comment.query.filter_by(id=comment_id).first()

    if comment is None:
        return failure_response("Comment not found")
    
    ser = comment.serialize()
    body = json.loads(request.data)
    comment_message = body.get("comment", ser.get("comment"))

    comment.comment = comment_message 
    db.session.commit()
    return success_response(comment.serialize())
    

"""POST TABLE ENDPOINTS"""

#GET ALL POSTS
@app.route("/api/posts/")
def get_posts():
    """ Get all posts"""
    posts = [p.serialize() for p in Post.query.all()]
    return success_response(posts)


#GET A POST BY ITS ID
@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    """
        Get a post by it's ID
        Return a dictionary of the newly created post
    """
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        return failure_response("Post not found")
    return success_response(post.serialize())


#CREATE A POST
@app.route("/api/posts/<user_id>/", methods=["POST"])
def create_post(user_id):
    """ 
        Create a post
        Returns a dictionary of the created post 
    """
    user = User.query.filter_by(id=user_id).first()
    
    if user is None:
        return failure_response("User not found")
    
    body = json.loads(request.data)

    title = body.get("title")
    description = body.get("description")
    category = body.get("category")
    filename = body.get("filename")
    location = body.get("location")

    if title is None or description is None or category is None or filename is None or location is None:
        return failure_response("Body is missing fields", 400)
    
    post = Post(title = title, description = description, category = category, filename = filename, 
                user_id=user_id, location = location, time = datetime.now())

    db.session.add(post)
    user.posts.append(post)
    db.session.commit()

    return success_response(post.serialize(), 201)


#UPDATE A POST
@app.route("/api/posts/<int:post_id>/update/", methods=["POST"])
def update_post(post_id):
    """
        Update a Post's fields 
        If not all fields are provided, we use values already in the database
        Returns a dictionary of the updated post
    """
    new_post = Post.query.filter_by(id=post_id).first() #post is a dictionary
    post = new_post.serialize()
    if post is None:
        return failure_response("Post not found")
    old_title = post.get("title")
    
    body = json.loads(request.data)
    
    #updated fields; if field not provided in body just initialize with current value
    title = body.get("title", old_title)
    description = body.get("description", post.get("description"))
    category = body.get("category", post.get("category"))
    filename = body.get("filename", post.get("filename"))

    new_post.title = title
    new_post.description = description
    new_post.category = category
    new_post.filename = filename

    db.session.commit()
    
    #return updated post
    post = Post.query.filter_by(id=post_id).first().serialize()
    return success_response(post)

#DELETE A POST BY ITS ID
@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
        Delete a Post
        Returns a dictionary of the deleted post
    """
    post = Post.query.filter_by(id=post_id).first() #post is a dictionary
    
    if post is None:
        return failure_response("Post not found")
    
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize())
    
    
"""OTHER ENDPOINTS"""

@app.route("/api/login/", methods = ["POST"])
def login():
    body = json.loads(request.data)
    # name = body.get("name")
    # email = body.get("email")
    username = body.get("username")
    password = body.get("password")
    

    if username is None or password is None: 
        return failure_response("Missing body", 400)
    
    user = User.query.filter_by(username=username).first()

    if user is None:
        return failure_response("User not found")
    
    hashed_password = hash_password(password)

    ser_user = user.serialize()
    
    if not (hashed_password != ser_user.get("password")):
        return failure_response("Incorrect Password")
    
    return success_response(user.simple_serialize())

#TESTING THIS ROUTE FOR STORING IMAGES
@app.route("/api/upload/", methods=["POST"])
def upload_image():
    pic = request.files["pic"] #pic is the name of the file?

    if not pic:
        return failure_response("No image uploaded")
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Image(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return "Success!!!"

@app.route("/api/upload/<int:image_id>/")
def get_image(image_id):
    img = Image.query.filter_by(id=image_id).first()

    if img is None:
        return failure_response("Image not found")
    
    return Response(img.img, mimetype=img.mimetype)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
