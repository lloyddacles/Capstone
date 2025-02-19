#import streamlit as st

#st.title("THIS IS THE GREATEST SHOW!")
#st.subheader("It is always fun to be here!")
#st.write("Join us and earn great salary!")
#st.divider()
#st.image("LDRaidmaxLogo.jpg", "CodeLikeLD!")

import streamlit as st

# Page Configuration
st.set_page_config(page_title="Programming Dashboard", page_icon="💻", layout="wide")

st.title("💻 Programming Dashboard")
st.write("""
Welcome to the Programming Dashboard! Explore different programming languages, tutorials, and resources.
""")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ("Home", "Languages", "Resources", "About"))

# Home Section
if option == "Home":
    st.header("🏠 Home")
    st.write("""
    This dashboard provides an overview of programming concepts, language popularity, and helpful resources for beginners and professionals alike.
    """)

# Programming Languages Section
elif option == "Languages":
    st.header("📝 Programming Languages")
    st.write("""
    **Popular Languages:**
    - Python 🐍
    - JavaScript 🌐
    - Java ☕
    - C++ 💡
    - Ruby 💎
    """)

# Resources Section
elif option == "Resources":
    st.header("📚 Resources")
    st.write("""
    Here are some valuable resources for learning programming:

    - [Python Documentation](https://docs.python.org/3/)
    - [MDN Web Docs (JavaScript)](https://developer.mozilla.org/en-US/)
    - [GeeksforGeeks](https://www.geeksforgeeks.org/)
    - [LeetCode](https://leetcode.com/)
    """)

# About Section
elif option == "About":
    st.header("ℹ️ About")
    st.write("""
    This dashboard was created to help programmers explore various aspects of coding, from languages to practical resources.
    """)

st.markdown("""
<style>
    .stTextInput > label, .stTextArea > label {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


