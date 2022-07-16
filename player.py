import html


class Player:

    def __init__(self, name):
        self.name = name
        self.life = 4
        self.games_played = 0
        self.total_score = 0
        self.questions_answered = 0

    def answer_question(self, question, options):  # DELETE
        """


        Parameters
        ----------
        question : TYPE
            DESCRIPTION.
        options : TYPE
            DESCRIPTION.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.
        TYPE
            DESCRIPTION.

        """
        options_list = ''

        for i in range(len(options)):
            options_list += f'({i + 1}) {options[i]}\n'
        print(
            html.unescape(f"Question {self.questions_answered + 1} :{question['question']} \n{options_list[:-1]}"))

        try:
            choice = int(input('Answer :'))
            if choice < 1 or choice > len(options):
                raise ValueError
            else:
                print(f'You selected : {options[choice - 1]}')
                self.questions_answered += 1
            return True, options[choice - 1]
        except ValueError:
            print(f'Invalid entry. Please enter number between 1 & {len(options)}')
            return False, None

    def update_score(self, score):
        self.total_score += score

    def update_life(self, value):
        self.life += value
        print(f'You have {self.life} lives left')

    def load(self, score, games_played, questions_answered):
        self.total_score += score
        self.games_played += games_played
        self.questions_answered += questions_answered
