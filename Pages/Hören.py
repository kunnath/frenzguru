import streamlit as st
import time
from audio_recorder_streamlit import audio_recorder
import os
from feedback import analyze_speech  # Hypothetical speaking analysis function

# --- Page Config ---
st.set_page_config(
    page_title="B1 Hören Practice | DeutschFit",
    page_icon="👂"
)

# --- Constants ---
AUDIO_DIR = "audio_samples"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Sample listening tasks (replace with your own audio files)
TASKS = [
    {
        "id": 1,
        "title": "Task 1: Short Conversations",
        "audio_file": "hören_task1.mp3",
        "questions": [
            {
                "text": "Wo will die Frau hin?",
                "options": ["a) Zum Bahnhof", "b) Zum Supermarkt", "c) Zur Apotheke"],
                "answer": "a"
            },
            {
                "text": "Wann fährt der nächste Bus?",
                "options": ["a) In 5 Minuten", "b) In 10 Minuten", "c) In 20 Minuten"],
                "answer": "b"
            }
        ]
    },
    {
        "id": 2,
        "title": "Task 2: Radio Announcement",
        "audio_file": "hören_task2.mp3",
        "questions": [
            {
                "text": "Was wird im Radio angekündigt?",
                "options": ["a) Ein Konzert", "b) Eine Ausstellung", "c) Ein Sportevent"],
                "answer": "c"
            }
        ]
    }
]

# --- Session State ---
if "current_task" not in st.session_state:
    st.session_state.current_task = 0
    st.session_state.user_answers = {}
    st.session_state.show_results = False

# --- Audio Player ---
def play_audio(audio_file):
    audio_path = os.path.join(AUDIO_DIR, audio_file)
    if os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mp3")
    else:
        st.warning("Audio file not found. Using placeholder.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# --- Task Display ---
st.title("👂 B1 Hören Practice")
st.markdown("""
Practice the listening section of the **telc B1 exam**.  
Listen to each audio clip and answer the questions.
""")

# --- Task Navigation ---
if st.session_state.current_task < len(TASKS):
    task = TASKS[st.session_state.current_task]
    
    st.subheader(task["title"])
    play_audio(task["audio_file"])
    
    # Display questions
    for i, question in enumerate(task["questions"]):
        st.markdown(f"**{i+1}. {question['text']}**")
        user_answer = st.radio(
            f"Select your answer for question {i+1}:",
            question["options"],
            key=f"task_{task['id']}_q_{i}",
            index=None
        )
        st.session_state.user_answers[f"task_{task['id']}_q_{i}"] = user_answer
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answers"):
            st.session_state.show_results = True
    with col2:
        if st.session_state.current_task < len(TASKS) - 1:
            if st.button("Next Task"):
                st.session_state.current_task += 1
                st.session_state.show_results = False
                st.rerun()
    
    # Show results if submitted
    if st.session_state.show_results:
        st.markdown("---")
        st.subheader("📝 Your Answers")
        correct_count = 0
        
        for i, question in enumerate(task["questions"]):
            user_answer = st.session_state.user_answers.get(f"task_{task['id']}_q_{i}")
            correct_answer = question["answer"]
            
            # Determine which option letter the user selected
            user_choice = None
            if user_answer:
                user_choice = user_answer[0]  # Gets the 'a', 'b', or 'c' from the selected option
            
            if user_choice == correct_answer:
                st.success(f"✅ Question {i+1}: Correct! ({user_answer})")
                correct_count += 1
            else:
                st.error(f"❌ Question {i+1}: Incorrect. You chose {user_answer}. Correct answer was: {correct_answer})")
        
        # Calculate score
        score = (correct_count / len(task["questions"])) * 15  # Scale to 15 points like telc
        st.metric("Your Score", f"{score:.1f}/15")
        
        # Speaking practice extension
        st.markdown("---")
        st.subheader("💬 Speaking Practice")
        st.markdown("Try repeating what you heard to practice pronunciation:")
        
        recorded_audio = audio_recorder("Press to record", key=f"recorder_{task['id']}")
        if recorded_audio:
            st.audio(recorded_audio, format="audio/wav")
            if st.button("Analyze Pronunciation"):
                with st.spinner("Analyzing your speech..."):
                    feedback = analyze_speech(recorded_audio)  # Hypothetical function
                    st.markdown(f"**Feedback:** {feedback}")
else:
    st.success("🎉 You've completed all listening tasks!")
    if st.button("Restart"):
        st.session_state.current_task = 0
        st.session_state.user_answers = {}
        st.session_state.show_results = False
        st.rerun()

# --- Exam Tips Section ---
st.markdown("---")
st.subheader("📚 B1 Listening Tips")
st.markdown("""
1. **Read questions first** - Scan them before listening  
2. **Focus on keywords** - Dates, locations, numbers  
3. **Don't panic** if you miss something - Keep listening  
4. **Practice daily** with German podcasts/news  
""")