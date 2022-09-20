#!/usr/bin/env python3
import sys
import nltk
import aiml
from py2neo import Graph, NodeMatcher
import speech_recognition as sr
import time
import gtts
from gtts import gTTS
from pygame import mixer
import rospy
from std_msgs.msg import String
from robotics_task_tree_msgs.msg import ControlMessage
#graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))

#matcher = NodeMatcher(graph)
skill_choose_pub_ = rospy.Publisher('/skill_choose', String, queue_size=10)
topic_activate_pub_ = rospy.Publisher('/SKILL_7_1_014_0_parent', ControlMessage, queue_size=100)

rospy.init_node('skill_publisher', anonymous=True)

#kernel = aiml.Kernel()
##kernel.learn("startup.aiml")
#kernel.bootstrap(learnFiles="startup.aiml", commands="load aiml b")
skill_set_object = {
  "Tea": ["tea","sugar","cup"],
  "Sandwich": ["bread","meat","lettuce"]
}
ITEM_FROM_NEO4J = None
while True:
        mixer.init()
        # quiet the endless 'insecurerequest' warning
        # import urllib3stt

        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # while (True == True):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # print("Please wait. Calibrating microphone...")
            # listen for 1 second and create the ambient noise energy level
            r.adjust_for_ambient_noise(source, duration=1)
            print("Say something!")
            audio = r.listen(source, phrase_time_limit=5)
            # recognize speech using Sphinx/Google
            #   try:
            # response = r.recognize_sphinx(audio)
            try:
                response = r.recognize_google(audio, language="en-US")
                print("I think you said '" + response + "'")
                # tts = gTTS(text="I think you said " + str(response), lang='en')
                # tts.save("response.mp3")
                # mixer.music.load('response.mp3')
                # mixer.music.play()
                # time.sleep(5)
                # text = nltk.word_tokenize(response)
                # tagged = nltk.pos_tag(text)
                length = len(response)
                # print(length)
                # print(tagged)

     
                  
            except Exception as e:
                print("I am here")
                print (e)
            #print(vb)

