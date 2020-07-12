
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv, os, random
doc = ''


class Constants(BaseConstants):
    name_in_url = 'Judgment_experiment'
    players_per_group = 2

    # find all images (this should also include videos!)
    image_path = os.path.join('_static/my_folder/')
    images = os.listdir(image_path)  # this generates a list of filenames
    images = ["my_folder/" + x for x in images] # gives correct relative path to filenames
    images.sort()


    # find all questions, split into list
    question = open('_static/questions_all.txt').read()
    questionsplit = [x for x in question.split('\n')]  # this generates a list of the actual questions as strings

    anchorslist = open('_static/anchors.txt').read()
    anchors = [x for x in anchorslist.split('\n')]

    num_rounds = len(questionsplit) #number of trials equal to number stimuli





class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            number = [x for x in range(len(Constants.questionsplit))]  # list of positions to draw stims from image and question list
            random.shuffle(number) # randomize order
            self.session.vars['stim_order'] = number





class Group(BaseGroup):
    discussion1 = models.FloatField()
    def live_slider(self, id_in_group, package):
        broadcast = {"slider_value": package["slider_value"], "disable": package["disable"]}
        return {0: broadcast}


class Player(BasePlayer):
    Name = models.StringField(label='What is your name?')
    Age = models.IntegerField(label='What is your age?')
    PartnerAgreement = models.StringField(choices=[['Strongly disagree', 'Strongly disagree'], ['Disagree', 'Disagree'], ['Somewhat disagree', 'Somewhat disagree'], ['Neither agree nor disagree', 'Neither agree nor disagree'], ['Somewhat agree', 'Somewhat agree'], ['Agree', 'Agree']], label='I think that my partner and I are on the same wavelength with regard to our judgments of the video', widget=widgets.RadioSelectHorizontal)
    judgement1 = models.FloatField()
    certainty1 = models.FloatField()
    judgement2 = models.FloatField()
    certainty2 = models.FloatField()
    judgement3 = models.FloatField()
    certainty3 = models.FloatField()
    mutual_judgment = models.IntegerField()
    my_field = models.StringField()

    PQ_1 = models.StringField()
    PQ_2 = models.StringField()
    PQ_3 = models.StringField()
    PQ_4 = models.StringField()
    PQ_5 = models.StringField()
    PQ_6 = models.StringField()
    PQ_7 = models.LongStringField()
    PQ_8 = models.StringField()
    PQ_9 = models.StringField()
    PQ_10 = models.StringField()

    IOS_1 = models.StringField()

    def my_method(self):
        "live_slider"
    def vars_for_template(self):
        # get image
        stim_name = Constants.images[self.session.vars['stim_order'][self.round_number-1]]

        #check if stim is image or video
        if stim_name.split('.')[1]=="png":
            is_image = 1
        else:
            is_image = 0

        # Get question
        this_question = Constants.questionsplit[self.session.vars['stim_order'][self.round_number-1]]

        # Get anchors
        anchors = Constants.anchors[self.session.vars['stim_order'][self.round_number-1]]
        anchorssplit = [x for x in anchors.split(',')]
        anchor1 = anchorssplit[0]
        anchor2 = anchorssplit[1]

        return dict(stim_path =stim_name,
            is_image = is_image,
            question = this_question,
            anch1=anchor1,
            anch2 = anchor2,
             debug = Constants.images,
             debug2 = Constants.questionsplit,
             number_debug = self.session.vars['stim_order'])
