import html

import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Urdu ⇄ English Translator", page_icon="🌐")

MAX_CHARS = 4500

DIRECTIONS = {
    "Urdu → English": ("ur", "en"),
    "English → Urdu": ("en", "ur"),
    "Hindi → English": ("hi", "en"),
    "English → Hindi": ("en", "hi"),
    "Urdu → Hindi": ("ur", "hi"),
    "Hindi → Urdu": ("hi", "ur"),
}

RTL_LANGS = {"ur"}


def translate(text: str, source: str, target: str) -> str:
    return GoogleTranslator(source=source, target=target).translate(text)


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

if st.button("Translate", type="primary"):
    cleaned = text.strip()
    if not cleaned:
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Translating..."):
                result = translate(cleaned, source, target)
            if not result:
                st.error("No translation returned. Please try different text.")
            else:
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
            st.error(
                "Translation failed. Check your internet connection and try again."
            )
            st.caption(f"Details: {exc}")

st.divider()
st.caption("Note: Balochi is not supported by the translation service, so Urdu, English and Hindi are offered.")
