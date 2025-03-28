import streamlit as st
import ollama
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np
    
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
    .exercise-card {
        background-color: #fff8e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .verb-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .verb-table th, .verb-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .verb-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

# Data for the app
vocab_data = {
    "Wichtige Präpositionen (mit Fällen)": {
        "wegen": "wegen + Genitiv (because of) - Wegen des Wetters...",
        "trotz": "trotz + Genitiv (despite) - Trotz der Kälte...",
        "während": "während + Genitiv (during) - Während des Kurses...",
        "gegenüber": "gegenüber + Dativ (opposite) - Gegenüber dem Bahnhof...",
        "bis": "bis + Akkusativ (until) - Bis nächsten Montag...",
        "durch": "durch + Akkusativ (through) - Durch den Park...",
        "für": "für + Akkusativ (for) - Für meine Prüfung...",
        "ohne": "ohne + Akkusativ (without) - Ohne mein Buch..."
    },
    "Essentielle Verben": {
        "sich bewerben um": "to apply for (Bewirbst du dich um die Stelle?)",
        "erledigen": "to complete (Ich erledige meine Hausaufgaben)",
        "verschieben": "to postpone (Wir verschieben den Termin)",
        "verstehen": "to understand (Verstehst du die Frage?)",
        "mitteilen": "to inform (Teilen Sie mir bitte mit...)",
        "sich erkundigen nach": "to inquire about (Ich erkundige mich nach dem Kurs)",
        "zustimmen": "to agree (Stimmst du mir zu?)",
        "ablehnen": "to refuse (Sie lehnte die Einladung ab)"
    },
    "Zeitformen (Verb Tenses)": {
        "Präsens": "Ich lerne Deutsch (I learn/am learning German)",
        "Perfekt": "Ich habe gelernt (I learned/have learned)",
        "Präteritum": "Ich lernte Deutsch (I learned German) - mostly written",
        "Plusquamperfekt": "Ich hatte gelernt (I had learned)",
        "Futur I": "Ich werde lernen (I will learn)",
        "Futur II": "Ich werde gelernt haben (I will have learned)"
    },
    "Konjunktionen (Conjunctions)": {
        "weil": "because (Hauptsatz + Nebensatz) - Ich bleibe zu Hause, weil ich krank bin.",
        "denn": "because (Hauptsatz + Hauptsatz) - Ich bleibe zu Hause, denn ich bin krank.",
        "obwohl": "although - Obwohl es regnet, gehe ich spazieren.",
        "damit": "so that - Ich lerne viel, damit ich die Prüfung bestehe.",
        "wenn": "if/when - Wenn ich Zeit habe, lese ich ein Buch.",
        "als": "when (past) - Als ich jung war, spielte ich Fußball.",
        "während": "while - Während ich koche, höre ich Musik.",
        "nachdem": "after - Nachdem ich gegessen habe, trinke ich Kaffee."
    },
    "Weil vs. Denn": {
        "Position": "WEIL: Verb at end | DENN: Normal word order",
        "Example 1": "WEIL: Ich bin müde, weil ich spät ins Bett gegangen bin.",
        "Example 2": "DENN: Ich bin müde, denn ich bin spät ins Bett gegangen.",
        "Comma": "Both ALWAYS need a comma before them",
        "Usage": "DENN is more formal, WEIL is more common"
    },
    "Übergangswörter (Transition Words)": {
        "zuerst": "first - Zuerst lese ich die Anleitung.",
        "dann": "then - Dann beginne ich mit der Aufgabe.",
        "anschließend": "afterwards - Anschließend überprüfe ich die Antworten.",
        "schließlich": "finally - Schließlich gebe ich den Test ab.",
        "deshalb": "therefore - Ich bin krank, deshalb bleibe ich im Bett.",
        "trotzdem": "nevertheless - Es regnet, trotzdem gehe ich spazieren."
    },
    "Prüfungsschlüsselwörter": {
        "die Aufgabe": "task/question - Lesen Sie die Aufgabe genau!",
        "die Lösung": "solution - Die Lösung steht auf Seite 10.",
        "die Note": "grade - Ich habe eine gute Note bekommen.",
        "bestehen": "to pass - Ich möchte die Prüfung bestehen.",
        "durchfallen": "to fail - Leider ist er durchgefallen.",
        "der Fehler": "mistake - Korrigieren Sie die Fehler."
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

exam_info = {
    "Passing Requirements": {
        "description": "To pass the Goethe-Zertifikat B1 exam, you must:",
        "requirements": [
            "Score at least 60% overall (180 points)",
            "Score at least 60% in each module (Reading, Writing, Listening, Speaking)"
        ]
    },
    "Exam Structure": {
        "Lesen": "65 Minuten - 5 Teile",
        "Schreiben": "60 Minuten - 2 Aufgaben",
        "Hören": "40 Minuten - 4 Teile",
        "Sprechen": "15 Minuten - 3 Teile (mit Partner)"
    }
}

exercises = {
    "Lesen": [
        {"question": "Lesen Sie den Text und beantworten Sie die Fragen:", "text": """
In Deutschland gibt es vier Jahreszeiten: Frühling, Sommer, Herbst und Winter. 
Der Frühling beginnt im März und endet im Mai. Viele Menschen freuen sich auf 
den Frühling, weil die Tage länger werden und die Blumen blühen. Im Sommer 
gehen viele Deutsche in den Urlaub, besonders an die Nordsee oder Ostsee.
"""},
        {"question": "Welche Aussage passt zu welchem Abschnitt?", "text": """
1. Verkehrsmittel: In deutschen Städten gibt es Busse, Bahnen und U-Bahnen. 
2. Freizeitaktivitäten: Viele Deutsche treiben Sport oder gehen wandern.
"""}
    ],
    "Schreiben": [
        {"task": "Schreiben Sie eine formelle Email an eine Sprachschule (80-100 Wörter)", "hints": """
- Fragen Sie nach einem Deutschkurs
- Geben Sie Ihr Sprachniveau an
- Fragen Sie nach dem Preis und dem Startdatum
"""},
        {"task": "Schreiben Sie einen Brief an einen Freund über Ihren letzten Urlaub", "hints": """
- Wohin sind Sie gefahren?
- Was haben Sie gemacht?
- Wie war das Wetter?
- Wollen Sie wieder dorthin fahren?
"""}
    ],
    "Hören": [
        {"task": "Hören Sie die Durchsage und beantworten Sie die Fragen:", "questions": """
1. Wann fährt der nächste Zug nach Berlin?
2. Von welchem Gleis fährt der Zug?
"""},
        {"task": "Welche Antwort passt zu welchem Dialog?", "options": """
A) "Entschuldigung, wo ist die Post?" 
B) "Ich möchte ein Ticket nach Hamburg kaufen"
"""}
    ],
    "Sprechen": [
        {"task": "Stellen Sie sich vor:", "prompts": """
- Name, Alter
- Hobbys
- Beruf/Studium
- Warum lernen Sie Deutsch?
"""},
        {"task": "Diskutieren Sie mit einem Partner:", "topics": """
- Vor- und Nachteile des Lebens in der Stadt
- Wie verbringen junge Leute ihre Freizeit?
"""}
    ]
}

# Ollama/DeepSeek integration
def get_ai_response(question):
    """Get response from DeepSeek R1 via Ollama"""
    try:
        response = ollama.generate(
            model='deepseek-r1',
            prompt=f"""Du bist ein B1-Prüfungsexperte. Beantworte die Frage kurz und präzise:
            
            Frage: {question}
            
            - Maximal 3 Sätze
            - Fokus auf Prüfungsstrategien
            - Wichtige Grammatikpunkte
            - Typische Fehler vermeiden""",
            options={'temperature': 0.3}
        )
        return response['response']
    except Exception as e:
        st.error(f"Fehler bei der AI-Anfrage: {e}")
        return None

# Main app
def main():
    st.title("🇩🇪 B1 Prüfung Blitzvorbereitung")
    st.subheader("Intensivkurs für die Goethe B1 Prüfung")
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Übersicht", "Wortschatz", "Schreiben", "Prüfungsinfo", "Übungen"])
    
    with tab1:
        st.header("2-Tage-Lernplan")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### **Tag 1: Grundlagen**")
            st.markdown("""
            - ⏰ 2h - Wichtiger Wortschatz & Präpositionen
            - ⏰ 1.5h - Leseverstehen Strategien
            - ⏰ 2h - Schreiben Vorlagen
            - ⏰ 1h - Hörverstehen Praxis
            """)
        with col2:
            st.markdown("### **Tag 2: Prüfungssimulation**")
            st.markdown("""
            - ⏰ 3h - Komplette Übungsprüfung
            - ⏰ 1h - Sprechen üben
            - ⏰ 1h - Schwachstellen wiederholen
            """)
        
        st.header("Prüfungsteile")
        cols = st.columns(4)
        teile = ["Lesen", "Schreiben", "Hören", "Sprechen"]
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="teil-card">
                    <h3>Teil {i+1}: {teile[i]}</h3>
                    <p>{exam_info['Exam Structure'][teile[i]]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.header("Wichtiger Wortschatz")
        
        for category, items in vocab_data.items():
            with st.expander(f"📌 {category}"):
                col1, col2 = st.columns(2)
                items_list = list(items.items())
                
                for i, (word, meaning) in enumerate(items_list):
                    if i % 2 == 0:
                        col1.markdown(f"**{word}**  \n{meaning}")
                    else:
                        col2.markdown(f"**{word}**  \n{meaning}")
        
        st.markdown("---")
        with st.expander("📝 Verbkonjugation (Beispiele)"):
            st.markdown("""
            <table class="verb-table">
                <tr><th>Pronomen</th><th>lernen (Präsens)</th><th>gelernt (Perfekt)</th><th>lernen (Futur I)</th></tr>
                <tr><td>ich</td><td>lerne</td><td>habe gelernt</td><td>werde lernen</td></tr>
                <tr><td>du</td><td>lernst</td><td>hast gelernt</td><td>wirst lernen</td></tr>
                <tr><td>er/sie/es</td><td>lernt</td><td>hat gelernt</td><td>wird lernen</td></tr>
                <tr><td>wir</td><td>lernen</td><td>haben gelernt</td><td>werden lernen</td></tr>
                <tr><td>ihr</td><td>lernt</td><td>habt gelernt</td><td>werdet lernen</td></tr>
                <tr><td>sie/Sie</td><td>lernen</td><td>haben gelernt</td><td>werden lernen</td></tr>
            </table>
            """, unsafe_allow_html=True)
        
        with st.expander("✍️ Weil/Denn Übung"):
            st.markdown("**Ergänzen Sie mit 'weil' oder 'denn':**")
            exercise1 = st.text_input("1. Ich nehme einen Regenschirm, ___ es regnet.")
            exercise2 = st.text_input("2. Sie geht früh ins Bett, ___ sie müde ist.")
            
            if st.button("Antworten überprüfen"):
                answers = {
                    1: {"correct": "weil", "explanation": "Verb 'regnet' am Ende → Nebensatz"},
                    2: {"correct": "denn", "explanation": "'ist' vor dem Subjekt → Hauptsatz"}
                }
                for i, ans in enumerate([exercise1, exercise2], 1):
                    if ans.lower() == answers[i]["correct"]:
                        st.success(f"Richtig! {answers[i]['explanation']}")
                    else:
                        st.error(f"Falsch! Richtige Antwort: {answers[i]['correct']}")
    
    with tab3:
        st.header("Schreiben Vorlagen")
        template_type = st.radio("Vorlage auswählen:", list(writing_templates.keys()))
        
        st.markdown("### Struktur:")
        for item in writing_templates[template_type]["structure"]:
            st.markdown(f"- {item}")
        
        st.markdown("### Beispiel:")
        st.text_area("Mustertext:", 
                    writing_templates[template_type]["example"], 
                    height=200,
                    disabled=True)
        
        st.markdown("### Tipps für das Schreiben")
        st.markdown("""
        1. Struktur immer einhalten (Anrede, Einleitung, Hauptteil, Schluss)
        2. Mindestens 100 Wörter schreiben
        3. Auf Formal/Informal achten
        4. 5 Minuten für Planung verwenden
        5. 10 Minuten für Korrektur am Ende
        """)
    
    with tab4:
        st.header("Prüfungsinformationen")
        
        with st.expander("Bestandenkriterien"):
            st.markdown(exam_info["Passing Requirements"]["description"])
            for req in exam_info["Passing Requirements"]["requirements"]:
                st.markdown(f"- {req}")
        
        with st.expander("Prüfungsstruktur"):
            for part, info in exam_info["Exam Structure"].items():
                st.markdown(f"**{part}**: {info}")
        
        with st.expander("Bewertungskriterien"):
            st.table(pd.DataFrame({
                "Teil": ["Lesen", "Schreiben", "Hören", "Sprechen"],
                "Punkte": [100, 100, 100, 100],
                "Bestanden": [60, 60, 60, 60],
                "Zeit": ["65 min", "60 min", "40 min", "15 min"]
            }))
    
    with tab5:
        st.header("Übungen")
        selected_part = st.radio(
            "Wähle einen Prüfungsteil:",
            ["Lesen", "Schreiben", "Hören", "Sprechen"],
            horizontal=True
        )
        
        st.markdown(f"### {selected_part} Übung")
        exercise = random.choice(exercises[selected_part])
        
        with st.container():
            st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
            
            if selected_part == "Lesen":
                st.markdown(f"**{exercise['question']}**")
                st.markdown(f"*{exercise['text']}*")
                st.text_area("Deine Antwort:", height=150, key="reading_answer")
            
            elif selected_part == "Schreiben":
                st.markdown(f"**Aufgabe:** {exercise['task']}")
                st.markdown(f"*Hinweise:* {exercise['hints']}")
                user_text = st.text_area("Deine Antwort:", height=200, key="writing_answer")
                if st.button("Feedback erhalten"):
                    feedback = get_ai_response(f"Gib kurzes Feedback zu diesem B1-Text: {user_text}")
                    if feedback:
                        st.info(feedback)
            
            elif selected_part == "Hören":
                st.markdown(f"**{exercise['task']}**")
                st.audio("https://www.goethe.de/pro/relaunch/prf/de/GOETHE-ZERTIFIKAT_B1_HOEREN.mp3")
                if "questions" in exercise:
                    st.markdown(f"*Fragen:* {exercise['questions']}")
                else:
                    st.markdown(f"*Optionen:* {exercise['options']}")
                st.text_input("Deine Antwort:", key="listening_answer")
            
            elif selected_part == "Sprechen":
                st.markdown(f"**{exercise['task']}**")
                st.markdown(f"*Themen:* {exercise['prompts'] if 'prompts' in exercise else exercise['topics']}")
                st.text_input("Deine Stichpunkte:", key="speaking_notes")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🤖 Frag den B1-Experten")
        user_question = st.text_input("Stelle eine Frage zur Prüfung:")
        
        if user_question:
            with st.spinner("AI analysiert..."):
                answer = get_ai_response(user_question)
                if answer:
                    st.success(answer)
                    st.markdown("---")
                    st.markdown("**🔍 Weiterführende Übungen:**")
                    if "hören" in user_question.lower():
                        st.markdown("- [Hörverstehen Übung 1](#)")
                        st.markdown("- [Dialoge verstehen](#)")
                    elif "schreiben" in user_question.lower():
                        st.markdown("- [Formeller Brief üben](#)")
                        st.markdown("- [E-Mail an Freund schreiben](#)")

if __name__ == "__main__":
    main()