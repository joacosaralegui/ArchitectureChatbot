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
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered

from actions import vectors

import requests
import csv

req_index = {
    'availability': 0,
    'fault_tolerance': 1,
    'maintainability': 2,
    'performance': 3,
    'scalability': 4,
    'security': 5,
    'usability': 6,
    'portability': 7,
    'interoperability': 8
}

RESET_CONVERSATION = [SlotSet("user_id", None), SlotSet(
    "project_id", None), FollowupAction("utter_greeting")]
SUCCESS_CODE = 200
API_URL = "http://fastapi-training1.herokuapp.com"


def login(self, dispatcher, tracker, create_if_not_found=True):
    """
    Attempts login, returns user_data dict if found or created, otherwise returns None
    """
    email = tracker.get_slot('email')

    # Si no esta cargado el slot de email entonces no podemos continuar
    if email == None:
        dispatcher.utter_message(
            "No se pudo reconocer el email. Por favor, ingresalo de nuevo.")
        return None
        # return [UserUttered("/greeting",intent={'name': 'greeting', 'confidence': 1.0})]
        # TODO: forzar que la intent que sigue se marque como email?? reenviar el form (followupAction)
        # return [FollowupAction("action_login")]

    # Lo busco por email a ver si existe
    response_get_user = requests.get(API_URL+'/users/get/email/'+email)

    # Si no lo encuentra
    if response_get_user.status_code != SUCCESS_CODE:
        if create_if_not_found:
            # Intento crear usuario
            response_create_user = requests.post(
                API_URL+'/users/create', data='{"email": "'+email+'"}')

            # Si falla la creación,
            if response_create_user.status_code != SUCCESS_CODE:
                dispatcher.utter_message(
                    "Error al crear el usuario "+email+", por favor intente nuevamente!")
                return None
        else:
            dispatcher.utter_message("No se encontro el usuario: " + email)
            return None

    # Se que la info esta en alguno de los dos response porque la ejecucion llego hasta aca. Elijo de cual lo agarro.
    user_data = response_get_user.json(
    ) if response_get_user.status_code == 200 else response_create_user.json()

    # Buscar user_id value, project_id y project_name
    return user_data


class ActionListProjects(Action):

    def name(self) -> Text:
        return "action_list_projects"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obtengo el email del usuario actual y busco en la api su lista de proyectos
        email = tracker.get_slot('email')
        user_data = requests.get(API_URL+'/users/get/email/'+email).json()
        projects_match = user_data['projects']

        if not projects_match:  # Si la lista esta vacia
            dispatcher.utter_message(text="El usuario no tiene proyectos")
        else:
            # Recorro la lista de projectos del usuario, imprimiendo los datos de c/u
            dispatcher.utter_message(text="Proyectos")
            for p in projects_match:
                dispatcher.utter_message(
                    text="Titulo: " + p['title'] + " | ID: " + str(p['id']))

        return []


class ActionRegisterProject(Action):

    def name(self) -> Text:
        return "action_register_project"

    def run(self, dispatcher, tracker, domain):
        user_data = login(self, dispatcher, tracker, create_if_not_found=True)

        # If login failed, go back to start
        if user_data == None:
            return RESET_CONVERSATION

        # Buscar user_id value, project_id y project_name
        user_id = user_data['id']

        # Tenemos que crear el proyecto
        project = tracker.get_slot('project')
        # Limpio un poco el slot (compiten dos clasificadores, y ademas le agregan comillas)
        if project and isinstance(project, list):
            project = project[0]
        project = project.replace('"','')

        response_create_project = requests.post(
            API_URL+'/projects/create', data='{"title": "'+str(project)+'"}')

        if response_create_project.status_code != SUCCESS_CODE:
            dispatcher.utter_message(
                "Error al crear el proyecto: " + str(response_create_project.json()['detail']))
            # VOLVER AL FORM
            return RESET_CONVERSATION
            
        # Extraigo la info del proyecto particular
        project_data = response_create_project.json()
        # Guardo la id del proyecto como str
        project_id = str(project_data['id'])
        # Guardo el nombre del proyecto como str
        project_name = str(project_data['title'])

        params = (
            ('project_id', project_id),
            ('user_id', str(user_id)),
        )
        # Me agrego al proyecto
        response_join_project = requests.put(
            API_URL+'/projects/join', params=params)

        if response_join_project.status_code != SUCCESS_CODE:
            dispatcher.utter_message(
                "Error al crear el proyecto: " + str(response_create_project.json()))
            # VOLVER AL FORM
            return RESET_CONVERSATION

        # Muestro al usuario el id para la proxima vez
        dispatcher.utter_message(
            f"Proyecto creado exitosamente! Guarda este ID para poder acceder más adelante: {project_id}")
        dispatcher.utter_message(template="utter_work_with_project")

        # Guardo tanto el id de usuario como el de proyecto para mas adelante

        return [SlotSet("user_id", user_id), SlotSet("project_id", project_id), SlotSet("project", project_name)]


