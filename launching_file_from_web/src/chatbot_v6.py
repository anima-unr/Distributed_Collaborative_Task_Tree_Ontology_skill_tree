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

global tagged_query, word, vb, item

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
# Press CTRL-C to break this loop
def main():
    while True:
        query = input("HUMAN : ")
        tokenized_query = nltk.word_tokenize(query)
        tagged_query = nltk.pos_tag(tokenized_query)
        print("tagged : ", tagged_query)
        previous_tag = None
        for word, tag in tagged_query:
            if (tag == 'VB') or (tag == 'NN') or (tag == 'JJ'):
            #if (previous_tag == 'VBG') and (tag == 'NN'):
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
            previous_tag = tag
    # while True:
    #     mixer.init()
    #     r = sr.Recognizer()
    #     # query = input("HUMAN : ")
    #     with sr.Microphone() as source:
    #         r.adjust_for_ambient_noise(source, duration=1)
    #         print("Say something!")
    #         audio = r.listen(source, phrase_time_limit=5)
    #         response = r.recognize_google(audio, language="en-US",show_all=True)
    #         print("I think you said '" + response + "'")
    #         tokenized_query = nltk.word_tokenize(response)
    #         tagged_query = nltk.pos_tag(tokenized_query)
    #         print("tagged : ", tagged_query)
    #         previous_tag = None
    #         for word, tag in tagged_query:
    #             if (tag == 'VB') or (tag == 'NN') or (tag == 'JJ'):
    #             #if (previous_tag == 'VBG') and (tag == 'NN'):
    #                 ITEM_FROM_NEO4J = graph.run(
    #                     """
    #                         MATCH(concept_in:Concept)-[r]-(intermediateNodesCluster_1:Concept)
    #                         WHERE concept_in.name = $variable
    #                         WITH concept_in, collect(id(intermediateNodesCluster_1)) AS collection1
    #                         MATCH(concept_out: Concept)-[r] - (intermediateNodesCluster_2:Concept)
    #                         WHERE concept_out.name IN['tea','sugar','cup','bread','meat','cheese','lettuce']
    #                         WITH concept_in, collection1, concept_out, collect(id(intermediateNodesCluster_2))
    #                         AS collection2
    #                         WITH concept_out, gds.alpha.similarity.jaccard(collection1, collection2)
    #                         AS conceptual_similarity
    #                         RETURN concept_out.name as concept_out
    #                         ORDER BY conceptual_similarity
    #                         DESC LIMIT 1
    #                     """, variable=word
    #                      ).evaluate()
    #                 print(ITEM_FROM_NEO4J)
    #                 for key in skill_set_object:
    #                     if str(ITEM_FROM_NEO4J) in skill_set_object[key]:
    #                         print(key)
    #                         break
    #                 # temp = list(skill_set_object.items())
    #                 # print(temp) 
    #                 # res = [idx for idx, key_ in enumerate(temp) if key_[0] == "bread"]
    #                 # print(int(res))

    #                 # skill_index = list(skill_set_object.keys()).index(str(key))
    #                 # print(list(skill_set_object.keys()))
    #                 # print(skill_index)

    #                 skill_choose_pub_.publish(str(key))
    #                 topic_activate_msg_ = ControlMessage()
    #                 topic_activate_msg_.activation_level = 10000000000000000000000000000000.0
    #                 topic_activate_pub_.publish(topic_activate_msg_)

    #             previous_tag = tag
    #kernel.setPredicate("verb", ITEM_FROM_NEO4J)
    ##kernel.setPredicate("playable", item)
    #print("NiHA : ", kernel.respond(query))


# kernel.setPredicate("verb", item)
if __name__ == '__main__':
    main()
