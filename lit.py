import streamlit as st

st.write("""
# App with something
"""
)
x = st.slider("Select a number", 0, 100)
st.write("You selected: ", x)