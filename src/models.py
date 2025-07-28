from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class Type(enum.Enum):
    Foto = 1
    Carrusel = 2
    Video = 3

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    firstname: Mapped[str] = mapped_column(String(120))
    lastname: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    # Relacionando las tablas
    posts = relationship("Post", back_populates="user")
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
# Follower se trae la id de User y da información a User
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # Relacionando las tablas
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }
    
# Media se trae la id de post
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    url: Mapped[str] = mapped_column(String(120))
    # Relacionando las tablas
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }

# Post se trae la id de User y da información a Media y Comment
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # Relacionando las tablas
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
    
# Comment se trae la id de User y Post
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120))
    # Relacionando las tablas
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
