

# [Previous classes remain the same as in the previous implementation]
# [Copy all the previous classes: AITeachingAssistantConfig, StudentProfile, 
#  SocraticQuestionGenerator, CodeDebugAssistant, RealWorldExampleMapper, 
#  AITeachingAssistant from the previous artifact]

import streamlit as st
import json
import os
from typing import Dict, Any


from ai_teaching_assistant import (
    AITeachingAssistantConfig, 
    AITeachingAssistant, 
    CodeDebugAssistant, 
    RealWorldExampleMapper, 
    SocraticQuestionGenerator
)



# Streamlit Configuration
st.set_page_config(
    page_title="AI DSA Learning Assistant",
    page_icon="🧠",
    layout="wide"
)

class StreamlitTeachingAssistantApp:
    def __init__(self):
        # Initialize session state variables
        if 'assistant' not in st.session_state:
            # Use environment variable or placeholder for API key
            api_key = os.getenv('GOOGLE_AI_API_KEY', 'AIzaSyDEgkuRHWmrNbA77dpSgj0rbcPAU2yw8B0')
            config = AITeachingAssistantConfig(api_key=api_key)
            st.session_state.assistant = AITeachingAssistant(config)
        
        if 'student_initialized' not in st.session_state:
            st.session_state.student_initialized = False
        
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []

    def render_sidebar(self):
        """Render the sidebar for student profile configuration"""
        st.sidebar.title("🎓 Student Profile")
        
        # Student Name Input
        student_name = st.sidebar.text_input("Your Name", key="student_name")
        
        # Learning Topic Selection
        topics = [
            'Fundamental Data Structures', 
            'Advanced Graph Algorithms', 
            'Sorting Algorithms', 
            'Dynamic Programming', 
            'Tree Traversals'
        ]
        current_topic = st.sidebar.selectbox("Select Learning Topic", topics)
        
        # Difficulty Level
        difficulty = st.sidebar.radio(
            "Difficulty Level", 
            ['beginner', 'intermediate', 'advanced']
        )
        
        # Learning Style
        learning_style = st.sidebar.radio(
            "Preferred Learning Style", 
            ['visual', 'textual', 'interactive']
        )
        
        # Initialize Student Button
        if st.sidebar.button("Initialize Student Profile"):
            if student_name:
                st.session_state.assistant.initialize_student(
                    name=student_name, 
                    initial_topic=current_topic
                )
                st.session_state.student_profile = {
                    'name': student_name,
                    'topic': current_topic,
                    'difficulty': difficulty,
                    'learning_style': learning_style
                }
                st.session_state.student_initialized = True
                st.sidebar.success(f"Profile created for {student_name}!")
            else:
                st.sidebar.error("Please enter a student name.")

    def generate_question(self):
        """Generate a personalized question"""
        if st.session_state.student_initialized:
            question = st.session_state.assistant.generate_personalized_question(
                st.session_state.student_profile['topic']
            )
            st.session_state.conversation_history.append({
                'type': 'question', 
                'content': question
            })
            return question
        return "Please initialize your student profile first."

    def process_response(self, response: str):
        """Process student's response and generate feedback"""
        if st.session_state.student_initialized:
            evaluation = st.session_state.assistant.process_student_response(response)
            st.session_state.conversation_history.append({
                'type': 'response', 
                'content': response
            })
            st.session_state.conversation_history.append({
                'type': 'evaluation', 
                'content': evaluation
            })
            return evaluation
        return {"error": "Student profile not initialized"}

    def code_debugging_section(self):
        """Code debugging interface"""
        st.header("🐞 Code Debugging Assistant")
        
        code_input = st.text_area("Paste your code here:", height=300)
        
        language = st.selectbox(
            "Select Programming Language", 
            ['python', 'javascript', 'java', 'cpp']
        )
        
        if st.button("Analyze Code"):
            if code_input:
                debug_analysis = CodeDebugAssistant.analyze_code(code_input, language)
                st.json(debug_analysis)
                
                # Highlight key debugging insights
                st.subheader("Learning Opportunities")
                for opportunity in debug_analysis.get('learning_opportunities', []):
                    st.info(opportunity)

    def real_world_examples_section(self):
        """Generate real-world analogies for DSA concepts"""
        st.header("🌍 Real-World DSA Analogies")
        
        concepts = [
            'Graph Algorithms', 
            'Sorting Algorithms', 
            'Dynamic Programming', 
            'Tree Structures', 
            'Hash Tables'
        ]
        
        selected_concept = st.selectbox("Choose a DSA Concept", concepts)
        
        if st.button("Generate Analogy"):
            analogy = RealWorldExampleMapper.generate_analogy(selected_concept)
            st.write(analogy)

    def main_app(self):
        """Main Streamlit application layout"""
        st.title("🤖 AI Data Structures & Algorithms Learning Assistant")
        
        # Sidebar for student profile
        self.render_sidebar()
        
        # Main content area with tabs
        tab1, tab2, tab3 = st.tabs([
            "Interactive Learning", 
            "Code Debugging", 
            "Real-World Analogies"
        ])
        
        with tab1:
            st.header("Personalized Learning Journey")
            
            # Question Generation
            if st.button("Generate Question"):
                question = self.generate_question()
                st.write(question)
            
            # Response Input
            student_response = st.text_area("Your Response:")
            
            if st.button("Submit Response"):
                if student_response:
                    evaluation = self.process_response(student_response)
                    
                    # Display evaluation
                    st.subheader("Response Evaluation")
                    st.json(evaluation)
                    
                    # Display follow-up Socratic questions
                    st.subheader("Probing Questions")
                    for q in evaluation.get('next_questions', []):
                        st.info(q)
        
        with tab2:
            self.code_debugging_section()
        
        with tab3:
            self.real_world_examples_section()

    def run(self):
        """Run the Streamlit application"""
        self.main_app()

def main():
    app = StreamlitTeachingAssistantApp()
    app.run()

if __name__ == "__main__":
    main()

# Additional requirements.txt content:
# streamlit
# google-generativeai
# langchain
# python-dotenv  # For environment variable management