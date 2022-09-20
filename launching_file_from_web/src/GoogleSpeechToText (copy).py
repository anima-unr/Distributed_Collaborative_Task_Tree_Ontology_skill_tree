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
graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))

matcher = NodeMatcher(graph)
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
                global tagged_comment, word, vb
                previous_tag = None
                # for i in range(0, length):
                token_comment = nltk.word_tokenize(response)
                tagged_comment = nltk.pos_tag(token_comment)
                for word, tag in tagged_comment:
                    if (tag == 'VB') or (tag == 'NN') or (tag == 'JJ'):
                        vb = word
                        ITEM_FROM_NEO4J = graph.run(
                            """
                                MATCH(concept_in:Concept)-[r]-(intermediateNodesCluster_1:Concept)
                                WHERE concept_in.name = $variable
                                WITH concept_in, collect(id(intermediateNodesCluster_1)) AS collection1
                                MATCH(concept_out: Concept)-[r] - (intermediateNodesCluster_2:Concept)
                                WHERE concept_out.name IN['tea','sugar','cup','bread','meat','cheese','lettuce']
                                WITH concept_in, collection1, concept_out, collect(id(intermediateNodesCluster_2))
                                AS collection2
                                WITH concept_out, gds.alpha.similarity.jaccard(collection1, collection2)
                                AS conceptual_similarity
                                RETURN concept_out.name as concept_out
                                ORDER BY conceptual_similarity
                                DESC LIMIT 1
                            """, variable=word
                             ).evaluate()
                        print(ITEM_FROM_NEO4J)
                        print(tagged_comment)
                        for key in skill_set_object:
                            if str(ITEM_FROM_NEO4J) in skill_set_object[key]:
                                print(key)
                                break
                        tts = gTTS(text="I think you said " + str(response) + "Let me make you a cup of " + str(key), lang='en')
                        tts.save("response.mp3")
                        mixer.music.load('response.mp3')
                        mixer.music.play()
                        skill_choose_pub_.publish(str(key))
                        topic_activate_msg_ = ControlMessage()
                        topic_activate_msg_.activation_level = 10000000000000000000000000000000.0
                        topic_activate_pub_.publish(topic_activate_msg_)
                        time.sleep(10)
                    previous_tag = tag
            except Exception as e:
                print("I am here")
                print (e)
            #print(vb)

