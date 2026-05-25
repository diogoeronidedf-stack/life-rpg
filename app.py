import streamlit as st
import pandas as pd
import random
import datetime

# Configuração com tema Dark
st.set_page_config(page_title="LIFE RPG v4.5", page_icon="⚔️", layout="centered")

# Estilos CSS Customizados
st.markdown("""
<style>
    .stat-card { background-color: #1E1E2E; border: 2px solid #313244; border-radius: 10px; padding: 15px; text-align: center; }
    .stat-label { color: #A6ADC8; font-size: 14px; font-weight: bold; }
    .stat-value { color: #deff9a; font-size: 22px; font-weight: bold; }
    .status-banner { padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 20px; border: 2px dashed rgba(255,255,255,0.3); }
    .npc-box { background-color: #181825; border-left: 4px solid #FAB387; padding: 12px; border-radius: 4px; font-style: italic; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# Inicializar Estados
if "xp" not in st.session_state: st.session_state.xp = 100
if "habitos" not in st.session_state: st.session_state.habitos = []
if "tarefas" not in st.session_state: st.session_state.tarefas = []
if "grade_aulas" not in st.session_state: st.session_state.grade_aulas = []
if "historico_grafico" not in st.session_state: st.session_state.historico_grafico = [90, 100, 95, 110, 105, 100, 100]

# Título
st.markdown("<h1 style='text-align: center;'>⚔️ LIFE RPG: HARDCORE ⚔️</h1>", unsafe_allow_html=True)

# Lógica de Rank e iFood (Meta 180 XP)
meta_xp = 180
if st.session_state.xp >= meta_xp:
    rank, ifood, banner = "👑 LENDÁRIO", "✅ iFOOD LIBERADO!", "background-color: #2e7d32; color: white;"
    npc = "🧙‍♂️ Mestre: 'Você atingiu os 180 XP! O banquete é seu!'"
else:
    rank, ifood, banner = "🛡️ AVENTUREIRO", "❌ BLOQUEADO!", "background-color: #c62828; color: white;"
    npc = f"🧙‍♂️ Mestre: 'A meta de 180 XP é pesada. Falta {meta_xp - st.session_state.xp} XP para o jantar!'"

st.markdown(f"<div class='npc-box'>{npc}</div>", unsafe_allow_html=True)

# Status
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-card'><div class='stat-label'>🔋 XP</div><div class='stat-value'>{st.session_state.xp}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'><div class='stat-label'>⚔️ RANK</div><div class='stat-value'>{rank}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'><div class='stat-label'>🎯 META</div><div class='stat-value'>{meta_xp} XP</div></div>", unsafe_allow_html=True)

# Banner iFood
st.markdown(f"<div class='status-banner' style='{banner}'>{ifood}</div>", unsafe_allow_html=True)

# Abas
t1, t2, t3, t4 = st.tabs(["🎯 Hábitos", "⚔️ Missões", "🏫 Aulas", "📈 Gráfico"])

with t1:
    st.subheader("🎯 Seus Hábitos")
    novo = st.text_input("💎 Novo hábito:")
    if st.button("Adicionar"):
        st.session_state.habitos.append({"name": novo, "done": False})
        st.rerun()
    for i, h in enumerate(st.session_state.habitos):
        check = st.checkbox(f"🔮 {h['name']}", value=h['done'], key=f"h_{i}")
        if check != h['done']:
            st.session_state.habitos[i]['done'] = check
            st.session_state.xp += 10 if check else -10
            st.rerun()

with t2:
    st.subheader("⚔️ Missões Futuras")
    col_a, col_b = st.columns(2)
    m_nome = col_a.text_input("📜 Missão:")
    m_data = col_b.date_input("📅 Prazo:")
    if st.button("Agendar"):
        st.session_state.tarefas.append({"task": m_nome, "date": m_data, "done": False})
        st.rerun()
    for i, t in enumerate(st.session_state.tarefas):
        col1, col2 = st.columns([0.8, 0.2])
        status = col1.checkbox(f"📜 {t['task']} ({t['date'].strftime('%d/%m')})", value=t['done'], key=f"t_{i}")
        if status != t['done']:
            st.session_state.tarefas[i]['done'] = status
            st.session_state.xp += 15 if status else -15
            st.rerun()
        if col2.button("🗑️", key=f"d_{i}"):
            st.session_state.tarefas.pop(i)
            st.rerun()

with t3:
    st.subheader("🏫 Grade de Aulas")
    for r in st.session_state.grade_aulas:
        st.info(f"📚 {r['materia']} | 📍 {r['sala']} | ⏰ {r['horario']}")

with t4:
    st.subheader("📈 Evolução de XP")
    # Gráfico dinâmico
    df = pd.DataFrame({"Dias": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"], "XP": st.session_state.historico_grafico})
    df.loc[6, 'XP'] = st.session_state.xp # Atualiza o XP atual no último ponto
    st.line_chart(df.set_index("Dias"))
    st.write("Acompanhe sua subida rumo aos 180 XP!")
