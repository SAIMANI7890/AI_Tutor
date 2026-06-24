"""
Study Planner - Example Usage
Demonstrates how to use the study planning system
"""
from datetime import date, timedelta
from app.study_planner.services.planner_service import planner_service
from app.study_planner.config.chapters import (
    get_all_chapters,
    get_chapters_by_category,
    get_chapter_by_id
)
from pprint import pprint


def example_1_basic_plan():
    """Example 1: Generate a basic study plan"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Study Plan")
    print("="*60)
    
    # Setup
    exam_date = date.today() + timedelta(days=30)  # 30 days from now
    daily_hours = 3.0
    chapter_ids = [1, 2, 11]  # French Revolution, Industrial Revolution, Climate
    
    print(f"\nInput:")
    print(f"  Exam Date: {exam_date} (30 days from now)")
    print(f"  Daily Study Hours: {daily_hours}")
    print(f"  Chapters: {chapter_ids}")
    
    # Generate plan
    plan = planner_service.generate_study_plan(
        exam_date=exam_date,
        daily_study_hours=daily_hours,
        selected_chapter_ids=chapter_ids
    )
    
    # Display results
    print(f"\nGenerated Plan:")
    print(f"  Total Days: {plan.total_days}")
    print(f"  Total Required Hours: {plan.total_required_hours:.1f}")
    print(f"  Total Available Hours: {plan.total_available_hours:.1f}")
    
    if plan.warnings:
        print(f"\n  Warnings:")
        for warning in plan.warnings:
            print(f"    - {warning}")
    
    print(f"\n  Chapter Allocations:")
    for alloc in plan.chapter_allocations:
        print(f"    {alloc.chapter_name} ({alloc.difficulty}):")
        print(f"      Sessions: {alloc.allocated_sessions}, Hours/Session: {alloc.hours_per_session}")
    
    print(f"\n  Day-by-Day Schedule (first 10 days):")
    for day in plan.days[:10]:
        activity = day.activity_type.value
        if day.chapter_name:
            print(f"    Day {day.day_number} ({day.study_date}): {activity} - {day.chapter_name} ({day.allocated_hours}h)")
        else:
            print(f"    Day {day.day_number} ({day.study_date}): {activity} ({day.allocated_hours}h)")
    
    if len(plan.days) > 10:
        print(f"    ... and {len(plan.days) - 10} more days")
    
    # Get summary
    summary = planner_service.get_plan_summary(plan)
    print(f"\n  Summary:")
    print(f"    Study Days: {summary['study_days']}")
    print(f"    Revision Days: {summary['revision_days']}")
    print(f"    Mock Test Days: {summary['mock_test_days']}")
    print(f"    Total Study Hours: {summary['total_study_hours']:.1f}")


def example_2_comprehensive_plan():
    """Example 2: Comprehensive plan with many chapters"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comprehensive Study Plan")
    print("="*60)
    
    # Select multiple chapters from different categories
    chapter_ids = [1, 2, 3, 11, 12, 21, 22, 31, 32]  # 9 chapters
    exam_date = date.today() + timedelta(days=45)  # 45 days
    daily_hours = 4.0
    
    print(f"\nInput:")
    print(f"  Exam Date: {exam_date} (45 days from now)")
    print(f"  Daily Study Hours: {daily_hours}")
    print(f"  Number of Chapters: {len(chapter_ids)}")
    
    # Show selected chapters
    print(f"\n  Selected Chapters:")
    for cid in chapter_ids:
        chapter = get_chapter_by_id(cid)
        if chapter:
            print(f"    - {chapter.chapter_name} ({chapter.category}, {chapter.difficulty.value})")
    
    # Generate plan
    plan = planner_service.generate_study_plan(
        exam_date=exam_date,
        daily_study_hours=daily_hours,
        selected_chapter_ids=chapter_ids
    )
    
    # Display results
    print(f"\nGenerated Plan:")
    print(f"  Total Days: {plan.total_days}")
    print(f"  Total Required Hours: {plan.total_required_hours:.1f}")
    print(f"  Total Available Hours: {plan.total_available_hours:.1f}")
    
    summary = planner_service.get_plan_summary(plan)
    print(f"\n  Activity Breakdown:")
    print(f"    Study Days: {summary['study_days']}")
    print(f"    Revision Days: {summary['revision_days']}")
    print(f"    Mock Test Days: {summary['mock_test_days']}")


