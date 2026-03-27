import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
chave = st.secrets.get("API_GEMINI") or os.getenv("API_GEMINI")

# chamando a chave e o modelo
client = genai.Client(api_key=chave,
                      http_options={'api_version':'v1'})
modelo = "gemini-2.5-flash"

#organizando a pagina
col_esq, col_meio, col_dir = st.columns([1, 2, 1])

with col_esq:
    # Foto da Frente
    st.image("frente.png", use_container_width=True)

with col_meio:
    # Título centralizado verticalmente e horizontalmente
    # Adicionei uns <br> para dar um espaço no topo e alinhar com as imagens
    st.markdown("<br><h1 style='text-align: center; font-size: 40px;'>MathClass</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Tutor de matemática</p>", unsafe_allow_html=True)

with col_dir:
    # Foto do Verso
    st.image("verso.png", use_container_width=True)

st.divider()

#clasificando o tipo de professor
modo = st.radio(
    "Qual tipo de professor você prefere?",
    ["Professor tutor", "Professor corretor"]
)

#ensinando oq ele é
PROIBICAO ="""
    Você é o MathClass, um tutor de matemática que somente responde sobre matemática.
    Pode ser sobre história, conta, geometria, porém tudo ligado somente à matemática.
    Se tentarem perguntar sobre algo que não tem a ver com matemática, responda a seguinte frase:
    "Eu sou um professor de matemática, vc vai perder muita aura perguntando isso pra mim"        
"""

#clasificando os modos
if modo == "Professor Tutor":
    instrucao = PROIBICAO + "Seja didático e explique passo a passo o exercício ou a dúvida em questão"
else:
    instrucao = PROIBICAO + "Seja didático, porém explique rapidamente o exercício para não perder muito tempo"

# mandar foto pra explicação
foto_arquivo = st.file_uploader("Ou envie uma foto da sua conta no caderno:", type=["png", "jpg", "jpeg"])


#lista pra salvar as conversas e as conversas tbm
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Diga algo para o MathClass...")



if pergunta:
    # salva a pergunta do usuário no histórico
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    
    try:
        # qual tipo de professor escolhido
        conteudo_para_envio = [instrucao]
        
        # adicionando todas as mensagens do histórico
        for m in st.session_state.mensagens:
            conteudo_para_envio.append(f"{m['role']}: {m['content']}")
        
        #adicionando a foto por ultimo para analisar o contexto
        if foto_arquivo:
            img = Image.open(foto_arquivo)
            conteudo_para_envio.append(img)

        #resposta do modelo
        response = client.models.generate_content(
            model=modelo,
            contents=conteudo_para_envio
        )
        
        resposta_professor = response.text
        
        # Salva a resposta do professor para ele lembrar
        st.session_state.mensagens.append({"role": "assistant", "content": resposta_professor})
        
        # força a recarregar pra mostrar as mensagens novas
        st.rerun()

    except Exception as e:
        st.error(f"Erro: {e}")


if st.button("Limpar conversa / tirar novas dúvidas"):
    st.session_state.mensagens = []
    st.rerun()