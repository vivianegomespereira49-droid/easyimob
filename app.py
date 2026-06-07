import sys
import asyncio

# Corrige o bug de conexão perdida (WinError 10054) no Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
import streamlit as st
from supabase import create_client, Client
import pandas as pd
from fpdf import FPDF
import datetime
import hashlib
import json
import requests
# Requer: pip install streamlit-js-eval requests Pillow fpdf2 google-generativeai
from streamlit_js_eval import get_geolocation

# =========================================================================
# --- CONFIGURAÇÕES DO EASYIMOB & STACK TECNOLÓGICO ---
# =========================================================================

# --- CONFIGURAÇÕES DE ACESSO AO BANCO DE DADOS (SUPABASE) ---
# Substitua com suas chaves reais do Supabase (Project Settings -> API)
URL = "ykditqjxulxnmkwkukzb"
KEY = "ykditqjxulxnmkwkukzb"
supabase: Client = create_client(URL, KEY)

# --- ESTILIZAÇÃO E LOGO EASYIMOB (Identidade 360°) ---
# Stack: Streamlit (Frontend/Interface gráfica Python)
st.set_page_config(page_title="EasyImob - Ecossistema Imobiliário 360°", layout="wide", page_icon="🏢")

# Cores da Identidade Visual (Degradê Turquesa/Verde Água)
primary_color = "#00C2CB" # Turquesa
secondary_color = "#00E676" # Verde Água
text_color = "#1F2937" # Cinza Escuro
bg_color = "#F9FAFB" # Cinza Muito Claro

# Estilização CSS personalizada para interface moderna
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

# =========================================================================
# --- MÓDULOS & FUNÇÕES DE ELITE (HELPER FUNCTIONS) ---
# =========================================================================

# --- MÓDULO DE AUTENTICAÇÃO SEGURA ---
# Stack: Supabase Auth + SHA-256 criptografia
def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- MÓDULO DE RELATÓRIOS (PDF GENERATOR) ---
# Stack: FPDF2 (Geração programática de arquivos PDF)
def gerar_pdf_vistoria(dados):
    """Gera PDF completo com carimbo GPS e Tempo"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 194, 203) # Cor da marca
    pdf.cell(0, 15, "EASYIMOB - RELATÓRIO 360°", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(31, 41, 55)
    for k, v in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, f"{k}:", 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f" {v}", 1, 1)
    
    # Adiciona aviso legal de validação GPS (Validação Jurídica)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 8, f"Relatório validado juridicamente via georreferenciamento em {dados['Data']}. GPS: {dados['GPS']}.")
    
    fn = f"vistoria_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    pdf.output(fn)
    return fn

# --- MÓDULO DE INTELIGÊNCIA ARTIFICIAL (IA VISTORIA) ---
# Stack: Gemini Pro Vision (Google AI) integrado via API
def simular_ia_vistoria(imagem, comodo):
    """Simula análise de Visão Computacional"""
    # Em produção, usaria API do Gemini ou GPT-4 Vision
    reparos = ["Pintura descascando", "Rachadura superficial", "Mofo detectado", "Taco solto", "Vidro trincado"]
    import random
    return f"IA Diagnosticou em '{comodo}': {random.choice(reparos)}."

# --- MÓDULO FINANCEIRO AUTÔNOMO (PIX AUTOMÁTICO) ---
# Stack: API Asaas (Integração de pagamento via REST API com requests)
def simular_pagamento_pix(valor, vencimento, usuario):
    """Simula integração com Asaas para gerar link PIX"""
    # Em produção, usaria requests.post(F"{ASAAS_URL}/payments", json=payload, headers=headers)
    asaas_id = f"pay_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Link simulado para o painel do cliente
    link = f"https://easyimob.co/p/{asaas_id}" 
    return link, asaas_id

# --- HEADER COM LOGO ---
st.markdown(f"""
    <div class="logo-container">
        <div class="logo-text">
            <span class="logo-icon">🏢</span>
            <span>EasyImob</span>
        </div>
        <div class="logo-subtext">Ecossistema Imobiliário 360°</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
# --- INTERFACE PRINCIPAL & LÓGICA DO APLICATIVO ---
# =========================================================================

# Inicializa estado da sessão de login
if 'logged_in' not in st.session_state:
    st.session_state.update({'logged_in': False, 'user': None, 'tipo': None})

# --- SISTEMA DE LOGIN E CADASTRO ---
if not st.session_state['logged_in']:
    tab_in, tab_reg = st.tabs(["Acessar EasyImob", "Novo Locatário"])
    
    with tab_in:
        u = st.text_input("Usuário/E-mail")
        p = st.text_input("Senha", type='password')
        if st.button("Entrar no EasyImob"):
            res = supabase.table('usuarios').select("*").eq('user_id', u).execute()
            if res.data and res.data[0]['password'] == hash_pw(p):
                st.session_state.update({'logged_in': True, 'user': u, 'tipo': res.data[0]['tipo']})
                st.rerun()
            else: st.error("Dados incorretos ou conta inexistente.")

    with tab_reg:
        nu = st.text_input("Crie seu Usuário/E-mail")
        np = st.text_input("Crie sua Senha", type='password')
        if st.button("Registrar Conta"):
            supabase.table('usuarios').insert({"user_id": nu, "password": hash_pw(np), "tipo": "Locatário"}).execute()
            st.success("Conta criada! Faça login na aba ao lado.")

