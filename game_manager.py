import html
import PySimpleGUI as sg
import pandas as pd

from generator import Generator
from player import Player


class Game:
    def __init__(self):
        self.LEADER_BOARD = None
        self.VALUES = None
        self.OPTIONS_FONT = None
        self.CATEGORIES = None
        self.OPTIONS = None
        self.QUESTION = None
        self.GENERATOR = None
        self.ANSWER_SELECTION = None
        self.CATEGORY_SELECTION = None
        self.WINDOW = None
        self.FONT = None
        self.DIGIT_FONT = None
        self.FILENAME = r'resources/Millionaire.png'  # if you want to use a file instead of data, then use this in Image Element
        self.FILENAME_SMALL = r'resources/Millionaire_small.png'
        self.DISPLAY_TIME_MILLISECONDS = 4000
        self.WINDOW_SIZE = (900, 560)
        self.LEADERBOARD_WINDOW_SIZE = (650, 250)
        self.TEXT_BG = ['#060644', '#161458', '#6844C6']
        self.TABLE_BG = '#5848A6'
        self.WINDOW_BG = '#060644'
        self.PLAYERS = dict()
        self.HEADINGS = ['Name', 'Score', 'Games Played', 'Questions']
        self.GENERATOR = Generator()
        self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv('resources/leaderboard.csv')
        except FileNotFoundError:
            sg.popup_quick_message('No Save data', background_color=self.TEXT_BG[0])

        else:
            self.VALUES = [[row['Name'], int(row['Score']), int(row['Games Played']), int(row['Questions Answered'])]
                           for
                           _, row in
                           df.iterrows()]

        self.LEADER_BOARD = pd.read_csv('resources/leaderboard.csv')

    def splash_screen(self):
        sg.Window('Window Title', [[sg.Image(filename=self.FILENAME)]], size=self.WINDOW_SIZE,
                  transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(
            timeout=self.DISPLAY_TIME_MILLISECONDS, close=True)

    def add_player(self, player_name):
        self.PLAYERS[player_name] = Player(player_name)  # Creates a new player object

    def get_players(self):
        return self.PLAYERS

    def get_window(self, window_name=None):
        score_life_col = [[sg.T('Score:', background_color=self.TEXT_BG[1],
                                font=self.FONT),
                           sg.T('', background_color=self.TEXT_BG[2],
                                font=self.DIGIT_FONT,
                                size=(10, 1),
                                key='-SCORE-')], [sg.T('Lives: ', background_color=self.TEXT_BG[1],
                                                       font=self.FONT),
                                                  sg.T('', background_color=self.TEXT_BG[2],
                                                       font=self.DIGIT_FONT,
                                                       size=(10, 1),
                                                       key='-LIVES-')]]
        col1 = sg.Col([[sg.Text('Name', background_color=self.TEXT_BG[0]), sg.InputText(key='-PLAYER_NAME-'),
                        sg.Button('Add Player', bind_return_key=True, key='-ADD_PLAYER-')],
                       [sg.Image(filename=self.FILENAME_SMALL, pad=((200, 0), (100, 50)))]],
                      background_color=self.WINDOW_BG,
                      expand_y=True, pad=((0, 100), (0, 0)))

        col2 = sg.Col([[sg.Table('', headings=['Player ' + self.HEADINGS[0]], background_color=self.TABLE_BG,
                                 num_rows=5, justification='left', key='-PLAYERS_TABLE-')],
                       [sg.Button('Start Game', key='-START_GAME-')]],
                      background_color=self.WINDOW_BG, expand_y=True, pad=((0, 0), (0, 0)))

        welcome_layout = [[sg.Button('Leaderboard', key='-LEADERBOARD-', tooltip='view leaderboard')],
                          [sg.Col([[col1, col2]], background_color=self.WINDOW_BG, )]]

        category_layout = [
            [sg.T('Choose question category', background_color=self.TEXT_BG[0], font=self.FONT)],
            [sg.Frame('Category Options',
                      [[sg.Radio('', group_id=1, font=self.FONT, background_color=self.TEXT_BG[0],
                                 visible=False, key=f'-CATEGORY_B{x}')] for x in range(5)],
                      expand_x=True, background_color=self.TEXT_BG[0], key='-CATEGORY_FRAME-')
             ], [sg.Button('Submit', size=(10, 1), key='-CATEGORY_SUBMIT-')]]

        question_layout = [
            [sg.Text(background_color=self.TEXT_BG[0], font=self.FONT)],
            [sg.Text(font=self.FONT, background_color=self.TEXT_BG[0], key='-QUESTION-')],
            [sg.Frame('Question Options',
                      [[sg.Radio('', group_id=2, font=self.OPTIONS_FONT, background_color=self.TEXT_BG[0],
                                 visible=False, key=f'-QUESTION_B{x}')] for x in range(5)],
                      expand_x=False, background_color=self.TEXT_BG[0], key='-QUESTION_FRAME-')
             ], [sg.Button('Submit', size=(10, 1), key='-ANSWER_SUBMIT-')]]

        game_layout = [
            [sg.Button('Leaderboard', key='-LEADERBOARD-', tooltip='view leaderboard'),
             sg.Col(score_life_col, pad=((630, 0), (20, 0)), background_color='#161458')],
            [sg.T('Player Turn:', background_color=self.TEXT_BG[0], font=self.FONT),
             sg.T('', key='-PLAYER_NAME-', background_color=self.TEXT_BG[0], font=self.FONT)],
            # [sg.Col(category_layout, background_color=self.TEXT_BG[0], visible=False,
            #        key='-CATEGORY_LAYOUT-')],
            [sg.Col(question_layout, background_color=self.TEXT_BG[0], visible=True,
                    key='-QUESTION_LAYOUT-')]]

        leaderboard_layout = [
            [sg.Table(values=self.VALUES, headings=self.HEADINGS, background_color=self.TABLE_BG, num_rows=10,
                      justification='left', expand_y=True, expand_x=True,
                      def_col_width=5, auto_size_columns=True, key='-PLAYERS_TABLE-')],
            [sg.OK(size=(5, 1))]
        ]

        if window_name is None:
            self.WINDOW = sg.Window('Who wants to be a Millionaire !!'
                                    , welcome_layout, size=self.WINDOW_SIZE,
                                    background_color=self.WINDOW_BG, finalize=True)
        if window_name == 'game_layout':
            self.WINDOW = sg.Window('Millionaire!!'
                                    , game_layout, size=self.WINDOW_SIZE,
                                    background_color=self.WINDOW_BG, finalize=True)
        if window_name == 'leaderboard_layout':
            main_window_loc = self.WINDOW.current_location()
            main_window_loc = (main_window_loc[0] + 15, main_window_loc[1] + 64)
            sub_window = sg.Window('Leaderboard', leaderboard_layout, size=self.LEADERBOARD_WINDOW_SIZE,
                                   location=main_window_loc,
                                   keep_on_top=True,
                                   background_color=self.WINDOW_BG, no_titlebar=True, transparent_color=self.WINDOW_BG,
                                   grab_anywhere=True,
                                   finalize=True)
            return sub_window

        return self.WINDOW

    def update_layout(self, player, event=None):  # TODO
        # category_layout = self.WINDOW['-CATEGORY_LAYOUT-']
        question_layout = self.WINDOW['-QUESTION_LAYOUT-']

        #  ---- Layout button Generators ----
        # category_visible = (lambda z: window[f'-CATEGORY_B{z}'].update(text=self.CATEGORIES[z], visible=True))
        # category_invisible = (lambda y: window[f'-CATEGORY_B{y}'].update(text='', visible=False))
        question_visible = (
            lambda z: self.WINDOW[f'-QUESTION_B{z}'].update(value=False, text=html.unescape(self.OPTIONS[z]),
                                                            visible=True))
        question_invisible = (lambda y: self.WINDOW[f'-QUESTION_B{y}'].update(text='', visible=False))
        self.WINDOW['-PLAYER_NAME-'].update(value=player.name)
        self.WINDOW['-SCORE-'].update(value=player.total_score)
        self.WINDOW['-LIVES-'].update(value=player.life)
        self.WINDOW['-QUESTION-'].update(value=html.unescape(self.QUESTION['question']))
        ac = len(self.OPTIONS)
        [question_visible(x) if x < ac else question_invisible(x) for x in range(ac)]

    def ask_question(self, player):
        self.QUESTION, self.OPTIONS = self.GENERATOR.get_question()
        self.update_layout(player)

    def get_selected_option(self, values):
        for key, value in values.items():
            if value:
                if '-CATEGORY_B' in key:  # Not yet implemented
                    self.CATEGORY_SELECTION = self.CATEGORIES[int(key.strip('-CATEGORY_B'))]
                if '-QUESTION_B' in key:
                    self.ANSWER_SELECTION = self.OPTIONS[int(key.strip('-QUESTION_B'))]

    def check_answer(self, player):
        self.GENERATOR.check_answer(self.QUESTION, self.ANSWER_SELECTION, player)

    def update_deal_count(self):
        self.GENERATOR.deals += 1

    def game_over(self):
        sg.popup_quick_message('GAME OVER')

    def update_leaderboard(self):
        leaderboard_names = []
        try:
            for i, row in self.LEADER_BOARD.iterrows():
                ts = row['Score'] + self.PLAYERS[row['Name']].total_score
                gp = row['Games Played'] + self.PLAYERS[row['Name']].games_played + 1
                qa = row['Questions Answered'] + self.PLAYERS[row['Name']].questions_answered
                leaderboard_names.append(row['Name'])
                self.LEADER_BOARD.loc[i, ['Score', 'Games Played', 'Questions Answered']] = [ts, gp, qa]
        except:
            # TODO: suppose to do something here
            pass
        player_, score, games_played, questions_answered = list(), list(), list(), list()
        players = list(self.PLAYERS.keys())
        for player in leaderboard_names:
            players.remove(player)

        for player in players:
            player_.append(player)
            score.append(self.PLAYERS[player].total_score)
            games_played.append(self.PLAYERS[player].games_played + 1)
            questions_answered.append(self.PLAYERS[player].questions_answered)

        df2 = pd.DataFrame({'Name': player_,
                            'Score': score,
                            'Games Played': games_played,
                            'Questions Answered': questions_answered})
        self.LEADER_BOARD = pd.concat([self.LEADER_BOARD, df2], ignore_index=True)

    def save(self):
        sg.popup_quick_message('Data Saved')
        self.LEADER_BOARD.to_csv('leaderboard.csv', index=False)

    def update_deals(self):
        self.GENERATOR.update_deals()
