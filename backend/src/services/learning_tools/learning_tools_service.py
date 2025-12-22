"""
Learning Tools Service for the textbook generation system.

This module implements auto-generated summaries, quizzes, and learning boosters
as specified in the constitution requirements.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import random
import re

from ...models.textbook import Textbook
from ...models.chapter import Chapter
from ...models.section import Section
from ...services.personalization.personalization_service import PersonalizationService


class LearningToolsService:
    """
    Service class for generating learning tools including summaries, quizzes, and boosters.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.personalization_service = PersonalizationService()

    async def generate_summary(self, content: str, length: str = 'medium') -> str:
        """
        Generate a summary of the provided content.

        Args:
            content: Content to summarize
            length: Length of summary ('short', 'medium', 'long')

        Returns:
            Generated summary
        """
        if not content:
            return ""

        # Simple approach: extract key sentences based on length
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Determine number of sentences based on requested length
        if length == 'short':
            num_sentences = min(3, len(sentences))
        elif length == 'long':
            num_sentences = min(10, len(sentences))
        else:  # medium
            num_sentences = min(6, len(sentences))

        # Select sentences to include in summary (every nth sentence)
        if len(sentences) <= num_sentences:
            selected_sentences = sentences
        else:
            step = len(sentences) // num_sentences
            selected_sentences = [sentences[i] for i in range(0, len(sentences), step)][:num_sentences]

        summary = '. '.join(selected_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'

        return summary

    async def generate_chapter_summary(self, chapter: Chapter) -> Dict[str, Any]:
        """
        Generate a summary for a chapter.

        Args:
            chapter: Chapter to summarize

        Returns:
            Dictionary with chapter summary information
        """
        summary = await self.generate_summary(chapter.content or chapter.summary or chapter.title)

        return {
            'chapter_id': chapter.id,
            'chapter_title': chapter.title,
            'chapter_number': chapter.chapter_number,
            'summary': summary,
            'generated_at': datetime.now().isoformat(),
            'word_count': len(summary.split())
        }

    async def generate_textbook_summary(self, textbook: Textbook) -> Dict[str, Any]:
        """
        Generate a summary for an entire textbook.

        Args:
            textbook: Textbook to summarize

        Returns:
            Dictionary with textbook summary information
        """
        content_to_summarize = textbook.generated_content or textbook.description or textbook.title
        summary = await self.generate_summary(content_to_summarize, 'long')

        return {
            'textbook_id': textbook.id,
            'textbook_title': textbook.title,
            'summary': summary,
            'generated_at': datetime.now().isoformat(),
            'word_count': len(summary.split())
        }

    async def generate_quiz_questions(self, content: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate quiz questions based on the content.

        Args:
            content: Content to generate questions from
            num_questions: Number of questions to generate

        Returns:
            List of quiz questions
        """
        if not content:
            return []

        # Simple approach: extract key concepts and generate questions based on them
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]  # Filter short sentences

        questions = []
        used_sentences = set()

        for i in range(min(num_questions, len(sentences))):
            # Pick a random sentence that hasn't been used
            available_sentences = [s for s in sentences if s not in used_sentences]
            if not available_sentences:
                break

            sentence = random.choice(available_sentences)
            used_sentences.add(sentence)

            # Generate a question based on the sentence
            question = await self._generate_question_from_sentence(sentence, i + 1)
            if question:
                questions.append(question)

        # If we don't have enough questions, generate some generic ones
        while len(questions) < num_questions:
            question = {
                'id': f'gen_q_{len(questions) + 1}',
                'question': f'What are the key concepts covered in this chapter?',
                'type': 'open_ended',
                'options': [],
                'correct_answer': 'Various concepts depending on the chapter content',
                'difficulty': 'medium'
            }
            questions.append(question)

        return questions

    async def _generate_question_from_sentence(self, sentence: str, question_num: int) -> Optional[Dict[str, Any]]:
        """
        Generate a question based on a specific sentence.

        Args:
            sentence: Sentence to generate question from
            question_num: Question number for ID generation

        Returns:
            Generated question dictionary or None if unable to generate
        """
        words = sentence.split()
        if len(words) < 5:
            return None

        # Identify potential key terms/concepts
        key_terms = [word for word in words if len(word) > 4 and word.isalpha()]
        if not key_terms:
            key_terms = words

        key_term = random.choice(key_terms)

        # Determine question type based on content
        if '?' in sentence or any(w.lower() in ['what', 'who', 'where', 'when', 'why', 'how'] for w in words[:5]):
            question_type = 'factual'
        elif any(w.lower() in ['define', 'meaning', 'term', 'concept'] for w in words):
            question_type = 'definition'
        else:
            question_type = 'comprehension'

        # Generate question based on type
        if question_type == 'definition':
            question_text = f"What is the definition of '{key_term}' as described in the text?"
            difficulty = 'easy'
        elif question_type == 'factual':
            question_text = f"According to the text, what is the significance of '{key_term}'?"
            difficulty = 'medium'
        else:  # comprehension
            question_text = f"How does the concept of '{key_term}' relate to the overall topic?"
            difficulty = 'medium'

        # Generate multiple choice options (for MCQ type)
        options = [
            f"This concept relates to {key_term}",
            f"{key_term} is a key term in this context",
            f"The text discusses {key_term} extensively",
            f"All of the above"  # This would be the correct answer
        ]

        # Shuffle options to avoid predictable pattern
        random.shuffle(options)

        return {
            'id': f'q_{question_num}',
            'question': question_text,
            'type': 'multiple_choice' if random.choice([True, False]) else 'short_answer',
            'options': options if random.choice([True, False]) else [],
            'correct_answer': options[-1] if options and 'all of the above' in options[-1].lower() else f"Information about {key_term} in the text",
            'difficulty': difficulty
        }

    async def generate_chapter_quiz(self, chapter: Chapter, num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate a quiz for a specific chapter.

        Args:
            chapter: Chapter to generate quiz for
            num_questions: Number of questions to generate

        Returns:
            Dictionary with quiz information
        """
        questions = await self.generate_quiz_questions(
            (chapter.content or chapter.summary or chapter.title),
            num_questions
        )

        return {
            'chapter_id': chapter.id,
            'chapter_title': chapter.title,
            'chapter_number': chapter.chapter_number,
            'questions': questions,
            'total_questions': len(questions),
            'generated_at': datetime.now().isoformat(),
            'recommended_time': len(questions) * 2  # 2 minutes per question
        }

    async def generate_textbook_quiz(self, textbook: Textbook, num_questions: int = 10) -> Dict[str, Any]:
        """
        Generate a comprehensive quiz for the entire textbook.

        Args:
            textbook: Textbook to generate quiz for
            num_questions: Number of questions to generate

        Returns:
            Dictionary with comprehensive quiz information
        """
        content = textbook.generated_content or textbook.description
        questions = await self.generate_quiz_questions(content, num_questions)

        return {
            'textbook_id': textbook.id,
            'textbook_title': textbook.title,
            'questions': questions,
            'total_questions': len(questions),
            'generated_at': datetime.now().isoformat(),
            'recommended_time': len(questions) * 2.5  # 2.5 minutes per question for comprehensive quiz
        }

    async def generate_learning_boosters(self, content: str, num_boosters: int = 3) -> List[Dict[str, Any]]:
        """
        Generate learning boosters for the content.

        Args:
            content: Content to generate boosters for
            num_boosters: Number of boosters to generate

        Returns:
            List of learning boosters
        """
        boosters = []

        # Generate different types of learning boosters
        booster_types = [
            "key_concept",
            "memory_tip",
            "real_world_connection",
            "critical_thinking",
            "application_example"
        ]

        for i in range(num_boosters):
            booster_type = random.choice(booster_types)

            if booster_type == "key_concept":
                booster = {
                    "type": "key_concept",
                    "title": "Key Concept Reminder",
                    "content": f"Remember the key concept: {random.choice(content.split()[:10] if content.split() else ['important topic'])}. This concept is fundamental to understanding the material.",
                    "tip": "Review this concept before moving to the next section."
                }
            elif booster_type == "memory_tip":
                booster = {
                    "type": "memory_tip",
                    "title": "Memory Tip",
                    "content": f"Use this mnemonic or visualization technique to remember the important information in this section.",
                    "tip": "Create a mental image or acronym to help recall the main points."
                }
            elif booster_type == "real_world_connection":
                booster = {
                    "type": "real_world_connection",
                    "title": "Real-World Connection",
                    "content": f"Think about how this concept applies in real-life situations or current events.",
                    "tip": "Try to find examples in your daily life where this concept is evident."
                }
            elif booster_type == "critical_thinking":
                booster = {
                    "type": "critical_thinking",
                    "title": "Critical Thinking Question",
                    "content": f"Consider: How might this concept be challenged or applied differently in various contexts?",
                    "tip": "Evaluate the strengths and limitations of this concept."
                }
            else:  # application_example
                booster = {
                    "type": "application_example",
                    "title": "Application Example",
                    "content": f"Try applying this concept to a new situation or problem.",
                    "tip": "Create your own example or scenario that uses this concept."
                }

            booster['id'] = f'booster_{i+1}'
            booster['generated_at'] = datetime.now().isoformat()
            boosters.append(booster)

        return boosters

    async def generate_chapter_learning_materials(self, chapter: Chapter) -> Dict[str, Any]:
        """
        Generate all learning materials for a chapter (summary, quiz, boosters).

        Args:
            chapter: Chapter to generate learning materials for

        Returns:
            Dictionary with all learning materials
        """
        summary = await self.generate_chapter_summary(chapter)
        quiz = await self.generate_chapter_quiz(chapter, 5)
        boosters = await self.generate_learning_boosters(chapter.content or chapter.summary or chapter.title, 3)

        return {
            'chapter_id': chapter.id,
            'chapter_title': chapter.title,
            'chapter_number': chapter.chapter_number,
            'summary': summary,
            'quiz': quiz,
            'boosters': boosters,
            'generated_at': datetime.now().isoformat()
        }

    async def generate_textbook_learning_materials(self, textbook: Textbook) -> Dict[str, Any]:
        """
        Generate comprehensive learning materials for a textbook.

        Args:
            textbook: Textbook to generate learning materials for

        Returns:
            Dictionary with comprehensive learning materials
        """
        summary = await self.generate_textbook_summary(textbook)
        quiz = await self.generate_textbook_quiz(textbook, 15)
        boosters = await self.generate_learning_boosters(textbook.generated_content or textbook.description, 5)

        return {
            'textbook_id': textbook.id,
            'textbook_title': textbook.title,
            'summary': summary,
            'quiz': quiz,
            'boosters': boosters,
            'generated_at': datetime.now().isoformat()
        }

    async def personalize_learning_materials(self, materials: Dict[str, Any], user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Personalize learning materials based on user preferences.

        Args:
            materials: Original learning materials
            user_preferences: User preferences for personalization

        Returns:
            Personalized learning materials
        """
        # Adjust difficulty based on user preferences
        if 'learning_preferences' in user_preferences:
            user_pref = user_preferences['learning_preferences']

            # Adjust quiz difficulty
            if 'difficulty_level' in user_pref:
                difficulty = user_pref['difficulty_level']
                for question in materials.get('quiz', {}).get('questions', []):
                    question['difficulty'] = difficulty

            # Adjust summary length
            if 'reading_preference' in user_pref:
                reading_pref = user_pref['reading_preference']
                if reading_pref == 'concise':
                    # The summary was already generated, but we could regenerate with shorter length
                    pass
                elif reading_pref == 'detailed':
                    # Could expand summaries if needed
                    pass

        # Adjust based on learning style
        if 'learning_style' in user_preferences:
            learning_style = user_preferences['learning_style']

            # Modify boosters based on learning style
            for booster in materials.get('boosters', []):
                if learning_style == 'visual':
                    booster['tip'] = booster.get('tip', '') + " Consider drawing a diagram or chart to visualize this."
                elif learning_style == 'auditory':
                    booster['tip'] = booster.get('tip', '') + " Try explaining this concept aloud to someone else."
                elif learning_style == 'kinesthetic':
                    booster['tip'] = booster.get('tip', '') + " Try a hands-on activity related to this concept."

        materials['personalized_at'] = datetime.now().isoformat()
        materials['personalization_applied'] = True

        return materials


# Example usage:
# learning_tools = LearningToolsService()
# summary = await learning_tools.generate_summary(textbook_content)
# quiz = await learning_tools.generate_quiz_questions(textbook_content, 10)
# boosters = await learning_tools.generate_learning_boosters(textbook_content)