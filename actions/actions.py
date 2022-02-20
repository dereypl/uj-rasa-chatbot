# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime as date


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionShowOpeningHours(Action):

    def name(self) -> Text:
        return "action_show_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        opening_hours = json.load(open("data/opening_hours.json"))
        dispatcher.utter_message(text="Our restaurant is open:\n")

        for day in opening_hours["items"]:
            text = ""
            opening_hour = opening_hours["items"][day]["open"]
            closing_hour = opening_hours["items"][day]["close"]

            if opening_hour == 0 and closing_hour == 0:
                text += day + ": - Closed -\n"
            else:
                text += day + ": " + str(opening_hour) + "-" + str(closing_hour) + "\n"

            dispatcher.utter_message(text=text)
        return []


class ActionCheckIsOpenOnDay(Action):
    opening_hours = json.load(open("data/opening_hours.json"))["items"]

    def name(self) -> Text:
        return "action_check_is_open_on_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'days_of_week_entities':
                selected_day = blob['value'].capitalize()

                if self.opening_hours.get(selected_day):
                    opening_hour = self.opening_hours[selected_day]["open"]
                    closing_hour = self.opening_hours[selected_day]["close"]

                    if opening_hour == 0 and closing_hour == 0:
                        dispatcher.utter_message(text=f"Restaurant is closed on {selected_day}.")
                    else:
                        dispatcher.utter_message(
                            text=f"Yes, on {selected_day} we are open from {opening_hour} to {closing_hour}.")
                else:
                    dispatcher.utter_message(text="Please check if given day of week is correct.")

        return []


class ActionCheckIsOpenNow(Action):

    def name(self) -> Text:
        return "action_check_is_open_now"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        opening_hours = json.load(open("data/opening_hours.json"))

        now = date.today()
        today = now.strftime("%A")

        opening_hour = opening_hours["items"][today]["open"]
        closing_hour = opening_hours["items"][today]["close"]

        if opening_hour == 0 and closing_hour == 0 or not (opening_hour <= now.hour < closing_hour):
            dispatcher.utter_message(text="We are closed. You can visit us: ")
            for day in opening_hours["items"]:
                text = ""
                day_opening_hour = opening_hours["items"][day]["open"]
                day_closing_hour = opening_hours["items"][day]["close"]

                if day_opening_hour == 0 and day_closing_hour == 0:
                    text += day + ": - Closed -\n"
                else:
                    text += day + ": " + str(day_opening_hour) + "-" + str(day_closing_hour) + "\n"

                dispatcher.utter_message(text=text)
        else:
            dispatcher.utter_message(text="Yes, today restaurant is open till " + str(closing_hour) + ":00.")

        return []


class ActionShowMenu(Action):
    menu = json.load(open("data/menu.json"))

    def name(self) -> Text:
        return "action_show_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Restaurant's menu:\n")
        text = ""
        for item in self.menu["items"]:
            text += item["name"].capitalize() + "- " + str(item["price"]) + ",00 - preparation time: " + str(item[
                'preparation_time']) + "h\n"

        dispatcher.utter_message(text=text)
        return []
