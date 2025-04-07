import streamlit as st
import pandas as pd
import random
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import os
import time
from vosk import Model, KaldiRecognizer

# Configuration
AUDIO_FILE = "temp_recording.wav"
VOSK_MODEL_PATH = "vosk-malayalam-model"
SAMPLE_RATE = 16000
CHANNELS = 1

# Language configuration dictionary
LANGUAGE_CONFIG = {
    "Malayalam": {
        "code": "ml",
        "examples": {
            "sentence": "ഞാൻ സ്കൂളിൽ പോകുന്നു",
            "translation": "Ich gehe zur Schule",
            "structure": "SOV (Subject-Object-Verb)",
            "common_errors": {
                "word_order": "Malayalam uses SOV while German uses SVO",
                "articles": "Malayalam doesn't use articles like German"
            }
        }
    },
    "Hindi": {
        "code": "hi",
        "examples": {
            "sentence": "मैं स्कूल जाता हूँ",
            "translation": "Ich gehe zur Schule",
            "structure": "SOV (Subject-Object-Verb)",
            "common_errors": {
                "word_order": "Hindi uses SOV while German uses SVO",
                "gender": "Hindi has 2 genders vs German's 3"
            }
        }
    }
}

# Initialize session state
if "native_lang" not in st.session_state:
    st.session_state.native_lang = "Malayalam"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "German"

def get_current_config():
    return LANGUAGE_CONFIG[st.session_state.native_lang]



def analyze_speech(audio_file):
    """Mock speech analysis function"""
    # Simulate analysis delay
    time.sleep(2)
    
    return {
        "pronunciation_score": 82,
        "feedback_points": [
            "Good vowel sounds in 'Schule'",
            "Work on ending consonants in 'gehe'"
        ],
        "comparison": {
            "native_sound": "Malayalam 'സ്കൂൾ' vs German 'Schule'",
            "articulation_tip": "Round lips more for 'ü' sound"
        }
    }

def grammar_analysis(text):
    """Mock grammar analysis function"""
    return {
        "errors": [
            {"position": 12, "message": "Incorrect article usage (der/die/das)"},
            {"position": 25, "message": "Verb conjugation mismatch"}
        ],
        "suggestions": [
            "Try using 'die' instead of 'der' here",
            "Use 'gehen' instead of 'geht' for plural subjects"
        ]
    }


# Mock translation function with multi-language support
def translate_to_german(text):
    lang_config = get_current_config()
    translations = {
        "ml": {
            "ഞാൻ സ്കൂളിൽ പോകുന്നു": "Ich gehe zur Schule",
            "എനിക്ക് വെള്ളം വേണം": "Ich brauche Wasser"
        },
        "hi": {
            "मैं स्कूल जाता हूँ": "Ich gehe zur Schule",
            "मुझे पानी चाहिए": "Ich brauche Wasser"
        }
    }
    return translations[lang_config["code"]].get(text, "Translation not available")

def get_grammar_feedback(sentence):
    config = get_current_config()
    return {
        "errors": [
            {"message": config["examples"]["common_errors"]["word_order"]},
            {"message": "Remember to capitalize all nouns in German"}
        ],
        "comparison": {
            "native_sentence": config["examples"]["sentence"],
            "german_sentence": config["examples"]["translation"],
            "structure_explanation": config["examples"]["common_errors"]["word_order"]
        }
    }

# App layout
st.set_page_config(page_title="DeutschLern", layout="wide")

# Language Selection Sidebar
with st.sidebar:
    st.header("🌍 Language Setup")
    st.session_state.native_lang = st.selectbox(
        "Choose Your Native Language",
        list(LANGUAGE_CONFIG.keys()),
        index=list(LANGUAGE_CONFIG.keys()).index(st.session_state.native_lang)
    )
    st.session_state.target_lang = "German"  # Fixed target language
    st.divider()
    st.write(f"Current Mode: {st.session_state.native_lang} → {st.session_state.target_lang}")
    st.video("https://www.youtube.com/watch?v=1dEbWl5rkWg")  # Language-specific videos

# Main Interface
st.title(f"🎓 {st.session_state.native_lang} to {st.session_state.target_lang} Learning App")

