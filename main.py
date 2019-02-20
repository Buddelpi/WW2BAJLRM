'''
Created on Nov 25, 2018

@author: delpi
'''

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen,\
 FadeTransition, WipeTransition, FallOutTransition
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty,StringProperty,ListProperty, DictProperty, \
BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
import kivy.metrics
from kivy.metrics import Metrics
from playsound import playsound
from os import environ
from kivy.base import EventLoop
import json

CREDITS = """
"""

class Answer(Widget):
    q = StringProperty("")
    color = ListProperty([1,1,0,0])
    textColor = ListProperty([1,1,1,0])
    bgColor = ListProperty([0,0,0,0])

class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class WinScreen(Screen):
    pass
 
class CreditsScreen(Screen):
    
    creditsText = StringProperty(CREDITS)
    posyCredits = NumericProperty(-1000)
       
    def startClock(self):
        Clock.schedule_interval(self.moveCredits, 0.05)
        
    def moveCredits(self,dt):
        self.posyCredits+=1
        print self.posyCredits
    
class StateTimer():
    def __init__(self):
        self.cnt = 0
    
    def stateTimer(self,upto):
        self.cnt+=1
        if self.cnt == upto:
            self.cnt = 0
            return True
        else:
            return False
        
class GameScreen(Screen):
    answer1 = ObjectProperty(None)
    answer2 = ObjectProperty(None)
    answer3 = ObjectProperty(None)
    answer4 = ObjectProperty(None)
    question = ObjectProperty(None)

    data = ListProperty(None)
    
    actualAnswer1 = StringProperty('')
    actualAnswer2 = StringProperty('')
    actualAnswer3 = StringProperty('')
    actualAnswer4 = StringProperty('')
    actualQuestion = StringProperty('')
    fiftyJokerImage = StringProperty('Images/jpge50.jpg')
    phoneJokerImage = StringProperty('Images/jpgePhone.jpg')
    peopleJokerImage = StringProperty('Images/jpgePeople.jpg')
    
    questionSize = NumericProperty(20)
    
    questionNumber = NumericProperty(0)
    numOfQuestions = NumericProperty(0)
    questionSequenceCounter = NumericProperty(0)
    
    gameState = NumericProperty(-3)
     
    isAnswerCame = BooleanProperty(False)
    isStartup = BooleanProperty(True)
    currentAnswer = NumericProperty(0)
    
    isFiftyJokerPressed = BooleanProperty(False)
    isFiftyJokerPressedOnce = BooleanProperty(False)
    isPhoneJokerPressed = BooleanProperty(False)
    isPhoneJokerPressedOnce = BooleanProperty(False)
    phoneJokerCounter = NumericProperty(30)
    phoneJokerColor = ListProperty([1,1,1,0])
    isPeopleJokerPressed = BooleanProperty(False)
    isPeopleJokerPressedOnce = BooleanProperty(False)
    peopleJokerCounter = NumericProperty(30)
    peopleJokerColor = ListProperty([1,1,1,0])
    
    prizeTrackerImage = StringProperty("Images/Prizetracker/prizetracker_1.jpg")
    
    isSpacePressed = BooleanProperty(False)
    isButtonActivityBlocked = BooleanProperty(False)
    
    #playsound('Sounds/question_start.mp3')
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        #Load data from Json file
        self.data = self.loadData()
        self.numOfQuestions = len(self.data)-1
        self.questionSize = self.data[self.numOfQuestions]['Text_Size']
        #update actual data set for the first round
        self.updateQuestion(self.questionNumber)
        
        self.st = StateTimer()
        Window.bind(on_keyboard=self._on_keyboard_handler)
        Window.fullscreen = 'auto'
        Clock.schedule_interval(self.updateSM, 1)
    
    def _on_keyboard_handler(self, instance, key, *args):
        if key == 32  and not self.isButtonActivityBlocked:
            self.isSpacePressed = True
        else:
            print key
        if self.isButtonActivityBlocked:
            print 'Sorry, activity is blocked'
    
    def loadData(self):
        with open("questions.json", "r") as read_file:
            return json.load(read_file)
        
    def updateSM(self,dt):
        #print EventLoop.window.dpi 
        #print Metrics.dpi
        #print Metrics.fontscale
        if self.gameState == -3: #Start Screen
            
            if self.isSpacePressed:
                self.manager.current = 'intro'
                self.gameState = -2
                self.isButtonActivityBlocked = True
                self.isSpacePressed = False
                playsound('Sounds/main_theme.mp3',False)
        elif self.gameState == -2: #Intro Screen
            if self.st.stateTimer(34):
            #if self.st.stateTimer(1):
                print 'let us start'
                self.manager.current = 'game'
                self.gameState = -1
                self.isButtonActivityBlocked = False
            else:
                print 'else'
                
        elif self.gameState == -1: #
            if self.isSpacePressed:           
                self.sequencedStart(self.questionSequenceCounter)
                self.questionSequenceCounter+=1
                self.isSpacePressed = False
                
                if self.questionSequenceCounter == 5:
                    self.gameState = 0
                    self.questionSequenceCounter = 0
        elif self.gameState == 0: #Set Answer
            
            if self.isFiftyJokerPressed:
                self.isFiftyJokerPressed = False
                self.makeVisible(5)
                playsound('Sounds/question_start.mp3',False)
                
            if self.isPhoneJokerPressed:
                self.peopleJokerColor = [1,1,1,0]
                if self.isSpacePressed:
                    if not self.st.stateTimer(30):
                        if self.st.cnt == 1:
                            playsound('Sounds/phone.mp3',False)
                        self.phoneJokerCounter = 30-self.st.cnt
                    else:
                        self.phoneJokerCounter = 30-self.st.cnt
                        self.isPhoneJokerPressed = False
                        self.isPhoneJokerPressedOnce = True
                        self.setPhoneJokerVisible(False)
                else:
                    print 'Waiting for space pressed, then clock starts'
             
            if self.isPeopleJokerPressed:
                self.phoneJokerColor = [1,1,1,0]
                if self.isSpacePressed:
                    if not self.st.stateTimer(30):
                        if self.st.cnt == 1:
                            playsound('Sounds/phone.mp3',False)
                        self.peopleJokerCounter = 30-self.st.cnt
                    else:
                        self.peopleJokerCounter = 30-self.st.cnt
                        self.isPeopleJokerPressed = False
                        self.isPeopleJokerPressedOnce = True
                        self.setPeopleJokerVisible(False)
                else:
                    print 'Waiting for space pressed, then clock starts'
                        
                # if not self.st.stateTimer(14):
                    # if self.st.cnt == 1:
                        # playsound('Sounds/people.mp3',False)
                        # self.peopleJokerColor = [1,1,1,1]
                # else:
                    # self.peopleJokerVote = "Images/votescreen.jpg"
                    # self.isPeopleJokerPressed = False
                   
            if self.isAnswerCame: 
                print 'In Question'
                self.gameState=1
                self.isAnswerCame = False
            
        elif self.gameState == 1: #Set Answer
            self.isSpacePressed = False
            if not self.st.stateTimer(5):
                if self.st.cnt == 1:
                    playsound('Sounds/final_answer.mp3',False)
                self.updateQuestionColor(self.currentAnswer, 2, None)
                
            else:
                if self.currentAnswer == self.data[self.questionNumber]['Right']:
                    self.gameState = 2
                else:
                    self.gameState = 3
        elif self.gameState == 2: #Answer was right      
            if not self.st.stateTimer(10):
                if self.st.cnt == 1:
                    playsound('Sounds/correct_answer.mp3',False)
                    self.updateQuestionColor(self.currentAnswer, 1, None) 
                    self.questionNumber+=1
                    if self.questionNumber == self.numOfQuestions:
                        self.st.cnt = 7
                     
            else: 
                if self.questionNumber == self.numOfQuestions:
                    self.manager.current = 'win'
                    playsound('Sounds/main_theme.mp3',False)
                    self.gameState = 4
                else:
                    self.peopleJokerColor = [1,1,1,0]
                    self.gameState = -1
                    self.updateQuestion(self.questionNumber)
                    self.invisibleAnswers()
                    
                    
        elif self.gameState == 3: #Answer was wrong, but continue the game  
            if not self.st.stateTimer(10):
                if self.st.cnt == 1:   
                    playsound('Sounds/wrong_answer.mp3',False)
                    self.updateQuestionColor(self.currentAnswer, 0, self.data[self.questionNumber]['Right'])
                    self.questionNumber+=1
                    if self.questionNumber == self.numOfQuestions:
                        self.st.cnt = 6
            else:   
                if self.questionNumber == self.numOfQuestions:
                    self.manager.current = 'win'
                    playsound('Sounds/main_theme.mp3',False)
                    self.gameState = 4
                else:
                    self.peopleJokerColor = [1,1,1,0]
                    self.gameState = -1
                    self.updateQuestion(self.questionNumber)
                    self.invisibleAnswers()
                    
                    
        elif self.gameState == 4: #Winner screen shows up
            #if self.st.stateTimer(2):
            if self.st.stateTimer(40):
                self.manager.get_screen('credits').startClock()
                self.manager.current = 'credits'
                 
        else:
            print 'else'
     
    def invisibleAnswers(self):
        self.answer1.color = [0,0,0,0]
        self.answer1.textColor = [0,0,0,0]
        self.answer1.bgColor = [0,0,0,0]
        self.answer2.color = [0,0,0,0]
        self.answer2.textColor = [0,0,0,0]
        self.answer2.bgColor = [0,0,0,0]
        self.answer3.color = [0,0,0,0]
        self.answer3.textColor = [0,0,0,0]
        self.answer3.bgColor = [0,0,0,0]
        self.answer4.color = [0,0,0,0]
        self.answer4.textColor = [0,0,0,0]
        self.answer4.bgColor = [0,0,0,0]
        self.answer5.color = [0,0,0,0]
        self.answer5.textColor = [0,0,0,0]
        self.answer5.bgColor = [0,0,0,0]
        self.question.textColor = [0,0,0,0]
        self.question.color = [0,0,0,0]
        
    def makeVisible(self, num):
        if num == 0:
            self.question.color = [1,1,0,1]
            self.question.textColor = [1,1,1,1]
        elif num == 1:
            self.answer1.color = [1,1,0,1]
            self.answer1.textColor = [1,1,1,1]
            self.answer1.bgColor = [0,0,0,0]
        elif num ==2:
            self.answer2.color = [1,1,0,1]
            self.answer2.textColor = [1,1,1,1]
            self.answer2.bgColor = [0,0,0,0]
        elif num ==3:
            self.answer3.color = [1,1,0,1]
            self.answer3.textColor = [1,1,1,1]
            self.answer3.bgColor = [0,0,0,0]
        elif num ==4:
            self.answer4.color = [1,1,0,1]
            self.answer4.textColor = [1,1,1,1]
            self.answer4.bgColor = [0,0,0,0]
        elif num ==5:
            self.answer5.color = [1,1,0,1]
            self.answer5.textColor = [1,1,1,1]
            self.answer5.bgColor = [0,0,0,0]
        else:
            print 'Something went wrong'
               
    def sequencedStart(self,cycle):
        if cycle == 0:
            self.makeVisible(0)
            playsound('Sounds/question_start.mp3',False)
        elif cycle == 1:
            self.makeVisible(1)
        elif cycle == 2:
            self.makeVisible(2)
        elif cycle == 3:
            self.makeVisible(3)
        elif cycle == 4:
            self.makeVisible(4)
        else:
            print 'Odd cycle'
     
    def showRightAnswerWhenWrong(self,num):
        if num == 1:
            self.answer1.color = [0,1,0,1]
            self.answer1.bgColor = [0,1,0,0.5]
        elif num ==2:
            self.answer2.color = [0,1,0,1]
            self.answer2.bgColor = [0,1,0,0.5]
        elif num ==3:
            self.answer3.color = [0,1,0,1]
            self.answer3.bgColor = [0,1,0,0.5]
        elif num ==4:
            self.answer4.color = [0,1,0,1]
            self.answer4.bgColor = [0,1,0,0.5]
        elif num ==5:
            self.answer5.color = [0,1,0,1]
            self.answer5.bgColor = [0,1,0,0.5]
        else:
            print 'Something went wrong'
            
    def updateQuestionColor(self,num,answerState,rightAnswer):
        if num == 1:
            if answerState == 0: #Color answer to red - Wrong
                self.answer1.color = [1,0,0,1]
                self.answer1.bgColor = [1,0,0,0.5]
                self.showRightAnswerWhenWrong(rightAnswer)
            elif answerState == 1: #Color answer to green - Right
                self.answer1.color = [0,1,0,1]
                self.answer1.bgColor = [0,1,0,0.5]
            elif answerState == 2: #Color answer to blue - Set
                self.answer1.color = [0,0,1,1]
                self.answer1.bgColor = [0,0,1,0.5]
            else:
                print 'Something went wrong'
        elif num ==2:
            if answerState == 0: #Color answer to red - Wrong
                self.answer2.color = [1,0,0,1]
                self.answer2.bgColor = [1,0,0,0.5]
                self.showRightAnswerWhenWrong(rightAnswer)
            elif answerState == 1: #Color answer to green - Right
                self.answer2.color = [0,1,0,1]
                self.answer2.bgColor = [0,1,0,0.5]
            elif answerState == 2: #Color answer to blue - Set
                self.answer2.color = [0,0,1,1]
                self.answer2.bgColor = [0,0,1,0.5]
            else:
                print 'Something went wrong'
        elif num ==3:
            if answerState == 0: #Color answer to red - Wrong
                self.answer3.color = [1,0,0,1]
                self.answer3.bgColor = [1,0,0,0.5]
                self.showRightAnswerWhenWrong(rightAnswer)
            elif answerState == 1: #Color answer to green - Right
                self.answer3.color = [0,1,0,1]
                self.answer3.bgColor = [0,1,0,0.5]
            elif answerState == 2: #Color answer to blue - Set
                self.answer3.color = [0,0,1,1]
                self.answer3.bgColor = [0,0,1,0.5]
            else:
                print 'Something went wrong'
        elif num ==4:
            if answerState == 0: #Color answer to red - Wrong
                self.answer4.color = [1,0,0,1]
                self.answer4.bgColor = [1,0,0,0.5]
                self.showRightAnswerWhenWrong(rightAnswer)
            elif answerState == 1: #Color answer to green - Right
                self.answer4.color = [0,1,0,1]
                self.answer4.bgColor = [0,1,0,0.5]
            elif answerState == 2: #Color answer to blue - Set
                self.answer4.color = [0,0,1,1]
                self.answer4.bgColor = [0,0,1,0.5]
            else:
                print 'Something went wrong'
        elif num ==5:
            if answerState == 0: #Color answer to red - Wrong
                self.answer5.color = [1,0,0,1]
                self.answer5.bgColor = [1,0,0,0.5]
                self.showRightAnswerWhenWrong(rightAnswer)
            elif answerState == 1: #Color answer to green - Right
                self.answer5.color = [0,1,0,1]
                self.answer5.bgColor = [0,1,0,0.5]
            elif answerState == 2: #Color answer to blue - Set
                self.answer5.color = [0,0,1,1]
                self.answer5.bgColor = [0,0,1,0.5]
            else:
                print 'Something went wrong'
        else:
            print 'Something went wrong'
                    
    
    def updateQuestion(self,num):
        self.actualAnswer1 = self.data[num]['A1']
        self.actualAnswer2 = self.data[num]['A2']
        self.actualAnswer3 = self.data[num]['A3']
        self.actualAnswer4 = self.data[num]['A4']
        self.actualQuestion = self.data[num]['Q']
        