else:
    # --- BARRA LATERAL (SIDEBAR NAVIGATION) ---
    st.sidebar.markdown(f"""<div style='text-align: center; color: {primary_color}; font-size: 2rem; font-weight: bold;'>🏢 EasyImob Pro</div>""", unsafe_allow_html=True)
    st.sidebar.write(f"Conectado: **{st.session_state['user']}** ({st.session_state['tipo']})")
    
    # Menu dinâmico baseado no perfil do usuário
    if st.session_state['tipo'] == 'Empresa':
        menu = ["📊 Dashboard 360°", "🔍 Vistoria IA", "🛠️ Reparos & Chat Enterprise", "💰 Financeiro Autônomo", "🔑 Chaves IoT"]
    else:
        menu = ["🏠 Meu Smart Home", "🛠️ Central de Ajuda", "💵 Pagamentos & Recibos"]
        
    choice = st.sidebar.selectbox("Navegação Integrada", menu)

    # =========================================================================
    # --- VISÃO EMPRESA (ADMIN) ---
    # =========================================================================
    if st.session_state['tipo'] == 'Empresa':

        if choice == "📊 Dashboard 360°":
            st.title("Painel de Controle Integrado")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Imóveis", "124", "+3")
            c2.metric("Vistorias/Mês", "45", "10%")
            c3.metric("Reparos Abertos", "8", "-2")
            c4.metric("Receita PIX", "R$ 42k", "15%")
            
            # Gráfico de Projeção de Ganhos
            chart_data = pd.DataFrame([10, 15, 8, 22], columns=['Receita'])
            st.line_chart(chart_data)

        elif choice == "🔍 Vistoria IA":
            st.title("Módulo de Vistoria 360°")
            col_d, col_v = st.columns(2)
            
            with col_d:
                st.subheader("Captura com GPS e IA")
                # MÓDULO DE GPS (Obrigatória para validação jurídica)
                loc = get_geolocation()
                if loc:
                    gps_coords = f"{loc['coords']['latitude']}, {loc['coords']['longitude']}"
                    st.success(f"GPS Autenticado: {gps_coords}")
                    
                    # Identificação e Captura
                    imovel_id = st.text_input("Cód. Imóvel", key="imov_vis")
                    comodo = st.selectbox("Cômodo", ["Sala", "Cozinha", "Quarto 1", "Banheiro", "Sacada"])
                    foto = st.camera_input("Tirar foto para análise")
                    
                    if foto:
                        diagnostico = simular_ia_vistoria(foto, comodo)
                        st.warning(diagnostico)
                        
                        if st.button("Finalizar Vistoria Validada"):
                            supabase.table('vistorias').insert({
                                "imovel_id": imovel_id,
                                "vistoriador_id": st.session_state['user'],
                                "coordenadas_gps": gps_coords,
                                "comodo": comodo,
                                "diagnostico_ia": diagnostico
                            }).execute()
                            st.success("Vistoria salva na nuvem EasyImob!")
                else:
                    st.warning("⚠️ Aguardando permissão do navegador para GPS (Obrigatório).")

            with col_v:
                st.subheader("Gerar Relatório PDF Certificado")
                # Buscaria as últimas vistorias no Supabase
                st.write("Lista de vistorias recentes...")

        elif choice == "🛠️ Reparos & Chat Enterprise":
            st.title("Central de Manutenção Enterprise")
            st.write("Gestão de chamados de reparo com chat integrado.")
            # Carregar chamados abertos no Supabase

        elif choice == "💰 Financeiro Autônomo":
            st.title("Gestão Financeira com PIX Automático")
            # MÓDULO FINANCEIRO (Automação de cobrança via API Asaas)
            st.subheader("Lançar Aluguel com PIX")
            with st.form("gerar_cobranca"):
                u_loc = st.text_input("E-mail do Locatário (EasyImob User)")
                valor = st.number_input("Valor Aluguel", min_value=0.0)
                venc = st.date_input("Vencimento")
                
                if st.form_submit_button("Gerar PIX"):
                    # Simula a integração com Asaas
                    link, asaas_id = simular_pagamento_pix(valor, venc, u_loc)
                    
                    supabase.table('financeiro').insert({
                        "usuario": u_loc,
                        "valor": valor,
                        "vencimento": str(venc),
                        "link_pagamento": link,
                        "asaas_id": asaas_id,
                        "status": "Aguardando Pagamento"
                    }).execute()
                    st.success(f"Cobrança gerada! Asaas ID: {asaas_id}")

        elif choice == "🔑 Chaves IoT":
            st.title("Gestão de Acessos IoT (Smart Key System)")
            # MÓDULO IOT (Simula envio de comando para fechaduras inteligentes viarequests)
            st.write("Gere acessos temporários para prestadores.")
            prest = st.text_input("E-mail do Prestador")
            if st.button("Gerar Token de Acesso"):
                st.success(f"Token 'AC-9921-X' gerado e enviado para {prest}. Válido por 4h.")
                st.balloons()

    # =========================================================================
    # --- VISÃO LOCATÁRIO (CLIENTE) ---
    # =========================================================================
    else:
        st.title("Portal do Locatário EasyImob")
        if choice == "🏠 Meu Smart Home":
            st.write("Acompanhe seus dados, contratos e controle IoT do imóvel.")
            if st.button("Abrir Porta Principal (Via App)"):
                 st.success("Porta aberta via Bluetooth/Wi-Fi")

        elif choice == "🛠️ Central de Ajuda":
            st.write("Solicitar reparos e acompanhar a resolução com chat de manutenção.")
            # Abrir chamado de reparo no Supabase

        elif choice == "💵 Pagamentos & Recibos":
            st.write("Acompanhar pagamentos de aluguéis e taxas com PIX integrado.")
            # Carregar pagamentos do Supabase

    if st.sidebar.button("Encerrar Sessão EasyImob Pro"):
        st.session_state['logged_in'] = False
        st.rerun()