class ActionContinueProject(Action):

    def name(self) -> Text:
        return "action_continue_project"

    def run(self, dispatcher, tracker, domain):
        user_data = login(self, dispatcher, tracker, create_if_not_found=False)

        # If login failed, go back to start
        if user_data == None:
            return [UserUttered("/greeting", {"intent": {'name': 'greeting', 'confidence': 1.0}})]

        # Sino, continuar proyecto
        user_id = user_data['id']
        project_id = tracker.get_slot('project_id')

        # Si nos piden continuar un proyecto (osea si tenemos project_id)
        if project_id != None:
            project_id = int(project_id)
            projects = user_data['projects']
            project_data = None
            # list comprehension python
            for p in projects:
                if p['id'] == project_id:
                    project_data = p
                    
            if not project_data:
                dispatcher.utter_message("No existe projecto con ese ID!")
                return [FollowupAction("action_list_projects")]
                # TODO: VOLVER A preguntar si quiere crear o no (quizas listar ids del proyecto que ya existe)
            else:
                # Si llegamos hasta acá entonces tenemos todo.
                dispatcher.utter_message(
                    "Proyecto recuperado exitosamente!")
                dispatcher.utter_message(template="utter_work_with_project")
                return [SlotSet("user_id", user_id),SlotSet("project", project_data['title'])]

            return [SlotSet("user_id", user_id)]
        else:
            dispatcher.utter_message("No se cargó el ID!")
            return RESET_CONVERSATION


class ActionJoinProject(Action):

    def name(self) -> Text:
        return "action_join_project"

    def run(self, dispatcher, tracker, domain):
        user_data = login(self, dispatcher, tracker)

        # If login failed, go back to start
        if user_data == None:
            return RESET_CONVERSATION

        # Buscar user_id value, project_id y project_name
        user_id = user_data['id']
        project_id = tracker.get_slot('project_id')

        if project_id != None:
            params = (
                ('project_id', project_id),
                ('user_id', str(user_id)),
            )

            # Me agrego al proyecto
            response_join_project = requests.put(
                API_URL+'/projects/join', params=params)

            if response_join_project.status_code == SUCCESS_CODE:
                dispatcher.utter_message(template="utter_work_with_project")
                return [SlotSet("project", response_join_project.json()['title'])]
            else:
                dispatcher.utter_message(
                    "No se pudo agregar el usuario al proyecto!")
                return [FollowupAction("action_list_projects")]
        else:
            dispatcher.utter_message("No se encontró id para el proyecto.")
            return RESET_CONVERSATION


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
        #Update requirements vector
        attribute = tracker.latest_message['intent']['name']
        requirement = tracker.latest_message['intent']['text']
        print(attribute)
        print(requirement)
        return []
        # requirements = tracker.get_slot('requirements')
        # requirements[req_index[intent_name]] += 1

        # # Dispatch message to validate
        # dispatcher.utter_message(text=self.intent_mappings[intent_name])

        # # Set slot value
        # return [SlotSet("requirements", requirements)]


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

        for i, arch in enumerate(match):
            dispatcher.utter_message(
                text=f"Arquitectura sugerida n°{i+1}: " + str(arch.name))
            dispatcher.utter_message(text=arch.analysis(vector))

        # TODO: CLEAN VECTOR?

        return []


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
            message = "Para vos ese requerimiento se refiere a {}?".format(
                intent_prompt)
            buttons = [{'title': 'Si',
                        'payload': '/{}'.format(prev_1_name)},
                       {'title': 'No',
                        'payload': '/back'}]
            dispatcher.utter_message(message, buttons=buttons)
        # ask rephrase
        else:
            dispatcher.utter_message(
                "No te entendí. Podrías volver a escribirlo de otra manera?")

        return []
