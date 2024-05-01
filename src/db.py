from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    
    
class User(db.Model):
    """Creates the User Class"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    bio = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable = False)
    posts = db.relationship("Post", cascade="delete")
    comments = db.relationship("Comment", cascade="delete")


    def __init__(self, **kwargs):
        """Initializes the User Class"""
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
    
    def simple_serialize(self):
        """Serializes the User Class without posts and comments"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
    
    def serialize(self):
        """Serializes the User Class"""
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "posts": [p.serialize() for p in self.posts],
            "comments": [c.serialize() for c in self.comments]
        }
    


#Post has a one to many relationship with user
class Post(db.Model):
    """Post Class"""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, **kwargs):
        """Initializes the Post Class"""
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.category = kwargs.get("category")
        self.filename = kwargs.get("filename")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """Initializes the Post Class"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "filename": self.filename,
            "user_id": self.user_id
        }
    
    
class Comment(db.Model):
    """Comment Class"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def __init__(self, **kwargs):
        """Initializes the Comment Class """
        self.comment = kwargs.get("comment")
        self.post_id = kwargs.get("post_id")
        self.user_id = kwargs.get("user_id")
    
    def serialize(self):
        """Serialize the Comment Class """
        return {
            "id": self.id,
            "comment": self.comment,
            "post_id": self.post_id,
            "user_id": self.user_id
        }