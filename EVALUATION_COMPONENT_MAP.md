# Evaluation Module - Component Map

Visual guide to all components and their relationships.

---

## 🗺️ Page Structure

```
/dashboard/social/evaluation
│
├─ EvaluationPage
│  ├─ Header (Title + "View History" Button)
│  ├─ EvaluationForm
│  │  ├─ Question Input (Textarea)
│  │  ├─ Student Answer Input (Textarea)
│  │  ├─ Chapter Select (Dropdown)
│  │  └─ Submit Button
│  │
│  ├─ EvaluationLoadingSkeleton (during evaluation)
│  │  ├─ Skeleton Cards
│  │  └─ Rotating Messages
│  │
│  └─ EvaluationResultCard (after evaluation)
│     ├─ ScoreCard
│     │  ├─ Score Display (X / 5)
│     │  ├─ Percentage
│     │  ├─ Status Badge
│     │  └─ Progress Bar
│     │
│     ├─ FeedbackCard
│     │  └─ AI Feedback Text
│     │
│     ├─ StrengthsCard
│     │  └─ Strength List (✓ items)
│     │
│     ├─ ImprovementCard
│     │  └─ Improvement List (• items)
│     │
│     ├─ ModelAnswerCard
│     │  └─ Ideal Answer Text
│     │
│     ├─ Question Section
│     │  └─ Original Question
│     │
│     └─ Student Answer Section
│        └─ Submitted Answer

/dashboard/social/evaluation/history
│
└─ EvaluationHistoryPage
   ├─ Header (Title + "New Evaluation" Button)
   │
   ├─ Chapter Performance Section
   │  └─ ChapterPerformanceCard × N
   │     ├─ Chapter Icon + Name
   │     ├─ Status Badge
   │     ├─ Average Score + Progress Bar
   │     ├─ Stats Grid
   │     │  ├─ Total Evaluations
   │     │  ├─ Total Marks
   │     │  ├─ Best Score
   │     │  └─ Lowest Score
   │     └─ Last Evaluation Date
   │
   ├─ EvaluationFilters
   │  ├─ Search Input
   │  ├─ Chapter Filter
   │  ├─ Score Range Filter
   │  └─ Sort By Select
   │
   ├─ Results Summary
   │  └─ "Showing X of Y evaluations"
   │
   ├─ EvaluationHistoryTable
   │  ├─ Desktop: Table View
   │  │  ├─ Date Column
   │  │  ├─ Chapter Column
   │  │  ├─ Question Column
   │  │  ├─ Score Column
   │  │  ├─ Status Column
   │  │  └─ Actions Column (View, Delete)
   │  │
   │  └─ Mobile: Card View
   │     ├─ Question + Date
   │     ├─ Status Badge
   │     ├─ Chapter + Score
   │     └─ Actions (View, Delete)
   │
   └─ EvaluationDetailsDialog (Modal)
      ├─ Dialog Header
      │  ├─ Title
      │  └─ Status Badge
      │
      └─ Scrollable Content
         ├─ Score Section (Large)
         │  ├─ Score Display
         │  ├─ Percentage
         │  └─ Progress Bar
         │
         ├─ Feedback Card
         ├─ Strengths Card
         ├─ Improvements Card
         ├─ Model Answer Card
         ├─ Question Card
         ├─ Student Answer Card
         └─ Metadata (Chapter, Date)
```

---

## 🧩 Component Hierarchy

```
App
└─ Dashboard Layout
   └─ SocialNav (UPDATED with Evaluation link)
      └─ Evaluation Section
         │
         ├─ /evaluation [Main Page]
         │  └─ EvaluationPage
         │     ├─ EvaluationForm
         │     ├─ EvaluationLoadingSkeleton
         │     └─ EvaluationResultCard
         │        ├─ ScoreCard
         │        ├─ FeedbackCard
         │        ├─ StrengthsCard
         │        ├─ ImprovementCard
         │        └─ ModelAnswerCard
         │
         └─ /evaluation/history [History Page]
            └─ EvaluationHistoryPage
               ├─ ChapterPerformanceCard (multiple)
               ├─ EvaluationFilters
               ├─ EvaluationHistoryTable
               └─ EvaluationDetailsDialog
```

---

## 📦 Component Dependencies

