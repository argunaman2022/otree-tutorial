from otree.api import *


doc = """
Here i document a tutorial for future reference using Otree documentation

I. Objects
    1. Session - self-explanatory
        1.a Session is divided into subsessions, subsessions into pages. each round is a single subsession. for instance if a game
        has 2 rounds the session has 2 subsessions.
    2. Groups subsessions (participants) are divided into groups of players. in each subsession a group represents participants that will interract
        if participants should be subdivided into a single group for the entirety of the game there's a single subsession
        if you need to mix the groups twice (i.e. one person will be in 3 groups throughout the game) there are 3 subsessions
    3. Object hierarchy Session -> subsession -> Group -> Player
        3.a you can access higher up objects in the following way player.group, player. subsession etc.
    4. Participant is the factual person playing the game who will be paid at the end. one participant (person) is divided into players. 
        i.e. if participant Argun can be player 1 and player 2 and player 3 then there are 3 players for the participant object
II. Models and Fields
    - A model is just a database table
    1. There are 3 models: Subsession, Group, Player.
    2. Each model has fields which is a column in the said database table.
        2.a fields are created in the class of the model (e.g. in class Player(BasePlayer) name=models.StrinfField())
        2.b There are 6 field types: BooleanField, CurrencyField, IntegerField, FloatField, StringField, LongStringField.
            - initial value of a field is by default None unless you set initial=something (e.g. somefield=models.BooleanField(initial=True))
    3. Each model has predefined fields that do not show up in code
        - e.g. player model has "fields", "payoff", "id_in_group"; as well as methods like "in_all_round()", "get_others_in_group()" {look these up}
        - Subsession model has "round_number","get_groups()","get_players()" and etc. see https://otree.readthedocs.io/en/latest/models.html            
"""

