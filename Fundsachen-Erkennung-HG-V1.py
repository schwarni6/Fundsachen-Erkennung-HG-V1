import streamlit as st
import requests
from PIL import Image

# 👉 Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

# 👉 Optional: eigenen API Key eintragen (empfohlen!)
headers = {
    "Authorization": "Bearer DEIN_API_KEY"  # <- hier deinen Token rein
}

st.set_page_config(page_title="Fundsachen KI", page_icon="🔍")

st.title("🔍 Fundsachen-Erkennung")
st.write("Lade ein Bild hoch und die KI erkennt den Gegenstand.")

uploaded_file = st.file_uploader("📸 Bild hochladen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)

    with st.spinner("⏳ KI analysiert das Bild..."):
        response = requests.post(
            API_URL,
            headers=headers,
            files={"file": uploaded_file}
        )

    # ❗ Fehlerbehandlung
    if response.status_code == 503:
        st.warning("⏳ Modell lädt gerade. Bitte in ein paar Sekunden nochmal versuchen.")
    
    elif response.status_code != 200:
        st.error(f"❌ Fehler: {response.status_code}")
        st.text(response.text)

    else:
        try:
            result = response.json()

            # Top 3 Ergebnisse anzeigen
            st.subheader("📌 Ergebnisse:")

            for i in range(min(3, len(result))):
                label = result[i]["label"]
                score = result[i]["score"]

                st.success(f"{i+1}. {label}")
                st.write(f"🔎 Sicherheit: {score * 100:.2f}%")

        except Exception:
            st.error("❌ Antwort konnte nicht verarbeitet werden")
            st.text(response.text)