### Core UI Components (shadcn/ui)
```
ui/
├─ alert.tsx                 → Used by: EvaluationHistoryPage (errors)
├─ alert-dialog.tsx          → Used by: EvaluationHistoryTable (delete confirm)
├─ badge.tsx                 → Used by: All score displays
├─ button.tsx                → Used by: All pages
├─ card.tsx                  → Used by: All content sections
├─ dialog.tsx                → Used by: EvaluationDetailsDialog
├─ input.tsx                 → Used by: EvaluationForm, EvaluationFilters
├─ label.tsx                 → Used by: Forms
├─ progress.tsx              → Used by: Score displays
├─ scroll-area.tsx           → Used by: EvaluationDetailsDialog
├─ select.tsx                → Used by: EvaluationForm, EvaluationFilters
├─ separator.tsx             → Used by: Various content sections
├─ skeleton.tsx              → Used by: Loading states
└─ table.tsx                 → Used by: EvaluationHistoryTable
```

### Evaluation Components
```
evaluation/
├─ ChapterPerformanceCard       → Standalone, uses: Card, Badge, Progress
├─ EvaluationDetailsDialog      → Uses: Dialog, ScrollArea, all cards
├─ EvaluationFilters            → Uses: Card, Input, Select, Label
├─ EvaluationForm               → Uses: Card, Input, Textarea, Select, Button
├─ EvaluationHistoryTable       → Uses: Table, Button, Badge, AlertDialog
├─ EvaluationLoadingSkeleton    → Uses: Card, Skeleton
├─ EvaluationResultCard         → Composite, uses all cards below
├─ FeedbackCard                 → Uses: Card
├─ ImprovementCard              → Uses: Card
├─ ModelAnswerCard              → Uses: Card
├─ ScoreCard                    → Uses: Card, Badge, Progress
└─ StrengthsCard                → Uses: Card
```

---

## 🔄 Data Flow

```
┌─────────────────┐
│  User Action    │
│  (Submit Form)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  EvaluationForm     │
│  validates input    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────┐
│  evaluation-api.ts      │
│  evaluateAnswer()       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Backend API                │
│  POST /evaluations/evaluate │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  AI Services            │
│  - RAG (model answer)   │
│  - Gemini (evaluation)  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────┐
│  Database           │
│  Save evaluation    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────┐
│  API Response           │
│  EvaluationResponse     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  EvaluationResultCard   │
│  Display results        │
└─────────────────────────┘
```

---

## 🎨 Styling System

### Color Coding by Score Status

```
Excellent (≥80%)
├─ Text: text-green-600
├─ Background: bg-green-50
├─ Border: border-green-200
└─ Progress: bg-green-600

Good (60-79%)
├─ Text: text-blue-600
├─ Background: bg-blue-50
├─ Border: border-blue-200
└─ Progress: bg-blue-600

Needs Improvement (<60%)
├─ Text: text-amber-600
├─ Background: bg-amber-50
├─ Border: border-amber-200
└─ Progress: bg-amber-600
```

### Component Styling Patterns

```
Card Layouts
├─ Standard: p-6, rounded-lg, border, shadow-sm
├─ Header: pb-3, flex, items-start, justify-between
├─ Content: pt-6, space-y-4
└─ Footer: pt-4, border-t

Responsive Breakpoints
├─ Mobile: 320px-767px (cards stack, single column)
├─ Tablet: 768px-1023px (2 columns)
└─ Desktop: 1024px+ (3-4 columns)

Typography
├─ Page Title: text-3xl, font-bold, tracking-tight
├─ Card Title: text-lg, font-semibold
├─ Body Text: text-sm, text-muted-foreground
└─ Labels: text-xs, text-muted-foreground
```

---

## 🔌 API Integration Points

```
Component                    → API Method                      → Endpoint
───────────────────────────────────────────────────────────────────────────
EvaluationForm              → evaluateAnswer()                → POST /evaluations/evaluate
EvaluationHistoryPage       → getUserEvaluations()            → GET /evaluations
EvaluationHistoryPage       → getChaptersPerformance()        → GET /evaluations/stats/chapters
EvaluationHistoryTable      → deleteEvaluation()              → DELETE /evaluations/{id}
EvaluationDetailsDialog     → [Data passed as prop]           → (No direct API call)
ChapterPerformanceCard      → [Data passed as prop]           → (No direct API call)
```

---

## 🧭 Navigation Flow

```
User Journey 1: First Evaluation
┌───────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Dashboard   │ ──> │   Evaluation    │ ──> │  View Results    │
│               │     │   Submit Form   │     │  (Result Card)   │
└───────────────┘     └─────────────────┘     └────────┬─────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │  View History    │
                                              │  Button          │
                                              └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │  History Page    │
                                              └──────────────────┘

User Journey 2: Review Past Evaluations
┌───────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Dashboard   │ ──> │  Evaluation     │ ──> │  View History    │
│               │     │  (Navbar Link)  │     │  Button          │
└───────────────┘     └─────────────────┘     └────────┬─────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │  History Page    │
                                              │  - Apply Filters │
                                              │  - View Details  │
                                              └──────────────────┘

User Journey 3: Track Progress
┌───────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  History Page │ ──> │  Scroll to      │ ──> │  Identify Weak   │
│               │     │  Chapter Perf.  │     │  Chapters        │
└───────────────┘     └─────────────────┘     └────────┬─────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │  Back to Eval    │
                                              │  Submit New      │
                                              └──────────────────┘
```