# Workflow Tabs
tab1, tab2, tab3 = st.tabs(["Core Learning", "Grammar Bridge", "Practice Zone"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Input in {st.session_state.native_lang}")
        input_text = st.text_area(
            f"Type/speak in {st.session_state.native_lang}:",
            height=150,
            placeholder=get_current_config()["examples"]["sentence"]
        )
        
        if st.button("Translate & Analyze"):
            st.session_state.translation = translate_to_german(input_text)
    
    with col2:
        st.subheader(f"{st.session_state.target_lang} Output & Analysis")
        if 'translation' in st.session_state:
            st.markdown(f"**Translation:** `{st.session_state.translation}`")
            
            feedback = get_grammar_feedback(st.session_state.translation)
            
            st.markdown("**Key Differences:**")
            for error in feedback["errors"]:
                st.error(f"⚠️ {error['message']}")
            
            st.divider()
            st.markdown("**Structure Comparison**")
            comp_data = {
                "Aspect": ["Sentence Structure", "Example"],
                st.session_state.native_lang: [
                    LANGUAGE_CONFIG[st.session_state.native_lang]["examples"]["structure"],
                    feedback["comparison"]["native_sentence"]
                ],
                st.session_state.target_lang: [
                    "SVO (Subject-Verb-Object)",
                    feedback["comparison"]["german_sentence"]
                ]
            }
            st.table(pd.DataFrame(comp_data).set_index("Aspect"))

with tab2:
    st.subheader("Cross-Language Grammar Guide")
    
    concept = st.selectbox("Select Grammar Concept", [
        "Sentence Structure",
        "Noun Genders",
        "Verb Conjugation"
    ])
    
    config = get_current_config()
    
    if concept == "Sentence Structure":
        st.markdown(f"""
        ### {st.session_state.native_lang} vs {st.session_state.target_lang}
        **{st.session_state.native_lang} Structure:**  
        {config['examples']['structure']}  
        Example: `{config['examples']['sentence']}`  
        
        **{st.session_state.target_lang} Structure:**  
        SVO (Subject-Verb-Object)  
        Example: `{config['examples']['translation']}`
        """)
    elif concept == "Noun Genders":
        st.markdown(f"""
        ### Gender System Comparison
        **{st.session_state.native_lang}:**  
        {config['examples']['common_errors'].get('gender', 'No grammatical gender')}  
        
        **{st.session_state.target_lang}:**  
        Three genders (der, die, das) with complex rules
        """)

with tab3:
    st.subheader("Bilingual Practice")
    
    # Language-switching exercise
    st.markdown(f"**Translate this {st.session_state.native_lang} sentence:**")
    native_sentence = st.code(config["examples"]["sentence"])
    
    german_translation = st.text_input(
        f"Write {st.session_state.target_lang} translation:",
        placeholder=config["examples"]["translation"]
    )
    
    if german_translation:
        if german_translation == config["examples"]["translation"]:
            st.success("🎉 Correct! Good job!")
        else:
            st.error("Try again! Here's a hint:")
            st.write(get_current_config()["examples"]["common_errors"]["word_order"])

# Run with: streamlit run app.py
# Mock LLM integration (replace with actual DeepSeek R1 API)
def get_grammar_feedback(sentence):
    feedback = {
        "errors": [
            {"word": "gehe", "message": "Use 'gehen' instead of 'gehe' in this context"},
            {"message": "Remember to capitalize nouns (Schule)"}
        ],
        "comparison": {
            "malayalam": "ഞാൻ സ്കൂളിൽ പോകുന്നു",
            "german_correct": "Ich gehe zur Schule",
            "explanation": "Malayalam uses SOV structure while German uses SVO"
        }
    }
    return feedback



def record_audio(duration=5):
    """Record audio from microphone"""
    st.info("Recording... Speak now!")
    audio_data = sd.rec(int(duration * SAMPLE_RATE),
                        samplerate=SAMPLE_RATE,
                        channels=CHANNELS)
    sd.wait()
    sf.write(AUDIO_FILE, audio_data, SAMPLE_RATE)
    return AUDIO_FILE

def transcribe_google(audio_file):
    """Use Google Web Speech API (requires internet)"""
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        
    try:
        text = r.recognize_google(audio, language="ml-IN")
        return text
    except sr.UnknownValueError:
        st.error("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google: {e}")

def transcribe_vosk(audio_file):
    """Use offline Vosk model (requires model download)"""
    if not os.path.exists(VOSK_MODEL_PATH):
        st.error("Vosk Malayalam model not found!")
        return None
        
    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    with open(audio_file, "rb") as f:
        data = f.read()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return json.loads(result)["text"]
    return None



# Mock translation function (replace with MarianMT/Google API)
def translate_to_german(text, source_lang='ml'):
    st.header("Malayalam Speech to Text")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Speak in Malayalam (Online)"):
            audio_file = record_audio()
            text = transcribe_google(audio_file)
            if text:
                input_text = text
                st.experimental_rerun()

    with col2:
        if st.button("🎤 Speak in Malayalam (Offline)"):
            audio_file = record_audio()
            text = transcribe_vosk(audio_file)
            if text:
                input_text = text
                st.experimental_rerun()
        translations = {
            "ml": {
                "ഞാൻ സ്കൂളിൽ പോകുന്നു": "Ich gehe zur Schule",
                "എനിക്ക് വെള്ളം വേണം": "Ich brauche Wasser"
            }
        }
    return translations[source_lang].get(text, "Translation not available")

# Cleanup
if os.path.exists(AUDIO_FILE):
    os.remove(AUDIO_FILE)

# App layout
st.set_page_config(page_title="DeutschLern", layout="wide")

# Sidebar
with st.sidebar:
    st.header("Settings")
    native_lang = st.selectbox("Native Language", ["Malayalam", "Hindi", "Tamil"])
    level = st.selectbox("Proficiency Level", ["A1", "A2", "B1"])

# Main interface
st.title("🎓 DeutschLern Prototype")
tab1, tab2, tab3 = st.tabs(["Translate & Learn", "Grammar Coach", "Practice"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Speak/Writing {native_lang}")
        input_text = st.text_area("Enter text:", height=150)
        
        if st.button("Translate to German"):
            translated = translate_to_german(input_text)
            st.session_state.translation = translated
    
    with col2:
        st.subheader("German Translation & Feedback")
        if 'translation' in st.session_state:
            st.markdown(f"**Translation:** {st.session_state.translation}")
            
            feedback = get_grammar_feedback(st.session_state.translation)
            
            st.markdown("**Grammar Feedback:**")
            for error in feedback['errors']:
                st.error(f"⚠️ {error['message']}")
            
            st.divider()
            st.markdown("**Language Comparison:**")
            comp = feedback['comparison']
            df = pd.DataFrame({
                "Aspect": ["Sentence Structure", "Example"],
                "Malayalam": [comp['explanation'], comp['malayalam']],
                "German": ["SVO (Subject-Verb-Object)", comp['german_correct']]
            })
            st.dataframe(df.set_index('Aspect'), use_container_width=True)

with tab2:
    st.subheader("Grammar Concept Explorer")
    
    concept = st.selectbox("Choose concept", [
        "Word Order (SVO vs SOV)",
        "Noun Genders",
        "Case System"
    ])
    
    if concept == "Word Order (SVO vs SOV)":
        st.markdown("""
        **Comparison Table:**
        | Malayalam          | German              |
        |--------------------|---------------------|
        | Subject-Object-Verb | Subject-Verb-Object |
        
        **Example:**
        - Malayalam: ഞാൻ പുസ്തകം വായിക്കുന്നു (I book reading)
        - German: Ich lese das Buch (I read the book)
        """)
        
    elif concept == "Noun Genders":
        st.image("noun_genders_chart.png")  # Add actual image

with tab3:
    st.subheader("Interactive Practice")
    
    # Chat-style practice
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Try speaking in German..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mock AI response
        ai_response = "Good attempt! Remember to use the correct article: 'der Tisch' instead of 'das Tisch'"
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    st.divider()
    st.markdown("**Vocabulary Builder**")
    word = st.selectbox("Learn new words", ["Tisch (Table)", "Buch (Book)"])
    st.audio(f"{word}.mp3")  # Add actual audio files

# Video section
st.sidebar.divider()
st.sidebar.video("https://youtu.be/sample-german-lesson")  # Add actual video URL