def example_3_insufficient_time():
    """Example 3: Insufficient time scenario"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Insufficient Time Warning")
    print("="*60)
    
    # Impossible scenario: too many chapters, too little time
    exam_date = date.today() + timedelta(days=10)  # Only 10 days!
    daily_hours = 2.0
    chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13, 21, 22]  # 10 chapters
    
    print(f"\nInput:")
    print(f"  Exam Date: {exam_date} (only 10 days!)")
    print(f"  Daily Study Hours: {daily_hours}")
    print(f"  Number of Chapters: {len(chapter_ids)}")
    
    # Generate plan
    plan = planner_service.generate_study_plan(
        exam_date=exam_date,
        daily_study_hours=daily_hours,
        selected_chapter_ids=chapter_ids
    )
    
    # Display warnings
    print(f"\nGenerated Plan:")
    print(f"  Total Required Hours: {plan.total_required_hours:.1f}")
    print(f"  Total Available Hours: {plan.total_available_hours:.1f}")
    
    if plan.warnings:
        print(f"\n  ⚠️  WARNINGS:")
        for warning in plan.warnings:
            print(f"    {warning}")


def example_4_difficulty_prioritization():
    """Example 4: Demonstrate difficulty-based prioritization"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Difficulty-Based Prioritization")
    print("="*60)
    
    # Mix of difficulties
    chapter_ids = [
        1,   # Hard - French Revolution
        9,   # Easy - Ancient Civilizations
        11,  # Medium - Climate
        18,  # Hard - Environmental Issues
        13   # Easy - Rivers
    ]
    
    print(f"\nSelected Chapters:")
    for cid in chapter_ids:
        chapter = get_chapter_by_id(cid)
        if chapter:
            print(f"  {chapter.chapter_name}: {chapter.difficulty.value}")
    
    exam_date = date.today() + timedelta(days=20)
    daily_hours = 3.0
    
    # Generate plan
    plan = planner_service.generate_study_plan(
        exam_date=exam_date,
        daily_study_hours=daily_hours,
        selected_chapter_ids=chapter_ids
    )
    
    print(f"\nScheduling Order (Hard chapters first):")
    study_days = [day for day in plan.days if day.activity_type.value == "Study"]
    
    for i, day in enumerate(study_days[:8], 1):
        chapter = get_chapter_by_id(day.chapter_id)
        difficulty = chapter.difficulty.value if chapter else "Unknown"
        print(f"  {i}. Day {day.day_number}: {day.chapter_name} ({difficulty})")
    
    if len(study_days) > 8:
        print(f"  ... and {len(study_days) - 8} more study days")


def example_5_browse_chapters():
    """Example 5: Browse available chapters"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Browse Available Chapters")
    print("="*60)
    
    # Get all chapters
    all_chapters = get_all_chapters()
    print(f"\nTotal Chapters Available: {len(all_chapters)}")
    
    # Group by category
    categories = ["History", "Geography", "Politics", "Economics"]
    
    for category in categories:
        chapters = get_chapters_by_category(category)
        print(f"\n{category} ({len(chapters)} chapters):")
        for ch in chapters[:5]:  # Show first 5
            print(f"  [{ch.chapter_id}] {ch.chapter_name} - {ch.difficulty.value} ({ch.estimated_study_hours}h)")
        if len(chapters) > 5:
            print(f"  ... and {len(chapters) - 5} more")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("STUDY PLANNER - EXAMPLE USAGE")
    print("="*60)
    
    try:
        example_1_basic_plan()
        example_2_comprehensive_plan()
        example_3_insufficient_time()
        example_4_difficulty_prioritization()
        example_5_browse_chapters()
        
        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nNext Steps:")
        print("  1. Run unit tests: pytest backend/tests/study_planner/")
        print("  2. Apply database migration: alembic upgrade head")
        print("  3. Integrate with your application")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
