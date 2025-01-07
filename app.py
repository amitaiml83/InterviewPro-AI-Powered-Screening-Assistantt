import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
import hashlib
import json
import os
import re

# Your Hugging Face API key
api_key = "your api from hugging face "


# Setting up Hugging Face Endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

llm = HuggingFaceEndpoint(
    repo_id=repo_id, 
    temperature=0.4,  # Pass temperature directly
    model_kwargs={
        "max_length": 300,
        "token": api_key
    }
)



# Utility Functions
def anonymize_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

def evaluate_answer(question, answer):
    prompt = f"""
        You are an AI assistant tasked with evaluating a candidate's response to a technical interview question. **Your goal is to provide a score between 0 and 10 based on the following criteria**:

        **1. Relevance (0-3 points)**:
        - Does the answer directly address the question asked?
        - Is the response aligned with the intent of the question?

        **2. Accuracy (0-4 points)**:
        - Is the information factually correct and technically sound?
        - Are there any misconceptions or errors in the explanation?

        **3. Completeness (0-3 points)**:
        - Does the answer sufficiently cover all necessary aspects of the question?
        - Are there any missing components or incomplete explanations?

        **Scoring Breakdown:**
        - 0-3: Poor (Incorrect, irrelevant, or very incomplete)
        - 4-6: Fair (Partially correct, but with notable gaps)
        - 7-8: Good (Mostly correct and covers key points, but minor details missing)
        - 9-10: Excellent (Accurate, complete, and highly relevant)

        **Instructions:**
        - Review the question and answer thoroughly.
        - Provide only the final score in numerical form between 0 and 10, with one decimal point if necessary (e.g., 7.5, 9.0).
        - Do **not** include any explanations, comments, or additional text in your response.
        - **Always return a score and only return the score.** 
        - If you cannot evaluate, return a score of 0.0.
        - The score must be in the format: number (e.g., 7.5 or 9.0).
        
        **Question:** {question}
        **Answer:** {answer}
    """

    response = llm.invoke(prompt)
    # print(response.strip())
    match = re.search(r"(\d+(\.\d+)?)", response)
    if match:
        score = float(match.group(1))
        return score

    # else:
    #     return 0


def check_answer_alignment(question, answer):
    prompt = f"""
    You are an AI assistant evaluating a candidate's answer to a technical interview question. Your task is to assess the relevance, accuracy, and completeness of the candidate's answer, and provide detailed feedback that helps improve their response.
    Question: {question}
    Answer: {answer}

    Please follow these steps:
    1. Review the question and the candidate's answer.
    2. Evaluate the answer based on:
        - **Relevance**: Does the answer address the question properly?
        - **Accuracy**: Is the information in the answer correct and aligned with the question?
        - **Completeness**: Does the answer cover all aspects of the question?
    3. Provide feedback with one of the following:
        - **If the answer is mostly correct**: "Thank you for your response. Your answer is mostly correct and aligns well with the question. You can proceed to the next question."
        - **If the answer is partially correct**: "Thank you for your response. Your answer is partially correct but could use some improvement. Here's a hint to guide you: [Provide specific suggestions to improve the answer]. Please refine your response or proceed to the next question."
        - **If the answer is incorrect**: "Thank you for your response. It's a good attempt, but the answer is not correct. Here's a hint to help you improve: [Provide suggestions to correct or enhance the answer]. Please refine your response or proceed to the next question."
    
    Provide professional and constructive feedback to encourage the candidate's improvement or help them proceed confidently to the next step."""

    try:
        response = llm.invoke(prompt)
        return response.strip().lower()
    except Exception:
        return "yes"  # Default to yes if there's an error

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.candidate_data = {}
    st.session_state.questions = []
    st.session_state.responses = []
    st.session_state.scores = []  # List to store individual question scores
    st.session_state.error_message = ""
    st.session_state.continue_anyway = False
    st.session_state.current_question_index = 0

# Sidebar Navigation
st.sidebar.title("TalentScout Hiring Assistant")
st.sidebar.markdown("### Steps")
steps = [
    "Full Name", "Email Address", "Phone Number",
    "Years of Experience", "Desired Position(s)",
    "Current Location", "Tech Stack", "Questions"
]

# Display steps in sidebar with the current step highlighted
for i, step in enumerate(steps):
    if st.session_state.step == i + 1:
        st.sidebar.markdown(f"**{step}** (Current Step)")
    else:
        st.sidebar.markdown(step)


# Main UI
st.title("TalentScout Hiring Assistant")
# st.write("Welcome to TalentScout!")

