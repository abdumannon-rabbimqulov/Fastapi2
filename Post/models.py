from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index, func
from sqlalchemy.orm import relationship
from db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title = Column(String(255), nullable=False)


    slug = Column(String(255), unique=True, index=True, nullable=True)

    desc = Column(Text, nullable=False)

    view_count = Column(Integer, default=0, server_default="0")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


    auth = relationship("User", back_parents="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title[:20]}...)>"



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(user_id={self.user_id}, post_id={self.post_id})>"


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("unique_user_post_wishlist", "user_id", "post_id", unique=True),
    )

    user = relationship("User", back_populates="wishlist_items")
    post = relationship("Post")