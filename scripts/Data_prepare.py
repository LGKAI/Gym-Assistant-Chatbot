#import thư viện
import json
import pandas as pd

#Load the new unlabled intents and responses to dataframe
with open("unlableled_intents.json", "r",encoding="utf-8") as file:
  intents = json.load(file) #load các intents đã xử lý

with open("responses.json","r",encoding="utf") as file:
  responses = json.load(file)#load các responses đã xử lý

responses_keys  = []
intent_keys = list(intents.keys())
intent_values = list(intents.values())
response_values = list(responses.values())
for intent_key in intent_keys:
  responses_keys.append(f"utter_ans_{intent_key}")

#Tạo dataframe cho các intent và response
Data = {"intent_keys": intent_keys,
        "intent_values": intent_values,
        "response_keys": responses_keys,
        "response_values": response_values}
DF = pd.DataFrame(Data) 
DF_size = len(intent_keys)


if __name__ == "__main__":
  #Lưu file domain.yml dưới dạng list
  with open("domain.yml","r") as domain: 
    domain_data = domain.readlines()

  #đánh dấu vị trí của intent và thêm dữ liệu vào sau đó
  mark_intents = domain_data.index("intents:\n") + 1 
  for intent_key in DF["intent_keys"].tolist():
    domain_data.insert(mark_intents,f"  - {intent_key}\n")

  #đánh dấu vị trí của responses và thêm dữ liệu vào sau đó
  mark_responses = domain_data.index("responses:\n") + 1
  for i in range(DF_size):
    for j in range(len(response_values[i])):
      domain_data.insert(mark_responses,f"  {responses_keys[i]}:\n  - text: \"{response_values[i]}\"\n\n")

  #Viết lại toàn bộ file domain.yml bằng dữ liệu mới
  with open("domain.yml","w",encoding="utf-8") as domain:
    domain.writelines(domain_data)

#Lưu file nlu.yml dưới dạng list
  with open("data/nlu.yml","r") as nlu:
    nlu_data = nlu.readlines()

#đánh dấu vị trí để viết vào các intent
  mark_nlu = nlu_data.index("nlu:\n") + 1 

#Thêm dữ liệu vào vị trí thích hợp
  for i in range(DF_size):
    for question in intent_values[i]:
      nlu_data.insert(mark_nlu,f"    - {question}\n" )
    nlu_data.insert(mark_nlu,f"  examples: |\n")
    nlu_data.insert(mark_nlu,f"- intent: {intent_keys[i]}\n")
    nlu_data.insert(mark_nlu,"\n")

 #Viết lại toàn bộ file nlu.yml với dữ liệu mới   
  with open("data/nlu.yml","w") as nlu:
    nlu.writelines(nlu_data)

#Lưu dữ liệu file rules.yml dưới dạng list
  with open("data/rules.yml","r") as rules:
    rules_data = rules.readlines()

#Đánh dấu vị trí và thêm vào các intent và action
  mark_rule = rules_data.index("rules:\n") + 1
  for i in range(DF_size):
    rules_data.insert(mark_rule,f"  - action: {responses_keys[i]}\n")
    rules_data.insert(mark_rule,f"  - intent: {intent_keys[i]}\n")
    rules_data.insert(mark_rule,f"  steps:\n")
    rules_data.insert(mark_rule,f"- rule: response to {intent_keys[i]}\n")
    rules_data.insert(mark_rule,"\n" )

#Viết lại dữ liệu vào file.
  with open("data/rules.yml","w") as rules:
    rules.writelines(rules_data)







