from pydantic import ValidationError, BaseModel

import re
import json
import pythonmonkey

def _extract_first_json_object(text: str) -> str:
    brace_count = 0
    in_string = False
    escape = False
    start_index = None

    for i, char in enumerate(text):
        if char == '"' and not escape:
            in_string = not in_string
        elif char == '\\' and in_string:
            escape = not escape
            continue
        else:
            escape = False

        if not in_string:
            if char == '{':
                if brace_count == 0:
                    start_index = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_index is not None:
                    return text[start_index:i+1]

    raise ValueError("No complete JSON object found.")

## Using regex to get pure json from answer of planner model
def clean_response_to_str(text: str) -> str: 
    # Finding first valid JSON object in response
    try: 
        _extract_first_json_object(text)
    except ValueError as e: 
        print(f"ValueError: {e}\n{e.__traceback__}\n")

    # cutting out unnecessary json flags
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match: 
        json_str = match.group(1)
    else: 
        json_str = text


    # Clean common issues
    jsonrepair = pythonmonkey.require('jsonrepair').jsonrepair
    print(f"String after repair: {jsonrepair}")
    cleaned_json = jsonrepair(json_str)
    cleaned_json = re.sub(r'[\"\']null[\"\']', "null", cleaned_json)
    # json_str = re.sub(r"[`´]", "'", json_str)  # Replace all single quotes with '
    # json_str = re.sub(r'[“”«»]', '"', json_str)  # Replace all double quotes with "
    # json_str = re.sub(r"\"\"", r"\"", json_str)  # Fix double quotes
    # json_str = re.sub(r"\\\"", r"\"", json_str)  # Fix escaped quotes
    # json_str = re.sub(r"\" \"", r"\", \"", json_str)  # Fix missing comma between values in list
    # json_str = re.sub(r'(")(\s*)("(?=[^"]*?":))', r'\1,\2\3', json_str) # Fix missing comma between values in dicts
    # json_str = re.sub(r",\s*([\]}])", r"\1", json_str)  # Remove trailing commas

    print(f"Cleaned json: {cleaned_json}")

    return json_str

def _get_model_keys(model_class: BaseModel):
    """
    Extracts the keys (field names) from a Pydantic model class.
    """
    return list(model_class.model_fields.keys())


def build_model_from_string(input_str: str) -> BaseModel:
    # Find out what specific type of BaseModel the incoming object is, using the first key 
    # of each Schema. To cut time and circumvent errors, the json is sliced first
    model_class : BaseModel
    sliced_json = input_str[:40]
    if "\"name\"" in sliced_json:
        model_class = format.Character
    elif "\"genre\"" in sliced_json:
        model_class = format.Plot
    elif "\"time\"" in sliced_json: 
        model_class = format.Setting
    else:
        model_class = BaseModel

    # Fetch appropriate keys of the provided model
    valid_keys = _get_model_keys(model_class)

    # Clean the JSON string
    cleaned_json_str = clean_response_to_str(input_str)
    
    try:
        # Parse cleaned JSON into a dictionary
        data_dict = json.loads(cleaned_json_str)
        print(f"Brainstorming.py: build_model_from_string(): data_dict: {data_dict}")
        
        # Remove any unnecessary keys that aren't in the valid keys
        filtered_data = {key: value for key, value in data_dict.items() if key in valid_keys}
        print(f"Brainstorming.py: build_model_from_string(): filtered_data: {filtered_data}")
        
        # Validate and return the filtered dictionary
        result_data = model_class.model_validate(filtered_data)
        print(f"Brainstorming.py: build_model_from_string(): character_data: {result_data}")
        return result_data
    
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(f"Validation failed at character {e.pos} with character {cleaned_json_str[e.pos]}")
        return None
    except ValidationError as e:
        # write it so the answer of the last round of iteration is used and written into the file
        print(f"Pydantic validation error: {e}")
        return None