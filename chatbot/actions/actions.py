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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Update requirements vector
        intent_name = tracker.latest_message['intent']['name']
        requirements = tracker.get_slot('requirements')
        requirements[req_index[intent_name]] += 1

        # Dispatch message to validate
        dispatcher.utter_message(text = intent_name)

        # Set slot value
        return [SlotSet("requirements", requirements)]
       

class ActionShowVector(Action):
    def name(self) -> Text:
        return "action_show_vector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        requirements = tracker.get_slot('requirements')
        match = vectors.get_closer_architecture(requirements)
        dispatcher.utter_message(text = "Solución sugerida: " + str(match.name))
        return []