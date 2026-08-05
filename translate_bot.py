import time
import os
from deep_translator import GoogleTranslator
from ruamel.yaml import YAML

translator = GoogleTranslator(source='en', target='vi')

def translate_text(text):
    try:
        if not text.strip():
            return text
        res = translator.translate(text)
        time.sleep(0.05) # Be nice to the API
        return res
    except Exception as e:
        print(f"Error translating: {text[:30]}... - {e}")
        return text

def translate_nlu():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    
    nlu_path = 'data/nlu.yml'
    if not os.path.exists(nlu_path):
        print(f"{nlu_path} not found.")
        return

    with open(nlu_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
    
    print("Translating NLU examples...")
    for item in data.get('nlu', []):
        if 'intent' in item and 'examples' in item:
            examples_str = item['examples']
            lines = examples_str.split('\n')
            translated_lines = []
            for line in lines:
                if line.strip().startswith('- '):
                    # Extract the text after '- '
                    prefix_idx = line.find('- ') + 2
                    text = line[prefix_idx:]
                    translated = translate_text(text)
                    translated_lines.append(line[:prefix_idx] + translated)
                else:
                    translated_lines.append(line)
            
            from ruamel.yaml.scalarstring import PreservedScalarString
            item['examples'] = PreservedScalarString('\n'.join(translated_lines))
            print(f"Translated intent: {item['intent']}")

    with open(nlu_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print("NLU translated successfully!")

def translate_domain():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    
    domain_path = 'domain.yml'
    if not os.path.exists(domain_path):
        print(f"{domain_path} not found.")
        return

    with open(domain_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
    
    print("Translating Domain responses...")
    if 'responses' in data:
        for response_key, response_list in data['responses'].items():
            for resp in response_list:
                if 'text' in resp:
                    original_text = resp['text']
                    translated = translate_text(original_text)
                    
                    from ruamel.yaml.scalarstring import PreservedScalarString
                    resp['text'] = PreservedScalarString(translated)
            print(f"Translated response: {response_key}")

    with open(domain_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print("Domain translated successfully!")

if __name__ == '__main__':
    translate_nlu()
    translate_domain()
    print("Done!")
