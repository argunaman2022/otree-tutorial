from otree.api import *


doc = """
This is a tutorial for the multiplayer games section from OtreeDocumentation
Where necessary comments are added
"""


class C(BaseConstants):
    NAME_IN_URL = 'tutorialAppMultiplayerGames'
    PLAYERS_PER_GROUP = 2  #if in the game 2 players should interract group size should be 2, default is None
    NUM_ROUNDS = 1 # how many times the sessions will be repeated
    '''
    1.If in a group there are multiple roles such as buyer/seller etc create them in constants, make sure they end with _ROLE
    2. O tree assigns each role to a different player - sequentually according to id_in_group.
    3. using this we can make certain pages only visible to certain roles
    4. in templates use {{player.role}}
    5. can also use principial=group.get_player_by_role(C.PRINCIPIAL_ROLE). to get the principial
    '''
    PRINCIPIAL_ROLE='Principial'
    AGENT_ROLE="Agent"


class Subsession(BaseSubsession):
    '''
    1. by default each group will be a set of same participants since players_per_group is a constant and groups are assigned based on player_id sequentially
        to change this use Subsession method: group_randomly()
    2. To keep the group structure use group_like_round(n)
    '''
    def creating_subsession(subsession):
        'this function shuffles players in round one and keeps this structure for rounds n>1'
        if subsession.round_number==1:
            subsession.group_randomly(fixed_id_in_group=True) #this argument ensures that players are shuffled between groups but players are fixed in their roles
        else: subsession.group_like_round(1)
    '''Methods:
    1. get_group_matrix() returns the structure of the group as a matrix
    2. set_group_matrix() lets you modify the structure
    '''

class Group(BaseGroup):
    '''
    1. each player has attribute id_in_group which tells you if its player 1 or 2 or etc in the group.
    2. Group objects have following methods
        2.a get_players: returns a list of players ordered by id_in_group
        2.b get_player_by_id(id): returns the player in the group with the given id
    3. groups also have group.set_players() method for shuffling players within group
    '''
    pass


class Player(BasePlayer):
    '''
    1. player objects have the methods that return list of players in the group or subsession:
        1.a get_others_in_group()
        1.b get_others_in_subsession()
    '''
    pass


# PAGES

class ShuffleWaitPage(WaitPage):
    '''
    1.Often groups are shuffled when session is created,
        sometimes you wanna shuffle groups after they've done something, to achieve this shuffle them on a wait page after the said thing is done
    2. See waitpages in the tutorialAppBasics.
    '''
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly()

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
