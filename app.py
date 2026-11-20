import html
import time

import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator

st.set_page_config(page_title="Urdu ⇄ English Translator", page_icon="🌐")

MAX_CHARS = 1000  # MyMemory fallback has a smaller limit per request

DIRECTIONS = {
    "Urdu → English": ("ur", "en"),
    "English → Urdu": ("en", "ur"),
    "Hindi → English": ("hi", "en"),
    "English → Hindi": ("en", "hi"),
    "Urdu → Hindi": ("ur", "hi"),
    "Hindi → Urdu": ("hi", "ur"),
}

# Codes / names used by the MyMemory fallback service
MYMEMORY_CODES = {"ur": "ur-PK", "en": "en-GB", "hi": "hi-IN"}
MYMEMORY_NAMES = {"ur": "urdu", "en": "english", "hi": "hindi"}

RTL_LANGS = {"ur"}


def _google(text, source, target):
    last_error = None
    for attempt in range(2):
        try:
            return GoogleTranslator(source=source, target=target).translate(text)
        except Exception as exc:  # rate limit etc.
            last_error = exc
            time.sleep(1.5)
    raise last_error


def _mymemory(text, source, target):
    try:
        return MyMemoryTranslator(
            source=MYMEMORY_CODES[source], target=MYMEMORY_CODES[target]
        ).translate(text)
    except Exception:
        return MyMemoryTranslator(
            source=MYMEMORY_NAMES[source], target=MYMEMORY_NAMES[target]
        ).translate(text)


@st.cache_data(show_spinner=False, ttl=3600)
def translate(text: str, source: str, target: str) -> str:
    errors = []
    for backend in (_google, _mymemory):
        try:
            result = backend(text, source, target)
            if result and result.strip():
                return result
        except Exception as exc:
            errors.append(f"{backend.__name__}: {exc}")
    raise RuntimeError(" | ".join(errors) or "No translation returned")


st.title("🌐 Urdu ⇄ English Translator")
st.caption("Simple NLP translation app built with Streamlit")

direction = st.selectbox("Translation direction", list(DIRECTIONS.keys()))
source, target = DIRECTIONS[direction]

text = st.text_area(
    "Enter text",
    height=160,
    max_chars=MAX_CHARS,
    placeholder="یہاں اپنا متن لکھیں / Type your text here",
)
st.caption("Tip: the text must be in the language you picked as the source.")

if st.button("Translate", type="primary"):
    cleaned = text.strip()
    if not cleaned:
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Translating..."):
                result = translate(cleaned, source, target)
            st.subheader("Translation")
            direction_css = "rtl" if target in RTL_LANGS else "ltr"
            align = "right" if target in RTL_LANGS else "left"
            st.markdown(
                f"<div dir='{direction_css}' style='text-align:{align};"
                f"font-size:1.3rem;padding:0.8rem;border:1px solid #8884;"
                f"border-radius:8px;'>{html.escape(result)}</div>",
                unsafe_allow_html=True,
            )
            st.code(result, language=None)
        except Exception as exc:
            st.error("Translation service is busy right now. Please wait a few seconds and try again.")
            st.caption(f"Details: {exc}")

st.divider()
st.caption("Note: Balochi is not supported by the translation services, so Urdu, English and Hindi are offered.")
