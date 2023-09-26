import streamlit as st
import os

from PIL import Image
image = Image.open("./img/reply-logo.png")
st.image(image)

version = os.environ.get("WEB_VERSION", "0.1")

st.header(f"Chat with Private Docs - Bedrock Demo App (Version {version})")
st.markdown("This is a demo of Bedrock models ")
