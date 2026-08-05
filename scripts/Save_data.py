import json
from data_prepare import DF


def clear_file(file_path):
    """Xoá nội dung của một file."""
    with open(file_path, "w") as file:
        file.write("")


# Lưu câu hỏi mới vào dataset và xoá file tạm
with open("New_questions.txt", "r", encoding="utf-8") as questions:
    question_list = questions.readlines()

with open("dataset/Questions.txt", "a", encoding="utf-8") as writer:
    writer.writelines(question_list)

clear_file("New_questions.txt")

# Lưu intents mới vào dataset và xoá file tạm
with open("dataset/Intents.json", "r", encoding="utf-8") as intents_file:
    cur_intents = json.load(intents_file)
with open("dataset/Intents.json", "w", encoding="utf-8") as intents_file:
    new_intents = dict(zip(DF["intent_keys"].tolist(), DF["intent_values"].tolist()))
    updated_intents = cur_intents.copy()
    updated_intents.update(new_intents)
    json.dump(updated_intents, intents_file, indent=4)

clear_file("unlableled_intents.json")

# Lưu responses mới vào dataset và xoá file tạm
with open("dataset/Responses.json", "r", encoding="utf-8") as responses_file:
    cur_responses = json.load(responses_file)
with open("dataset/Responses.json", "w", encoding="utf-8") as responses_file:
    new_responses = dict(zip(DF["response_keys"].tolist(), DF["response_values"].tolist()))
    updated_responses = cur_responses.copy()
    updated_responses.update(new_responses)
    json.dump(updated_responses, responses_file, indent=4)

clear_file("responses.json")
