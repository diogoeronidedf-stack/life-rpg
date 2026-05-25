import streamlit as st
import pandas as pd
import random

# Configuração com tema Dark nativo e layout responsivo
st.set_page_config(
    page_title="LIFE RPG v3.5 - Hardcore", 
    page_icon="⚔️", 
    layout="centered"
)

# Injeção de CSS para customização de estilo Gamer
st.markdown("""
<style>
    .stat-card {
        background-color: #1E1E2E;
        border: 2px solid #313244;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stat-label {
        color: #A6ADC8;
        font-size: 14px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .stat-value {
        color: #CBA6F7;
        font-size: 22px;
        font-weight: bold;
        margin-top: 5px;
    }
    .status-banner {
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        font-size: 18px;
        border: 2px dashed rgba(255,255,255,0.3);
    }
    .npc-box {
        background-color: #181825;
        border-left: 4px solid #FAB387;
        padding: 12px;
        border-radius: 4px;
        font-style: italic;
        margin-bottom: 20px;
        color: #CDD6F4;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar dados se não existirem
if "xp" not in st.session_state:
    st.session_state.xp = 100
if "habitos" not in st.session_state:
    st.session_state.habitos = []
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []
if "grade_aulas" not in st.session_state:
    st.session_state.grade_aulas = []
if "historico_dados" not in st.session_state:
    st.session_state.historico_dados = []

# TÍTULO DO JOGO
st.markdown("<h1 style='text-align: center; color: #F5E0DC;'>⚔️ LIFE RPG: HARDCORE MODE ⚔️</h1>", unsafe_allow_html=True)

# LÓGICA DE RANKS (NOVA META DE 180 XP)
meta_xp = 180

if st.session_state.xp >= 240:
    rank = "🔱 SEMIDEUS DO FOCO"
    npc_frase = "🧙‍♂️ Mestre da Taverna: 'Inacreditável! Você pulverizou a meta de 180 XP. Os deuses do foco estão maravilhados com seu rendimento!'"
    ifood_status = "🍗 BANQUETE DIVINO! Peça o combo mais insano do iFood, você obliterou a semana!"
    banner_style = "background-color: #A6E3A1; color: #11111B;"
elif st.session_state.xp >= meta_xp:
    rank = "👑 PALADINO LENDÁRIO"
    npc_frase = "🧙‍♂️ Mestre da Taverna: 'Você alcançou os gloriosos 180 XP! O selo do iFood foi quebrado com sucesso. Desfrute da vitória!'"
    ifood_status = "✅ iFOOD LIBERADO! Missão cumprida, guerreiro. Pode fazer o pedido!"
    banner_style = "background-color: #2e7d32; color: white;"
elif st.session_state.xp >= 120:
    rank = "🛡️ AVENTUREIRO DE ELITE"
    npc_frase = "🧙‍♂️ Mestre da Taverna: 'Você está produzindo bem, mas a nova dificuldade de 180 XP não perdoa. Continue farmando e não acumule missões!'"
    ifood_status = "❌ iFOOD BLOQUEADO! Continue focado. A meta agora é mais alta!"
    banner_style = "background-color: #f57f17; color: black;"
else:
    rank = "💀 GOBLIN DA PREGUIÇA"
    npc_frase = "🧙‍♂️ Mestre da Taverna: 'Apenas 180 XP te salvam do jejum de delivery... e você está aí vacilando? Vá treinar e estudar agora mesmo!'"
    ifood_status = "🚨 ALERTA DE DERROTA! iFood bloqueadíssimo. Menos tela, mais ação!"
    banner_style = "background-color: #c62828; color: white;"

# MENSAGEM DO NPC INTERATIVA
st.markdown(f"<div class='npc-box'>{npc_frase}</div>", unsafe_allow_html=True)

# PAINEL DE STATUS GERAL
st.markdown("### 🗺️ Ficha do Personagem")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='stat-card'><div class='stat-label'>🔋 XP / ENERGIA</div><div class='stat-value'>{st.session_state.xp} pts</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-card'><div class='stat-label'>⚔️ CLASSE / RANK</div><div class='stat-value' style='color: #89B4FA;'>{rank}</div></div>", unsafe_allow_html=True)
with col3:
    restante = max(0, meta_xp - st.session_state.xp)
    val_col3 = "✨ META OK!" if restante == 0 else f"{restante} XP"
    st.markdown(f"<div class='stat-card'><div class='stat-label'>🎯 ATÉ O JANTAR</div><div class='stat-value' style='color: #F9E2AF;'>{val_col3}</div></div>", unsafe_allow_html=True)

st.write("")
# Barra de progresso baseada na nova meta
progresso_pct = min(int((st.session_state.xp / meta_xp) * 100), 100)
st.progress(progresso_pct / 100.0)

# Banner do Destino do iFood
st.markdown(f"<div class='status-banner' style='{banner_style}'>{ifood_status} (Progresso: {progresso_pct}%)</div>", unsafe_allow_html=True)

# ABAS DO JOGO
aba1, aba2, aba3, aba4 = st.tabs(["🎯 Guilda de Hábitos", "⚔️ Mural de Missões", "🏫 Arena das Aulas", "🎲 Cassino do Azar (D20)"])

# 1. HÁBITOS
with aba1:
    st.subheader("🎯 Forja de Hábitos Inabaláveis")
    st.write("*Hábitos diários constroem sua armadura. Cada check concede +10 XP.*")
    
    novo_habito = st.text_input("💎 Adicionar hábito à sua rotina:", key="new_hab", placeholder="Ex: Treinar Muay Thai, Revisar Cálculo...")
    if st.button("✨ Forjar Hábito"):
        if novo_habito and novo_habito not in st.session_state.habitos:
            st.session_state.habitos.append({"name": novo_habito, "done": False})
            st.toast(f"⚡ Hábito '{novo_habito}' adicionado ao grimório!")
            st.rerun()
    
    st.markdown("---")
    if not st.session_state.habitos:
        st.info("Nenhum hábito ativo. Use o campo acima para começar o farm.")
    else:
        for i, h in enumerate(st.session_state.habitos):
            col_h1, col_h2 = st.columns([0.85, 0.15])
            with col_h1:
                checado = st.checkbox(f"🔮 {h['name']}", value=h["done"], key=f"hab_{i}")
                if checado != h["done"]:
                    st.session_state.habitos[i]["done"] = checado
                    if checado:
                        st.session_state.xp += 10
                        st.toast("⚡ +10 XP! Fortalecendo a armadura!")
                    else:
                        st.session_state.xp -= 10
                    st.rerun()
            with col_h2:
                if st.button("🗑️", key=f"del_hab_{i}"):
                    st.session_state.habitos.pop(i)
                    st.rerun()

# 2. MISSÕES DIÁRIAS
with aba2:
    st.subheader("⚔️ Quadro de Missões Temporárias")
    st.write("*Completar missões dá +15 XP. Procrastinar drena sua vida de forma implacável.*")
    
    nova_tarefa = st.text_input("📜 Digite uma nova missão:", key="new_task", placeholder="Ex: Resolver lista de Física, Entregar relatório...")
    if st.button("🔥 Ativar Missão"):
        if nova_tarefa:
            st.session_state.tarefas.append({"task": nova_tarefa, "done": False})
            st.toast("🎯 Nova missão afixada no mural!")
            st.rerun()
            
    st.markdown("---")
    if not st.session_state.tarefas:
        st.success("🎉 Mural de missões limpo! Descanse na taverna.")
    else:
        for i, t in enumerate(st.session_state.tarefas):
            col_t1, col_t2, col_t3 = st.columns([0.60, 0.27, 0.13])
            with col_t1:
                status_check = st.checkbox(f"📜 {t['task']}", value=t["done"], key=f"task_{i}")
                if status_check != t["done"]:
                    st.session_state.tarefas[i]["done"] = status_check
                    if status_check:
                        st.session_state.xp += 15
                        st.toast("🪙 MISSÃO CUMPRIDA! +15 XP pro herói!")
                    else:
                        st.session_state.xp -= 15
                    st.rerun()
            with col_t2:
                if not t["done"]:
                    if st.button("🚨 Procrastinei", key=f"proc_{i}"):
                        perda = random.randint(15, 30)
                        st.session_state.xp -= perda
                        st.session_state.historico_dados.append(f"🛑 Procrastinou em '{t['task']}' e perdeu {perda} XP!")
                        st.error(f"💥 DANO CRÍTICO! Você perdeu {perda} pontos de XP!")
                        st.rerun()
            with col_t3:
                if st.button("🗑️", key=f"del_task_{i}"):
                    st.session_state.tarefas.pop(i)
                    st.rerun()

# 3. GRADE DE AULAS
with aba3:
    st.subheader("🏫 Arena do Conhecimento (Sua Grade)")
    
    with st.expander("⚡ Adicionar Nova Aula ao Mapa"):
        dia = st.selectbox("Dia", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
        materia = st.text_input("Nome da Disciplina:")
        sala = st.text_input("Número da Sala / Bloco:")
        horario = st.text_input("Horário da Aula:")
        if st.button("💾 Marcar no Mapa"):
            if materia and sala:
                st.session_state.grade_aulas.append({"dia": dia, "materia": materia, "sala": sala, "horario": horario})
                st.toast("🗺️ Nova masmorra catalogada!")
                st.rerun()

    df = pd.DataFrame(st.session_state.grade_aulas)
    if not df.empty:
        ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        for d in ordem_dias:
            g = df[df["dia"] == d]
            if not g.empty:
                st.markdown(f"#### 📅 {d}-feira")
                for _, r in g.iterrows():
                    st.markdown(
                        f"""<div style='background-color: #11111B; border-left: 4px solid #F38BA8; padding: 10px; border-radius: 4px; margin-bottom: 8px;'>
                            🔥 <b>{r['materia']}</b><br>
                            📍 Local: {r['sala']} | ⏰ Horário: {r['horario']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
    else:
        st.info("Nenhuma masmorra acadêmica mapeada.")

# 4. CASSINO DO AZAR (D20)
with aba4:
    st.subheader("🎲 O Tabuleiro do Destino")
    st.write("Está desesperado pelos 180 XP? Rife um D20 para tentar acelerar, por sua conta e risco!")
    
    if st.button("🎲 ROLAR D20 (Custa 5 XP)"):
        st.session_state.xp -= 5
        resultado_dado = random.randint(1, 20)
        
        if resultado_dado == 20:
            st.session_state.xp += 40
            st.balloons()
            msg = "🎰 CRÍTICO SUPREMO! Tirou 20 no dado: +40 XP!"
            st.success(msg)
        elif resultado_dado >= 12:
            ganho = resultado_dado * 1.5
            st.session_state.xp += int(ganho)
            msg = f"🟢 Sorte! Tirou {resultado_dado}: +{int(ganho)} XP de bônus!"
            st.success(msg)
        elif resultado_dado == 1:
            st.session_state.xp -= 25
            msg = "💀 FALHA CRÍTICA! Tirou 1 no dado: PERDEU -25 XP!"
            st.error(msg)
        else:
            msg = f"🔴 Azar! Tirou {resultado_dado}. Nada mudou."
            st.warning(msg)
            
        st.session_state.historico_dados.append(msg)
        st.write("---")
        st.rerun()
        
    if st.session_state.historico_dados:
        st.write("**Histórico de Eventos:**")
        for log in reversed(st.session_state.historico_dados[-5:]):
            st.write(f"- {log}")          
