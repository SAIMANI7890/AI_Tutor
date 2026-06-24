"""
AI Study Companion - Automated Retrieval Accuracy Testing Script

This script tests the RAG system's accuracy by asking 20 questions
and verifying the sources and answers.

Usage:
    python test_accuracy.py
"""

import requests
import json
import time
from typing import List, Dict, Tuple
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "password123"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


# Test questions with expected sources
TEST_QUESTIONS = [
    # History Questions
    {
        "id": 1,
        "category": "History",
        "question": "What were the main causes of the French Revolution?",
        "expected_source": "social_history.pdf",
        "keywords": ["economic", "social inequality", "enlightenment", "revolution"]
    },
    {
        "id": 2,
        "category": "History",
        "question": "When did the Industrial Revolution begin and where?",
        "expected_source": "social_history.pdf",
        "keywords": ["18th century", "britain", "industrial"]
    },
    {
        "id": 3,
        "category": "History",
        "question": "What triggered World War I?",
        "expected_source": "social_history.pdf",
        "keywords": ["archduke", "ferdinand", "assassination", "sarajevo"]
    },
    {
        "id": 4,
        "category": "History",
        "question": "What was colonialism and which countries were major colonial powers?",
        "expected_source": "social_history.pdf",
        "keywords": ["britain", "france", "spain", "portugal", "colonial"]
    },
    {
        "id": 5,
        "category": "History",
        "question": "What was the Renaissance and where did it begin?",
        "expected_source": "social_history.pdf",
        "keywords": ["italy", "14th century", "cultural", "renaissance"]
    },
    
    # Geography Questions
    {
        "id": 6,
        "category": "Geography",
        "question": "What is a monsoon and which regions experience it?",
        "expected_source": "social_geography.pdf",
        "keywords": ["seasonal", "wind", "south asia", "rainfall"]
    },
    {
        "id": 7,
        "category": "Geography",
        "question": "What are the major rivers of India?",
        "expected_source": "social_geography.pdf",
        "keywords": ["ganges", "yamuna", "brahmaputra"]
    },
    {
        "id": 8,
        "category": "Geography",
        "question": "What are the different climate zones of the world?",
        "expected_source": "social_geography.pdf",
        "keywords": ["tropical", "temperate", "polar", "climate"]
    },
    {
        "id": 9,
        "category": "Geography",
        "question": "What are renewable and non-renewable resources?",
        "expected_source": "social_geography.pdf",
        "keywords": ["renewable", "solar", "wind", "fossil fuels"]
    },
    {
        "id": 10,
        "category": "Geography",
        "question": "What are the major mountain ranges in Asia?",
        "expected_source": "social_geography.pdf",
        "keywords": ["himalayas", "karakoram", "mountain"]
    },
    
    # Politics Questions
    {
        "id": 11,
        "category": "Politics",
        "question": "What is democracy and what are its key features?",
        "expected_source": "social_politics.pdf",
        "keywords": ["people", "elections", "rights", "representation"]
    },
    {
        "id": 12,
        "category": "Politics",
        "question": "What are the three branches of government?",
        "expected_source": "social_politics.pdf",
        "keywords": ["legislative", "executive", "judicial"]
    },
    {
        "id": 13,
        "category": "Politics",
        "question": "What is a constitution?",
        "expected_source": "social_politics.pdf",
        "keywords": ["supreme law", "fundamental", "constitution"]
    },
    {
        "id": 14,
        "category": "Politics",
        "question": "What are fundamental rights?",
        "expected_source": "social_politics.pdf",
        "keywords": ["rights", "freedom", "fundamental"]
    },
    {
        "id": 15,
        "category": "Politics",
        "question": "What is the role of political parties in democracy?",
        "expected_source": "social_politics.pdf",
        "keywords": ["party", "representation", "governance", "opposition"]
    },
    
    # Economics Questions
    {
        "id": 16,
        "category": "Economics",
        "question": "What is the law of supply and demand?",
        "expected_source": "social_economics.pdf",
        "keywords": ["price", "supply", "demand", "market"]
    },
    {
        "id": 17,
        "category": "Economics",
        "question": "What are the different types of economic systems?",
        "expected_source": "social_economics.pdf",
        "keywords": ["capitalism", "socialism", "mixed economy"]
    },
    {
        "id": 18,
        "category": "Economics",
        "question": "What is GDP and why is it important?",
        "expected_source": "social_economics.pdf",
        "keywords": ["gdp", "gross domestic product", "economic"]
    },
    {
        "id": 19,
        "category": "Economics",
        "question": "What is inflation?",
        "expected_source": "social_economics.pdf",
        "keywords": ["inflation", "prices", "purchasing power"]
    },
    {
        "id": 20,
        "category": "Economics",
        "question": "What is international trade and why do countries trade?",
        "expected_source": "social_economics.pdf",
        "keywords": ["trade", "export", "import", "comparative advantage"]
    }
]


