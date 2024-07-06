import sqlite3


class Quiz:
    def __init__(self, questions, difficulty):
        self.questions = questions
        self.difficulty = difficulty
        self.score = 0

    def start(self):
        for question in self.questions:
            print(question.text)
            for i, option in enumerate(question.options):
                print(f"{i + 1}. {option}")
            answer = int(input("Ваш ответ: "))
            if question.check_answer(answer):
                self.score += 1
        print(f"Ваш результат: {self.score} правильных ответов")


class Question:
    def __init__(self, text, options, correct_option):
        self.text = text
        self.options = options
        self.correct_option = correct_option

    def check_answer(self, answer):
        return answer == self.correct_option


class User:
    def __init__(self, name, score, difficulty):
        self.name = name
        self.score = score
        self.difficulty = difficulty


class Leaderboard:
    def __init__(self, db):
        self.db = db

    def save_result(self, user):
        self.db.insert_result(user.name, user.score, user.difficulty)

    def show_leaderboard(self, difficulty):
        results = self.db.get_results(difficulty)
        for result in results:
            print(f"Имя: {result[0]}, Очки: {result[1]}")


class Database:
    def __init__(self, db_name="quiz.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    def create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS leaderboard (name TEXT, score INTEGER, difficulty TEXT)"
            )

    def insert_result(self, name, score, difficulty):
        with self.conn:
            self.conn.execute(
                "INSERT INTO leaderboard (name, score, difficulty) VALUES (?, ?, ?)",
                (name, score, difficulty),
            )

    def get_results(self, difficulty):
        cursor = self.conn.execute(
            "SELECT name, score FROM leaderboard WHERE difficulty=? ORDER BY score DESC",
            (difficulty,),
        )
        return cursor.fetchall()


easy_questions = [
    Question("Какого цвета небо?", ["Синий", "Зеленый", "Красный", "Желтый"], 1),
    Question("Сколько дней в августе?", ["28", "29", "30", "31"], 3),
    Question("Какого цвета молоко?", ["чёрное", "белое", "красное", "жёлтое"], 2),
    Question("Сколько ног у человека?", ["123", "2", "4", "5"], 2),
    Question("Столица Германии?", ["Берлин", "Мадрид", "Киев", "Париж"], 3)
]

medium_questions = [
    Question("Первый президент США?", ["Дж.Вашингтон", "Франклин Рузвельт[", "Джон Кеннеди", "Томас Джефферсон"], 1),
    Question("Кто написал 'Граф Монте-Кристо'?", ["Дюма", "Пушкин", "Достоевский", "Толстой"], 2),
    Question("Кто был лучшим футболистом 2019 года?", ["Роналду", "Месси", "Мбаппе", "Круз"], 2),
    Question("Кто является основателем компании Apple?",
             ["Стив Джобс", "Билл Гейтс", "Марк Цукерберг", "Илон Маск"], 2),
    Question("В какой стране появилась компания Ford?", ["США", "Британия", "Франция", "Россия"], 2)
]

hard_questions = [
    Question("С какого года комания Alfa Romeo учавствует в автогонках?", ["1911", "1961", "1990", "2001"], 1),
    Question("Как переводится слово Hello на русский язык?", ["как дела", "привет", "пока", "сделать"], 2),
    Question("четвёртая планета солнечной системы?", ["Марс", "Земля", "Меркурий", "Нептун"], 2),
    Question("Кто является автором картины 'Мона Лиза'?",
             ["Ван Гог", "Пабло Пикассо", "Леонардо да Винчи", "Рембрандт"], 3),
    Question("Что в море является ориентиром для моряка?", ["дельфины", "луна", "волны", "полярная звезда"], 3)
]


def main():
    db = Database()
    leaderboard = Leaderboard(db)

    name = input("Введите ваше имя: ")
    difficulty = input(
        "Выберите уровень сложности (легкий, средний, сложный): ").lower()

    if difficulty == "легкий":
        questions = easy_questions
    elif difficulty == "средний":
        questions = medium_questions
    elif difficulty == "сложный":
        questions = hard_questions
    else:
        print("Некорректный уровень сложности. Попробуйте снова.")
        return

    quiz = Quiz(questions, difficulty)
    quiz.start()

    user = User(name, quiz.score, difficulty)
    leaderboard.save_result(user)

    print("\nТаблица лидеров в этой категории сложности:")
    leaderboard.show_leaderboard(difficulty)


if __name__ == "__main__":
    main()
