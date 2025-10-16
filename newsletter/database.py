# newsletter/database.py

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/newsletter_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================
# DATABASE MODELS
# ============================================

class User(Base):
    """USERS table"""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    newsletters = relationship("Newsletter", back_populates="creator")
    feedback = relationship("Feedback", back_populates="user")


class Newsletter(Base):
    """NEWSLETTERS table"""
    __tablename__ = "newsletters"
    
    newsletter_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content_html = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"))
    is_sent = Column(Boolean, default=False)
    sent_at = Column(TIMESTAMP)
    total_views = Column(Integer, default=0)
    avg_rating = Column(DECIMAL(3, 2), default=0.0)
    total_feedback = Column(Integer, default=0)
    
    creator = relationship("User", back_populates="newsletters")
    feedback = relationship("Feedback", back_populates="newsletter", cascade="all, delete-orphan")
    logs = relationship("NewsletterLog", back_populates="newsletter")


class Feedback(Base):
    """FEEDBACK table"""
    __tablename__ = "feedback"
    
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.newsletter_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    rating = Column(Integer, nullable=False)
    comments = Column(Text)
    submitted_at = Column(TIMESTAMP, server_default=func.now())
    recipient_email = Column(String(255))
    user_agent = Column(Text)
    ip_address = Column(String(45))
    
    newsletter = relationship("Newsletter", back_populates="feedback")
    user = relationship("User", back_populates="feedback")


class NewsletterLog(Base):
    """NEWSLETTER_LOGS table"""
    __tablename__ = "newsletter_logs"
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.newsletter_id"))
    action = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    details = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    
    newsletter = relationship("Newsletter", back_populates="logs")


# ============================================
# DATABASE FUNCTIONS
# ============================================

def init_db():
    """Initialize PostgreSQL database and create tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ PostgreSQL database initialized successfully")
        print(f"   Tables: users, newsletters, feedback, newsletter_logs")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")


def save_newsletter(title, content_html, created_by_email="system@vbit.edu"):
    """Save newsletter to database"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == created_by_email).first()
        if not user:
            user = User(name="System Admin", email=created_by_email, role="admin")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        newsletter = Newsletter(
            title=title,
            content_html=content_html,
            created_by=user.user_id,
            is_sent=False
        )
        db.add(newsletter)
        db.commit()
        db.refresh(newsletter)
        
        print(f"✅ Newsletter saved (ID: {newsletter.newsletter_id})")
        return newsletter.newsletter_id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error saving newsletter: {e}")
        return None
    finally:
        db.close()


def log_newsletter_sent(newsletter_id, recipient_emails, status="success"):
    """Log newsletter delivery"""
    db = SessionLocal()
    try:
        newsletter = db.query(Newsletter).filter(Newsletter.newsletter_id == newsletter_id).first()
        if newsletter:
            newsletter.is_sent = True
            newsletter.sent_at = func.now()
        
        log = NewsletterLog(
            newsletter_id=newsletter_id,
            action="sent",
            status=status,
            details=f"Sent to {len(recipient_emails)} recipients"
        )
        db.add(log)
        db.commit()
        
        print(f"✅ Newsletter #{newsletter_id} marked as sent")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error logging newsletter: {e}")
        return False
    finally:
        db.close()


def save_feedback(newsletter_id, user_email, rating, comments=None, user_agent=None, ip_address=None):
    """Save user feedback"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(
                name=user_email.split('@')[0].title(),
                email=user_email,
                role="recipient"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        existing = db.query(Feedback).filter(
            Feedback.newsletter_id == newsletter_id,
            Feedback.recipient_email == user_email
        ).first()
        
        if existing:
            existing.rating = rating
            existing.comments = comments
            existing.submitted_at = func.now()
            existing.user_agent = user_agent
            existing.ip_address = ip_address
        else:
            feedback = Feedback(
                newsletter_id=newsletter_id,
                user_id=user.user_id,
                rating=rating,
                comments=comments,
                recipient_email=user_email,
                user_agent=user_agent,
                ip_address=ip_address
            )
            db.add(feedback)
        
        newsletter = db.query(Newsletter).filter(Newsletter.newsletter_id == newsletter_id).first()
        if newsletter:
            avg_rating = db.query(func.avg(Feedback.rating)).filter(
                Feedback.newsletter_id == newsletter_id
            ).scalar()
            total_feedback = db.query(func.count(Feedback.feedback_id)).filter(
                Feedback.newsletter_id == newsletter_id
            ).scalar()
            
            newsletter.avg_rating = round(float(avg_rating), 2) if avg_rating else 0.0
            newsletter.total_feedback = total_feedback or 0
        
        db.commit()
        print(f"✅ Feedback saved: {rating}⭐ for newsletter #{newsletter_id}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error saving feedback: {e}")
        return False
    finally:
        db.close()


def get_newsletter_stats(newsletter_id):
    """Get statistics for a newsletter"""
    db = SessionLocal()
    try:
        newsletter = db.query(Newsletter).filter(Newsletter.newsletter_id == newsletter_id).first()
        if not newsletter:
            return None
        
        rating_counts = {}
        for i in range(1, 6):
            count = db.query(Feedback).filter(
                Feedback.newsletter_id == newsletter_id,
                Feedback.rating == i
            ).count()
            rating_counts[f"{i}_stars"] = count
        
        return {
            "newsletter_id": newsletter.newsletter_id,
            "title": newsletter.title,
            "sent_at": newsletter.sent_at,
            "total_feedback": newsletter.total_feedback,
            "avg_rating": float(newsletter.avg_rating),
            "rating_breakdown": rating_counts
        }
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return None
    finally:
        db.close()
