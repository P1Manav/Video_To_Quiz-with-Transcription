# Start by making sure the assemblyai package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use pip3 instead of pip.
import google.generativeai as genai
import json

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "e7d8d5a3801f4ceab1b87cc463aae0a8"

# URL of the file to transcribe
FILE_URL = "audio.mp3"#file path

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print("hello")
    print(transcript.text)



genai.configure(api_key="AIzaSyCGQkTdQD38UawvKumJ2HLzk1y5pBqngJo")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["hii"]
  },
  {
    "role": "model",
    "parts": ["Hello! How can I help you today?"]
  },
])

prompt = transcript.text + """

Create a quiz of ten multiple choice questions from the prompt text with their answers reply only json object in following format:
[
    {
        "question" : <Question Goes Here>,
        "options" : <List of 4 options, do not write ABCD or 1234 before options >,
        "answer" : <Correct answer as number from 1 to 4>
    }
]

I only want json as reply, if you want to write anything then write it comment in json
"""

convo.send_message(prompt)

json_string = convo.last.text[8:-3]
questions = json.loads(json_string)
#print(questions)