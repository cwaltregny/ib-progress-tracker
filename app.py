import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, save_data_github, save_plot_github, initialize_data
import pandas as pd
import os
from datetime import date

st.set_page_config(layout="wide")

# Sidebar Dropdown
students = ['SH', 'EA', 'LDA']  
selected_student = st.sidebar.selectbox("Choose IB tracker board", students)

loaded_data = None
if st.sidebar.button("Load Data"):
        loaded_data = load_data(selected_student)
        if loaded_data is not None:
            st.sidebar.text("Data Loaded Successfully")
        else:
            st.sidebar.text("Failed to Load Data")

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
        "Physics HL": ["1. Measurements and uncertainties", "2. Mechanics", "3. Thermal physics", "4. Waves", "5. Electricity and magnetism", "6. Circular motion and gravitation", "7. Atomic, nuclear and particle physics", "8. Energy Production", "9. Wave phenomena", "10. Fields", "11. Electromagnetic induction", "12. Quantum and nuclear physics", "13. Option"]
    }
elif selected_student == 'LDA':
    SUBJECTS_TOPICS = {
        "Physics SL": ["1. Measurements and uncertainties", "2. Mechanics", "3. Thermal physics", "4. Waves", "5. Electricity and magnetism", "6. Circular motion and gravitation", "7. Atomic, nuclear and particle physics", "8. Energy Production"],
        "Mathematics AA SL": ["1. Number and algebra", "2. Functions", "3. Geometry and trigonometry", "4. Statistics and probability", "5. Calculus"],
    }


st.title('IB Subject Progress and Confidence Tracker')

# Create columns for Progress, Confidence, and Plot
col1, col2, col3 = st.columns(3)

progress_initial, confidence_initial = initialize_data(loaded_data, SUBJECTS_TOPICS)

# Progress and Confidence Input Fields
progress_data = {}
confidence_data = {}
# Progress Selectboxes on the first column
col1.header('Progress')
col2.header('Confidence')
for subject, topics in SUBJECTS_TOPICS.items():
    if subject in progress_initial:
        latest_topic_idx = int(progress_initial[subject])
        latest_topic_val = topics[latest_topic_idx - 1] if latest_topic_idx != 0 else 'Not Started'
    else:
        latest_topic_val = 'Not Started'
    latest_topic = col1.selectbox(f'{subject} Latest Covered Topic', ['Not Started'] + topics, index=topics.index(latest_topic_val) if latest_topic_val != 'Not Started' else 0)

    if latest_topic == 'Not Started':
        progress_data[subject] = 0
    else:
        progress_data[subject] = topics.index(latest_topic) + 1

    col2.subheader(subject)
    confidences = []
    if subject in confidence_initial:
        confidence_str = confidence_initial[subject]
        if type(confidence_initial[subject])==str:
            confidence_list = list(confidence_str.strip('][').split(', '))
        else:
            confidence_list = confidence_str

    for idx, topic in enumerate(topics):
        try:
            default_confidence = int(list(confidence_list)[idx])
        except IndexError:
            default_confidence = 0
        except TypeError:
            default_confidence = 0
        confidence = col2.slider(f'Confidence for Topic {topic}', 0, 100, default_confidence, 5)
        confidences.append(confidence)
    confidence_data[subject] = confidences #np.mean(confidences)


with col3:
    col3.header('Summary Plot')
    subjects = list(SUBJECTS_TOPICS.keys())
    progress_values = [progress_data[subject]/len(SUBJECTS_TOPICS[subject]) * 100 for subject in subjects]  
    confidence_values = [np.mean(confidence_data[subject]) for subject in subjects]
    y = np.arange(len(subjects))
    height = 0.35

    fig, ax = plt.subplots(figsize=(10, 7))

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

    if st.button('Save'):
        df = pd.DataFrame({
        'Subject': subjects,
        'Progress': [progress_data[subject] for subject in subjects],
        'Confidence': [confidence_data[subject] for subject in subjects]
        })
        today = date.today()
        plot_path = f'data/{selected_student}_{today}.png'
        fig.savefig(plot_path)
        token = os.environ.get('TOKEN')  
        save_data_github(df, selected_student, token)
        save_plot_github(plot_path, token)
