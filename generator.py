import random
import PySimpleGUI as sg
import requests


class Generator:
    # category 0: Any, else, start from 9
    def __init__(self):
        self.difficulty = ['easy', 'medium', 'hard']
        self.type = ['boolean', 'multiple']
        self.questions = ''
        self.categories = ['General Knowledge', 'Entertainment: Cartoon & Animations', 'Entertainment: Film',
                           'Entertainment: Music', 'Entertainment: Television', 'Celebrities', 'Sports',
                           'Entertainment: Comics', 'Science: Mathematics', 'Science: Computers', 'Vehicles', 'Animals',
                           'Science & Nature', 'Entertainment: Video Games', 'Entertainment: Musicals & Theatres',
                           'Entertainment: Books', 'Science: Gadgets', 'Entertainment: Japanese Anime & Manga']
        self.dic = {'category': [0] + [x + 10 for x in range(len(self.categories))],
                    'difficulty': 'easy',
                    'type': ['boolean', 'multiple'],
                    'questions': 50}
        self.deals = 1
        self.deal_value = {3: 200, 5: 400, 7: 600, 9: 400}
        self.get_questions(self.dic)

    def get_questions(self, dic):
        category = random.choice(dic['category'])
        difficulty = dic['difficulty']
        questions = dic['questions']
        type_ = random.choice(dic['type'])
        BaseURL = 'https://opentdb.com/api.php?'
        r = f'amount={str(questions)}&category={str(category)}&difficulty={str(difficulty)}&type={type_}'
        response = requests.get(BaseURL + r, timeout=1000)
        response.raise_for_status()

        if response.status_code != 200 or response.json()["response_code"] == 1:
            self.get_questions(self.dic)  # retry
        else:
            result = response.json()['results']
            self.questions = result
            return result

    def get_question(self):
        options = ['True', 'False']
        question = random.choice(self.questions)
        if question['type'] == 'multiple':
            options = question['incorrect_answers'] + [question['correct_answer']]
            random.shuffle(options)
        return question, options

    def check_answer(self, question: object, answer_selection: object, player: object) -> object:
        value = 0
        keys = list(self.deal_value.keys())
        keys.sort(reverse=True)
        correct_answer = question['correct_answer']
        for key in keys:
            if self.deals < key:
                value = self.deal_value[key]
            else:
                value = self.deal_value[max(keys)]
        if answer_selection == correct_answer:
            sg.popup_quick_message('You are correct!!', background_color='#060644')
            player.total_score += value
            player.questions_answered += 1
        else:
            sg.popup_quick_message(f'You are wrong!!\nThe correct answer is {correct_answer}',
                                   background_color='#060644')
            player.life -= 1

    def update_deals(self):
        self.deals += 1
