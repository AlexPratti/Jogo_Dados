import streamlit as st
import time
import random
import os

# Configuração da página
st.set_page_config(page_title="Jogo dos Blocos", layout="centered")
st.title("🧩 Jogo dos Blocos")

# 1. GERENCIAMENTO DO DICIONÁRIO DE FIGURAS
if "dicionario_figuras" not in st.session_state:
    st.session_state.dicionario_figuras = {
        "fig_1": "Escada",
        "fig_2": "Bola",
        "fig_3": "Carro",
        "fig_4": "Árvore",
        "fig_5": "Casa"
    }

# Inicializa a lista de controle para evitar repetições consecutivas
if "imagens_restantes" not in st.session_state:
    st.session_state.imagens_restantes = []

# Cria as três abas de gerenciamento na barra lateral
st.sidebar.header("⚙️ Painel de Controle")
aba_cadastro, aba_editar, aba_lista = st.sidebar.tabs(["➕ Cadastrar", "✏️ Editar Nomes", "📋 Ver Todas"])

# ABA 1: Cadastrar nova figura
with aba_cadastro:
    st.write("### Adicionar Nova Figura")
    novo_id = st.text_input("Nome do arquivo (Ex: fig_6):").strip()
    novo_nome_real = st.text_input("O que é a figura? (Ex: Cadeira):").strip()

    if st.button("Adicionar ao Jogo", use_container_width=True):
        if novo_id and novo_nome_real:
            if novo_id not in st.session_state.dicionario_figuras:
                st.session_state.dicionario_figuras[novo_id] = novo_nome_real
                # Força recriação da lista de sorteio para incluir a nova imagem
                st.session_state.imagens_restantes = [] 
                st.success(f"Adicionado! {novo_id}.png = '{novo_nome_real}'")
                st.rerun()
            else:
                st.warning("Este ID de arquivo já está cadastrado.")
        else:
            st.error("Preencha ambos os campos!")

# ABA 2: EDITAR OS NOMES EXISTENTES (Atualização Instantânea)
with aba_editar:
    st.write("### Modificar Nomes Atuais")
    st.caption("Os nomes são atualizados nos botões assim que você digita.")
    
    mudou = False
    for arquivo_id, nome_atual in list(st.session_state.dicionario_figuras.items()):
        novo_nome = st.text_input(
            f"Nome para {arquivo_id}.png:", 
            value=nome_atual, 
            key=f"edit_{arquivo_id}"
        ).strip()
        
        if novo_nome != nome_atual:
            st.session_state.dicionario_figuras[arquivo_id] = novo_nome
            mudou = True
            
    if mudou:
        st.session_state.jogo_ativo = False
        st.rerun()

# ABA 3: Visualizar a lista atual de relações
with aba_lista:
    st.write("### Relação Atual:")
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
    st.session_state.figura_atual = None 
if "status_jogada" not in st.session_state:
    st.session_state.status_jogada = None


# 3. FUNÇÃO PARA INICIAR NOVA RODADA SEM REPETIÇÃO
def iniciar_rodada():
    todas_chaves = list(st.session_state.dicionario_figuras.keys())
    
    # Se a lista de figuras restantes estiver vazia, recarrega com todas as opções disponíveis
    if not st.session_state.imagens_restantes or any(img not in todas_chaves for img in st.session_state.imagens_restantes):
        st.session_state.imagens_restantes = todas_chaves.copy()
        random.shuffle(st.session_state.imagens_restantes)
        
    # Remove a última figura da lista embaralhada para jogar na rodada corrente
    st.session_state.figura_atual = st.session_state.imagens_restantes.pop()
    st.session_state.posicao_y = 0
    st.session_state.jogo_ativo = True
    st.session_state.status_jogada = None


# 4. INTERFACE PRINCIPAL E PLACAR
st.subheader(f"Pontuação: {st.session_state.score} pontos")

# Mostra informações sobre o ciclo atual de imagens no modo de desenvolvimento/teste se desejar
restantes_count = len(st.session_state.imagens_restantes)
totais_count = len(st.session_state.dicionario_figuras)
if st.session_state.jogo_ativo:
    st.caption(f"Imagens restantes neste ciclo: {restantes_count + 1} de {totais_count}")

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
        st.warning("Arquivo 'emogi.png' não encontrado no seu repositório GitHub.")


# 5. LÓGICA DO JOGO EM ANDAMENTO
if st.session_state.jogo_ativo and st.session_state.figura_atual:
    
    st.write("---")
    st.write("### Clique no nome correto da figura que está caindo:")
    
    # Criar botões dinâmicos com os nomes em colunas
    colunas = st.columns(len(st.session_state.dicionario_figuras))
    
    for idx, (arquivo_id, nome_real) in enumerate(st.session_state.dicionario_figuras.items()):
        with colunas[idx]:
            if st.button(nome_real, key=f"btn_{arquivo_id}_{nome_real}", use_container_width=True):
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
        # ALTERAÇÃO AQUI: o passo mudou de 12 para 6 para a queda acontecer na metade da velocidade anterior
        for y in range(st.session_state.posicao_y, 300, 6):
            st.session_state.posicao_y = y
            with container_queda.container():
                st.markdown(f"<div style='height:{y}px;'></div>", unsafe_allow_html=True)
                st.image(caminho_imagem, width=130)
            time.sleep(0.15) 
            
        # Perda por tempo
        st.session_state.score -= 5
        st.session_state.status_jogada = "errou"
        st.session_state.jogo_ativo = False
        st.rerun()
        
    else:
        nome_da_figura_com_erro = st.session_state.dicionario_figuras[st.session_state.figura_atual]
        st.error(f"Erro: O arquivo '{caminho_imagem}' correspondente a '{nome_da_figura_com_erro}' não foi encontrado no seu GitHub.")
        st.session_state.jogo_ativo = False
