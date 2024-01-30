# importing libraries

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

# Step 1: configure API_KEY
genai.configure(api_key=os.getenv('API_KEY'))

# Step 2: create a method to get response from google-pro-vision for the given image and prompt
def gen_response(prompt, uploaded_image):
    """
    this method takes the user given prompt and image and performs the task that user asked on the image and returns a response
    :param prompt: user given prompt
    :param uploaded_image: user uploaded image
    :return: returns gemini-pro generated response
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, uploaded_image[0]])
    return response.text

def format_image(uploaded_image):
    """
    Since, the model gemini-pro-vision takes images as bytes, we need to reformat the image uploaded by
    the user in the form that gemini-pro-vision can understand.
    :param uploaded_image: user uploaded image
    :return: returns the image_data which is a list of dictionary with the type of image and bytes data of user uploaded image
    """
    if uploaded_image is not None:
        # if user uploaded image is not None (valid file)
        image_data = [
            {
                "mime_type" : uploaded_image.type, # type of the image uploaded by user
                "data": uploaded_image.getvalue() # bytes data of the image uploaded by user
            }
        ]
        return image_data
    else: # if no image is uploaded, raise error
        raise FileNotFoundError('No file uploaded')

# Step 3:  initialize streamlit page

st.set_page_config(page_title='Describe your image') # page title
st.header('Describe your image') # page header
# file upload option
uploaded_image = st.file_uploader('Upload image', type=['jpg', 'jpeg','png'])# image file types supported are 'jpg','png', 'jpeg'

# display the user uploaded image on the screen
if uploaded_image: # if user uploaded image is not None (valid file)
    image = Image.open(uploaded_image)
    st.image(image, caption='uploaded image', use_column_width=True)

prompt = 'describe the image'

#submit button for the user
submit = st.button('Describe image')

if submit:
    up_img = format_image(uploaded_image)
    respn = gen_response(prompt, up_img)
    st.header('Response:')
    st.write(respn)














