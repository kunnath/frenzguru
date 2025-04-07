import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# --- Page Config ---
st.set_page_config(
    page_title="Your Progress | DeutschFit",
    page_icon="📊"
)

# --- Constants ---
PROGRESS_FILE = "user_progress.json"

# --- Initialize Progress Data ---
def init_progress():
    return {
        "user_info": {
            "name": "",
            "target_exam_date": ""
        },
        "scores": {
            "Hören": [],
            "Lesen": [],
            "Schreiben": [],
            "Sprechen": []
        },
        "attempts": 0,
        "last_updated": ""
    }

# --- Load/Save Progress ---
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return init_progress()

def save_progress(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Update Progress ---
def update_score(section, score):
    progress_data = load_progress()
    progress_data["scores"][section].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "score": score,
        "max_score": 15  # telc B1 scale
    })
    progress_data["attempts"] += 1
    save_progress(progress_data)

# --- Page Content ---
st.title("📊 Your B1 Exam Progress")
st.markdown("Track your performance across all exam sections over time.")

# --- User Info Form ---
with st.expander("✏️ Update Your Profile"):
    progress_data = load_progress()
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", 
                           value=progress_data["user_info"]["name"])
    with col2:
        exam_date = st.date_input("Target Exam Date",
                                 value=datetime.strptime(progress_data["user_info"]["target_exam_date"], "%Y-%m-%d") 
                                 if progress_data["user_info"]["target_exam_date"] else datetime.now())
    
    if st.button("Save Profile"):
        progress_data["user_info"]["name"] = name
        progress_data["user_info"]["target_exam_date"] = exam_date.strftime("%Y-%m-%d")
        save_progress(progress_data)
        st.success("Profile updated!")

# --- Progress Dashboard ---
progress_data = load_progress()

if not progress_data["scores"]["Hören"]:
    st.info("ℹ️ Complete practice tasks to see your progress data")
else:
    # --- Metrics ---
    st.subheader("📈 Overview")
    cols = st.columns(4)
    sections = ["Hören", "Lesen", "Schreiben", "Sprechen"]
    
    for i, section in enumerate(sections):
        if progress_data["scores"][section]:
            last_score = progress_data["scores"][section][-1]["score"]
            cols[i].metric(
                label=f"{section} Score",
                value=f"{last_score}/15",
                delta=f"{(last_score/15*100):.1f}%"
            )

    # --- Progress Chart ---
    st.subheader("📅 Progress Over Time")
    
    # Prepare DataFrame for visualization
    chart_data = []
    for section in sections:
        for attempt in progress_data["scores"][section]:
            chart_data.append({
                "Date": attempt["date"],
                "Section": section,
                "Score": attempt["score"],
                "Percentage": (attempt["score"]/15)*100
            })
    
    df = pd.DataFrame(chart_data)
    
    if not df.empty:
        fig = px.line(
            df,
            x="Date",
            y="Percentage",
            color="Section",
            markers=True,
            title="Your Exam Section Performance",
            labels={"Percentage": "Score (%)"},
            height=400
        )
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No progress data available yet")

    # --- Section Breakdown ---
    st.subheader("🔍 Section Analysis")
    selected_section = st.selectbox("Select section to analyze", sections)
    
    if progress_data["scores"][selected_section]:
        section_df = pd.DataFrame(progress_data["scores"][selected_section])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Score History**")
            st.dataframe(
                section_df[["date", "score"]].rename(
                    columns={"date": "Date", "score": "Score"}
                ),
                hide_index=True
            )
        
        with col2:
            st.markdown("**Statistics**")
            avg_score = section_df["score"].mean()
            max_score = section_df["score"].max()
            last_improvement = (section_df["score"].iloc[-1] - section_df["score"].iloc[0]) if len(section_df) > 1 else 0
            
            st.metric("Average Score", f"{avg_score:.1f}/15")
            st.metric("Highest Score", f"{max_score}/15")
            st.metric("Total Improvement", f"+{last_improvement} points" if last_improvement > 0 else f"{last_improvement} points")

# --- Study Recommendations ---
st.markdown("---")
st.subheader("🎯 Personalized Recommendations")

if progress_data["attempts"] > 0:
    weaknesses = []
    for section in sections:
        if progress_data["scores"][section]:
            last_score = progress_data["scores"][section][-1]["score"]
            if last_score < 10:  # Below passing threshold
                weaknesses.append(section)
    
    if weaknesses:
        st.warning(f"Focus on improving: {', '.join(weaknesses)}")
        for section in weaknesses:
            with st.expander(f"📚 Resources for {section}"):
                if section == "Hören":
                    st.markdown("- Listen to [Slow German](https://www.slowgerman.com/) podcasts daily")
                    st.markdown("- Practice with [Deutsche Welle](https://www.dw.com/) 'Langsam gesprochene Nachrichten'")
                elif section == "Schreiben":
                    st.markdown("- Write 3 emails/week using [Goethe B1 vocabulary](https://www.goethe.de/)")
                    st.markdown("- Review [common letter formats](https://www.deutsch-perfekt.com/)")
    else:
        st.success("Great job! All sections are at or above passing level.")
        st.balloons()
else:
    st.info("Complete at least one practice task to get recommendations")

# --- Mock Data Button (Dev Only) ---
if st.button("🚧 Generate Mock Data (Dev Only)"):
    mock_data = init_progress()
    mock_data["user_info"] = {
        "name": "Max Mustermann",
        "target_exam_date": "2024-12-01"
    }
    
    from random import randint, choice
    dates = pd.date_range(start="2024-01-01", end=datetime.now().strftime("%Y-%m-%d"), freq="7D").strftime("%Y-%m-%d").tolist()
    
    for section in sections:
        mock_data["scores"][section] = [{
            "date": date,
            "score": min(15, randint(5, 8) + i*2),
            "max_score": 15
        } for i, date in enumerate(dates[:4])]
    
    save_progress(mock_data)
    st.rerun()