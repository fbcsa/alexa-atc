# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model.dialog import (ElicitSlotDirective, DelegateDirective)
from ask_sdk_model.ui import LinkAccountCard
from ask_sdk_model import (Response, Slot, Intent)

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def loadLangData():
    with open('/var/task/lang.json', encoding="utf8") as json_file:
        return json.load(json_file)
        
def returnLinkCard(_handlerInput,_phrase,_token):
    if _token == None:
        return _handlerInput.response_builder.speak(_phrase).set_card(LinkAccountCard()).response
    else:
        return None
        
def initialConfig(handler_input):
    language = handler_input.request_envelope.request.locale
    lang_strings = loadLangData()
    language = language[0:2]
    rToken = handler_input.request_envelope.context.system.user.access_token
    resultLinkCard = returnLinkCard(handler_input,lang_strings[language]["MSG_LINK_CARD"],rToken)
    retorno = {"traductions": lang_strings[language], "token": rToken, "resultLinkCard": resultLinkCard}
    return retorno
    
    
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        language = handler_input.request_envelope.request.locale
        lang_strings = loadLangData()
        language = language[0:2]
        speak_output = lang_strings[language]["MSG_HELLO"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ChangeHeaterTemperatureHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChangeHeaterTemperature")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["radiador"].value

        temperaturaRadiador = handler_input.request_envelope.request.intent.slots["temperature"].value
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "heater",
          "cambios": [
            {
              "campo": "IdModoActual",
              "valor": "C"
            },
            {
              "campo": "TempComfort",
              "valor": temperaturaRadiador                
            }
          ],
          "idCia": 0,
          "traza": ""
        }
        

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)

        
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
        


class ChangeInstalationTemperatureHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChangeInstalationTemperature")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ChangeInstalationTemperatureHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["instalation"].value


        temperaturaRadiador = handler_input.request_envelope.request.intent.slots["temperature"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        logger.info("TARGET TEMP: " + temperaturaRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "instalation",
          "cambios": [
            {
              "campo": "IdModoActual",
              "valor": "C"
            },
            {
              "campo": "TempComfort",
              "valor": temperaturaRadiador                
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)

        
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
     


class ChangeZoneTemperatureHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChangeZoneTemperature")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In changeZoneTemperatureHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
        
        nombreRadiador = handler_input.request_envelope.request.intent.slots["zone"].value


        temperaturaRadiador = handler_input.request_envelope.request.intent.slots["temperature"].value
        if temperaturaRadiador == None or int(temperaturaRadiador)<12 or int(temperaturaRadiador)>30:
            speak_output = config["traductions"]["ASK_TEMPERATURE"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="temperature")).response   
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        logger.info("TARGET TEMP: " + temperaturaRadiador)
        nombreExtra = handler_input.request_envelope.request.intent.slots["instalation"].value
        if nombreExtra == None:
            nombreExtra = ""
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": nombreExtra,
          "upd_type": "zone",
          "cambios": [
            {
              "campo": "IdModoActual",
              "valor": "C"
            },
            {
              "campo": "TempComfort",
              "valor": temperaturaRadiador                
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)

        if str(respuesta) == "2":
            logger.info("REDIRIGIENDO SALIDA")
            speak_output = config["traductions"]["ASK_INSTALATION"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="instalation")).response
        else:
            speech = the_fact
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response        
 
 
 
 
      
class ChangeHeaterModeHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChangeHeaterMode")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CHANGEHEATERMODE")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]

        nombreRadiador = handler_input.request_envelope.request.intent.slots["radiador"].value
        if handler_input.request_envelope.request.intent.slots["modo"].resolutions == None:
            speak_output = config["traductions"]["ASK_MODE"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="modo")).response
        mode_match = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].status.code
        logger.info("MATCH CODE: " + str(mode_match))
        if(mode_match == StatusCode.ER_SUCCESS_MATCH):
            modoRadiador = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].values[0].value.id
            logger.info("TARGET RADIADOR: " + nombreRadiador)
            logger.info("TARGET MODO: " + modoRadiador)
            url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
            datos = {
              "nombreElemento": nombreRadiador,
              "nombreElementoExtra": "",
              "upd_type": "heater",
              "cambios": [
                {
                  "campo": "IdModoActual",
                  "valor": modoRadiador
                }
              ],
              "idCia": 0,
              "traza": ""
            }

            response = requests.put(url,
            headers={'Authorization': 'Bearer ' + config["token"]},
            json=datos)

            the_fact = ""
            if response.status_code == 200:
                respuesta = response.text
                logger.info("RESPUESTA TXT: " + str(respuesta))
                the_fact = config["traductions"]["MSG_DONE"]
                
            else:
                the_fact = str(response.status_code)
        else:
            the_fact = config["traductions"]["ER_SUCCESS_NO_MATCH"] 
        
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
        



class changeInstalationModeHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("changeInstalationMode")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In changeInstalationModeHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]

        nombreRadiador = handler_input.request_envelope.request.intent.slots["instalation"].value

        if handler_input.request_envelope.request.intent.slots["modo"].resolutions == None:
            speak_output = config["traductions"]["ASK_MODE"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="modo")).response
        mode_match = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].status.code
        logger.info("MATCH CODE: " + str(mode_match))
        if(mode_match == StatusCode.ER_SUCCESS_MATCH):
            modoRadiador = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].values[0].value.id
            logger.info("TARGET RADIADOR: " + nombreRadiador)
            logger.info("TARGET MODO: " + modoRadiador)
            url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
            datos = {
              "nombreElemento": nombreRadiador,
              "nombreElementoExtra": "",
              "upd_type": "instalation",
              "cambios": [
                {
                  "campo": "IdModoActual",
                  "valor": modoRadiador
                }
              ],
              "idCia": 0,
              "traza": ""
            }
            response = requests.put(url,
            headers={'Authorization': 'Bearer ' + config["token"]},
            json=datos)

            the_fact = ""
            if response.status_code == 200:
                respuesta = response.text
                logger.info("RESPUESTA TXT: " + str(respuesta))
                the_fact = config["traductions"]["MSG_DONE"]
                
            else:
                the_fact = str(response.status_code)
        else:
            the_fact = config["traductions"]["ER_SUCCESS_NO_MATCH"] 
        
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class changeZoneModeHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("changeZoneMode")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In changeZoneModeHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
        
        nombreRadiador = handler_input.request_envelope.request.intent.slots["zone"].value

        logger.info("RESOLUTIONS: " + str(handler_input.request_envelope.request.intent.slots["modo"].resolutions))
        if handler_input.request_envelope.request.intent.slots["modo"].resolutions == None:
            speak_output = config["traductions"]["ASK_MODE"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="modo")).response
        mode_match = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].status.code
        logger.info("MATCH CODE: " + str(mode_match))
        if(mode_match == StatusCode.ER_SUCCESS_MATCH):
            modoRadiador = handler_input.request_envelope.request.intent.slots["modo"].resolutions.resolutions_per_authority[0].values[0].value.id
            logger.info("TARGET RADIADOR: " + nombreRadiador)
            logger.info("TARGET MODO: " + modoRadiador)
            nombreExtra = handler_input.request_envelope.request.intent.slots["instalation"].value
            if nombreExtra == None:
                nombreExtra = ""
            url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
            datos = {
              "nombreElemento": nombreRadiador,
              "nombreElementoExtra": nombreExtra,
              "upd_type": "zone",
              "cambios": [
                {
                  "campo": "IdModoActual",
                  "valor": modoRadiador
                }
              ],
              "idCia": 0,
              "traza": ""
            }

            response = requests.put(url,
            headers={'Authorization': 'Bearer ' + config["token"]},
            json=datos)

            the_fact = ""
            if response.status_code == 200:
                respuesta = response.text
                logger.info("RESPUESTA TXT: " + str(respuesta))
                the_fact = config["traductions"]["MSG_DONE"]
                
            else:
                the_fact = str(response.status_code)
        else:
            speech = config["traductions"]["ER_SUCCESS_NO_MATCH"] 
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response 
        speech = the_fact
        if str(respuesta) == "2":
            logger.info("REDIRIGIENDO SALIDA")
            speak_output = config["traductions"]["ASK_INSTALATION"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="instalation")).response
        else:
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response        
 
 
 


        
class TurnOnHeaterHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TurnOnHeater")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOnHeaterHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["radiador"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "heater",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "true"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response



class TurnOffHeaterHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TurnOffHeater")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOnHeaterHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["radiador"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "heater",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "false"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response




class TurnOnInstalationHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TurnOnInstalation")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOnInstalationHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["instalacion"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "instalation",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "true"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class TurnOffInstalationHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TurnOffInstalation")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOffInstalationHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["instalacion"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": "",
          "upd_type": "instalation",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "false"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
        
        
class TurnOnZoneHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return ask_utils.is_intent_name("TurnOnZone")(handler_input)
        bCanHandle = ask_utils.is_intent_name("TurnOnZone")(handler_input)
        logger.info("TurnOnZoneHandler CAN HANDLE: " + str(bCanHandle))
        return bCanHandle
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOnZoneHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["zone"].value
        nombreExtra = handler_input.request_envelope.request.intent.slots["instalation"].value
        if nombreExtra == None:
            nombreExtra = ""
        logger.info("SLOTS: " + str(handler_input.request_envelope.request.intent.slots))
        logger.info("TARGET ZONE: " + nombreRadiador)
        logger.info("TARGET INSTALATION: " + nombreExtra)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": nombreExtra,
          "upd_type": "zone",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "true"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        if str(respuesta) == "2":
            logger.info("REDIRIGIENDO SALIDA")
            newSlots = {
                "zone":Slot(name="zone", value=nombreRadiador),
                "instalation": Slot(name="zone", value="-")
            }
            newIntent = Intent(name="TurnOnZone",slots= newSlots)
            #return handler_input.response_builder.add_directive(DelegateDirective(updated_intent=newIntent)).response
            speak_output = config["traductions"]["ASK_INSTALATION"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="instalation")).response
        else:
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response

        
class TurnOffZoneHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return ask_utils.is_intent_name("TurnOnZone")(handler_input)
        bCanHandle = ask_utils.is_intent_name("TurnOffZone")(handler_input)
        logger.info("TurnOffZoneHandler CAN HANDLE: " + str(bCanHandle))
        return bCanHandle
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOffZoneHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["zone"].value
        nombreExtra = handler_input.request_envelope.request.intent.slots["instalation"].value
        if nombreExtra == None:
            nombreExtra = ""
        logger.info("SLOTS: " + str(handler_input.request_envelope.request.intent.slots))
        logger.info("TARGET ZONE: " + nombreRadiador)
        logger.info("TARGET INSTALATION: " + nombreExtra)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater"
        datos = {
          "nombreElemento": nombreRadiador,
          "nombreElementoExtra": nombreExtra,
          "upd_type": "zone",
          "cambios": [
            {
              "campo": "Encendido",
              "valor": "false"
            }
          ],
          "idCia": 0,
          "traza": ""
        }

        response = requests.put(url,
        headers={'Authorization': 'Bearer ' + config["token"]},
        json=datos)

        the_fact = ""
        if response.status_code == 200:
            respuesta = response.text
            logger.info("RESPUESTA TXT: " + str(respuesta))
            the_fact = config["traductions"]["MSG_DONE"]
            
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        if str(respuesta) == "2":
            logger.info("REDIRIGIENDO SALIDA")
            newSlots = {
                "zone":Slot(name="zone", value=nombreRadiador),
                "instalation": Slot(name="zone", value="-")
            }
            newIntent = Intent(name="TurnOnZone",slots= newSlots)
            #return handler_input.response_builder.add_directive(DelegateDirective(updated_intent=newIntent)).response
            speak_output = config["traductions"]["ASK_INSTALATION"]
            return handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(ElicitSlotDirective(slot_to_elicit="instalation")).response
        else:
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response


class GetRemoteTemperatureHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetRemoteTemperature")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetRemoteTemperatureHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        nombreRadiador = handler_input.request_envelope.request.intent.slots["radiador"].value
        logger.info("TARGET RADIADOR: " + nombreRadiador)
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater/temperatura/" + nombreRadiador

        response = requests.get(url,
        headers={'Authorization': 'Bearer ' + config["token"]})

        speak_output = config["traductions"]["MSG_HELLO"]
        the_fact = ""
        if response.status_code == 200:
            respuesta = response.json()
            logger.info("RESPUESTA JSON: " + str(respuesta))
            for attribute, value in respuesta.items():
                the_fact =the_fact + attribute + ' <break strength="medium"/>' + str(value) + 'ºC<break strength="strong"/>'
        else:
            the_fact = str(response.status_code)
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class GetRemoteHeatersHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetRemoteHeaters")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetRemoteHeatersHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]
            
        url = "https://gateway.grupoferroli.es/API_EXTERNAL/api/Heater/temperaturas"

        response = requests.get(url,
        headers={'Authorization': 'Bearer ' + config["token"]})

        speak_output = config["traductions"]["MSG_HELLO"]
        the_fact = ""
        if response.status_code == 200:
            respuesta = response.json()
            logger.info("RESPUESTA JSON: " + str(respuesta))
            for attribute, value in respuesta.items():
                the_fact =the_fact + attribute + ' <break strength="medium"/>' + str(value) + 'ºC<break strength="strong"/>'
        else:
            the_fact = str(response.status_code)
        speech = config["traductions"]["MSG_H_LIST"] + '<break strength="x-strong"/>' + the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        language = handler_input.request_envelope.request.locale
        lang_strings = loadLangData()
        language = language[0:2]
        # type: (HandlerInput) -> Response
        speak_output = lang_strings[language]["MSG_HELP"]


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        language = handler_input.request_envelope.request.locale
        lang_strings = loadLangData()
        language = language[0:2]
        # type: (HandlerInput) -> Response
        speak_output = lang_strings[language]["CANCEL_STOP"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        language = handler_input.request_envelope.request.locale
        lang_strings = loadLangData()
        language = language[0:2]
        # type: (HandlerInput) -> Response
        speech = lang_strings[language]["MSG_FALLBACK"]
        reprompt = lang_strings[language]["MSG_FALLBACK_REPROMPT"]

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        language = handler_input.request_envelope.request.locale
        lang_strings = loadLangData()
        language = language[0:2]
        # type: (HandlerInput) -> Response
        speak_output = lang_strings[language]["MSG_TROUBLE"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpWithCommandHandler(AbstractRequestHandler):
    """Handler for get number fact intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelpWithCommand")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpWithCommandHandler")
        config = initialConfig(handler_input)
        if config["resultLinkCard"] != None:
            return config["resultLinkCard"]


        if handler_input.request_envelope.request.intent.slots["command"].resolutions == None:
            mode_match = StatusCode.ER_SUCCESS_NO_MATCH
        else:
            mode_match = handler_input.request_envelope.request.intent.slots["command"].resolutions.resolutions_per_authority[0].status.code

        if(mode_match == StatusCode.ER_SUCCESS_MATCH):
            idComando = handler_input.request_envelope.request.intent.slots["command"].resolutions.resolutions_per_authority[0].values[0].value.id

            the_fact = config["traductions"]["COMMAND_" + idComando]
      
        else:
            the_fact = config["traductions"]["COMMAND_LIST"]
            return handler_input.response_builder.speak(the_fact).ask(the_fact).add_directive(ElicitSlotDirective(slot_to_elicit="command")).response
        
        speech = the_fact
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
        

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(HelpWithCommandHandler())

sb.add_request_handler(GetRemoteHeatersHandler())
sb.add_request_handler(GetRemoteTemperatureHandler())

sb.add_request_handler(ChangeHeaterModeHandler())
sb.add_request_handler(changeInstalationModeHandler())
sb.add_request_handler(changeZoneModeHandler())

sb.add_request_handler(ChangeHeaterTemperatureHandler())
sb.add_request_handler(ChangeInstalationTemperatureHandler())
sb.add_request_handler(ChangeZoneTemperatureHandler())


sb.add_request_handler(TurnOffHeaterHandler())
sb.add_request_handler(TurnOnHeaterHandler())
sb.add_request_handler(TurnOffZoneHandler())
sb.add_request_handler(TurnOnZoneHandler())
sb.add_request_handler(TurnOffInstalationHandler())
sb.add_request_handler(TurnOnInstalationHandler())


sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()