class AccuracyTester:
    def __init__(self):
        self.token = None
        self.session_id = None
        self.results = []
        
    def authenticate(self) -> bool:
        """Authenticate and get JWT token"""
        print_info("Authenticating...")
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login",
                json={
                    "email": TEST_USER_EMAIL,
                    "password": TEST_USER_PASSWORD
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                print_success("Authentication successful")
                return True
            else:
                print_error(f"Authentication failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print_error(f"Authentication error: {str(e)}")
            return False
    
    def check_health(self) -> bool:
        """Check if the API is healthy"""
        print_info("Checking API health...")
        try:
            response = requests.get(f"{API_BASE_URL}/tutor/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    chunks = data.get("data", {}).get("chunks_loaded", 0)
                    print_success(f"API is healthy - {chunks} chunks loaded")
                    return True
            
            print_error("API health check failed")
            return False
            
        except Exception as e:
            print_error(f"Health check error: {str(e)}")
            return False
    
    def create_session(self) -> bool:
        """Create a new chat session"""
        print_info("Creating chat session...")
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{API_BASE_URL}/chat/sessions",
                headers=headers,
                json={"title": f"Accuracy Test - {datetime.now().isoformat()}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get("data", {}).get("id")
                print_success(f"Session created: {self.session_id}")
                return True
            else:
                print_error(f"Session creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Session creation error: {str(e)}")
            return False
    
    def ask_question(self, question: str) -> Tuple[str, List[Dict], float]:
        """
        Ask a question and return the answer, sources, and response time
        
        Returns:
            Tuple[answer, sources, response_time]
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/chat/{self.session_id}/messages",
                headers=headers,
                json={
                    "message": question,
                    "mode": "explain"  # Not Socratic mode for testing
                }
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("data", {}).get("response", "")
                sources = data.get("data", {}).get("sources", [])
                return answer, sources, response_time
            else:
                print_error(f"Question failed: {response.status_code}")
                return "", [], response_time
                
        except Exception as e:
            print_error(f"Question error: {str(e)}")
            return "", [], 0.0
    
    def verify_source(self, sources: List[Dict], expected_source: str) -> bool:
        """Verify if the expected source is in the returned sources"""
        for source in sources:
            if expected_source.lower() in source.get("source", "").lower():
                return True
        return False
    
    def verify_answer(self, answer: str, keywords: List[str]) -> Tuple[bool, int]:
        """
        Verify if the answer contains relevant keywords
        
        Returns:
            Tuple[is_relevant, keyword_count]
        """
        answer_lower = answer.lower()
        keyword_count = sum(1 for keyword in keywords if keyword.lower() in answer_lower)
        is_relevant = keyword_count >= (len(keywords) * 0.5)  # At least 50% of keywords
        return is_relevant, keyword_count
    
    def test_question(self, test_case: Dict) -> Dict:
        """Test a single question and return results"""
        question_id = test_case["id"]
        category = test_case["category"]
        question = test_case["question"]
        expected_source = test_case["expected_source"]
        keywords = test_case["keywords"]
        
        print(f"\n{Colors.BOLD}Question {question_id} ({category}):{Colors.ENDC}")
        print(f"  {question}")
        
        # Ask the question
        answer, sources, response_time = self.ask_question(question)
        
        if not answer:
            print_error("  No answer received")
            return {
                "id": question_id,
                "category": category,
                "question": question,
                "source_correct": False,
                "answer_relevant": False,
                "response_time": 0,
                "passed": False
            }
        
        # Verify source
        source_correct = self.verify_source(sources, expected_source)
        if source_correct:
            print_success(f"  Source: {expected_source} ✓")
        else:
            print_error(f"  Source: Expected {expected_source}, got {[s.get('source') for s in sources]}")
        
        # Verify answer relevance
        answer_relevant, keyword_count = self.verify_answer(answer, keywords)
        if answer_relevant:
            print_success(f"  Answer: Relevant ({keyword_count}/{len(keywords)} keywords) ✓")
        else:
            print_warning(f"  Answer: Less relevant ({keyword_count}/{len(keywords)} keywords)")
        
        # Check response time
        if response_time < 5:
            print_success(f"  Response time: {response_time:.2f}s ✓")
        else:
            print_warning(f"  Response time: {response_time:.2f}s (slow)")
        
        passed = source_correct and answer_relevant
        
        return {
            "id": question_id,
            "category": category,
            "question": question,
            "answer": answer[:200] + "..." if len(answer) > 200 else answer,
            "sources": sources,
            "expected_source": expected_source,
            "source_correct": source_correct,
            "answer_relevant": answer_relevant,
            "keyword_count": keyword_count,
            "total_keywords": len(keywords),
            "response_time": response_time,
            "passed": passed
        }
    
    def run_tests(self):
        """Run all test questions"""
        print_header("AI Study Companion - Accuracy Test")
        
        # Check health
        if not self.check_health():
            print_error("API is not healthy. Please start the backend server.")
            return
        
        # Authenticate
        if not self.authenticate():
            print_error("Authentication failed. Please check credentials.")
            return
        
        # Create session
        if not self.create_session():
            print_error("Session creation failed.")
            return
        
        print_header("Testing Questions")
        
        # Test each question
        for test_case in TEST_QUESTIONS:
            result = self.test_question(test_case)
            self.results.append(result)
            time.sleep(1)  # Rate limiting
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate final test report"""
        print_header("Test Results Summary")
        
        total_questions = len(self.results)
        correct_sources = sum(1 for r in self.results if r["source_correct"])
        relevant_answers = sum(1 for r in self.results if r["answer_relevant"])
        passed = sum(1 for r in self.results if r["passed"])
        
        source_accuracy = (correct_sources / total_questions) * 100
        answer_accuracy = (relevant_answers / total_questions) * 100
        overall_accuracy = (passed / total_questions) * 100
        
        avg_response_time = sum(r["response_time"] for r in self.results) / total_questions
        
        # Print summary
        print(f"\n{Colors.BOLD}Overall Statistics:{Colors.ENDC}")
        print(f"  Total Questions: {total_questions}")
        print(f"  Correct Sources: {correct_sources}/{total_questions} ({source_accuracy:.1f}%)")
        print(f"  Relevant Answers: {relevant_answers}/{total_questions} ({answer_accuracy:.1f}%)")
        print(f"  Overall Passed: {passed}/{total_questions} ({overall_accuracy:.1f}%)")
        print(f"  Avg Response Time: {avg_response_time:.2f}s")
        
        # Print category breakdown
        print(f"\n{Colors.BOLD}Category Breakdown:{Colors.ENDC}")
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0}
            categories[cat]["total"] += 1
            if result["passed"]:
                categories[cat]["passed"] += 1
        
        for cat, stats in categories.items():
            accuracy = (stats["passed"] / stats["total"]) * 100
            print(f"  {cat}: {stats['passed']}/{stats['total']} ({accuracy:.1f}%)")
        
        # Overall status
        print(f"\n{Colors.BOLD}Overall Status:{Colors.ENDC}")
        if overall_accuracy >= 85:
            print_success(f"PASSED ✓ - {overall_accuracy:.1f}% accuracy (target: 85%+)")
        else:
            print_error(f"FAILED ✗ - {overall_accuracy:.1f}% accuracy (target: 85%+)")
            print_warning("\nImprovement Suggestions:")
            print("  1. Increase chunk size in chunker.py")
            print("  2. Increase top_k in retriever_service.py")
            print("  3. Improve prompt in tutor_prompt.py")
            print("  4. Re-run ingestion pipeline")
        
        # Save detailed report
        self.save_report()
    
    def save_report(self):
        """Save detailed report to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(self.results),
            "correct_sources": sum(1 for r in self.results if r["source_correct"]),
            "relevant_answers": sum(1 for r in self.results if r["answer_relevant"]),
            "passed": sum(1 for r in self.results if r["passed"]),
            "avg_response_time": sum(r["response_time"] for r in self.results) / len(self.results),
            "results": self.results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print_success(f"\nDetailed report saved to: {filename}")


def main():
    """Main entry point"""
    try:
        tester = AccuracyTester()
        tester.run_tests()
    except KeyboardInterrupt:
        print_warning("\n\nTest interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