"""
Constants that should not be changing from player to player are stored in this instance of the BaseConstants class
+Important: constants can be numbers, booleans, lists etc but for more complex types like dicts should define instead a function 
    e.g def my_dict(subsession): return dict(a=[1,2],b=[3,4]). the subsession class will call this function to create the constant.
"""
class C(BaseConstants):
    NAME_IN_URL = 'tutorialAppBasics-change' #this is how the app is displayed on the webbrowser
    PLAYERS_PER_GROUP = None #next tutorial
    NUM_ROUNDS = 1 #next tutorial



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """
    Each page can contain a form.
    This is useful for many things for instance which the player can fill out submit the form to create its name etc.
    Another use would be to store hidden variables on the player level.
    """
    # these two will be called in page 1
    name=models.StringField(label="Your name is:") #this is the name field of the player module. we can use this in the page Class see below the choice page
    age=models.IntegerField(label="Your age:")

    # i will call these in page 2
    integer_choice=models.IntegerField(min=12,max=24)
    integer_choice_dropdown=models.IntegerField(choices=[1,2,3,4]) #dropdown menu
    integer_choice_radiobuttons1 = models.IntegerField(choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    integer_choice_radiobuttons2 = models.IntegerField(choices=[1, 2, 3, 4], widget=widgets.RadioSelectHorizontal )
    integer_choice_level=models.IntegerField(choices=[
        [1,'low'],[2,'mediumlow'],[3,'medium etc.']    ]) #uses ony see the labels not 1,2,3
    cooperated =models.BooleanField(label="would you liketo cooperate", choices=[[False,'Defect'],[True,'Cooperate']]) #a useful example
    #to get the human readable label of this users choice use player.field_display('cooperated') since player.cooperated returns boolean
    optional_choice=models.IntegerField(blank=True) #this makes this choice optional


    #dynamic  form field validation when you need the forms to depend on player attributes
    # i call these in page 3
    #the following field's min,max,choices will depend on the player attributes, i will define functions below this class that determines them
    dynamic_choice1= models.IntegerField()
    dynamic_choice2 = models.IntegerField()


    # you can have manual control over the fields this requires some basic knowledge of html.
    # first i define the field here. then i write the html code in the page in which i will display, see page3 for this
    players_slider_choice=models.StringField() #i will store his choice here - nobody but us sees this since i wont include it in form_fields

    #misc.
    tripled_age=models.IntegerField() #i set this field but will not display it to the player, instead i will multiply by 3 and pass it to the formfields below



#dynamic alternative to setting choices
def dynamic_choice1_choices(player):
    'this function gives the player 1 in the group the first choices, player 2 the second and the other players a single choice'
    if player.id_in_group==1:
        choices=[1,2,3,4]
    elif player.id_in_group==2: choices=[1,2]
    else: choices=[1]

    return choices
#dynamic alternative to setting max (min is omitted)
def dynamic_choice2_max(player):
    'this function sets the max choice to be the players budget for all players except for the first player, for him its min(budget,100)'
    value=player.id_in_group+100
    if player.id_in_group == 1:
        value=min(100,value)
    return value

# set up an error message if the player is trying to give in a value that is not accepted (e.g. for instance if they exceed the budget)
def dynamic_choice2_error_message(player, value):
    print('value is', value)
    if value > player.budget:
        return 'Cannot offer more than your remaining budget'

# PAGES
""""
Pages are what the participants see. you must create instances of the Page class as below and put the page order in "page_sequence=[]" as a list
if the game has multiple rounds the pages will be repeated in this sequence.
Below within the class I wrote down some methods that pages have 
"""
class MyPage(Page):
    @staticmethod
    def is_displayed(player):
        'this function is always called and determines who sees the page, default value is true'
        return player.id_in_group == 1 #returns True IFF participant is player 1 in the group. (== True since there's a single player in this app)

    @staticmethod
    def is_displayed(player):
        'if you want the players to see this page only in round 1'
        return player.round_number == 1  # returns True IFF participant is player 1 in the group. (== True since there's a single player in this app)
    @staticmethod
    def vars_for_template(player):
        """
        by default the following objects are passed to the templates in the page:
            - player, group, subsession, participant, session, C
        if you want to pass more objects to the template (so you can access them in the page.html) you need to put it in this function
        """
        a= player.age*10
        return dict(a=a, b=1+1)


    'Timeout- to set a timeout such that after the timeout the page autosubmits do the following'
    timout_seconds=60 #after 60 seconds page auto submits
    'If you want instead the timeout to depend on player, player.group etc. then do the get_timeout_seconds, eg:'
    #@staticmethod
    #def get_timeout_seconds(player: Player):
        #return player.my_page_timeout_seconds #afaik this should be a variable created in the player class, havent seen an exmaple yet and cannot get it to work



    @staticmethod
    def before_next_page(player, timeout_happened):
        'if there is code that should be run before the next page is displayed, put it here'
        player.tripled_age = player.age * 3  # dont forget to put this in vars_for_template for the next page ;)
        if timeout_happened:
            # fill in some default values for the fields so that they're not left null
            player.somefield = 'somevalue'
        """
            Timeout that spants multiple pages 
            - if you need the game to be on a timer you set up some fixed time somewhere 
                and on each page set get_timeout_seconds to return the remaining  time until this fixed time e.g. 
            for instance if the timer should start once this page is submitted (i.e. a button at the end of the page that says "press when ready to start timer"
            the following should be set to be executed after the page is submitted
        """
        participant=player.participant
        import time
        #participant fields are in settings.
        participant.expiry = time.time() + 5*60 #this sets the participant's expiry field to current time plus 5 minutes.
        'Then on each page\'s get_timeout_seconds should be set to the number of seconds until the expiration time'
        @staticmethod
        def get_timeout_seconds(player: Player):
            participant= player.participant
            import time
            return participant.expiry - time.time()
        'so once the expiry is 0 or negative the page autosubmits and the remaining pages quickly flash before the participants eyes' \
        'to avoid this make sure the pages are only displayed if expiry isnt 0' \
        '- just add return some_cond && get_timeout_seconds(player)>3 in the is_displayed(player) function'
        'last note: default timer says "time left on this page" but if it spans pages set the text accordingly'
        timer_text = "time left until blabla"


"""
WAIT PAGES.
Wait pages are important concepts. If there's a wait page then all players should arrive at this page before anyone can proceed.
For instance in a 2 player ultimatium game you would make sure that the player 2 (ultimatee) cannot get to his decision page untill player 1 (ultimator) makes his choice
so the page sequence would look like "ultimator_choice,waitpage,ultimateechoice,..." this means ALL PLAYERS IN THE GROUP will get to waitpage first then proceed to the next page

1. If you want the wait page to make sure all groups should arrive before anyone can proceed then should set wait_for_all_groups=True which is by default false
2. after_all_player_arrive lets us calculate important calculations such as the winners payoff only after everyone finishes. for instance:
    2.a. first set the function that calculates payoffs
    def set_payoffs(group):
        #for everyone in the group set the payoff
        for p in group.get_players():
            p.payoff = some value calculation
    2.b. then trigger this function in the waitpage:
        class mywaitpage(WaitPage):
            after_all_players_arrive=set_payoffs #after everyone arrives this function is called which sets payoffs
    2.c Alternatively (and preferably) you can define the following function within the waitpage:
        @staticmethod
        def after_all_players_arrive(group: Group):
            for p in group.get_players():
                p.payoff = 100
                
3. another useful method is "group_by_arrival_time=True" 
This can be used only if the wait page is the first in the page sequence.
This is useful if you have an app that filters participants before the main game and you want to group only those who make it to the main game see (https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html#group-by-arrival-time-method)
Make sure that this method is only passed in the first round and not the subsequent rounds 
"""

class Page1(Page):
    form_model='player'
    # here we're calling which fields should be displayed on the page when we use {{formfields}} template.
    form_fields =['name','age']   #==player.name, player.age


class Page2(Page):
    form_model='player'
    form_fields=['integer_choice','integer_choice_dropdown','integer_choice_radiobuttons1','integer_choice_radiobuttons2','integer_choice_level','cooperated','optional_choice']
    '''
    if you want form fields to be dynamic then instead of form_fields=[list], do
    @staticmethod
    def get_form_fields(player):
        if somecondition: return [list of fields]
        else: return [another list of fields]
    '''

    # you can also make the name of the field dynamic, example:
    @staticmethod
    def vars_for_template(player): #make sure to call {{formfield 'fieldname' label=thislabelnameindic'}}
        my_dict=dict(
            integer_choice_label=f"what integer would you, player {player.id_in_group} , like to choose"
        )
        return my_dict

class Page3(Page):
    form_model = 'player'
    form_fields=['players_slider_choice']
class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Page3,Page2,Page1,ResultsWaitPage, Results]