---

## 📱 Responsive Behavior

```
Desktop (1024px+)
├─ Navigation: Full text labels
├─ Chapter Performance: 4 columns grid
├─ History Table: Full table with all columns
├─ Filters: 4 columns (Search, Chapter, Score, Sort)
└─ Dialogs: Max width 4xl, centered

Tablet (768px-1023px)
├─ Navigation: Full text labels
├─ Chapter Performance: 2-3 columns grid
├─ History Table: Full table (may scroll horizontally)
├─ Filters: 2 columns
└─ Dialogs: Max width 3xl, centered

Mobile (375px-767px)
├─ Navigation: Icons only on very small screens
├─ Chapter Performance: 1-2 columns grid
├─ History Table: Card view (no table)
├─ Filters: Stack vertically
└─ Dialogs: Full screen, 90vh max height

Small Mobile (320px-374px)
├─ Navigation: Icons only
├─ Chapter Performance: 1 column
├─ History Table: Compact cards
├─ Filters: Single column, smaller inputs
└─ Dialogs: Full screen
```

---

## 🔍 State Management

```
EvaluationPage State
├─ isLoading: boolean
├─ error: string | null
└─ evaluation: EvaluationResponse | null

EvaluationHistoryPage State
├─ evaluations: Evaluation[]
├─ chapterPerformance: ChapterPerformance[]
├─ isLoading: boolean
├─ isLoadingPerformance: boolean
├─ error: string | null
├─ deletingId: string | null
├─ selectedEvaluation: Evaluation | null
├─ dialogOpen: boolean
└─ filters: EvaluationFilters
   ├─ searchQuery: string
   ├─ chapter: string
   ├─ scoreRange: string
   └─ sortBy: "newest" | "oldest" | "highest" | "lowest"
```

---

## 🎯 Key Interactions

### Evaluation Submission
1. User fills form
2. Client validates (required fields)
3. Submit button triggers API call
4. Loading skeleton appears
5. Backend processes (15-30s)
6. Results display
7. Option to view history or evaluate again

### History Filtering
1. User types in search box
2. Client filters evaluations instantly
3. Results update in real-time
4. No API call (client-side)

### View Details
1. User clicks "View" button
2. Modal opens with evaluation data
3. Scrollable content
4. Close button or click outside to dismiss

### Delete Evaluation
1. User clicks delete icon
2. Confirmation dialog appears
3. User confirms
4. API call to delete
5. Evaluation removed from list
6. Chapter performance updates

---

## 📊 Component Size Guide

```
Component                      Lines of Code    Complexity
──────────────────────────────────────────────────────────
ChapterPerformanceCard              ~120         Medium
EvaluationDetailsDialog             ~250         High
EvaluationFilters                   ~90          Low
EvaluationForm                      ~150         Medium
EvaluationHistoryTable              ~200         High
EvaluationLoadingSkeleton           ~80          Low
EvaluationResultCard                ~150         Medium
FeedbackCard                        ~40          Low
ImprovementCard                     ~50          Low
ModelAnswerCard                     ~50          Low
ScoreCard                           ~80          Medium
StrengthsCard                       ~50          Low

Total Evaluation Components:       ~1,310 LOC
Total UI Components:               ~400 LOC
Total Pages:                       ~400 LOC
Total Services/Utils:              ~500 LOC
───────────────────────────────────────────────────────
TOTAL FRONTEND:                    ~2,610 LOC
```

---

## 🧪 Testing Guide

### Component Testing Priority
1. **High Priority** (Critical Path)
   - EvaluationForm (submission logic)
   - EvaluationHistoryTable (data display)
   - EvaluationFilters (filtering logic)

2. **Medium Priority** (User Experience)
   - EvaluationResultCard (results display)
   - ChapterPerformanceCard (stats display)
   - EvaluationDetailsDialog (modal behavior)

3. **Low Priority** (Visual)
   - Individual card components
   - Loading skeletons
   - UI components

### Test Scenarios
```
✓ Form validation works
✓ Loading states display correctly
✓ Results render with all sections
✓ Filters apply correctly
✓ Sort functions work
✓ Delete confirmation works
✓ Modal opens and closes
✓ Mobile layout adapts
✓ Error states display
✓ Empty states display
```

---

**This component map provides a complete overview of the Evaluation Module architecture!**

Use this as a reference when:
- Adding new features
- Debugging issues
- Onboarding new developers
- Planning refactors
- Understanding data flow

Happy coding! 🚀
