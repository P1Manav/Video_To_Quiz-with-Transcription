import assemblyai as aai
import os
import google.generativeai as genai
import whisper
import json
from langdetect import detect
from pytube import YouTube

# Function to open a file
def startfile(fn):
    os.system('open %s' % fn)

# Function to create and open a txt file
def create_and_open_txt(text, filename):
    # Create and write the text to a txt file
    with open(filename, "w") as file:
        file.write(text)
    startfile(filename)

# Ask user for the YouTube video URL
url = input("Enter the YouTube video URL: ")

# Create a YouTube object from the URL
yt = YouTube(url)

# Get the audio stream
audio_stream = yt.streams.filter(only_audio=True).first()

# Download the audio stream
output_path = ""
filename = "audio.mp3"
audio_stream.download(output_path=output_path, filename=filename)

print(f"Audio downloaded to {output_path}/{filename}")

# Replace with your AssemblyAI API key
aai.settings.api_key = "e7d8d5a3801f4ceab1b87cc463aae0a8"

# URL of the file to transcribe
FILE_URL = "audio.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    #print(transcript.text)

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
    print(questions)
