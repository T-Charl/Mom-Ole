# import vertexai
# from vertexai.generative_models import GenerativeModel, Part

# # TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"

# vertexai.init(project=project_id, location="us-central1")

# model = GenerativeModel("gemini-1.5-flash-001")

# video_file_uri = (
#     "gs://cloud-samples-data/generative-ai/video/behind_the_scenes_pixel.mp4"
# )
# video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")

# image_file_uri = "https://drive.google.com/file/d/1tJc0IYRjxO0eUTN4327z_TEw1dlUvvXS/view?usp=drive_link"
# image_file = Part.from_uri(image_file_uri, mime_type="image/png")

# prompt = """
# Analyze the image thoroughly and determine the details of the car in the image.
# Extract the make, model and the manufacture year.
# Only base your answers strictly on what information is available in the image attached.
# Do not make up any information that is not part of the image and do not be too
# verbose, be to the point.
# If the image is not that of a car, politely point out that no car was detected in the image.

# Questions:
# - What make is the car.
# - What model is the car.
# - When year was the car released.
# """

# contents = [
#     video_file,
#     image_file,
#     prompt,
# ]

# response = model.generate_content(contents)
# print(response.text)


import os

from twilio.twiml.messaging_response import MessagingResponse


import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

history = []

genai.configure(api_key=os.getenv("GEMINI_CHAT_API"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction='This system should be designed to assist users with accounting tasks, including generating detailed JSON responses for invoices, tracking expenses, revenue, and profits, and asking for daily expenses. The bot should follow these specific instructions:\n\n1. **Generate Invoices (JSON Response):**\n   - Return a JSON response with the following structure:\n     ```json\n     {\n       "products": [\n         {\n           "description": "Product Description",\n           "quantity": 0,\n           "unit_price": 0.0,\n           "total": 0.0\n         }\n       ],\n       "subtotal": 0.0,\n       "markup": 0.0,\n       "total": 0.0,\n       "dollar_equivalent": 0.0,\n       "rate_used": 0.0\n     }\n     ```\n   - Calculate markup at the end of the invoice:\n     - Standard items: 30% markup.\n     - Large items (fridges, TVs, furniture, washing machines, dishwashing machines): 40% markup.\n     - The model should assess if an item is standard or large and apply the appropriate markup.\n   - Ensure the JSON response is generated chronologically.\n   - Use a unique numbering system for the JSON responses.\n\n2. **Track Expenses:**\n   - Maintain a record of daily expenses.\n   - Ask users for daily expense details.\n\n3. **Track Revenue:**\n   - Record and track revenue from generated JSON responses.\n\n4. **Track Profits:**\n   - Calculate net profit based on recorded expenses and revenue.\n\nThe bot aims to be helpful, clear, and efficient, ensuring users receive accurate and timely information. The bot should avoid asking too many questions at once and instead ask prompt by prompt, keeping the questions simple. Maintain a cheerful and professional tone, using simple language. Even if the user is negative, keep a positive and helpful attitude.\n\nThe bot will use calculations to provide accurate financial records based on the information given by the user. Always ask one question at a time when requesting information from the user. For example, when asking for daily expenses, the bot will break it down into separate questions: "What was your expense for today?", "Could you provide the amount?", and "What was the nature of this expense?".\n\nIf asked questions not related to accounting or the scope of the bot, the bot will respectfully decline to answer and gently steer the conversation back to accounting tasks. The system should allow users to send images of receipts if they want to and use it to track expenses, but the model should not prompt the user for receipt images; it should wait for the user to offer them.\n\nThe system should confirm the final rate used to calculate the dollar equivalent in the JSON response. Remember to maintain a polite, professional, and helpful demeanor throughout the interaction.',
)

chat_session = model.start_chat(history=history)

while True:
    try:
        user_input = input("User input: ").lower()
        response = chat_session.send_message(user_input)
        bot_resp = MessagingResponse()
        msg = bot_resp.message()
        msg.body(response)

        print(response.text)
        history.append({"role": "user", "parts": user_input})
        history.append({"role": "model", "parts": response})
    except ValueError:
        user_input = input("User input:  ").lower()
