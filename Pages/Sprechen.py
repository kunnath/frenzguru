import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
from datetime import datetime
from feedback import analyze_speech  # Hypothetical speech analysis function

# --- Page Config ---
st.set_page_config(
    page_title="B1 Sprechen Practice | DeutschFit",
    page_icon="🗣️"
)

# --- Constants ---
AUDIO_DIR = "speaking_samples"
os.makedirs(AUDIO_DIR, exist_ok=True)

# B1 Speaking Tasks (simulating telc/Goethe format)
TASKS = [
    {
        "id": 1,
        "type": "Self-introduction",
        "prompt": "Stellen Sie sich vor. (Name, Alter, Herkunft, Beruf, Hobbys)",
        "time": 2,  # minutes
        "tips": ["Use complete sentences", "Include 4-5 pieces of information"]
    },
    {
        "id": 2,
        "type": "Everyday Conversation",
        "prompt": "Sie möchten mit einem Kollegen Pause machen. Vereinbaren Sie einen Termin.",
        "time": 3,
        "tips": ["Suggest a time/place", "React to partner's input", "Use phrases like 'Wie wäre es mit...?'"]
    },
    {
        "id": 3,
        "type": "Discussion",
        "prompt": "Sie planen einen Ausflug mit einem Freund. Diskutieren Sie: Wohin? Wann? Was machen Sie?",
        "time": 4,
        "tips": ["Give opinions", "Make suggestions", "Use connectors (z.B. 'deshalb', 'trotzdem')"]
    }
]

# --- Session State ---
if "current_task" not in st.session_state:
    st.session_state.current_task = 0
    st.session_state.recordings = {}
    st.session_state.show_feedback = False

# --- Audio Handling ---
def save_audio(audio_bytes, task_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"task_{task_id}_{timestamp}.wav"
    path = os.path.join(AUDIO_DIR, filename)
    
    with open(path, "wb") as f:
        f.write(audio_bytes)
    
    return path

# --- Task Display ---
st.title("🗣️ B1 Sprechen Practice")
st.markdown("""
Practice the speaking section of the **telc B1 exam**.  
You'll complete 3 tasks: introduction, conversation, and discussion.
""")

# --- Current Task ---
if st.session_state.current_task < len(TASKS):
    task = TASKS[st.session_state.current_task]
    
    st.subheader(f"Aufgabe {task['id']}: {task['type']}")
    st.markdown(f"**{task['prompt']}**")
    
    # Timer and tips
    with st.expander("💡 Tips & Time Limit"):
        st.markdown(f"⏱️ **{task['time']} minutes**")
        for tip in task["tips"]:
            st.write(f"- {tip}")
    
    # Audio recorder
    st.markdown("## 🎤 Your Recording")
    audio_bytes = audio_recorder(
        energy_threshold=(-1.0, 1.0),
        pause_threshold=3.0,
        key=f"recorder_{task['id']}"
    )
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        # Save recording
        if st.button("Save Recording", key=f"save_{task['id']}"):
            audio_path = save_audio(audio_bytes, task["id"])
            st.session_state.recordings[task["id"]] = audio_path
            st.success("Recording saved!")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Feedback", disabled=task["id"] not in st.session_state.recordings):
            st.session_state.show_feedback = True
    with col2:
        if st.session_state.current_task < len(TASKS) - 1:
            if st.button("Next Task"):
                st.session_state.current_task += 1
                st.session_state.show_feedback = False
                st.rerun()
    
    # Feedback section
    if st.session_state.show_feedback and task["id"] in st.session_state.recordings:
        st.markdown("---")
        st.subheader("📝 Feedback")
        
        with st.spinner("Analyzing your speech..."):
            # Hypothetical analysis
            feedback = analyze_speech(st.session_state.recordings[task["id"]])
            
            st.markdown("### 🎯 Pronunciation")
            st.write(feedback.get("pronunciation", "No pronunciation feedback available"))
            
            st.markdown("### 📖 Vocabulary")
            st.write(feedback.get("vocabulary", "No vocabulary feedback available"))
            
            st.markdown("### 🔍 Grammar")
            st.write(feedback.get("grammar", "No grammar feedback available"))
            
            st.markdown("### 💬 Fluency")
            st.write(feedback.get("fluency", "No fluency feedback available"))

# --- All tasks completed ---
else:
    st.success("🎉 Congratulations! You've completed all speaking tasks.")
    if st.button("Start Again"):
        st.session_state.current_task = 0
        st.session_state.recordings = {}
        st.session_state.show_feedback = False
        st.rerun()

# --- B1 Speaking Tips ---
st.markdown("---")
st.subheader("📚 B1 Speaking Exam Tips")
st.markdown("""
1. **Speak clearly** - Moderate pace, good pronunciation  
2. **Use complete sentences** - Avoid one-word answers  
3. **Show variety** - Demonstrate B1 vocabulary/grammar  
4. **Ask questions** - Essential for conversation tasks  
5. **Don't panic** - If stuck, say: *"Können Sie das bitte wiederholen?"*  
""")

# --- Sample Responses (Expandable) ---
with st.expander("📋 Sample Responses"):
    st.markdown("""
    **Task 1 (Introduction):**  
    *"Guten Tag! Ich heiße Anna Müller. Ich bin 28 Jahre alt und komme aus Österreich. 
    Von Beruf bin ich Krankenschwester. In meiner Freizeit lese ich gern und mache Yoga."*

    **Task 2 (Making Plans):**  
    *"Hallo Thomas! Wie wäre es mit einer Pause um 11 Uhr? Wir könnten in die Cafeteria gehen. 
    Was meinst du?"*

    **Task 3 (Discussion):**  
    *"Lass uns am Wochenende einen Ausflug machen! Ich möchte gern ins Museum gehen. 
    Wann hast du Zeit? Samstag oder Sonntag?"*
    """)