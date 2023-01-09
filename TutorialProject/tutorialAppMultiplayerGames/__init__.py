from otree.api import *


doc = """
This is a tutorial for the multiplayer games section from OtreeDocumentation
Where necessary comments are added
"""


class C(BaseConstants):
    NAME_IN_URL = 'tutorialAppMultiplayerGames' #how the game will be displayed on webbrowser
    PLAYERS_PER_GROUP = 2  #if in the game 2 players should interract group size should be 2, default is None
    NUM_ROUNDS = 1 # how many times the sessions will be repeated


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
