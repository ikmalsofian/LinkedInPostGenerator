import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import GenerationConfig
from datetime import datetime, time

# Load environment variables from .env file
load_dotenv()


def generate_linkedin_post(event_details, ai_creativity):
    """
    Generates a LinkedIn post using the Google Generative AI Python SDK.

    Args:
        event_details (dict): Dictionary containing event details.
        ai_creativity (int): Creativity level for the generation (0-100).

    Returns:
        str: Generated LinkedIn post content.
    """
    # Configure the Google Generative AI client with your API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Google Generative AI API key not set. Please check your .env file.")

    genai.configure(api_key=api_key)

    # Prepare the generation configuration using the GenerationConfig class
    generation_config = GenerationConfig(
        temperature=ai_creativity / 100.0,  # Scale creativity level to the 0-1 range
        top_p=0.95,
        top_k=64,
        max_output_tokens=1500,  # Maximum number of generated tokens
    )

    # Prepare the prompt for generation
    prompt = f"""
    You are a university student pursuing a Bachelor's degree in Computer Science at Universiti Teknologi PETRONAS (UTP). You recently participated in an event and would like to share your experience on LinkedIn to highlight your involvement and professional growth.

    Create a professional and engaging LinkedIn post that captures the following event details:

    - **Event Name**: {event_details['name']}
    - **Venue**: {event_details['venue']}
    - **Start Date and Time**: {event_details['start_date_time']}
    - **End Date and Time**: {event_details['end_date_time']}
    - **Description**: {event_details['description']}
    - **Category**: {event_details['category']}
    - **Your Involvement**: {event_details['involvement']}
    - **Additional Details**: {event_details['additional_details']}

    ### Requirements for the Post:
    1. Begin with a **strong introduction** that highlights the significance of the event.
    2. Provide a **detailed description** of your personal experience and what you gained from participating.
    3. Include specific **examples or anecdotes** to make the post more compelling.
    4. Discuss how the event has **enhanced your professional skills** or knowledge.
    5. End with a **call-to-action** for your network, encouraging engagement or expressing gratitude.

    The post should be written in a conversational yet professional tone, using first-person language (e.g., "I had the opportunity to…"). Aim for at least **150 words** to ensure the content is informative and impactful.
    """

    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    st.set_page_config(layout="wide")
    st.title("LinkedScribe: Your University Event to LinkedIn Post Generator")

    # Split the page into two columns: left for inputs and right for the generated output
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("Event Details")
        st.write("Fill in the details of your event below:")

        # Input fields for event details
        event_name = st.text_input("Event Name", placeholder="e.g., Tech Symposium 2024")
        venue = st.text_input("Venue", placeholder="e.g., Main Hall, Building A")

        # Start Date and End Date selection using the calendar toggle
        start_date = st.date_input("Select Start Date")
        start_time = st.time_input("Select Start Time", value=time(9, 0))  # Default start time at 09:00 AM
        start_date_time = datetime.combine(start_date, start_time).strftime("%Y-%m-%d %H:%M:%S")

        end_date = st.date_input("Select End Date")
        end_time = st.time_input("Select End Time", value=time(17, 0))  # Default end time at 05:00 PM
        end_date_time = datetime.combine(end_date, end_time).strftime("%Y-%m-%d %H:%M:%S")

        description = st.text_area("Event Description", placeholder="Describe the event in detail.")
        category = st.text_input("Event Category", placeholder="e.g., Technology, Education, Networking")
        involvement = st.text_area("Your Involvement", placeholder="Describe your role or contribution.")
        additional_details = st.text_area("Additional Details (optional)",
                                          placeholder="Any other relevant information.")

        # Slider for AI creativity
        ai_creativity = st.slider("AI Creativity Level", 0, 100, 50)

        if st.button("Generate LinkedIn Post"):
            if not os.getenv("GEMINI_API_KEY"):
                st.error("Google Generative AI API key is not set. Please check your .env file.")
                return

            # Collect event details
            event_details = {
                "name": event_name,
                "venue": venue,
                "start_date_time": start_date_time,
                "end_date_time": end_date_time,
                "description": description,
                "category": category,
                "involvement": involvement,
                "additional_details": additional_details
            }

            # Call the function to generate the post
            generated_post = generate_linkedin_post(event_details, ai_creativity)

            # Store the generated post in session state
            st.session_state.generated_post = generated_post

    with right_col:
        st.header("Generated LinkedIn Post")
        # Usage in your Streamlit app
        if 'generated_post' in st.session_state:

            st.write(generated_post)
            st.code(generated_post, language="text")


    # Footer for the app
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Powered by Google Generative AI")


if __name__ == "__main__":
    main()