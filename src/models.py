"""
Database models for the Mergington High School Activities API
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between students and activities
activity_participants = Table(
    "activity_participants",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activity.id"), primary_key=True),
    Column("student_email", String, ForeignKey("student.email"), primary_key=True),
)


class Activity(Base):
    """Activity model"""
    __tablename__ = "activity"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    
    # Relationship to students
    participants = relationship(
        "Student",
        secondary=activity_participants,
        back_populates="activities"
    )
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": [p.email for p in self.participants],
            "current_participants": len(self.participants),
            "spots_available": self.max_participants - len(self.participants)
        }


class Student(Base):
    """Student model"""
    __tablename__ = "student"
    
    email = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    grade_level = Column(String, nullable=True)
    
    # Relationship to activities
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "email": self.email,
            "name": self.name,
            "grade_level": self.grade_level,
            "activities": [a.name for a in self.activities]
        }
