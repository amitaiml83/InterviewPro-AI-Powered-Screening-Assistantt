# Hiring Assistant Chatbot

## Project Overview
The **Hiring Assistant Chatbot** is a Streamlit-based application designed to streamline the candidate screening process. This chatbot assists recruiters by:
- Collecting candidate details (e.g., name, contact information, years of experience, desired position, and tech stack).
- Generating technical questions tailored to the candidate's expertise and experience level.
- Evaluating candidate responses for relevance, accuracy, and completeness.
- Providing feedback to help candidates refine their answers or proceed to the next step.
- Scoring candidate responses and saving the results for further review.

The chatbot leverages **LangChain's Hugging Face endpoint integration** for prompt-based question generation and response evaluation, ensuring a seamless and intelligent interview process.

---

## Installation Instructions

To set up and run the application locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/hiring-assistant-chatbot.git
   cd hiring-assistant-chatbot
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your Hugging Face API Key:**
   - Replace `"your hugging face api"` in the code with your actual Hugging Face API key.

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application:**
   - Open your browser and navigate to `http://localhost:8501`.

---

## Usage Guide

1. Launch the chatbot by following the installation instructions.
2. Follow the step-by-step prompts to input your details:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position
   - Current Location
   - Tech Stack
3. Answer the technical questions generated based on your profile.
4. Review feedback and proceed to the next question or refine your answers.
5. Once completed, view and save the results, including your average score.

---

## Technical Details

### Libraries Used
- **Streamlit**: For building the interactive user interface.
- **LangChain**: For integrating with Hugging Face's API and handling prompts.
- **HuggingFaceEndpoint**: For leveraging Mistral-7B-Instruct model for NLP tasks.
- **hashlib**: For anonymizing candidate data.
- **re**: For regular expression-based parsing and validation.
- **json**: For saving results in a structured format.
- **os**: For handling file paths and saving results.

### Model Details
- **Model**: `Mistral-7B-Instruct-v0.3` (via Hugging Face endpoint)
- **Parameters**:
  - `max_length=300`
  - `temperature=0.4`

### Architectural Decisions
- **Prompt Engineering**: Designed to extract high-quality, context-aware responses.
- **State Management**: Utilized `st.session_state` for preserving user data and progress across steps.
- **Anonymization**: Used SHA-256 hashing to anonymize candidate data for privacy.

---

## Prompt Design

### Information Gathering
Prompts were crafted to:
- Collect specific candidate details in a friendly and conversational tone.
- Validate responses for completeness before proceeding to the next step.

### Technical Question Generation
The model generates tailored questions based on:
- Candidate's years of experience.
- Desired position.
- Declared tech stack.
- Emphasis on assessing both technical skills and problem-solving abilities.

### Answer Evaluation
Prompts evaluate answers using:
- **Relevance**: Ensures the response aligns with the question intent.
- **Accuracy**: Validates factual correctness.
- **Completeness**: Checks for comprehensive coverage of the question.

---

## Challenges & Solutions

### Challenge 1: Generating Relevant Technical Questions
- **Problem**: Ensuring the model generates context-specific and diverse questions.
- **Solution**: Provided structured and detailed input prompts to guide the model's output.

### Challenge 2: Evaluating Answers Effectively
- **Problem**: Scoring answers accurately across multiple dimensions.
- **Solution**: Engineered a scoring prompt with clear evaluation criteria (relevance, accuracy, completeness) and instructed the model to return only numeric scores.

### Challenge 3: Handling Errors and Failures
- **Problem**: Managing failures in API calls or candidate inputs.
- **Solution**: Implemented error handling with fallback options and default responses to maintain user experience.

---

We hope you find this project useful! Feel free to contribute or provide feedback via the Issues tab on GitHub.

