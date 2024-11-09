import streamlit as st
import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import json
import numpy as np
import math
import re
from datetime import datetime
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize ChromaDB
chroma_client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collections for different subjects
subjects = ["mathematics", "physics", "chemistry"]
collections = {}
for subject in subjects:
    collections[subject] = chroma_client.get_or_create_collection(
        name=f"stem_{subject}",
        embedding_function=embedding_function
    )

class STEMTutor:
    def __init__(self):
        self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        self.current_level = "Beginner"
        self.subjects = subjects
        self.success_rate = {}
        
    def analyze_question(self, question):
        """Analyze question to determine subject and complexity"""
        prompt = f"""Analyze this STEM question and provide:
        1. The subject (mathematics, physics, or chemistry)
        2. The difficulty level (Beginner, Intermediate, or Advanced)
        3. The key concepts involved
        4. Any formulas that might be relevant

        Question: {question}
        
        Provide the response in JSON format with keys: subject, difficulty, concepts, formulas"""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        try:
            analysis = json.loads(completion.choices[0].message.content)
            return analysis
        except:
            return {
                "subject": "mathematics",
                "difficulty": "Beginner",
                "concepts": [],
                "formulas": []
            }

    def generate_solution(self, question, similar_problems, student_level):
        """Generate detailed solution with step-by-step explanation"""
        prompt = f"""As a STEM tutor, provide a detailed solution to this problem. The student's level is {student_level}.

        Question: {question}

        Similar problems and solutions for reference:
        {similar_problems}

        Please provide:
        1. Initial approach explanation
        2. Step-by-step solution
        3. Key concepts used
        4. Common mistakes to avoid
        5. Practice suggestions
        
        Make the explanation clear and appropriate for a {student_level} level student."""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2000
        )
        
        return completion.choices[0].message.content

    def generate_practice_problem(self, concepts, level):
        """Generate similar practice problem"""
        prompt = f"""Create a new STEM practice problem that:
        1. Covers these concepts: {', '.join(concepts)}
        2. Is appropriate for {level} level
        3. Has a clear solution
        
        Provide the problem and its solution."""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content

    def update_student_level(self, subject, success):
        """Update student's level based on performance"""
        if subject not in self.success_rate:
            self.success_rate[subject] = []
        
        self.success_rate[subject].append(success)
        
        # Calculate recent performance
        recent_rate = np.mean(self.success_rate[subject][-5:])
        
        current_index = self.difficulty_levels.index(self.current_level)
        if recent_rate > 0.8 and current_index < len(self.difficulty_levels) - 1:
            self.current_level = self.difficulty_levels[current_index + 1]
        elif recent_rate < 0.3 and current_index > 0:
            self.current_level = self.difficulty_levels[current_index - 1]

def main():
    st.set_page_config(page_title="Adaptive STEM Tutor", page_icon="🔬", layout="wide")
    
    # Initialize session state
    if 'tutor' not in st.session_state:
        st.session_state.tutor = STEMTutor()
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.title("🔬 Adaptive STEM Tutor")
    
    # Sidebar for analytics and history
    with st.sidebar:
        st.header("Learning Analytics")
        
        if st.session_state.history:
            # Create DataFrame for visualization
            df = pd.DataFrame(st.session_state.history)
            
            # Subject distribution
            st.subheader("Subject Distribution")
            fig = px.pie(df, names='subject')
            st.plotly_chart(fig)
            
            # Difficulty progression
            st.subheader("Difficulty Progression")
            fig = px.line(df, x=df.index, y='difficulty', 
                         title="Learning Progression")
            st.plotly_chart(fig)
    
    # Main area for problem solving
    st.header("Problem Solving Assistant")
    
    # Question input
    question = st.text_area("Enter your STEM question:", height=100)
    
    if st.button("Get Help"):
        if question:
            with st.spinner("Analyzing question..."):
                # Analyze question
                analysis = st.session_state.tutor.analyze_question(question)
                
                # Store in history
                st.session_state.history.append({
                    'timestamp': datetime.now(),
                    'question': question,
                    'subject': analysis['subject'],
                    'difficulty': analysis['difficulty']
                })
                
                # Display analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Question Analysis")
                    st.write(f"**Subject:** {analysis['subject'].title()}")
                    st.write(f"**Difficulty:** {analysis['difficulty']}")
                    st.write("**Key Concepts:**")
                    for concept in analysis['concepts']:
                        st.write(f"- {concept}")
                
                with col2:
                    st.markdown("### Relevant Formulas")
                    for formula in analysis['formulas']:
                        st.latex(formula)
                
                # Retrieve similar problems
                collection = collections[analysis['subject']]
                results = collection.query(
                    query_texts=[question],
                    n_results=3
                )
                
                # Generate solution
                with st.spinner("Generating detailed solution..."):
                    solution = st.session_state.tutor.generate_solution(
                        question,
                        results['documents'][0] if results['documents'] else [],
                        st.session_state.tutor.current_level
                    )
                    
                    st.markdown("### Detailed Solution")
                    st.write(solution)
                
                # Generate practice problem
                if st.button("Generate Similar Practice Problem"):
                    with st.spinner("Generating practice problem..."):
                        practice = st.session_state.tutor.generate_practice_problem(
                            analysis['concepts'],
                            st.session_state.tutor.current_level
                        )
                        st.markdown("### Practice Problem")
                        st.write(practice)
                
                # Feedback and level adjustment
                st.markdown("### Did this solution help you?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, I understand"):
                        st.session_state.tutor.update_student_level(
                            analysis['subject'],
                            True
                        )
                        st.success("Great! Keep up the good work!")
                with col2:
                    if st.button("No, I need more help"):
                        st.session_state.tutor.update_student_level(
                            analysis['subject'],
                            False
                        )
                        st.info("Let's try a simpler explanation...")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()