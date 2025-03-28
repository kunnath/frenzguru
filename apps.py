import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# App configuration
st.set_page_config(
    page_title="B1 Prüfung Strategien",
    page_icon="🇩🇪",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .exam-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f0f7ff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .time-slot {
        background-color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .highlight {
        background-color: #fff8e6;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Exam structure data
exam_data = {
    "Teil 1: Lesen": {
        "Dauer": "65 Minuten",
        "Aufgaben": [
            "Teil 1: Kurze Texte mit Multiple-Choice-Fragen",
            "Teil 2: Zuordnung von Überschriften zu Abschnitten",
            "Teil 3: Lückentext mit Wortauswahl",
            "Teil 4: Lange Texte mit Verständnisfragen"
        ],
        "Strategien": [
            "⏱️ Zeitmanagement: Max. 15 Min. pro Teil",
            "🔍 Zuerst Fragen lesen, dann Text scannen",
            "📌 Schlüsselwörter in Fragen markieren",
            "❌ Offensichtlich falsche Antworten sofort streichen"
        ],
        "Beispiel": {
            "Text": "In deutschen Städten gibt es viele Parks. Diese sind oft...",
            "Frage": "Was ist richtig? a) Parks sind selten b) Parks haben Spielplätze c) Parks sind immer geschlossen"
        }
    },
    "Teil 2: Schreiben": {
        "Dauer": "60 Minuten",
        "Aufgaben": [
            "Aufgabe 1: Formeller Brief/Email (80-100 Wörter)",
            "Aufgabe 2: Informeller Brief/Forumbeitrag (80-100 Wörter)"
        ],
        "Struktur": {
            "Formeller Brief": [
                "Ort, Datum (rechtsbündig)",
                "Betreffzeile",
                "Formelle Anrede (Sehr geehrte...)",
                "Einleitung: Grund des Schreibens",
                "Hauptteil: Details/Argumente",
                "Schluss: Höflichkeitsformel",
                "Grußformel (Mit freundlichen Grüßen)"
            ],
            "Informelle Email": [
                "Betreffzeile",
                "Persönliche Anrede (Liebe...)",
                "Einleitung: Smalltalk",
                "Hauptteil: Informationen/Fragen",
                "Schluss: Wunsch/Abschied",
                "Grußformel (Viele Grüße)"
            ]
        },
        "Tipps": [
            "✍️ Mindestens 100 Wörter schreiben",
            "⏳ 20 Min. für Planung, 30 Min. für Text, 10 Min. für Korrektur",
            "📌 3-4 Absätze verwenden",
            "✅ Typische Redemittel lernen"
        ]
    },
    "Teil 3: Hören": {
        "Dauer": "40 Minuten",
        "Aufgaben": [
            "Teil 1: Kurze Dialoge mit Bildern",
            "Teil 2: Radioansagen/Informationen",
            "Teil 3: Lange Dialoge mit Detailfragen",
            "Teil 4: Meinungen/Interviews verstehen"
        ],
        "Strategien": [
            "👂 Vor dem Hören: Fragen genau lesen",
            "✏️ Während des Hörens: Stichworte notieren",
            "🔁 Audio wird 2x abgespielt - beim ersten Mal Hauptidee, beim zweiten Mal Details",
            "❓ Unbekannte Wörter ignorieren - auf Kontext konzentrieren"
        ],
        "Übung": "Hören Sie deutsche Podcasts (Langsam gesprochene Nachrichten)"
    },
    "Teil 4: Sprechen": {
        "Dauer": "15 Minuten",
        "Aufgaben": [
            "Teil 1: Vorstellung (Name, Herkunft, Interessen)",
            "Teil 2: Thema präsentieren (2 Min. Monolog)",
            "Teil 3: Diskussion mit Partner"
        ],
        "Bewertung": [
            "🗣️ Aussprache und Verständlichkeit",
            "📚 Wortschatz und Grammatik",
            "💡 Ideenentwicklung und Logik",
            "🤝 Interaktion mit Partner"
        ],
        "Redemittel": [
            "Meiner Meinung nach... / Ich finde, dass...",
            "Was meinst du dazu? / Stimmt das deiner Ansicht nach?",
            "Einerseits... andererseits...",
            "Vielleicht sollten wir..."
        ]
    }
}

# Main app
def main():
    st.title(" B1 Prüfungsstrategien")
    st.markdown("""
    **Praktische Anleitung für jeden Prüfungsteil**  
    *Konzentriert auf reine Prüfungsvorbereitung*
    """)
    
    # Exam parts navigation
    selected_part = st.radio(
        "Prüfungsteil auswählen:",
        list(exam_data.keys()),
        horizontal=True
    )
    
    # Display selected part
    part_data = exam_data[selected_part]
    
    with st.container():
        st.markdown(f'<div class="exam-card">', unsafe_allow_html=True)
        
        # Header with time
        st.markdown(f"### {selected_part}  \n⏱️ **Dauer:** {part_data['Dauer']}")
        
        # Tasks section
        st.markdown("#### Aufgaben:")
        for task in part_data["Aufgaben"]:
            st.markdown(f"- {task}")
        
        # Special sections per part
        if "Lesen" in selected_part:
            st.markdown("#### Strategien:")
            for strategy in part_data["Strategien"]:
                st.markdown(f"- {strategy}")
            
            st.markdown("#### Beispiel:")
            st.markdown(f"*Text:* {part_data['Beispiel']['Text']}")
            st.markdown(f"*Frage:* {part_data['Beispiel']['Frage']}")
        
        elif "Schreiben" in selected_part:
            st.markdown("#### Textstruktur:")
            for text_type, structure in part_data["Struktur"].items():
                with st.expander(text_type):
                    for item in structure:
                        st.markdown(f"- {item}")
            
            st.markdown("#### Tipps:")
            for tip in part_data["Tipps"]:
                st.markdown(f"- {tip}")
        
        elif "Hören" in selected_part:
            st.markdown("#### Strategien:")
            for strategy in part_data["Strategien"]:
                st.markdown(f"- {strategy}")
            
            st.markdown(f"#### Übungstipp:  \n{part_data['Übung']}")
        
        elif "Sprechen" in selected_part:
            st.markdown("#### Bewertungskriterien:")
            for criterion in part_data["Bewertung"]:
                st.markdown(f"- {criterion}")
            
            st.markdown("#### Nützliche Redemittel:")
            cols = st.columns(2)
            for i, phrase in enumerate(part_data["Redemittel"]):
                if i % 2 == 0:
                    cols[0].markdown(f"- <span class='highlight'>{phrase}</span>", unsafe_allow_html=True)
                else:
                    cols[1].markdown(f"- <span class='highlight'>{phrase}</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Time management calculator
    st.markdown("---")
    st.markdown("### ⏱️ Zeitmanagement Rechner")
    exam_duration = int(part_data["Dauer"].split()[0])
    col1, col2 = st.columns(2)
    with col1:
        task_count = st.number_input("Anzahl der Aufgaben:", 
                                   min_value=1, 
                                   max_value=10, 
                                   value=len(part_data["Aufgaben"]))
    with col2:
        review_time = st.number_input("Korrekturzeit (Minuten):", 
                                    min_value=0, 
                                    max_value=30, 
                                    value=5 if "Schreiben" in selected_part else 0)
    
    time_per_task = (exam_duration - review_time) / task_count
    st.markdown(f"""
    **Empfohlene Zeit pro Aufgabe:**  
    <span class='time-slot'>{time_per_task:.1f} Minuten</span>  
    **Korrekturzeit:**  
    <span class='time-slot'>{review_time} Minuten</span>
    """, unsafe_allow_html=True)
    
    # Quick practice
    st.markdown("---")
    st.markdown("### 💡 Schnellübung")
    if "Lesen" in selected_part:
        st.text_area("Übersetzen Sie ins Deutsche:", 
                    "The park has many playgrounds for children.",
                    help="Versuchen Sie: 'Der Park hat viele Spielplätze für Kinder.'")
    elif "Schreiben" in selected_part:
        st.text_input("Formelle Anrede für eine Firma:", 
                     placeholder="Sehr geehrte Damen und Herren,")
    elif "Hören" in selected_part:
        st.markdown("💡 Hören Sie jetzt 10 Sekunden Deutsch: [Langsam gesprochene Nachrichten](https://www.dw.com/de/deutsch-lernen/nachrichten/s-8030)")
    elif "Sprechen" in selected_part:
        st.text_input("Satz beginnen mit 'Meiner Meinung nach...':",
                    placeholder="Meiner Meinung nach ist Deutsch lernen wichtig, weil...")

if __name__ == "__main__":
    main()