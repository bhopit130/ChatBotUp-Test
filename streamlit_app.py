
import streamlit as st
import requests

# Function to fetch word details from API
def get_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Initialize Streamlit app
def main():
    st.set_page_config(page_title="AI Chatbot Dictionary", layout="wide")

    st.title("AI Chatbot Dictionary")
    st.markdown("A modern, AI-powered dictionary app with history and favorite lists.")

    # Session state to track history and favorites
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

    # Input section
    word = st.text_input("Enter a word to search:", "")
    if st.button("Search") and word:
        details = get_word_details(word)
        if details:
            st.session_state['history'].append(word)
            st.write(f"### {details[0]['word'].capitalize()}")
            meanings = details[0].get('meanings', [])
            for meaning in meanings:
                st.write(f"**Part of Speech:** {meaning['partOfSpeech']}")
                for definition in meaning['definitions']:
                    st.write(f"- {definition['definition']}")
                    if 'example' in definition:
                        st.write(f"_Example: {definition['example']}_")
            if st.button(f"Add '{word}' to Favorites"):
                if word not in st.session_state['favorites']:
                    st.session_state['favorites'].append(word)
                    st.success(f"'{word}' added to favorites.")
                else:
                    st.warning(f"'{word}' is already in favorites.")
        else:
            st.error("Word not found. Please try another word.")

    # History section
    st.sidebar.header("Search History")
    if st.session_state['history']:
        st.sidebar.write(st.session_state['history'])
    else:
        st.sidebar.write("No search history yet.")

    # Favorites section
    st.sidebar.header("Favorite Words")
    if st.session_state['favorites']:
        st.sidebar.write(st.session_state['favorites'])
    else:
        st.sidebar.write("No favorite words yet.")

if __name__ == "__main__":
    main()
