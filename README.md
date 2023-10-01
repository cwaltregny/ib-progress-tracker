# IB Subject Progress and Confidence Tracker

An interactive Streamlit application designed to visualize and track the progress and confidence of IB students across various subjects and topics.

## Overview

The IB Subject Progress and Confidence Tracker is an application for International Baccalaureate (IB) students to visualize their study progress and assess their confidence in different subjects and topics. The application provides a visual summary to help students focus on subjects or topics where they might need additional review.

## Features

- **Student Selection**: Choose between different student profiles to load their specific data.
- **Data Loading**: Load a student's previous data to track progress over time.
- **Progress Tracking**: Input the latest topics covered for each subject.
- **Confidence Assessment**: For each topic in a subject, assess your confidence on a scale of 0 to 100.
- **Visual Summary**: View a combined bar chart that visualizes both the progress and confidence for each subject.
- **Data Saving**: Save the data to a GitHub repository for persistence and future reference. Additionally, save visual plots directly to a "plot" directory in the repository.

## Setup and Installation

### Prerequisites

- Python 3.x
- Streamlit
- Other dependencies from `requirements.txt`

### Steps

1. Clone the repository: `git clone https://github.com/cwaltregny/ib-progress-tracker.git`
2. Navigate to the project directory: `cd ib-progress-tracker`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up environment variables (if required): `export TOKEN="github_token"`
5. Run the Streamlit app: `streamlit run app.py`

## Usage
- Choose a student profile from the sidebar.
- (Optional) Load previous data for the selected student.
- Update progress and confidence for each subject.
- View the visual summary on the right panel.
- Save the data to GitHub using the 'Save' button.


## Contributions

Contributions are welcome! Please ensure that you test the changes locally before creating a pull request.