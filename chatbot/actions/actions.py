# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions import vectors

import csv

req_index = {
    'availability':0,
    'fault_tolerance':1,
    'maintainability':2,
    'performance':3,
    'scalability':4,
    'security':5,
    'usability':6,
    'portability':7,
    'interoperability':8
}

class ActionAddRequirement(Action):

    def name(self) -> Text:
        return "action_add_requirement"

    def __init__(self):
            self.intent_mappings = {}
            # read the mapping from a csv and store it in a dictionary
            with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    self.intent_mappings[row[0]] = row[1]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Update requirements vector
        intent_name = tracker.latest_message['intent']['name']
        requirements = tracker.get_slot('requirements')
        requirements[req_index[intent_name]] += 1

        # Dispatch message to validate
        dispatcher.utter_message(text = self.intent_mappings[intent_name])

        # Set slot value
        return [SlotSet("requirements", requirements)]
       

class ActionShowVector(Action):
    def name(self) -> Text:
        return "action_show_vector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Fetch requirements vector
        requirements = tracker.get_slot('requirements')
        vector = vectors.get_normalized_vector(requirements)
        print(vector)
        # Get closer architecture
        match = vectors.get_closer_architecture(vector)

        for i,arch in enumerate(match):
            dispatcher.utter_message(text = f"Arquitectura sugerida n°{i+1}: " + str(arch.name))
            analysis_done = arch.analysis(vector)
            for line in analysis_done.split("\n"):
                dispatcher.utter_message(text = line)
        
        # TODO: CLEAN VECTOR?

        return [SlotSet("requirements", [])]
        #return []


class ActionAskClarification(Action):
    def name(self) -> Text:
        return "action_ask_clarification"

    def __init__(self):
        self.intent_mappings = {}
        # read the mapping from a csv and store it in a dictionary
        with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # fetch two latest intents
        prev_intent_1 = tracker.latest_message['intent_ranking'][1]
        prev_intent_2 = tracker.latest_message['intent_ranking'][2]

        prev_1_name = prev_intent_1['name']
        prev_2_name = prev_intent_2['name']
        
        # both 
        if prev_1_name in req_index and prev_2_name in req_index:
            intent_prompt_1 = self.intent_mappings[prev_1_name]
            intent_prompt_2 = self.intent_mappings[prev_2_name]

            message = "Para vos este requerimiento se centra principalmente en ..."
            buttons = [
                    {'title': intent_prompt_1,
                    'payload': '/{}'.format(prev_1_name)},
                    {'title': intent_prompt_2,
                    'payload': '/{}'.format(prev_2_name)},
                    {'title': 'Ninguno de los dos',
                    'payload': '/back'}]
            dispatcher.utter_message(message, buttons=buttons)

            """
            requirements = tracker.get_slot('requirements')
            requirements[req_index[prev_1_name]] += 1
            message = self.intent_mappings[prev_1_name]

            if prev_intent_1['confidence']-prev_intent_2['confidence'] < 0.15:
                requirements[req_index[prev_2_name]] += 1
                message +=  " y " + self.intent_mappings[prev_2_name]

            dispatcher.utter_message(text = message)

            return [SlotSet("requirements", requirements)]
            """
        # validate only first
        elif prev_1_name in req_index:
            intent_prompt = self.intent_mappings[prev_1_name]
            message = "Para vos ese requerimiento se refiere a {}?".format(intent_prompt)
            buttons = [{'title': 'Si',
                    'payload': '/{}'.format(prev_1_name)},
                    {'title': 'No',
                    'payload': '/back'}]
            dispatcher.utter_message(message, buttons=buttons)
        # ask rephrase
        else:
            dispatcher.utter_message("No te entendí. Podrías volver a escribirlo de otra manera?")
            
        return []