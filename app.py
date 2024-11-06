# app.py

import os
import pandas as pd
import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

# Load the CSV file (ensure the file path is correct for deployment)
csv_file_path = 'imdb_movie_dataset.csv'  # Assuming file is in the same directory
movies_data = pd.read_csv(csv_file_path)

# Function to get movie analysis based on descriptions
def get_movie_analysis(query, dataset):
    # Filter dataset based on partial user query
    matching_movies = dataset[dataset['Title'].str.contains(query, case=False, na=False)]
    
    # Check if there are any matching movies
    if matching_movies.empty:
        return f"No movies found with the title containing '{query}'.", []
    
    # Suggest up to 5 similar titles
    suggested_titles = matching_movies['Title'].unique()[:5]
    
    # Use the first matching title to get movie analysis
    first_match = matching_movies.iloc[0]
    description = f"{first_match['Title']}: {first_match['Description']}"
    
    # Query the Groq API with the selected description
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this movie description for the following query: '{query}'. Description: {description}"
                }
            ],
            model="llama3-8b-8192",
        )
        analysis_result = chat_completion.choices[0].message.content
    except Exception as e:
        analysis_result = f"Error: {e}"
    
    return analysis_result, suggested_titles

# Streamlit UI
st.title("Movie Analyzer")
st.write("Enter a movie title to get analysis")

# User input
user_query = st.text_input("Enter movie title", "")

if user_query:
    # Get analysis and suggestions
    analysis_result, suggestions = get_movie_analysis(user_query, movies_data)
    
    if suggestions:
        st.subheader("")
        for i, title in enumerate(suggestions, start=1):
            st.write(f"{i}. {title}")
        
        st.subheader(f"Analysis for: {suggestions[0]}")
        st.write(analysis_result)
    else:
        st.write(analysis_result)

# Streamlit styling options
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #2E86C1;
        color: white;
    }
    .css-18e3th9 {
        background-color: #2E86C1;
        color: white;
    }
    h1, h2, h3 {
        color: #2E86C1;
    }
    </style>
    """,
    unsafe_allow_html=True
)
