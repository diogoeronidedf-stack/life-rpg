import streamlit as st
import pandas as pd
import random
import datetime

# Configuração da Página para modo amplo (wide) para a agenda caber perfeitamente lado a lado
st.set_page_config(page_title="LIFE RPG v6.5", page_icon="⚔️", layout="wide")

# --- ESTILIZAÇÃO VISUAL ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
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
    .status-banner {
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
        font-size: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .npc-box {
        background: rgba(250, 179, 135, 0.1);
        border-left: 5px solid #FAB387;
        padding: 15px;
        border-radius: 8px;
        font-style: italic;
        margin-bottom: 25px;
        color: #f8f8f2;
    }
    .class-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #89b4fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .ifood-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 2px dashed #F38BA8;
    }
    /* Estilo dos Containers da Agenda */
    .agenda-day-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        min-height: 320px;
    }
    .agenda-title {
        text-align: center;
        color: #deff9a;
        font-weight: bold;
        border-bottom: 2px solid rgba(222, 255, 154, 0.2);
        padding-bottom: 8px;
        margin-bottom: 12px;
        font-size: 16px;
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

# Painel Centralizado (com colunas responsivas para centralizar no layout wide)
st.markdown(f"<div class='npc-box'>{npc}</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-label'>🔋 XP ATUAL</div><div class='stat-value'>{st.session_state.xp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-label'>⚔️ RANK</div><div class='stat-value' style='color: #89b4fa;'>{rank}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-label'>🎯 META iFOOD</div><div class='stat-value' style='color: #f9e2af;'>{meta_xp} XP</div></div>", unsafe_allow_html=True)

st.write("")
st.markdown(f"<div class='status-banner' style='{banner}'>{ifood}</div>", unsafe_allow_html=True)

# --- ABAS DO APLICATIVO ---
t1, t2, t3, t4, t5 = st.tabs(["🎯 Guilda de Hábitos", "📅 Agenda de Missões", "🏫 Arena de Aulas", "📈 Crônicas de XP", "🍔 Recompensa: iFood"])

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

# 2. AGENDA DE MISSÕES SE MANAL 📅
with t2:
    st.subheader("📅 Sua Agenda Semanal de Campanhas")
    
    # Adicionar Missão rápida
    with st.expander("➕ Fixar Nova Missão na Agenda"):
        col_m1, col_m2 = st.columns([0.65, 0.35])
        m_nome = col_m1.text_input("📜 Nome da Missão:", placeholder="Ex: Entrega do Relatório de Física...")
        m_data = col_m2.date_input("📅 Escolha o Dia:", datetime.date.today(), key="cadastro_agenda")
        if st.button("🔥 Confirmar Missão"):
            if m_nome:
                st.session_state.tarefas.append({"task": m_nome, "date": m_data, "done": False})
                st.success("Missão alocada no pergaminho do tempo!")
                st.rerun()
                
    st.write("")
    
    # Lógica para definir os dias da semana atual
    hoje = datetime.date.today()
    inicio_semana = hoje - datetime.timedelta(days=hoje.weekday()) # Segunda-feira
    
    dias_semana = []
    nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    for i in range(7):
        dias_semana.append(inicio_semana + datetime.timedelta(days=i))
        
    # Renderizar a Agenda em 7 colunas (uma para cada dia da semana)
    colunas_agenda = st.columns(7)
    
    for indice, col in enumerate(colunas_agenda):
        dia_da_agenda = dias_semana[indice]
        nome_dia = nomes_dias[indice]
        data_formatada = dia_da_agenda.strftime("%d/%m")
        
        # Destacar se for o dia de hoje
        titulo_display = f"⭐ {nome_dia}\n({data_formatada})" if dia_da_agenda == hoje else f"{nome_dia}\n({data_formatada})"
        
        with col:
            st.markdown(f"<div class='agenda-day-box'><div class='agenda-title'>{titulo_display}</div>", unsafe_allow_html=True)
            
            # Pegar missões agendadas para este dia específico
            missoes_desse_dia = [t for t in st.session_state.tarefas if t["date"] == dia_da_agenda]
            
            if not missoes_desse_dia:
                st.caption("_Sem missões_")
            else:
                for idx, t in enumerate(st.session_state.tarefas):
                    if t["date"] == dia_da_agenda:
                        # Exibe o check e um mini botão de deletar abaixo para caber na coluna estreita
                        status = st.checkbox(f"{t['task']}", value=t['done'], key=f"agenda_check_{idx}")
                        if status != t['done']:
                            st.session_state.tarefas[idx]['done'] = status
                            st.session_state.xp += 15 if status else -15
                            st.rerun()
                        
                        # Mini ações dentro do dia
                        c_util1, c_util2 = st.columns(2)
                        if not t['done']:
                            if c_util1.button("🛑", key=f"fail_agenda_{idx}", help="Procrastinar (-20 XP)"):
                                st.session_state.xp -= 20
                                st.rerun()
                        if c_util2.button("🗑️", key=f"del_agenda_{idx}", help="Excluir"):
                            st.session_state.tarefas.pop(idx)
                            st.rerun()
                        st.markdown("<hr style='margin: 8px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# 3. GRADE DE AULAS
with t3:
    st.subheader("🏫 Arena de Aulas & Controle de Faltas")
    with st.expander("➕ Adicionar Nova Disciplina"):
        dia = st.selectbox("Dia da Semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
        materia = st.text_input("Nome da Matéria:")
        sala = st.text_input("Local (Sala/Bloco):")
        horario = st.text_input("Horário:")
        if st.button("🔒 Gravar Disciplina"):
            if materia:
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
            st.markdown(f"""
            <div class='class-card'>
                <b style='color: #89b4fa; font-size: 18px;'>{r['materia']}</b><br>
                📅 {r['dia']} | 📍 {r['sala']} | ⏰ {r['horario']}<br>
                <b style='color: #f38ba8;'>Total de Faltas: {r['faltas']}</b>
            </div>
            """, unsafe_allow_html=True)
            c_a, c_b, c_c = st.columns([0.4, 0.4, 0.2])
            with c_a:
                with st.popover("🛑 Faltei a esta aula"):
                    st.write("Quantas faltas você levou hoje?")
                    f_quantas = st.radio("Selecione:", [1, 2, 3], key=f"radio_{idx}")
                    if st.button("Confirmar Faltas", key=f"conf_{idx}"):
                        st.session_state.grade_aulas[idx]['faltas'] += f_quantas
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

# 5. ABA DO IFOOD
with t5:
    st.subheader("🍔 Menu de Recompensa: iFood")
    if st.session_state.xp >= meta_xp:
        st.balloons()
        st.markdown(f"""
        <div class='ifood-box' style='border-color: #A6E3A1; background: rgba(166, 227, 161, 0.1);'>
            <h2 style='color: #A6E3A1; margin: 0;'>👑 PARABÉNS, VOCÊ VENCEU!</h2>
            <p style='font-size: 18px; color: #CDD6F4; margin-top: 10px;'>
                Sua disciplina nesta semana rendeu <b>{st.session_state.xp} XP</b> e superou os 180 XP exigidos!
            </p>
            <p style='font-size: 24px; margin: 15px 0;'>🍕 🍔 🍣 🍟</p>
            <p style='color: #A6E3A1; font-weight: bold;'>O BANQUETE DO FINAL DE SEMANA ESTÁ 100% AUTORIZADO!</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Abrir o iFood Agora!"):
            st.markdown("[Clique aqui para ir para o iFood Web](https://www.ifood.com.br)", unsafe_allow_html=True)
    else:
        resta_pontos = meta_xp - st.session_state.xp
        st.markdown(f"""
        <div class='ifood-box'>
            <h2 style='color: #F38BA8; margin: 0;'>🔒 RECOMPENSA TRANCADA</h2>
            <p style='font-size: 18px; color: #CDD6F4; margin-top: 10px;'>
                Você está no nível <b>{st.session_state.xp} XP</b>. Para quebrar o selo do delivery, você precisa acumular mais poder.
            </p>
            <div style='margin: 20px 0;'>
                <b style='font-size: 20px; color: #FAB387;'>Faltam {resta_pontos} XP para o desbloqueio!</b>
            </div>
            <p style='font-size: 14px; color: #A6ADC8; font-style: italic;'>
                Dica: Volte nas abas de Hábitos e Missões e elimine os monstros pendentes do dia!
            </p>
        </div>
        """, unsafe_allow_html=True)
