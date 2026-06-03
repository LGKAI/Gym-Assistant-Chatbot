from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from groq import Groq
import json
class ActionRecommendExercise(Action):
    def name(self) -> str:
        return "action_recommend_exercise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        muscle_group = tracker.get_slot("muscle_group")
        user_message = tracker.latest_message.get("text")
        flag = True
        if muscle_group == "chest":
            exercise = "Bench Press or Push-Up"
            method = "To perform a bench press, lie on a flat bench with your feet flat on the floor and grip the barbell slightly wider than shoulder-width apart. Unrack the barbell and slowly lower it towards your chest, keeping your elbows tucked in. Press the barbell back up to the starting position. For push-ups, start in a plank position with your hands shoulder-width apart. Lower your body towards the ground, keeping your core engaged, and then push back up. Remember to warm up before starting, maintain proper form, listen to your body, and be patient as you build strength and muscle."
            link = "https://www.youtube.com/watch?v=CCZGD55NxGo\nhttps://www.youtube.com/watch?v=-MAABwVKxok"
 
        elif muscle_group == "leg" or muscle_group == "legs":
            exercise = "Squat or Leg Press"
            method = "To perform a squat, stand with your feet shoulder-width apart and your toes slightly pointed outward. Lower your hips back and down as if sitting in a chair, keeping your back straight and your core engaged. Push through your heels to return to the starting position. For a leg press, sit on the machine and place your feet on the platform shoulder-width apart. Push the platform away from you until your legs are fully extended, then slowly return to the starting position. Remember to maintain proper form and use a weight that is challenging but manageable."
            link = "https://www.youtube.com/watch?v=gcNh17Ckjgg\nhttps://www.youtube.com/shorts/ahaJTts1f3s"
        elif muscle_group == "core" or muscle_group == "abs":
            exercise = "Plank or Deadlift"
            method = "To perform a deadlift, stand with your feet hip-width apart in front of the barbell. Bend down and grip the barbell with an overhand grip, keeping your back straight and your core engaged. Lift the barbell by straightening your legs and hips, keeping the barbell close to your body. Slowly lower the barbell back to the ground. To do a plank, start in a push-up position with your forearms on the ground and your elbows directly under your shoulders. Hold this position, keeping your body in a straight line from your head to your heels"
            link = "https://www.youtube.com/watch?v=TvxNkmjdhMM\nhttps://www.youtube.com/watch?v=XxWcirHIwVo"
        elif muscle_group == "back":
            exercise = "Pull-ups or Seated Cable Rows"
            method = "To perform a pull-up, grip the bar with an overhand grip, hands slightly wider than shoulder-width apart. Engage your core and pull your body up towards the 1  bar, bringing your chest to the bar. Slowly lower yourself back down to the starting position. To perform a seated cable row, sit at the cable machine with your feet flat on the floor. Grip the handle and lean back slightly, keeping your back straight. Pull the handle towards your chest, squeezing your shoulder blades together. Slowly return to the starting position."
            link = "https://www.youtube.com/watch?v=bb8_5vZV5dU\nhttps://www.youtube.com/watch?v=vwHG9Jfu4sw"
        elif muscle_group == "shoulder":
            exercise = "Lateral Raises or Overhead Press"
            method = "To perform a lateral raise, stand tall with your feet shoulder-width apart, holding dumbbells at your sides. Raise your arms out to the sides, keeping them slightly bent at the elbows, until they are parallel to the ground. Slowly lower your arms back down to the starting position. For an overhead press, stand with your feet shoulder-width apart, holding dumbbells at shoulder height. Press the dumbbells straight up overhead, keeping your elbows tucked in. Slowly lower the dumbbells back down to the starting position. Remember to maintain proper form and use a weight that is challenging but manageable."
            link = "https://www.youtube.com/watch?v=PzsMitRdI_8\nhttps://www.youtube.com/watch?v=M2rwvNhTOu0"
        else:
            flag = False
        if flag: 
            text = f"You can try {exercise} for {muscle_group} building. {method}\n. Here are the links for better instruction:\n{link}"
        else:
            text = "I don't have the instructions for the muscle group that you want to train yet"
            with open("New_questions.txt","a") as file:
                file.write(f"{user_message}\n")
        dispatcher.utter_message(
            text=text
        )
        return []
    

class ActionLowConfidenceFallback(Action):
    def name(self) -> Text:
        return "action_low_confidence_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Retrieve the user's query
        user_message = tracker.latest_message.get("text")

        # Invoke your custom model here
        response = self.call_external_model(user_message)

        # Send the model's response back to the user
        dispatcher.utter_message(text=response)

        #Save the new questions for updating chatbot
        with open("New_questions.txt","a") as New_questions:
          New_questions.write(user_message + "\n")

    def call_external_model(self, query: Text) -> Text:
      #Get the api_key
      with open("api_keys.json","r") as keys_file:
          keys = json.load(keys_file)
      
      #load model
      client = Groq(api_key=keys["groq_api_key"])

      chat_completion = client.chat.completions.create(
          messages=[
              {
                  "role": "system", #Vài
                  "content": "Your name is Hoang Sang. You are a helpful and friendly gym assistant."
              },
              {
                  "role": "user",
                  "content": f"{query}",
              }
          ],
          model="llama3-8b-8192",
      )
      response = chat_completion.choices[0].message.content
      return f"\n{response}"
    
