from gui_menu import QuizUIMenu
from gui_quiz import QuizUIQuiz
from gui_edit import QuizUIEdit
from gui_ai_generator import QuizUIAIGenerator


class QuizUI(QuizUIMenu, QuizUIQuiz, QuizUIEdit, QuizUIAIGenerator):
    pass