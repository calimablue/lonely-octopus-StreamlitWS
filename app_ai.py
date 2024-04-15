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
st.subheader('I help you craft a social media post with an ideal length for maximum engagement.')

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
        {"role": "user", "content": f"""Craft a social media post to grab someone’s attention and encourage them to engage in the topic. Craft the same post for each of the following social platforms:
1. For Facebook Status Update use an average of 80 characters.
2. For X (Twitter) use an average of 100 characters. Add hashtags with a single word under 6 characters.
3. For Instagram use between 138 to 150 characters. Add 4-9 hashtags with 22 characters or less. 
4. For Instagram caption use an average of 125 characters. No hashtags.
5. For Linkedin use an average of 1700 characters. Add 2-4 hashtags.
Present your results in a table with headings: Social Platform, Post, Character Count.
After the table, craft a recommendation about using an image with the post.{text}"""
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
# Display the prompt in bold using Markdown
st.markdown("**Replace the text below with your post summary then click Generate Social Post:**")
# Provide a text area for user input with a simple placeholder
user_input = st.text_area("", """GOAL: Increase engagement and share new product launch.
AUDIENCE: Young adults interested in eco-friendly products.
CONTENT DETAILS: Highlight the key features of the new eco-friendly water bottle, emphasize sustainability, and introduce a limited-time launch discount.
TONE AND STYLE: Inspirational and energetic.
VISUAL ELEMENTS: Bright, eye-catching image of the product in a natural setting.
CALL TO ACTION: Encourage followers to visit the website to learn more and use a promo code for a discount.
HASHTAGS: #EcoFriendlyLiving #SustainableChoices
MENTIONS: Mention partner organizations and influencers.""", height=300)

if st.button('Generate Social Post'):
    with st.spinner('Generating Your Post...'):
        post_text = analyze_text(user_input)
        st.write(post_text)

    with st.spinner('Generating a Social Thumbnail...'):
        thumbnail_url = generate_image(user_input)  # Consider adjusting the prompt for image generation if needed
        st.image(thumbnail_url, caption='Generated Thumbnail')

