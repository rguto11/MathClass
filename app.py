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

modo = st.radio(
    "Qual tipo de professor você prefere?",
    ["Professor Tutor", "Professor Corretor"]
)

PROIBICAO ="""
    Você é o MathClass, um tutor de matemática que somente responde sobre matemática.
    Pode ser sobre história, conta, geometria, porém tudo ligado somente à matemática.
    Se tentarem perguntar sobre algo que não tem a ver com matemática, responda a seguinte frase:
    "Eu sou um professor de matemática, vc vai perder muita aura perguntando isso pra mim"        
"""

if modo == "Professor Tutor":
    instrucao = PROIBICAO + "Seja didático e explique passo a passo o exercício ou a dúvida em questão"
else:
    instrucao = PROIBICAO + "Seja didático, porém explique rapidamente o exercício para não perder muito tempo"


pergunta = st.text_input("Faça uma pergunta matemática:")

if pergunta:
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=pergunta,
            config={
                'system_instruction': instrucao  # Verifique se não há espaços antes/depois de 'system_instruction'
            }
        )
        st.write("### Resposta do Tutor:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Erro técnico: {e}")
