import json

def extractJson(text):
    json_objects = []
    stack = []
    start = None

    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start = i  # Record the start of a JSON object
            stack.append(char)
        elif char == '}':
            stack.pop()
            if not stack:
                json_snippet = text[start:i + 1]  # Capture the JSON snippet
                try:
                    # Try parsing the snippet as JSON
                    json_data = json.loads(json_snippet)
                    json_objects.append(json_data)  # Append if valid JSON
                except json.JSONDecodeError:
                    # Store incomplete JSON as raw string if parsing fails
                    json_objects.append(json_snippet)

    return str(json_objects[0])


# Example usage:
text = """
promptAnalyzer 
 ----------------------------------------------
Here is the structured JSON output as per the guidelines:

```
{
  "search_description": {
    "primary_search_terms": ["Python YouTube dashboard", "Flask YouTube API", "Heroku deployment", "MongoDB NoSQL database", "YouTube channel statistics", "Python web hosting", "Customizable dashboard", "Rest API methods", "Non-relational database", "Past 7 days analytics", "Easy setup instructions"],
    "domain_search_terms": ["Python web development", "YouTube API integration", "Flask framework", "Heroku hosting", "MongoDB database", "NoSQL database", "Customizable dashboard", "Restful API", "Python project", "YouTube analytics"],
    "suggested_filters": {
      "time_frame": "⏳ Last 2 years",
      "document_type": "📄 GitHub repositories",
      "exclude_terms": "Null"
    },
    "purpose_of_search": "🔍 The user wants to find a Python-based YouTube dashboard repository that uses the Flask framework, has detailed setup instructions, and can be deployed on Heroku or similar hosting platforms. The dashboard should use Rest API methods to communicate with the YouTube channel, and store statistics for the past 7 days in a non-relational database like MongoDB.",
    "searching": "The user is looking for a customizable dashboard that can be easily set up and used, with a focus on YouTube channel analytics. The repository should provide clear instructions for deployment and usage, and allow for modifications to the code, such as adding custom HTML code.",
    "miscellaneous": "💡 The user prioritizes ease of customization, deployment, and usage, with a focus on YouTube channel statistics.",
    "search_query": "🔑 Python Flask YouTube dashboard Heroku MongoDB Rest API"
  },
  "repo_description": {
    "purpose": "📝 A Python-based YouTube dashboard using Flask framework for easy deployment and customization.",
    "main_folders": {
      "src": "📂 Contains Python scripts for dashboard functionality and YouTube API integration.",
      "data": "📊 Stores YouTube channel statistics for the past 7 days.",
      "docs": "📜 Includes setup instructions, usage guides, and contributor guidelines."
    },
    "critical_files": {
      "README.md": "📘 Overview, deployment instructions, and usage guidelines.",
      "requirements.txt": "📦 Lists Python dependencies for easy setup.",
      "app.py": "📂 Main application script for the dashboard.",
      "models.py": "📂 Defines database models for storing YouTube channel statistics.",
      "Procfile": "📂 Configures Heroku deployment settings."
    },
    "miscellaneous": "💡 Includes a configuration file for customizing the dashboard's appearance and behavior.",
    "best_practices": "✅ Follows Flask and Heroku best practices for deployment and usage."
  },
  "analysis": {
    "search_description_assumptions": [
      "🤔 The user is familiar with Python and Flask framework.",
      "The user wants a customizable dashboard for YouTube channel analytics."
    ],
    "repo_description_assumptions": [
      "🧩 The repository will have a clear structure with separate folders for source code, data, and documentation.",
      "The dashboard will use a non-relational database like MongoDB for storing YouTube channel statistics."
    ],
    "other_assumptions_made": [
      "📌 The user has a basic understanding of YouTube API and Rest API methods."
    ],
    "thinking": [
      "🧠 Identified key topics: Python, YouTube dashboard, Flask, Heroku, MongoDB, and Rest API.",
      "Interpreted user goals: customizable dashboard, easy deployment, and YouTube channel analytics.",
      "Structured JSON sections based on user requirements and assumptions."
    ]
  }
}
```Traceback (most recent call last):
  File "C:\\Users\SUPERUSER\Desktop\sefgh-ai\Engine.py", line 34, in <module>
    AnalyzerReport = extractJson(promptAnalyzer(searchQuery)) #returns in json
  File "C:\\Users\SUPERUSER\Desktop\sefgh-ai\workers.py", line 19, in extractJson
    for _, json_str in jsonfinder(data):
ValueError: too many values to unpack (expected 2)

Process finished with exit code 1
"""

json_objects = extractJson(text)
print(json_objects)
