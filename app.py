import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, save_to_github
import pandas as pd
import os

st.set_page_config(layout="wide")

# Sidebar Dropdown
students = ['SH', 'EA', 'LDA']  # Add as many students as you have
selected_student = st.sidebar.selectbox("Choose IB tracker board", students)

if selected_student == 'SH':
    SUBJECTS_TOPICS = {
        "Biology HL": ["1. Cell biology", "2. Molecular biology", "3. Genetics", "4. Ecology", "5. Evolution and biodiversity", "6. Human physiology", "7. Nucleic acids", "8. Metabolism, cell respiration and photosynthesis", "9. Plant biology", "10.Genetics and evolution", "11.Animal physiology"],
        "Mathematics AA SL": ["1. Number and algebra", "2. Functions", "3. Geometry and trigonometry", "4. Statistics and probability", "5. Calculus"],
        "English A: Literature SL": ["1. Readers, writers and texts", "2. Time and space", "3. Intertextuality: connecting texts"],
        "French B HL": ["1. Identities", "2. Experiences", "3. Human ingenuity", "4. Social organization", "5. Sharing the planet"],
        "Geography HL": ["1. Population distribution—changing population", "2. Global climate—vulnerability and resilience", "3. Global resource consumption and security", "4. Power, places and networks", "5. Human development and diversity", "6. Global risks and resilience"],
        "Philo SL": ["1. Being human", "2. Selected optional theme"]
    }
elif selected_student == 'EA':
    SUBJECTS_TOPICS = {
        "Physics HL": ["1. Cell biology", "2. Molecular biology", "3. Genetics", "4. Ecology", "5. Evolution and biodiversity", "6. Human physiology", "7. Nucleic acids", "8. Metabolism, cell respiration and photosynthesis", "9. Plant biology", "10.Genetics and evolution", "11.Animal physiology"],
        "Mathematics AA SL": ["1. Number and algebra", "2. Functions", "3. Geometry and trigonometry", "4. Statistics and probability", "5. Calculus"],
        "English A: Literature SL": ["1. Readers, writers and texts", "2. Time and space", "3. Intertextuality: connecting texts"],
        "French B HL": ["1. Identities", "2. Experiences", "3. Human ingenuity", "4. Social organization", "5. Sharing the planet"],
        "Geography HL": ["1. Population distribution—changing population", "2. Global climate—vulnerability and resilience", "3. Global resource consumption and security", "4. Power, places and networks", "5. Human development and diversity", "6. Global risks and resilience"],
        "Philo SL": ["1. Being human", "2. Selected optional theme"]
    }


st.title('IB Subject Progress and Confidence Tracker')

# Create columns for Progress, Confidence, and Plot
col1, col2, col3 = st.columns(3)

# Progress Selectboxes on the first column
col1.header('Progress')
progress_data = {}
for subject, topics in SUBJECTS_TOPICS.items():
    latest_topic = col1.selectbox(f'{subject} Latest Covered Topic', ['Not Started'] + topics)
    if latest_topic == 'Not Started':
        progress_data[subject] = 0
    else:
        progress_data[subject] = topics.index(latest_topic) + 1

# Confidence Sliders on the second column
col2.header('Confidence')
confidence_data = {}
for subject, topics in SUBJECTS_TOPICS.items():
    col2.subheader(subject)
    confidences = []
    for topic in topics:
        confidence = col2.slider(f'Confidence for Topic {topic}', 0, 100, 0, 5)  # Default at 50% confidence
        confidences.append(confidence)
    confidence_data[subject] = np.mean(confidences)  # Storing the average confidence for plotting later

with col3:
    if st.sidebar.button("Load Data"):
        data = load_data(selected_student)
        if data is not None:
            st.sidebar.text("Data Loaded Successfully")
        else:
            st.sidebar.text("Failed to Load Data")
    col3.header('Summary Plot')
    # Plotting Summary on the third column
    subjects = list(SUBJECTS_TOPICS.keys())
    progress_values = [progress_data[subject]/len(SUBJECTS_TOPICS[subject]) * 100 for subject in subjects]  # Convert to percentages
    confidence_values = [confidence_data[subject] for subject in subjects]

    y = np.arange(len(subjects))
    height = 0.35

    fig, ax = plt.subplots(figsize=(6, 12))

    # Add light yellow boxes for each subject
    for i in y:
        ax.barh(i - height/2, 100, height, color='lightyellow')  # 100% for progress
        ax.barh(i + height/2, 100, height, color='lightyellow')  # 100% for confidence


    rects1 = ax.barh(y - height/2, progress_values, height, label='Progress', alpha=0.8)
    rects2 = ax.barh(y + height/2, confidence_values, height, label='Confidence', alpha=0.8)

    ax.set_xlabel('Percentage')
    ax.set_title('Progress and Confidence by Subject')
    ax.set_yticks(y)
    ax.set_xlim(0, 100)
    ax.set_yticklabels(subjects, rotation=45)
    ax.legend()
    ax.invert_yaxis()

    plt.tight_layout()
    col3.pyplot(fig)

    if st.button('Save and Send'):
        df = pd.DataFrame({
        'Subject': subjects,
        'Progress': [progress_data[subject] for subject in subjects],
        'Confidence': [confidence_data[subject] for subject in subjects]
        })

        token = os.environ.get('GITHUB_TOKEN')  
        save_to_github(df, selected_student, token)
