import json
from Data_prepare import DF

def clear_file(file_path):
  with open(file_path,"w") as file:
    file.write("")
#Save new questions to dataset and clear the current file.
with open("New_questions.txt","r",encoding="utf-8") as questions:
  question_list = questions.readlines()

with open("Dataset/Questions.txt","a",encoding="utf-8") as writer:
  writer.writelines(question_list)

clear_file("New_questions.txt")

#Save new intents to dataset and clear the current file.
with open("Dataset/Intents.json","r", encoding="utf-8") as Intents_file:
  cur_intents = json.load(Intents_file)
with open("Dataset/Intents.json","w", encoding="utf-8") as Intents_file:
  new_intents = dict(zip(DF["intent_keys"].tolist(), DF["intent_values"].tolist()))
  updated_intents = cur_intents.copy()
  updated_intents.update(new_intents)
  json.dump(updated_intents,Intents_file, indent=4)

clear_file("unlableled_intents.json")

#Save new responses to dataset and clear the current file.
with open("Dataset/Responses.json","r",encoding="utf-8") as Responses_file:
  cur_responses = json.load(Responses_file)
with open("Dataset/Responses.json","w", encoding="utf-8") as Responses_file:
  new_responses = dict(zip(DF["response_keys"].tolist(), DF["response_values"].tolist()))
  updated_responses = cur_responses.copy()
  updated_responses.update(new_responses)
  json.dump(updated_responses,Responses_file, indent=4)

clear_file("responses.json")
