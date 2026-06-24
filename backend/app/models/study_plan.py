"""
Study Plan Models
Database models for study planning and scheduling
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class ActivityType(str, enum.Enum):
    """Activity type enumeration"""
    STUDY = "Study"
    REVISION = "Revision"
    MOCK_TEST = "MockTest"


class StudyStatus(str, enum.Enum):
    """Study status enumeration"""
    PENDING = "Pending"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"


class StudyPlan(Base):
    """Study plan model"""
    
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exam_date = Column(Date, nullable=False)
    daily_study_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    items = relationship("StudyPlanItem", back_populates="study_plan", cascade="all, delete-orphan")
    user = relationship("User", backref="study_plans")
    
    def __repr__(self):
        return f"<StudyPlan {self.id}: Exam on {self.exam_date}>"


class StudyPlanItem(Base):
    """Study plan item model"""
    
    __tablename__ = "study_plan_items"
    
    id = Column(Integer, primary_key=True, index=True)
    study_plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)  # Day 1, 2, 3, etc.
    study_date = Column(Date, nullable=False)
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    chapter_id = Column(Integer, nullable=True)  # Null for revision/mock test days
    chapter_name = Column(String(255), nullable=True)  # Null for revision/mock test days
    allocated_hours = Column(Float, nullable=False)
    status = Column(SQLEnum(StudyStatus), default=StudyStatus.PENDING, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Timestamp when completed
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    study_plan = relationship("StudyPlan", back_populates="items")
    
    def __repr__(self):
        return f"<StudyPlanItem {self.id}: Day {self.day_number} - {self.activity_type}>"
