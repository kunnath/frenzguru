import streamlit as st
import ollama  # Ollama Python client
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Optional


# App configuration
st.set_page_config(
    page_title="B1 Prüfung Blitzvorbereitung",
    page_icon="🇩🇪",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .teil-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .teil-card:hover {
        transform: translateY(-2px);
    }
    .vocab-card {
        border-left: 4px solid #1a73e8;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
    }
    .time-slot {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .progress-container {
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# Data for the app
vocab_data = {
    "Important Prepositions": {
        "wegen": "because of (+Genitiv)",
        "trotz": "despite (+Genitiv)",
        "während": "during (+Genitiv)",
        "gegenüber": "opposite (+Dativ)",
        "bis": "until (+Akkusativ)",
        "durch": "through (+Akkusativ)",
        "für": "for (+Akkusativ)",
        "ohne": "without (+Akkusativ)"
    },
    "Key Verbs": {
        "sich bewerben um": "to apply for",
        "erledigen": "to complete",
        "verschieben": "to postpone",
        "verstehen": "to understand",
        "mitteilen": "to inform",
        "sich erkundigen nach": "to inquire about",
        "zustimmen": "to agree",
        "ablehnen": "to refuse"
    },
    "Formal Phrases": {
        "Sehr geehrte Damen und Herren,": "Dear Sir or Madam,",
        "mit freundlichen Grüßen": "Kind regards",
        "Ich möchte mich erkundigen...": "I would like to inquire...",
        "Ich wäre Ihnen dankbar, wenn...": "I would be grateful if...",
        "Ich beziehe mich auf...": "I'm referring to..."
    }
}

writing_templates = {
    "Formal Letter": {
        "structure": [
            "Ort, Datum (right aligned)",
            "Betreff: (subject line)",
            "Sehr geehrte Damen und Herren,",
            "Einleitung: State reason for writing",
            "Hauptteil: Provide details, ask questions",
            "Schluss: Request response, thank reader",
            "Mit freundlichen Grüßen,",
            "Ihr Name"
        ],
        "example": """
München, 15. März 2024

Betreff: Bewerbung für Praktikumsstelle

Sehr geehrte Damen und Herren,

mit großem Interesse habe ich Ihre Anzeige für ein Praktikum gelesen. 
Ich möchte mich für diese Stelle bewerben.

Ich studiere derzeit Wirtschaft an der Universität München und 
suche ein Praktikum im Bereich Marketing. In meinem Studium habe ich 
schon mehrere Kurse in diesem Bereich belegt.

Über eine positive Rückmeldung würde ich mich sehr freuen. 
Für weitere Informationen stehe ich gerne zur Verfügung.

Mit freundlichen Grüßen,
Anna Müller
"""
    },
    "Informal Email": {
        "structure": [
            "Betreff: (subject line)",
            "Liebe/Lieber [Name],",
            "Einleitung: Greeting, reason for writing",
            "Hauptteil: Share news, ask questions",
            "Schluss: Closing remarks",
            "Viele Grüße,",
            "Dein Name"
        ],
        "example": """
Betreff: Treffen am Wochenende

Liebe Sarah,

wie geht's dir? Ich hoffe, alles ist gut bei dir.

Ich schreibe dir, weil ich wissen wollte, ob du am Samstag Zeit hast. 
Ich möchte mit dir ins Kino gehen. Der neue Marvel-Film läuft jetzt.

Was hältst du davon? Lass mich bitte wissen, ob du kommen kannst.

Viele Grüße,
Deine Lisa
"""
    }
}

# In the exam_info dictionary, change this:

exam_info = {
    "Passing Requirements": {
        "description": "To pass the Zertifikat B1 exam, you must:",
        "requirements": [
            "Score at least 60% overall (180 points)",
            "Score at least 60% in each module (Reading, Writing, Listening, Speaking)"
        ]
    },
    "Exam Structure": {
        "Reading": "65 minutes - 5 parts",
        "Writing": "60 minutes - 2 tasks",
        "Listening": "40 minutes - 4 parts",
        "Speaking": "15 minutes - 3 parts (with partner)"
    }
}



# App functions
def display_vocab_card(title, items):
    with st.expander(title):
        col1, col2 = st.columns(2)
        for i, (word, meaning) in enumerate(items.items()):
            if i % 2 == 0:
                col1.markdown(f"**{word}** - {meaning}")
            else:
                col2.markdown(f"**{word}** - {meaning}")

def display_writing_template(template_type):
    template = writing_templates[template_type]
    st.subheader(template_type)
    
    st.markdown("**Structure:**")
    for item in template["structure"]:
        st.markdown(f"- {item}")
    
    st.markdown("**Example:**")
    st.code(template["example"], language=None)

def generate_practice_question(teil):
    questions = {
        "Reading": [
            "Read this short text and answer the questions below...",
            "Which statement matches each paragraph?..."
        ],
        "Writing": [
            "Write a formal email to a company requesting information...",
            "Write a letter to a friend about your recent vacation..."
        ],
        "Listening": [
            "Listen to the conversation and answer the questions...",
            "What is the main purpose of this announcement?..."
        ],
        "Speaking": [
            "Introduce yourself and talk about your hobbies...",
            "Discuss with your partner: What are the advantages of living in a big city?..."
        ]
    }
    return random.choice(questions[teil])


### --- OLLAMA + DEEPSEEK R1 INTEGRATION --- ###
def get_ai_response(user_question: str) -> Optional[str]:
    """Get a concise answer using Ollama's DeepSeek R1 model."""
    try:
        response = ollama.generate(
            model="deepseek-r1:8b",
            prompt=f"""
            You are a German B1 exam (Goethe-Zertifikat B1) expert. 
            Provide a **short, clear, and precise** answer to help the student prepare.
            
            Question: {user_question}
            
            Answer in **English or German** (based on the question language).
            Focus on:
            - Exam strategies
            - Key vocabulary
            - Grammar rules
            - Time management
            - Common mistakes
            """,
            options={"temperature": 0.3}  # Lower temp for factual answers
        )
        return response["response"]
    except Exception as e:
        st.error(f"Error fetching AI response: {e}")
        return None


# Initialize DeepSeek model (replace with actual initialization)
def get_deepseek_response(question):
    """
    Function to get response from DeepSeek model
    Replace this with actual API calls when available
    """
    # This is a mock response - replace with actual API call
    mock_responses = {
        "passing score": "The passing score for Goethe B1 exam is 60% (180 points) in total and at least 60% in each module.",
        "writing tips": "For B1 writing: 1) Follow the structure 2) Use formal language if required 3) Check grammar 4) Write at least 100 words 5) Manage your time (5 min planning, 20 min writing, 5 min checking).",
        "prepositions": "Important B1 prepositions: wegen (because of), trotz (despite), während (during), gegenüber (opposite) - remember their cases!",
        "speaking test": "B1 speaking has 3 parts: 1) Introduce yourself 2) Discuss a topic 3) Plan something with partner. Speak clearly and interact naturally."
    }
    
    question_lower = question.lower()
    for key in mock_responses:
        if key in question_lower:
            return mock_responses[key]
    
    return "I can help with B1 exam questions about: passing requirements, writing tips, important vocabulary, or test structure. Please ask specifically."


# Main app
def main():
    st.title("🇩🇪 B1 Prüfung Blitzvorbereitung")
    st.subheader("2-Tage-Intensivkurs für die Goethe B1 Prüfung")
    
    # Set exam date (default is 2 days from now)
    exam_date = st.date_input("Wann ist deine Prüfung?", 
                            min_value=datetime.today(), 
                            value=datetime.today() + timedelta(days=2))
    
    days_until = (exam_date - datetime.today().date()).days
    st.markdown(f"**Noch {days_until} Tage bis zur Prüfung!**")
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Übersicht", "Wortschatz", "Schreiben", "Prüfungsinfo", "Übungen"])
    
    with tab1:  # Overview tab
        st.header("2-Tage-Lernplan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### **Tag 1: Grundlagen**")
            st.markdown("""
            - ⏰ 2 Stunden - Wichtiger Wortschatz & Präpositionen
            - ⏰ 1.5 Stunden - Leseverstehen Strategien
            - ⏰ 2 Stunden - Schreiben Vorlagen (Emails, Briefe)
            - ⏰ 1 Stunde - Hörverstehen Praxis
            """)
            
        with col2:
            st.markdown("### **Tag 2: Prüfungssimulation**")
            st.markdown("""
            - ⏰ 3 Stunden - Komplette Übungsprüfung
            - ⏰ 1 Stunde - Sprechen Rollenspiele
            - ⏰ 1 Stunde - Schwachstellen wiederholen
            - ⏰ 1 Stunde - Letzte Tipps und Strategien
            """)
        
        st.header("Prüfungsteile")
        cols = st.columns(4)
        
        teile = [
            ("Lesen", "65 min", "Textverständnis, Zuordnung"),
            ("Schreiben", "60 min", "Formeller Brief, Email"),
            ("Hören", "40 min", "Dialoge, Ansagen"),
            ("Sprechen", "15 min", "Vorstellung, Diskussion")
        ]
        
        for i, (teil, time, desc) in enumerate(teile):
            with cols[i]:
                st.markdown(f"""
                <div class="teil-card">
                    <h3>Teil {i+1}: {teil}</h3>
                    <p>{time} | {desc}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Zu {teil} übungen", key=f"teil_{i}"):
                    st.session_state.current_tab = "Übungen"
    
    with tab2:  # Vocabulary tab
        st.header("Wichtiger Wortschatz für B1")
        
        for title, items in vocab_data.items():
            display_vocab_card(title, items)
        
        st.markdown("### Präpositionen mit Fallen")
        st.image("https://www.deutschtraining.org/wp-content/uploads/2020/04/präpositionen-tabelle.png", 
                caption="Präpositionen mit Dativ, Akkusativ und Genitiv")
    
    with tab3:  # Writing tab
        st.header("Schreiben Vorlagen")
        
        template_type = st.radio("Vorlage auswählen:", 
                               list(writing_templates.keys()),
                               horizontal=True)
        
        display_writing_template(template_type)
        
        st.markdown("### Tipps für das Schreiben")
        st.markdown("""
        1. Struktur immer einhalten (Anrede, Einleitung, Hauptteil, Schluss)
        2. Mindestens 80 Wörter schreiben
        3. Auf Formal/Informal achten
        4. 5 Minuten für Planung verwenden
        5. 10 Minuten für Korrektur am Ende
        """)
    
    # And modify the display code in tab4 to:
    with tab4:  # Exam info tab
        st.header("Prüfungsinformationen")
        
        for title, content in exam_info.items():
            with st.expander(title):
                if isinstance(content, dict):
                    if "description" in content:  # Check if description exists
                        st.markdown(content["description"])
                    if "requirements" in content:  # Handle requirements if they exist
                        for req in content["requirements"]:
                            st.markdown(f"- {req}")
                else:
                    # Handle the Exam Structure case
                    for part, info in content.items():
                        st.markdown(f"**{part}**: {info}")
    
    
# Modify the practice tab to include DeepSeek

### --- MODIFIED PRACTICE TAB WITH AI ANSWERS --- ###
    with tab5:  # Practice tab
        st.header("Übungen")
        
        teil = st.radio("Wähle einen Prüfungsteil:", 
                    ["Reading", "Writing", "Listening", "Speaking"],
                    horizontal=True)
        
        st.markdown(f"### {teil} Übung")
        st.markdown(generate_practice_question(teil))
        
        if teil == "Writing":
            user_text = st.text_area("Deine Antwort:", height=200)
            if st.button("Feedback erhalten"):
                feedback = get_ai_response(f"Give brief feedback on this B1 German writing task:\n\n{user_text}")
                if feedback:
                    st.success("✏️ **Schreiben Feedback:**")
                    st.markdown(feedback)

        # --- NEW: AI QUESTION ANSWERING SECTION --- #
        st.markdown("### 🤖 **Frag den B1-Prüfungsexperten (AI)**")
        user_question = st.text_input(
            "Stelle eine Frage zur B1-Prüfung:",
            placeholder="Wie kann ich im Hörverstehen besser werden?",
            key="ai_question_input"
        )

        if user_question:
            with st.spinner("🧠 DeepSeek R1 sucht die beste Antwort..."):
                ai_answer = get_ai_response(user_question)
                if ai_answer:
                    st.success("🎯 **Antwort:**")
                    st.markdown(ai_answer)
                    
                    # Suggest follow-up exercises
                    st.markdown("---")
                    st.markdown("**🔍 Weiterführende Übungen:**")
                    if "hören" in user_question.lower() or "listening" in user_question.lower():
                        st.markdown("- [Hörverstehen Übung 1](#)")
                        st.markdown("- [Dialoge verstehen](#)")
                    elif "schreiben" in user_question.lower() or "writing" in user_question.lower():
                        st.markdown("- [Formeller Brief üben](#)")
                        st.markdown("- [E-Mail an Freund schreiben](#)")


if __name__ == "__main__":
    main()