# Greeting and Introduction
greeting_prompt = """
Hello and welcome! 👋 I'm your TalentScout Assistant, here to guide you through the screening process. I’ll ask you a few questions to gather some basic information and evaluate your technical skills. This is a great opportunity for you to showcase your abilities and experience.

Let’s get started! 😊 If you need any assistance, feel free to ask.
"""

# Displaying greeting message
st.write(greeting_prompt)

# Progress Bar
progress = (st.session_state.step - 1) / len(steps)
st.progress(progress)

# Form Input Fields with interactive prompts
if st.session_state.step == 1:
    # st.header("Full Name")
    full_name_prompt = """
    Let's start with your full name. What's your name? 😊
    """
    full_name = st.text_input(full_name_prompt)

    # Replacing "Next Step" button with "Send" button
    if full_name and st.button("Send ➡️"):
        st.session_state.candidate_data["name"] = anonymize_data(full_name)
        st.session_state.step += 1
        st.write(f"Thank you, {full_name}! welcome {full_name} and Let's move to the question.")


elif st.session_state.step == 2:
    # st.header("Email Address")
    email_prompt = """
    Great! Now, could you please share your email address? 📧 This will help us contact you if needed.
    """
    email = st.text_input(email_prompt)

    # Replacing "Next Step" button with "Send" button
    if email and st.button("Send ➡️"):
        st.session_state.candidate_data["email"] = anonymize_data(email)
        st.session_state.step += 1
        st.write(f"Got it! We've recorded your email as {email} for further update. Next, let's move on.")


elif st.session_state.step == 3:
    # st.header("Phone Number")
    phone_prompt = """
    Next, could you please provide your phone number? 📱 It's optional, but it would be helpful in case we need to reach you quickly.
    """
    phone = st.text_input(phone_prompt)

    # Replacing "Next Step" button with "Send" button
    if phone and st.button("Send ➡️"):
        st.session_state.candidate_data["phone"] = anonymize_data(phone)
        st.session_state.step += 1
        st.write(f"Thanks! We've noted your phone number as {phone} for futher communication. Moving on!")


elif st.session_state.step == 4:
    # st.header("Step 4: Years of Experience")
    experience_prompt = """
    How many years of professional experience do you have? 🧑‍💻 Please enter a number (e.g., 3 years).
    """
    experience = st.number_input(experience_prompt, min_value=0, max_value=50, step=1)

    # Replacing "Next Step" button with "Send" button
    if experience and st.button("Send ➡️"):
        st.session_state.candidate_data["experience"] = experience
        st.session_state.step += 1
        st.write(f"Got it! You have {experience} years of experience wonderfull. Let's continue.")


elif st.session_state.step == 5:
    # st.header("Step 5: Desired Position(s)")
    position_prompt = """
    What position(s) are you applying for? Feel free to mention one or more roles you’re interested in. 🧐
    """
    position = st.text_input(position_prompt)

    # Replacing "Next Step" button with "Send" button
    if position and st.button("Send ➡️"):
        st.session_state.candidate_data["position"] = position
        st.session_state.step += 1
        st.write(f"Thank you! You've applied for the {position} position. Let's move to the next.")


elif st.session_state.step == 6:
    # st.header("Step 6: Current Location")
    location_prompt = """
    Where are you currently located? 🌍 Knowing your location helps us with scheduling and potential relocation needs.
    """
    location = st.text_input(location_prompt)

    # Replacing "Next Step" button with "Send" button
    if location and st.button("Send ➡️"):
        st.session_state.candidate_data["location"] = location
        st.session_state.step += 1
        st.write(f"Thanks! We have your location as {location}. We're almost done!")


elif st.session_state.step == 7:
    # st.header("Step 7: Tech Stack")
    tech_stack_prompt = """
    Finally, let's talk about your tech stack! 💻 What technologies do you specialize in? Please list them (e.g., Python, Django, SQL).
    """
    tech_stack = st.text_area(tech_stack_prompt)

    # Replacing "Next Step" button with "Send" button
    if tech_stack and st.button("Send ➡️"):
        st.session_state.candidate_data["tech_stack"] = tech_stack
        st.session_state.step += 1
        st.write(f"Awesome! You've listed your tech stack as {tech_stack}. You're all set! just give answer of few question to complete the screening round.")




