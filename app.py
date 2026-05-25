import streamlit as st
import pandas as pd

# Configuração do App
st.set_page_config(page_title="Life RPG", page_icon="🎮", layout="centered")

# Inicializar dados se não existirem
if "xp" not in st.session_state:
    st.session_state.xp = 100
if "habitos" not in st.session_state:
    st.session_state.habitos = []
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []
if "grade_aulas" not in st.session_state:
    st.session_state.grade_aulas = []

st.title("🎮 Life RPG: Level Up")
st.write("Transforme sua rotina em um jogo. Cumpra metas, ganhe XP e libere seu iFood!")

# STATUS DO JOGADOR
st.subheader("📊 Status do Herói")
col1, col2, col3 = st.columns(3)

if st.session_state.xp >= 140:
    status_critico = "👑 Lendário"
    ifood_status = "✅ LIBERADO! Pode pedir!"
    ifood_cor = "🟢"
elif st.session_state.xp >= 100:
    status_critico = "🛡️ Em dia"
    ifood_status = "❌ BLOQUEADO! Foque mais."
    ifood_cor = "🟡"
else:
    status_critico = "⚠️ Alerta Procrastinação"
    ifood_status = "❌ BLOQUEADO!"
    ifood_cor = "🔴"

col1.metric(label="Pontos de XP", value=f"{st.session_state.xp} XP")
col2.metric(label="Status", value=status_critico)
col3.metric(label="iFood", value=ifood_cor)

st.markdown(f"> **Veredito do Fim de Semana:** {ifood_status} *(Meta: 140 XP)*")

# ABAS
aba1, aba2, aba3, aba4 = st.tabs(["🎯 Meus Hábitos", "📝 Missões Diárias", "🏫 Grade de Aulas", "📈 Rendimento"])

# 1. HÁBITOS
with aba1:
    st.header("🎯 Gerenciar Meus Hábitos")
    novo_habito = st.text_input("Adicionar novo hábito fixo (Ex: Ir treinar):", key="new_hab")
    if st.button("Adicionar Hábito"):
        if novo_habito and novo_habito not in st.session_state.habitos:
            st.session_state.habitos.append({"name": novo_habito, "done": False})
            st.rerun()
    
    st.write("---")
    for i, h in enumerate(st.session_state.habitos):
        col_h1, col_h2 = st.columns([0.8, 0.2])
        with col_h1:
            checado = st.checkbox(h["name"], value=h["done"], key=f"hab_{i}")
            if checado != h["done"]:
                st.session_state.habitos[i]["done"] = checado
                st.session_state.xp += 10 if checado else -10
                st.rerun()
        with col_h2:
            if st.button("🗑️", key=f"del_hab_{i}"):
                st.session_state.habitos.pop(i)
                st.rerun()

# 2. TAREFAS
with aba2:
    st.header("📝 Missões (Tarefas Únicas)")
    nova_tarefa = st.text_input("Nova missão:", key="new_task")
    if st.button("Adicionar Missão"):
        if nova_tarefa:
            st.session_state.tarefas.append({"task": nova_tarefa, "done": False})
            st.rerun()
            
    st.write("---")
    for i, t in enumerate(st.session_state.tarefas):
        col_t1, col_t2, col_t3 = st.columns([0.6, 0.2, 0.2])
        with col_t1:
            status_check = st.checkbox(t["task"], value=t["done"], key=f"task_{i}")
            if status_check != t["done"]:
                st.session_state.tarefas[i]["done"] = status_check
                st.session_state.xp += 15 if status_check else -15
                st.rerun()
        with col_t2:
            if not t["done"]:
                if st.button("Procrastinei 🛑", key=f"proc_{i}"):
                    st.session_state.xp -= 20
                    st.toast("Ai! -20 XP por procrastinar!")
                    st.rerun()
        with col_t3:
            if st.button("🗑️", key=f"del_task_{i}"):
                st.session_state.tarefas.pop(i)
                st.rerun()

# 3. GRADE DE AULAS
with aba3:
    st.header("🏫 Minha Grade de Aulas")
    with st.expander("➕ Adicionar Aula"):
        dia = st.selectbox("Dia", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
        materia = st.text_input("Matéria:")
        sala = st.text_input("Sala / Bloco:")
        horario = st.text_input("Horário:")
        if st.button("Salvar Aula"):
            if materia and sala:
                st.session_state.grade_aulas.append({"dia": dia, "materia": materia, "sala": sala, "horario": horario})
                st.rerun()

    df = pd.DataFrame(st.session_state.grade_aulas)
    if not df.empty:
        for d, g in df.groupby("dia"):
            st.subheader(f"📅 {d}-feira")
            for _, r in g.iterrows():
                st.info(f"📚 **{r['materia']}** | 📍 Sala: {r['sala']} | ⏰ {r['horario']}")

# 4. RENDIMENTO
with aba4:
    st.header("📈 Rendimento")
    dados = {"Dias": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"], "XP": [90, 110, 105, 120, 130, st.session_state.xp, st.session_state.xp]}
    st.line_chart(pd.DataFrame(dados).set_index("Dias"))
