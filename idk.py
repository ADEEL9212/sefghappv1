import json
import re

def extractJson(data, key):
    """
    Extracts the JSON object associated with a given key from a JSON-like string.
    """
    try:
        # Find the position of the key
        key_pattern = rf'"{key}"\s*:\s*'
        match = re.search(key_pattern, data)
        if not match:
            return "NotFound"

        # Starting index is the end of the match
        start_index = match.end()

        # Now extract the JSON value starting from start_index
        # We can try to find the matching closing brace

        # Skip any whitespace
        while start_index < len(data) and data[start_index].isspace():
            start_index += 1

        # Determine the starting character
        first_char = data[start_index]
        if first_char == '{':
            # Extract the JSON object
            return extract_json_object(data, start_index)
        elif first_char == '[':
            # Extract the JSON array
            return extract_json_array(data, start_index)
        elif first_char == '"':
            # Extract the JSON string
            return extract_json_string(data, start_index)
        else:
            # Handle other JSON types (numbers, booleans, etc.)
            return extract_json_value(data, start_index)
    except Exception as e:
        return "Error"

def extract_json_object(data, start_index):
    brace_count = 0
    index = start_index
    while index < len(data):
        char = data[index]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                # Return the JSON object
                return data[start_index:index+1]
        index += 1
    return "Error"

def extract_json_array(data, start_index):
    bracket_count = 0
    index = start_index
    while index < len(data):
        char = data[index]
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                # Return the JSON array
                return data[start_index:index+1]
        index +=1
    return "Error"

def extract_json_string(data, start_index):
    index = start_index + 1
    while index < len(data):
        if data[index] == '"' and data[index - 1] != '\\':
            # Return the JSON string
            return data[start_index:index+1]
        index += 1
    return "Error"

def extract_json_value(data, start_index):
    # Extract until the next comma or closing brace/bracket
    index = start_index
    while index < len(data) and data[index] not in [',', '}', ']']:
        index += 1
    return data[start_index:index].strip()

def removeExcessBackslashes(text):
    """
    Attempts to clean excess backslashes from a JSON-like string.
    """
    # Replace double backslashes with single backslashes
    text = text.replace('\\\\', '\\')
    # Remove single backslashes before double quotes
    text = text.replace('\\"', '"')
    return text

def promptSplitter(input: str):
    # Clean the input
    input = removeExcessBackslashes(input)
    # Extract the three main sections
    out1 = extractJson(input, "search_description")
    out2 = extractJson(input, "repo_description")
    analysis = extractJson(input, "analysis")

    # Check for any extraction errors
    if any(result in ["Error", "NotFound"] for result in (out1, out2, analysis)):
        return input, input, input

    # Return extracted sections as strings
    return out1, out2, analysis


input_data = repr(input("enter"))

out1, out2, analysis = promptSplitter(input_data)
print("Search Description:\n", out1)
print("\nRepo Description:\n", out2)
print("\nAnalysis:\n", analysis)
