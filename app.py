import streamlit as st
import time
import random
import os

# Configuração da página
st.set_page_config(page_title="Jogo dos Blocos", layout="centered")
st.title("🧩 Jogo dos Blocos")

# 1. GERENCIAMENTO DO DICIONÁRIO DE FIGURAS (Arquivo vs Nome Real)
# Inicializa o dicionário padrão no estado da sessão
if "dicionario_figuras" not in st.session_state:
    st.session_state.dicionario_figuras = {
        "fig_1": "Escada",
        "fig_2": "Bola",
        "fig_3": "Carro",
        "fig_4": "Árvore",
        "fig_5": "Casa"
    }

# Cria as abas (Tabs) na barra lateral para organizar
st.sidebar.header("⚙️ Painel de Controle")
aba_cadastro, aba_lista = st.sidebar.tabs(["➕ Cadastrar", "📋 Figuras Ativas"])

with aba_cadastro:
    st.write("### Adicionar Nova Figura")
    novo_id = st.text_input("Nome do arquivo (Ex: fig_6):").strip()
    novo_nome_real = st.text_input("O que é a figura? (Ex: Cadeira):").strip()

    if st.button("Adicionar ao Jogo", use_container_width=True):
        if novo_id and novo_nome_real:
            if novo_id not in st.session_state.dicionario_figuras:
                st.session_state.dicionario_figuras[novo_id] = novo_nome_real
                st.success(f"Adicionado! {novo_id}.png corresponderá a '{novo_nome_real}'")
                st.rerun()
            else:
                st.warning("Este ID de arquivo já está cadastrado.")
        else:
            st.error("Preencha ambos os campos!")

with aba_lista:
    st.write("### Relação Atual:")
    # Exibe visualmente a tabela de correspondência
    for arquivo, nome_real in st.session_state.dicionario_figuras.items():
        st.text(f"📄 {arquivo}.png ➔ 🏷️ {nome_real}")


# 2. INICIALIZAÇÃO DAS VARIÁVEIS DE JOGO
if "score" not in st.session_state:
    st.session_state.score = 0
if "jogo_ativo" not in st.session_state:
    st.session_state.jogo_ativo = False
if "posicao_y" not in st.session_state:
    st.session_state.posicao_y = 0
if "figura_atual" not in st.session_state:
    st.session_state.figura_atual = None # Guarda a chave (Ex: 'fig_1')
if "status_jogada" not in st.session_state:
    st.session_state.status_jogada = None


# 3. FUNÇÃO PARA INICIAR NOVA RODADA
def iniciar_rodada():
    # Sorteia uma das chaves do dicionário
    chaves_disponiveis = list(st.session_state.dicionario_figuras.keys())
    st.session_state.figura_atual = random.choice(chaves_disponiveis)
    st.session_state.posicao_y = 0
    st.session_state.jogo_ativo = True
    st.session_state.status_jogada = None


# 4. INTERFACE PRINCIPAL E PLACAR
st.subheader(f"Pontuação: {st.session_state.score} pontos")

# Botão de Start
if not st.session_state.jogo_ativo:
    if st.button("▶️ START", use_container_width=True):
        iniciar_rodada()
        st.rerun()

# Feedback Visual
if st.session_state.status_jogada == "acertou":
    st.success("💥 ACERTOU! A figura explodiu! (+10 pontos)")
    st.balloons()
elif st.session_state.status_jogada == "errou":
    st.error("😢 ERROU! (-5 pontos)")
    if os.path.exists("emogi.png"):
        st.image("emogi.png", width=150, caption="Tente novamente")
    else:
        st.warning("Arquivo 'emogi.png' não encontrado no repositório GitHub.")


# 5. LÓGICA DO JOGO EM ANDAMENTO
if st.session_state.jogo_ativo and st.session_state.figura_atual:
    
    st.write("---")
    st.write("### Clique no nome correto da figura que está caindo:")
    
    # Criar botões com os NOMES REAIS (valores do dicionário)
    colunas = st.columns(len(st.session_state.dicionario_figuras))
    
    # Varre o dicionário para criar um botão para cada nome real
    for idx, (arquivo_id, nome_real) in enumerate(st.session_state.dicionario_figuras.items()):
        with colunas[idx]:
            if st.button(nome_real, key=f"btn_{arquivo_id}", use_container_width=True):
                # O acerto verifica se o arquivo_id do botão é o mesmo sorteado
                if arquivo_id == st.session_state.figura_atual:
                    st.session_state.score += 10
                    st.session_state.status_jogada = "acertou"
                else:
                    st.session_state.score -= 5
                    st.session_state.status_jogada = "errou"
                
                st.session_state.jogo_ativo = False
                st.rerun()

    st.write("---")
    
    # Animação de queda da imagem
    container_queda = st.empty()
    caminho_imagem = f"{st.session_state.figura_atual}.png"
    
    if os.path.exists(caminho_imagem):
        for y in range(st.session_state.posicao_y, 300, 12):
            st.session_state.posicao_y = y
            with container_queda.container():
                st.markdown(f"<div style='height:{y}px;'></div>", unsafe_allow_html=True)
                st.image(caminho_imagem, width=130)
            time.sleep(0.15) 
            
        # Perda por tempo (se chegar ao final do limite de pixels sem clicar)
        st.session_state.score -= 5
        st.session_state.status_jogada = "errou"
        st.session_state.jogo_ativo = False
        st.rerun()
        
    else:
        st.error(f"Erro: O arquivo '{caminho_imagem}' correspondente a '{st.session_state.dicionario_figuras[st.session_state.figura_atual]}' não foi encontrado no seu GitHub.")
        st.session_state.jogo_ativo = False
