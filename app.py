import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import random

# --- ESTILIZAÇÃO E LOGO EASYIMOB (Identidade 360°) ---
st.set_page_config(page_title="EasyImob - Ecossistema Imobiliário 360°", layout="wide", page_icon="🏢")

# Cores da Identidade Visual (Degradê Turquesa/Verde Água)
primary_color = "#00C2CB" # Turquesa
secondary_color = "#00E676" # Verde Água
text_color = "#1F2937" # Cinza Escuro
bg_color = "#F9FAFB" # Cinza Muito Claro

st.markdown(f"""
    <style>
    /* Estilização Geral */
    .main {{ background-color: {bg_color}; color: {text_color}; font-family: 'Helvetica Neue', sans-serif; }}
    
    /* Logo EasyImob no Topo */
    .logo-container {{
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .logo-text {{ color: white; font-size: 3rem; font-weight: bold; margin: 0; display: flex; align-items: center; justify-content: center; gap: 15px; }}
    .logo-icon {{ font-size: 3.5rem; }}
    .logo-subtext {{ color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-top: -5px; }}

    /* Botões Customizados */
    .stButton>button {{
        width: 100%; border-radius: 10px;
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        color: white; font-weight: bold; border: none; padding: 12px; transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ box-shadow: 0 4px 10px rgba(0,194,203,0.3); transform: translateY(-2px); }}

    /* Métricas e Cards */
    .stMetric {{ background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border-left: 5px solid {primary_color}; }}

    /* Estilo do Chat */
    .message-bubble {{ padding: 10px 15px; border-radius: 10px; margin-bottom: 8px; width: fit-content; max-width: 80%; }}
    .message-empresa {{ background-color: #E0F7FA; align-self: flex-end; }}
    .message-locatario {{ background-color: #F1F8E9; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER COM LOGO ---
st.markdown(f"""
    <div class="logo-container">
        <div class="logo-text">
            <span class="logo-icon">🏢</span>
            <span>EasyImob</span>
        </div>
        <div class="logo-subtext">Ecossistema Imobiliário 360° [MODO DEMO]</div>
    </div>
    """, unsafe_allow_html=True)

# --- MENU LATERAL DE NAVEGAÇÃO LIVRE ---
st.sidebar.markdown(f"""<div style='text-align: center; color: {primary_color}; font-size: 1.8rem; font-weight: bold;'>🏢 EasyImob Pro</div>""", unsafe_allow_html=True)

perfil = st.sidebar.radio("Alternar Visão do App:", ["Empresa (Administrador)", "Locatário (Cliente)"])

if perfil == "Empresa (Administrador)":
    menu = ["📊 Dashboard 360°", "🔍 Vistoria IA", "🛠️ Reparos & Chat Enterprise", "💰 Financeiro Autônomo", "🔑 Chaves IoT"]
else:
    menu = ["🏠 Meu Smart Home", "🛠️ Central de Ajuda", "💵 Pagamentos & Recibos"]
    
choice = st.sidebar.selectbox("Módulos do Sistema", menu)

# =========================================================================
# --- VISÃO EMPRESA (ADMIN) ---
# =========================================================================
if perfil == "Empresa (Administrador)":

    if choice == "📊 Dashboard 360°":
        st.title("Painel de Controle Integrado")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Imóveis Ativos", "124", "+3 novos")
        c2.metric("Vistorias/Mês", "45", "10% crescimento")
        c3.metric("Reparos Abertos", "8", "-2 concluídos")
        c4.metric("Receita PIX (Mês)", "R$ 42.500", "15% aumento")
        
        st.subheader("Gráfico de Ocupação e Rendimentos")
        chart_data = pd.DataFrame({'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'], 'Receita (R$)': [31000, 35000, 38000, 40000, 42500]})
        st.line_chart(chart_data.set_index('Mês'))

    elif choice == "🔍 Vistoria IA":
        st.title("Módulo de Vistoria 360°")
        col_d, col_v = st.columns(2)
        
        with col_d:
            st.subheader("Captura com Simulador de GPS e IA")
            st.success("GPS Autenticado via Satélite: -23.55052, -46.633308 (São Paulo/SP)")
            
            imovel_id = st.text_input("Código do Imóvel", value="AP-402")
            comodo = st.selectbox("Cômodo Analisado", ["Sala de Estar", "Cozinha", "Quarto Principal", "Banheiro"])
            foto = st.file_uploader("Envie uma foto do cômodo para simular a IA", type=['jpg','png','jpeg'])
            
            if foto:
                st.info("🤖 Inteligência Artificial EasyImob analisando imagem...")
                reparos = ["Pintura descascando na parede lateral", "Rachadura superficial no teto", "Mofo detectado próximo à janela", "Vidro da janela trincado"]
                st.warning(f"**Resultado da IA:** {random.choice(reparos)}")
            
            if st.button("Finalizar e Validar Vistoria Juridicamente"):
                st.balloons()
                st.success("Vistoria salva com sucesso no ecossistema 360°!")

        with col_v:
            st.subheader("Relatórios Emitidos recentemente")
            with st.expander("Vistoria AP-402 - Realizada Hoje"):
                st.write("**Cômodo:** Sala de Estar")
                st.write("**Status:** Necessita reparo na pintura")
                st.write("**Autenticação:** Carimbo de Tempo e Coordenadas GPS inclusos.")
                st.button("Baixar PDF Demonstrativo")

    elif choice == "🛠️ Reparos & Chat Enterprise":
        st.title("Central de Manutenção Enterprise")
        st.write("Histórico de chamados de manutenção ativos:")
        
        df_chamados = pd.DataFrame({
            'ID': [101, 102],
            'Imóvel': ['AP-402', 'CASA-12'],
            'Problema': ['Vazamento na Cozinha', 'Disjuntor caindo'],
            'Status': ['Em atendimento', 'Aberto']
        })
        st.table(df_chamados)
        
        st.subheader("Chat em Tempo Real com o Locatário")
        st.markdown('<div class="message-bubble message-locatario"><b>Locatário (João):</b> Olá, o encanador já está vindo? O vazamento aumentou.</div>', unsafe_allow_html=True)
        st.markdown('<div class="message-bubble message-empresa"><b>Imobiliária (Você):</b> Sim João, o técnico parceiro já está a caminho do AP-402. Estima-se 20 minutos.</div>', unsafe_allow_html=True)
        st.text_input("Digite sua resposta...", placeholder="Enviar mensagem para o inquilino...")

    elif choice == "💰 Financeiro Autônomo":
        st.title("Gestão Financeira com PIX Automático")
        st.subheader("Lançar Novo Aluguel")
        st.text_input("E-mail do Inquilino", value="joao.silva@email.com")
        st.number_input("Valor do Aluguel (R$)", value=2500.0)
        st.date_input("Data de Vencimento")
        if st.button("Gerar Link de Pagamento e PIX"):
            st.success("Cobrança criada via API de Pagamentos! Link gerado: https://easyimob.co/p/pay_demo")

    elif choice == "🔑 Chaves IoT":
        st.title("Gestão de Acessos IoT (Smart Key System)")
        st.write("Controle chaves digitais para prestadores de serviço entrarem nos imóveis.")
        st.text_input("E-mail do Prestador (ex: Eletricista)", value="pedro.reparos@email.com")
        if st.button("Gerar Token Temporário"):
            st.code("TOKEN DE ACESSO: KEY-8842-X", language="text")
            st.success("Chave digital enviada por SMS e ativa por 4 horas na fechadura digital Intelbras/Yale.")

# =========================================================================
# --- VISÃO LOCATÁRIO (CLIENTE) ---
# =========================================================================
else:
    st.title("Portal do Locatário EasyImob")
    
    if choice == "🏠 Meu Smart Home":
        st.subheader("Seu Imóvel Ativo: Apartamento 402 - Bloco B")
        st.write("Gerencie as funções integradas da sua casa.")
        if st.button("🔓 Destrancar Porta Principal (Via Aplicativo)"):
             st.success("Comando enviado! Porta destrancada via Bluetooth/Wi-Fi.")

    elif choice == "🛠️ Central de Ajuda":
        st.subheader("Solicitar Novo Reparo")
        st.selectbox("Qual o problema?", ["Problema Elétrico", "Problema Hidráulico", "Chave/Fechadura Danificada", "Outros"])
        st.text_area("Descreva detalhadamente o ocorrido...")
        if st.button("Abrir Chamado Técnico"):
            st.success("Chamado aberto! A imobiliária foi notificada no painel administrativo.")

    elif choice == "💵 Pagamentos & Recibos":
        st.subheader("Suas Cobranças")
        col_p1, col_p2 = st.columns([3, 1])
        col_p1.warning("Aluguel Competência Atual - Vencimento em 5 dias: **R$ 2.500,00**")
        col_p2.button("Pagar com PIX Agora ✅")
