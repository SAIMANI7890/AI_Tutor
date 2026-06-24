/**
 * Chapter Configuration
 * Matches backend chapter catalog
 */

import type { Chapter } from "@/types/study-plan";

export const CHAPTERS: Chapter[] = [
  // ===== HISTORY CHAPTERS =====
  {
    chapter_id: 1,
    chapter_name: "French Revolution",
    category: "History",
    difficulty: "Hard",
    estimated_study_hours: 5.0,
  },
  {
    chapter_id: 2,
    chapter_name: "Industrial Revolution",
    category: "History",
    difficulty: "Hard",
    estimated_study_hours: 4.5,
  },
  {
    chapter_id: 3,
    chapter_name: "World War I",
    category: "History",
    difficulty: "Medium",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 4,
    chapter_name: "World War II",
    category: "History",
    difficulty: "Medium",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 5,
    chapter_name: "Colonialism and Imperialism",
    category: "History",
    difficulty: "Hard",
    estimated_study_hours: 5.0,
  },
  {
    chapter_id: 6,
    chapter_name: "The Renaissance",
    category: "History",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 7,
    chapter_name: "Indian Independence Movement",
    category: "History",
    difficulty: "Medium",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 8,
    chapter_name: "Cold War Era",
    category: "History",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 9,
    chapter_name: "Ancient Civilizations",
    category: "History",
    difficulty: "Easy",
    estimated_study_hours: 3.0,
  },
  {
    chapter_id: 10,
    chapter_name: "Medieval Period",
    category: "History",
    difficulty: "Easy",
    estimated_study_hours: 3.0,
  },

  // ===== GEOGRAPHY CHAPTERS =====
  {
    chapter_id: 11,
    chapter_name: "Climate and Weather Patterns",
    category: "Geography",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 12,
    chapter_name: "Monsoon Systems",
    category: "Geography",
    difficulty: "Medium",
    estimated_study_hours: 3.0,
  },
  {
    chapter_id: 13,
    chapter_name: "Major Rivers and Water Bodies",
    category: "Geography",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 14,
    chapter_name: "Mountain Ranges and Plateaus",
    category: "Geography",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 15,
    chapter_name: "Natural Resources",
    category: "Geography",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 16,
    chapter_name: "Soil Types and Agriculture",
    category: "Geography",
    difficulty: "Medium",
    estimated_study_hours: 3.0,
  },
  {
    chapter_id: 17,
    chapter_name: "Population Distribution",
    category: "Geography",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 18,
    chapter_name: "Environmental Issues",
    category: "Geography",
    difficulty: "Hard",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 19,
    chapter_name: "Map Reading and Skills",
    category: "Geography",
    difficulty: "Easy",
    estimated_study_hours: 2.0,
  },
  {
    chapter_id: 20,
    chapter_name: "Climate Zones",
    category: "Geography",
    difficulty: "Medium",
    estimated_study_hours: 3.0,
  },

  // ===== POLITICS CHAPTERS =====
  {
    chapter_id: 21,
    chapter_name: "Democracy and Its Features",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 22,
    chapter_name: "Constitutional Framework",
    category: "Politics",
    difficulty: "Hard",
    estimated_study_hours: 4.5,
  },
  {
    chapter_id: 23,
    chapter_name: "Fundamental Rights",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 24,
    chapter_name: "Directive Principles",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 3.0,
  },
  {
    chapter_id: 25,
    chapter_name: "Three Branches of Government",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 26,
    chapter_name: "Electoral System",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 27,
    chapter_name: "Political Parties",
    category: "Politics",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 28,
    chapter_name: "Local Self-Government",
    category: "Politics",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 29,
    chapter_name: "Judiciary and Legal System",
    category: "Politics",
    difficulty: "Hard",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 30,
    chapter_name: "Federal Structure",
    category: "Politics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },

  // ===== ECONOMICS CHAPTERS =====
  {
    chapter_id: 31,
    chapter_name: "Supply and Demand",
    category: "Economics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 32,
    chapter_name: "Economic Systems",
    category: "Economics",
    difficulty: "Hard",
    estimated_study_hours: 4.5,
  },
  {
    chapter_id: 33,
    chapter_name: "National Income and GDP",
    category: "Economics",
    difficulty: "Hard",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 34,
    chapter_name: "Money and Banking",
    category: "Economics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 35,
    chapter_name: "Inflation and Deflation",
    category: "Economics",
    difficulty: "Medium",
    estimated_study_hours: 3.0,
  },
  {
    chapter_id: 36,
    chapter_name: "International Trade",
    category: "Economics",
    difficulty: "Hard",
    estimated_study_hours: 4.0,
  },
  {
    chapter_id: 37,
    chapter_name: "Poverty and Unemployment",
    category: "Economics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 38,
    chapter_name: "Economic Development",
    category: "Economics",
    difficulty: "Medium",
    estimated_study_hours: 3.5,
  },
  {
    chapter_id: 39,
    chapter_name: "Consumer Rights",
    category: "Economics",
    difficulty: "Easy",
    estimated_study_hours: 2.5,
  },
  {
    chapter_id: 40,
    chapter_name: "Globalization",
    category: "Economics",
    difficulty: "Hard",
    estimated_study_hours: 4.0,
  },
];

export const CATEGORIES = ["History", "Geography", "Politics", "Economics"];

export function getChaptersByCategory(category: string): Chapter[] {
  return CHAPTERS.filter((chapter) => chapter.category === category);
}

export function getChapterById(id: number): Chapter | undefined {
  return CHAPTERS.find((chapter) => chapter.chapter_id === id);
}