# Generate and Display Questions
elif st.session_state.step == 8:
    st.header("Step 8: Technical Questions")
    if not st.session_state.questions:
        tech_stack = st.session_state.candidate_data['tech_stack']
        Years_of_Experience = st.session_state.candidate_data['experience'] 
        Desired_Position = st.session_state.candidate_data['position']

        prompt = f"""
        You are an expert technical recruiter. Your task is to assess a candidate's technical skills and work experience.

        Candidate Details:
        - Years of Experience: {Years_of_Experience} years
        - Desired Position: {Desired_Position}
        - Tech Stack: {tech_stack}

        Follow these rules:
        - Do not include the name of the technology in the question itself.
        - Directly generate technical questions related to the candidate's specified technologies, based on their experience level and desired position.
        - The questions should be specific to the technologies they have experience with.
        - Each question should be a standalone prompt.

        **Generate only 3 technical questions tailored to assess the candidate’s proficiency based on their tech stack, years of experience, and desired position.**
        """

        try:
            response = llm.invoke(prompt)
            st.session_state.questions = [q.strip() for q in response.split("\n") if q.strip()]
        except Exception as e:
            st.error("Failed to generate questions. Please try again later.")
            st.stop()
  # Stop execution if no questions are available

    index = st.session_state.current_question_index
    
    if index < len(st.session_state.questions):
        question = st.session_state.questions[index]
        st.subheader(f"Question {index + 1}")
        st.write(question)
        response = st.text_area("Your Answer", key=f"response_{index}")
        
        # "Next Question" button handling
        if st.button("Next Question"):
            if response.strip():
                alignment_result = check_answer_alignment(question, response)
                score = evaluate_answer(question, response)
                print(score)
                if "your answer is mostly correct and aligns well with the question" in alignment_result:
                    st.success("Great! Your answer aligns with the question.")
                    st.write(alignment_result)
                    st.session_state.scores.append(score)
                    st.session_state.responses.append(response)
                    st.session_state.current_question_index += 1
                elif "your answer is partially correct but could use some improvement." in alignment_result:
                    st.success("Great! Your answer is partically correct")
                    st.write(alignment_result)
                    st.session_state.scores.append(score)
                    st.session_state.responses.append(response)
                    st.session_state.current_question_index += 1  
                else:
                    st.warning(f"Your answer may not be fully aligned: {alignment_result}")
                    st.session_state.scores.append(score)
                    st.session_state.error_message = "Your answer is not aligned. Use 'Continue Anyway' if you'd like to proceed."

        # "Continue Anyway" button handling
        if st.session_state.error_message:
            if st.button("Continue Anyway"):
                st.session_state.responses.append(response)
                st.session_state.current_question_index += 1
                st.session_state.error_message = ""  # Clear the error message
    else:
        st.success("Thank you for completing the questionnaire!")
        
        # Calculate the average score
        # Ensure that only valid scores (non-None) are included in the sum
        valid_scores = [score for score in st.session_state.scores if score is not None]

        if valid_scores:
            average_score = sum(valid_scores) / len(valid_scores)
        else:
            average_score = 0  # Default value if there are no valid scores

        # Now, average_score will be calculated safely

        # average_score = sum(st.session_state.scores) / len(st.session_state.scores) if st.session_state.scores else 0
        # Prepare the data to save
        candidate_name = st.session_state.candidate_data.get("name", "unknown_candidate")
        question_answer_data = {}
        for i, question in enumerate(st.session_state.questions):
            question_answer_data[f"Q{i+1}"] = {
                "question": question,
                "answer": st.session_state.responses[i],
                "score":st.session_state.scores[i]
            }
                # Add average score
        question_answer_data["average_score"] = average_score

        # Convert to JSON and save the file
        file_name = f"{candidate_name}.json"  # Using candidate's anonymized name as filename
        file_path = os.path.join(os.getcwd(), file_name)  # Save to current working directory

        try:
            with open(file_path, 'w') as json_file:
                json.dump(question_answer_data, json_file, indent=4)
            st.success(f"Your responses have been saved as {file_name}")
        except Exception as e:
            st.error(f"Failed to save the file: {e}")

        # Display the responses
        # st.write("Your Responses:")
        # for i, answer in enumerate(st.session_state.responses):
        #     st.write(f"**Q{i + 1}:** {st.session_state.questions[i]}")
        #     st.write(f"**Answer:** {answer}")
        st.write(f"**Average score:** {average_score}/10")
        conclude_prompt="""Thank you for your time and effort today! 🙏 It was great getting to know more about you and your skills. 
        We appreciate your responses and will review your answers carefully.Our team will reach out to you with the next steps in the hiring process soon. 
        If you have any further questions or need additional information, feel free to contact us.
        Best of luck, and we hope to speak with you again soon! 😊"""
        st.write(conclude_prompt)
