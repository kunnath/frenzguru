import streamlit as st
import time
from feedback import get_writing_feedback, format_feedback

# --- Page Config ---
st.set_page_config(
    page_title="B1 Schreiben Practice | DeutschFit",
    page_icon="✍️"
)

# --- Session State (Save user progress) ---
if "writing_score" not in st.session_state:
    st.session_state.writing_score = 0

# --- Constants ---
TASK_TIME_LIMIT = 900  # 15 minutes in seconds
TASK_EXAMPLE = """
**Aufgabe:**  
Sie haben eine Einladung von Ihrer Freundin Anna bekommen. Schreiben Sie eine E-Mail (80–100 Wörter):
- Dank für die Einladung  
- Ihre Meinung zum Ausflug  
- Fragen zum Treffpunkt  
"""

# --- Timer Function ---
def run_timer(seconds):
    timer_placeholder = st.empty()
    while seconds > 0 and st.session_state.timer_running:
        mins, secs = divmod(seconds, 60)
        timer_placeholder.markdown(
            f"⏳ **Time remaining:** {mins:02d}:{secs:02d}"
        )
        time.sleep(1)
        seconds -= 1
    if seconds <= 0:
        st.session_state.timer_running = False
        timer_placeholder.error("⏰ Time's up! Submit your response now.")

# --- Task Display ---
st.title("✍️ B1 Schreiben Practice")
st.markdown("""
Practice the writing section of the **telc B1 exam**.  
You'll have **15 minutes** to complete each task.
""")

# --- Start Task ---
if st.button("Start New Task"):
    st.session_state.timer_running = True
    st.session_state.task_started = True
    st.session_state.user_text = ""

# --- Task in Progress ---
if st.session_state.get("task_started"):
    st.markdown("### 📝 Aufgabe")
    st.markdown(TASK_EXAMPLE)
    
    # Timer
    run_timer(TASK_TIME_LIMIT)
    
    # Text input
    user_text = st.text_area(
        "Write your response here (80–100 words):",
        height=300,
        key="user_text"
    )
    
    # Submit button
    if st.button("Submit", type="primary"):
        st.session_state.timer_running = False
        
        # --- AI Feedback ---
        st.markdown("---")
        st.subheader("🔍 Your Feedback")
        
        if len(user_text.split()) < 60:
            st.warning("⚠️ Your text is too short (aim for 80–100 words).")
        else:
            # Analyze with feedback.py
            feedback = get_writing_feedback(user_text)
            st.markdown(format_feedback(feedback))
            
            # Score calculation (simplified)
            st.session_state.writing_score = min(
                len(user_text.split()) / 100 * 15, 15
            )  # Max 15 points like telc
            st.success(f"📊 **Estimated Score:** {st.session_state.writing_score:.1f}/15")

# --- How to Improve Section ---
st.markdown("---")
st.subheader("💡 B1 Writing Tips")
st.markdown("""
1. **Structure your text** (Greeting → Main Part → Closing).  
2. **Use connectors**: *deshalb, trotzdem, außerdem*.  
3. **Avoid repetition**: Use synonyms (e.g., *finden* → *meinen*).  
4. **Check cases**: Remember *wegen + Genitiv* (wegen des Wetters).  
""")

# --- Reset (Debug) ---
if st.sidebar.button("Reset Session"):
    st.session_state.clear()