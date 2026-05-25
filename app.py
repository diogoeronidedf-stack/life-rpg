import streamlit as st
import pandas as pd
import random
import datetime

# Configuração da Página
st.set_page_config(page_title="LIFE RPG v5.0", page_icon="⚔️", layout="centered")

# --- ESTILIZAÇÃO VISUAL (BACKGROUND E COMPONENTES) ---
st.markdown("""
<style>
    /* Plano de fundo Gamer Estilizado */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }

    /* Estilo dos Cards de Status (Efeito Vidro) */
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stat-label { color: #A6ADC8; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .stat-value { color: #deff9a; font-size: 26px; font-weight: bold; }

    /* Banner de iFood */
    .status-banner {
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
        font-size: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Diálogo do Mestre */
    .npc-box {
        background: rgba(250, 179, 135, 0.1);
        border-left: 5px solid #FAB387;
        padding: 15px;
        border-radius: 8px;
        font-style: italic;
        margin-bottom: 25px;
        color: #f8f8f2;
    }

    /* Estilo das matérias na grade */
    .class-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #F38BA8;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO SISTEMA ---
if "xp" not in st.session_state: st.session_state.xp = 100
if "habitos" not in st.session_state: st.session_state.habitos = []
if "tarefas" not in st.session_state: st.session_state.tarefas = []
if "grade_aulas" not in st.session_state: st.session_state.grade_aulas = []
if "historico_grafico" not in st.session_state: st.session_state.historico_grafico = [90, 105, 95, 115, 110, 100, 100]

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: white;'>⚔️ LIFE RPG: THE ULTIMATE ⚔️</h1>", unsafe_allow_html=True)

meta_xp = 180
if st.session_state.xp >= meta_xp:
    rank, ifood, banner = "👑 LENDÁRIO", "✅ iFOOD LIBERADO! BANQUETE DISPONÍVEL!", "background-color: #2e7d32; color: white; border: 2px solid #a6e3a1;"
    npc = "🧙‍♂️ Mestre: 'Herói, os deuses da disciplina te saúdam! Os 180 XP foram batidos. Pode pedir o banquete!'"
else:
    rank, ifood, banner = "🛡️ AVENTUREIRO", "❌ iFOOD BLOQUEADO!", "background-color: #c62828; color: white; border: 2px solid #f38ba8;"
    npc = f"🧙‍♂️ Mestre: 'A meta de 180 XP é implacável. Você ainda precisa de {meta_xp - st.session_state.xp} XP para comer como um rei!'"

st.markdown(f"<div class='npc-box'>{npc}</div>", unsafe_allow_html=True)

# Painel de Status
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-label'>🔋 XP ATUAL</div><div class='stat-value'>{st.session_state.xp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-label'>⚔️ RANK</div><div class='stat-value' style='color: #89b4fa;'>{rank}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-label'>🎯 META iFOOD</div><div class='stat-value' style='color: #f9e2af;'>{meta_xp} XP</div></div>", unsafe_allow_html=True)

st.write("")
st.markdown(f"<div class='status-banner' style='{banner}'>{ifood}</div>", unsafe_allow_html=True)

# --- ABAS DO APLICATIVO ---
t1, t2, t3, t4 = st.tabs(["🎯 Guilda de Hábitos", "⚔️ Mural de Missões", "🏫 Arena de Aulas", "📈 Crônicas de XP"])

# 1. HÁBITOS
with t1:
    st.subheader("🎯 Forja de Hábitos Diários")
    novo = st.text_input("💎 Registrar novo hábito fixo:", placeholder="Ex: Treinar Muay Thai, Estudar Cálculo...")
    if st.button("✨ Forjar"):
        if novo:
            st.session_state.habitos.append({"name": novo, "done": False})
            st.rerun()
    st.write("---")
    for i, h in enumerate(st.session_state.habitos):
        col_a, col_b = st.columns([0.85, 0.15])
        check = col_a.checkbox(f"🔮 {h['name']}", value=h['done'], key=f"h_{i}")
        if check != h['done']:
            st.session_state.habitos[i]['done'] = check
            st.session_state.xp += 10 if check else -10
            st.rerun()
        if col_b.button("🗑️", key=f"del_h_{i}"):
            st.session_state.habitos.pop(i)
            st.rerun()

# 2. MISSÕES (TAREFAS)
with t2:
    st.subheader("⚔️ Quadro de Missões Temporárias")
    col_m1, col_m2 = st.columns([0.7, 0.3])
    m_nome = col_m1.text_input("📜 Nome da Missão:", placeholder="Ex: Prova de Física...")
    m_data = col_m2.date_input("📅 Prazo:", datetime.date.today())
    if st.button("🔥 Fixar Missão"):
        if m_nome:
            st.session_state.tarefas.append({"task": m_nome, "date": m_data, "done": False})
            st.rerun()
    st.write("---")
    for i, t in enumerate(st.session_state.tarefas):
        col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
        status = col1.checkbox(f"📜 {t['task']} ({t['date'].strftime('%d/%m')})", value=t['done'], key=f"t_{i}")
        if status != t['done']:
            st.session_state.tarefas[i]['done'] = status
            st.session_state.xp += 15 if status else -15
            st.rerun()
        if not t['done'] and col2.button("🛑 Procrastinar", key=f"proc_{i}"):
            st.session_state.xp -= 20
            st.error("Dano Crítico! -20 XP")
            st.rerun()
        if col3.button("🗑️", key=f"del_t_{i}"):
            st.session_state.tarefas.pop(i)
            st.rerun()

# 3. GRADE DE AULAS (COM CONTROLE DE FALTAS)
with t3:
    st.subheader("🏫 Arena de Aulas & Controle de Faltas")
    
    with st.expander("➕ Adicionar Nova Disciplina"):
        dia = st.selectbox("Dia da Semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
        materia = st.text_input("Nome da Matéria:")
        sala = st.text_input("Local (Sala/Bloco):")
        horario = st.text_input("Horário:")
        if st.button("🔒 Gravar Disciplina"):
            if materia:
                # Adicionamos 'faltas' começando em 0
                st.session_state.grade_aulas.append({
                    "dia": dia, "materia": materia, "sala": sala, "horario": horario, "faltas": 0
                })
                st.success("Matéria registrada!")
                st.rerun()

    st.write("---")
    
    if not st.session_state.grade_aulas:
        st.info("Nenhuma matéria mapeada ainda.")
    else:
        for idx, r in enumerate(st.session_state.grade_aulas):
            # Card de cada aula
            st.markdown(f"""
            <div class='class-card'>
                <b style='color: #89b4fa; font-size: 18px;'>{r['materia']}</b><br>
                📅 {r['dia']} | 📍 {r['sala']} | ⏰ {r['horario']}<br>
                <b style='color: #f38ba8;'>Total de Faltas: {r['faltas']}</b>
            </div>
            """, unsafe_allow_html=True)
            
            c_a, c_b, c_c = st.columns([0.4, 0.4, 0.2])
            
            # Botão de Falta
            with c_a:
                with st.popover("🛑 Faltei a esta aula"):
                    st.write("Quantas faltas você levou hoje?")
                    f_quantas = st.radio("Selecione:", [1, 2, 3], key=f"radio_{idx}")
                    if st.button("Confirmar Faltas", key=f"conf_{idx}"):
                        st.session_state.grade_aulas[idx]['faltas'] += f_quantas
                        st.toast(f"Registradas {f_quantas} faltas em {r['materia']}")
                        st.rerun()
            
            with c_b:
                if st.button("🔄 Resetar Faltas", key=f"res_{idx}"):
                    st.session_state.grade_aulas[idx]['faltas'] = 0
                    st.rerun()
            
            with c_c:
                if st.button("🗑️", key=f"del_a_{idx}"):
                    st.session_state.grade_aulas.pop(idx)
                    st.rerun()
            st.write("---")

# 4. GRÁFICO
with t4:
    st.subheader("📈 Histórico de Rendimento")
    df = pd.DataFrame({"Dias": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"], "XP": st.session_state.historico_grafico})
    df.loc[6, 'XP'] = st.session_state.xp
    st.line_chart(df.set_index("Dias"))
    st.write("Mantenha a curva subindo para garantir o iFood!")