#         imagePath = "Images/Prizetracker/prizetracker_" + str(num+1) + ".jpg"
        imagePath = "Images/Prizetracker/prizetracker_" + str(num+1) + "_minborder.jpg"
#         imagePath = "Images/Prizetracker/prizetracker_" + str(num+1) + "_noborder.jpg"
        print imagePath
        self.prizeTrackerImage = imagePath
    
    def setAnswer(self, ans):
        if  self.isAnswerCame == False:
            self.currentAnswer = ans
            self.isAnswerCame = True
    
    def fiftyJokerPressed(self):
        if not self.isFiftyJokerPressedOnce and not self.isButtonActivityBlocked:
            self.isFiftyJokerPressed = True
            self.isFiftyJokerPressed = True
            self.fiftyJokerImage = 'Images/jpge50x.jpg'
    
    def phoneJokerPressed(self):
        if not self.isPhoneJokerPressedOnce and not self.isButtonActivityBlocked:
            self.setPhoneJokerVisible(True)
            self.isPhoneJokerPressed = True
            self.isPhoneJokerPressedOnce = True
            self.phoneJokerImage = 'Images/jpgePhoneX.jpg'
      
    def setPhoneJokerVisible(self,isSetPhone):
        if isSetPhone == True:
            self.phoneJokerColor = [1,1,1,1]
        else:
            self.phoneJokerColor = [1,1,1,0]
            
    def setPeopleJokerVisible(self,isSetPeople):
        if isSetPeople == True:
            self.peopleJokerColor = [1,1,1,1]
        else:
            self.peopleJokerColor = [1,1,1,0]
            
    def peopleJokerPressed(self):
        if not self.isPeopleJokerPressedOnce and not self.isButtonActivityBlocked:
            self.setPeopleJokerVisible(True)
            self.isPeopleJokerPressed = True
            self.isPeopleJokerPressedOnce = True
            self.peopleJokerImage = 'Images/jpgePeopleX.jpg'
            
class MissionnaireApp(App):
    
    
    
    def build(self):
        root = ScreenManager(transition=FallOutTransition())
        root.add_widget(FirstScreen(name = "start"))
        root.add_widget(SecondScreen(name = "intro"))
        root.add_widget(GameScreen(name = "game"))
        root.add_widget(WinScreen(name = "win"))
        root.add_widget(CreditsScreen(name = "credits"))
        
        return root

if __name__ == '__main__':
    MissionnaireApp().run()