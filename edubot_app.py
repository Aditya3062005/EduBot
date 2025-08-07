#!/usr/bin/env python
# coding: utf-8

# Step 0: Securely Enter API Key (Run in a Separate Cell)

# In[ ]:


import os
import getpass
os.environ["GEMINI_API_KEY"] = getpass.getpass("🔐 Enter your Gemini API Key: ")


# Step 1: Install necessary packages

# In[ ]:


get_ipython().system('pip install google-generativeai ipywidgets -q')


# Step 2: Import libraries

# In[ ]:


import os
import google.generativeai as genai
import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output


# Step 3: Load secure API key

# In[ ]:


API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ Gemini API key not found. Please set it using getpass first.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# Step 4: Define widgets

# In[ ]:


topic_input = widgets.Text(
    description='📘 Topic:',
    placeholder='e.g. Python Loops, Photosynthesis...',
    style={'description_width': 'initial'}
)

tone_input = widgets.Dropdown(
    options=['Simple', 'Detailed', 'Motivational', 'Conversational'],
    description='🎯 Tone:',
    style={'description_width': 'initial'}
)

audience_input = widgets.Text(
    description='👥 Audience:',
    placeholder='e.g. beginners, high school students...',
    style={'description_width': 'initial'}
)

level_input = widgets.Dropdown(
    options=['Beginner', 'Intermediate', 'Advanced'],
    description='⚙️ Level:',
    style={'description_width': 'initial'}
)

language_input = widgets.Dropdown(
    options=[
        'English', 'Hindi', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Kannada',
        'Gujarati', 'Malayalam', 'Urdu'
    ],
    description='🌐 Language:',
    style={'description_width': 'initial'}
)

submit_button = widgets.Button(
    description='Generate Tip',
    button_style='primary'
)

output = widgets.Output()


# Step 5: Define the generation function

# In[ ]:


def generate_tip(b):
    output.clear_output()

    selected_language = language_input.value

    content_prompt = f"""
You are EduBot – an expert AI Learning Assistant.
Create a short, engaging, and helpful educational snippet for this topic:
- Topic: "{topic_input.value}"
- Audience: {audience_input.value}
- Tone: {tone_input.value}
- Level: {level_input.value}
Respond in {selected_language}.
Keep it under 100 words. Avoid unnecessary technical jargon.
"""

    resource_prompt = f"""
Suggest 1 free online educational resource (website, video, or course) to learn about "{topic_input.value}".
Include a short reason and a clickable link.
Only recommend free content from trusted sources like YouTube, Coursera, edX, Khan Academy, GeeksforGeeks, etc.
Respond in {selected_language}.
"""

    with output:
        try:
            tip_response = model.generate_content(content_prompt)
            tip = tip_response.text.strip()

            resource_response = model.generate_content(resource_prompt)
            resource = resource_response.text.strip()

            display(Markdown(f"### 🎓 EduTip ({selected_language}):\n\n{tip}"))
            display(Markdown(f"---\n### 🌐 Learn More:\n\n{resource}"))
        except Exception as e:
            print("❌ Error:", e)

submit_button.on_click(generate_tip)


# Step 6: Display the form

# In[ ]:


form = widgets.VBox([
    widgets.HTML(value="<h2>🤖 EduBot – AI Learning Assistant with Language Support</h2>"),
    topic_input,
    tone_input,
    audience_input,
    level_input,
    language_input,
    submit_button,
    output
])

display(form)

