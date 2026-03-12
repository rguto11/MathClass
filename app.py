import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
chave = os.getenv("API_GEMINI")

client = genai.Client(api_key=chave,
                      http_options={'api_version':'v1'})
modelo = "gemini-2.5-flash"

st.title("🎓 MathClass 2026")

pergunta = st.text_input("Faça uma pergunta matemática:")

if pergunta:
    try:
        response = client.models.generate_content(
            model=modelo,
            contents=pergunta
        )
        st.write("### Resposta do Tutor:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Erro: {e}")

