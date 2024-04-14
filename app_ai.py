# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 00:15:39 2024

@author: pgiraldo  
"""

# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables 
api_key = os.getenv("OPENAI_API_KEY")  # Used in production
client = OpenAI(api_key=api_key)

# Cell 2: Title & Description
st.title('🤖 AI Social Media Poster')
st.markdown('I was made to help you craft a Social Media Post with the best Length for engagement.')

# Cell 3: Function to generate text using OpenAI
def analyze_text(text):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return
    
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"  # Using the GPT-3.5 model

    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are a professional copywriter and advertisement expert who helps craft social media posts."},
        {"role": "user", "content": """Craft a social media post to grab someone’s attention and encourage them to engage. Craft the same post for each of the following 4 social platforms:
1. Facebook status update with 80 characters.
2. X (formerly Twitter) up to 100 characters and hashtags with a single word under 6 characters.
3. Instagram between 138 to 150 characters, captions with less than 125 characters, and 4-9 hashtags with 22 characters or less.
4. Linkedin up to 1900 words and 2-4 hashtags.
Present your results in a table with the headings: Social Platform, Post, Total Characters.
Display the image after the table."""
}

        
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0  # Lower temperature for less random responses
    )
    return response.choices[0].message.content


# Cell 4: Function to generate the image
def generate_image(text):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return

    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Assuming the API returns an image URL; adjust based on actual response structure
    return response.data[0].url

# Cell 4: Streamlit UI 
user_input = st.text_area("Enter a brief for your post:", "What makes a great French Croissant pastry?")

if st.button('Generate Post Content'):
    with st.spinner('Generating Text...'):
        post_text = analyze_text(user_input)
        st.write(post_text)

    with st.spinner('Generating Thumbnail...'):
        thumbnail_url = generate_image(user_input)  # Consider adjusting the prompt for image generation if needed
        st.image(thumbnail_url, caption='Generated Thumbnail')

