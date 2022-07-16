from game_manager import Game

game = Game()
game.splash_screen()
window = game.get_window()
RUN = False
while True:
    event, values = window.read()
    if event is None:
        window.close()
        break
    if event == '-ADD_PLAYER-' and values['-PLAYER_NAME-'] != '':
        player_name = values['-PLAYER_NAME-']
        game.add_player(player_name)
        window['-PLAYER_NAME-'].update(value='')

    if event == '-START_GAME-':
        window.hide()
        window = game.get_window('game_layout')
        players = game.get_players()
        RUN = True

    if event == '-LEADERBOARD-':
        leaderboard_window = game.get_window('leaderboard_layout')
        event2, _ = leaderboard_window.read()
        if event2 == 'OK':
            leaderboard_window.close()

    if window.Title == 'Who wants to be a Millionaire !!':
        window['-PLAYERS_TABLE-'].update(values=game.PLAYERS.keys())
    count = 0
    while RUN:
        for player in players.values():
            # Check player lives
            if player.life == 0:
                count += 1
                if count > 5:
                    game.save()
                    game.game_over()
                    RUN = False
                    window.close()
                    break
                continue
            if player.life > 0:  # deal player
                game.ask_question(player)
                event, values = window.read()
                if event == '-ANSWER_SUBMIT-':
                    game.get_selected_option(values)
                    game.check_answer(player)
                    game.update_layout(player)
                count = 0
            game.update_deals()

    # TODO: implement SQLite db
