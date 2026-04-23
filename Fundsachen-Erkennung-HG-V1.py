import streamlit as st
import requests
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

headers = {
    "Authorization": "Bearer DEIN_API_KEY"
}

st.title("🔍 Fundsachen-Erkennung")

uploaded_file = st.file_uploader("📸 Bild hochladen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image)

    response = requests.post(
        API_URL,
        headers=headers,
        data=uploaded_file.getvalue()  # 🔥 wichtig!
    )

    if response.status_code != 200:
        st.error(f"Fehler: {response.status_code}")
        st.text(response.text)
    else:
        result = response.json()

        st.subheader("📌 Ergebnis:")
        st.write(result)
