import streamlit as st
from datetime import datetime
import pandas as pd
import re

# ---------------------------------
# Page config
# ---------------------------------
st.set_page_config(
    page_title="Mbarek – Gestion du Temps",
    layout="wide"
)

# ---------------------------------
# Session state for history
# ---------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------
# Sidebar – history
# ---------------------------------
with st.sidebar:
    st.title("📜 Historique")
    show_history = st.checkbox("Afficher l'historique")

    if show_history:
        if st.session_state.history:
            for h in reversed(st.session_state.history):
                st.markdown(f"**🕒 {h['time']}**")
                st.markdown(h["content"])
                st.markdown("---")
        else:
            st.info("Aucun planning généré.")

# ---------------------------------
# Main Title
# ---------------------------------
st.title("⏱️ Assistant Intelligent de Gestion du Temps")
st.markdown(
    "<p style='color:gray'>Analyse approfondie de vos habitudes + planning journalier + score.</p>",
    unsafe_allow_html=True
)

# ---------------------------------
# Quiz
# ---------------------------------
st.subheader("📝 Quiz de Gestion du Temps")
st.warning("⚠️ Toutes les questions sont obligatoires et doivent être répondues en français.")

with st.form("quiz"):
    col1, col2 = st.columns(2)

    with col1:
        q1 = st.text_input("1️⃣ À quelle heure commence ta journée ? (ex: 07:00)")
        q2 = st.text_area("2️⃣ Pourquoi te lèves-tu à cette heure ?")
        q3 = st.text_area("3️⃣ Comment se répartit ton temps quotidien ?")
        q4 = st.text_area("4️⃣ Quelle activité te fait perdre le plus de temps ?")
        q5 = st.text_area("5️⃣ Quel est ton principal problème d’organisation ?")

    with col2:
        q6 = st.text_area("6️⃣ Quelles activités souhaites-tu réduire ?")
        q7 = st.text_area("7️⃣ Quelles activités souhaites-tu ajouter ?")
        q8 = st.selectbox("8️⃣ Moment où tu es le plus productif ?", ["Matin", "Après-midi", "Soir", "Nuit"])
        q9 = st.selectbox("9️⃣ Moment où tu es le plus fatigué ?", ["Matin", "Après-midi", "Soir", "Nuit"])
        q10 = st.text_area("🔟 Quel est ton objectif principal ?")

    generate = st.form_submit_button("🚀 Générer le planning")

# ---------------------------------
# Validation + Generation
# ---------------------------------
if generate:
    answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    if any(a.strip() == "" for a in answers):
        st.error("❌ Vous devez répondre à TOUTES les questions.")
        st.stop()

    # ---------------------------------
    # Convert mon/mes/ma → ton/tes/ta
    # ---------------------------------
    def convert_to_user_tone(text):
        text = re.sub(r"\bmon\b", "ton", text)
        text = re.sub(r"\bmes\b", "tes", text)
        text = re.sub(r"\bma\b", "ta", text)
        return text

    q2, q3, q4, q5, q6, q7, q10 = [convert_to_user_tone(x) for x in [q2, q3, q4, q5, q6, q7, q10]]

    # ---------------------------------
    # SCORE calculation
    # ---------------------------------
    score = 50
    if "réduire" in q6.lower(): score += 10
    if "objectif" in q10.lower() or len(q10) > 20: score += 15
    if q8 == "Matin": score += 10
    if q9 != q8: score += 5
    if len(q5) > 15: score += 10
    score = min(score, 100)

    # ---------------------------------
    # Deep analysis (no repetition)
    # ---------------------------------
    analysis = f"""
## 🧠 Analyse experte de ton organisation

Ton rythme quotidien montre un potentiel intéressant, mais il manque de structure stable.
La répartition actuelle de ton temps indique une surcharge sur certaines activités
au détriment de tâches essentielles comme la planification et le repos.

Un déséquilibre apparaît entre tes périodes d’énergie et tes moments de fatigue,
ce qui réduit ton efficacité globale. Cela signifie que tes tâches importantes
ne sont pas toujours placées aux moments optimaux de la journée.

Ton organisation souffre principalement d’un manque de priorisation
et d'un contrôle insuffisant des distractions, ce qui explique la sensation
de perte de temps ou de manque d’avancement.
"""

    timetable = """
## 📅 Emploi du temps journalier recommandé

| Heure | Activité |
|------|---------|
| 07:00 – 08:00 | Réveil, hygiène, petit-déjeuner |
| 08:00 – 10:00 | Travail intellectuel important |
| 10:00 – 10:30 | Pause |
| 10:30 – 12:30 | Études / cours |
| 12:30 – 14:00 | Déjeuner + repos |
| 14:00 – 16:00 | Révisions ou devoirs |
| 16:00 – 17:00 | Activité personnelle |
| 17:00 – 18:30 | Loisirs contrôlés |
| 18:30 – 20:00 | Temps familial |
| 20:00 – 21:00 | Organisation du lendemain |
| 21:00 – 22:00 | Détente calme (sans écrans excessifs) |
"""

    adjustments = f"""
## 🔧 Ajustements recommandés

- Réduis progressivement les activités chronophages que tu as identifiées
- Introduis des plages fixes pour le travail important
- Exploite les moments de forte énergie pour tes tâches difficiles
- Allège volontairement les périodes de fatigue
"""

    score_section = f"""
## 📊 Score de gestion du temps

### **{score} / 100**

**Interprétation :**
- 80–100 : Organisation très efficace
- 60–79 : Bonne base avec axes d’amélioration
- 40–59 : Organisation instable
- <40 : Urgence d’organisation
"""

    final_advice = """
## 🎯 Conseil professionnel

Un emploi du temps efficace n’est pas celui qui est rempli,
mais celui qui est respecté.  
La clé de ta progression est la régularité, pas la perfection.
"""

    planning = analysis + timetable + adjustments + score_section + final_advice

    # ---------------------------------
    # Save to history
    # ---------------------------------
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M"),
        "content": planning
    })

    # ---------------------------------
    # Show final planning
    # ---------------------------------
    st.success("✅ Planning et score générés avec succès")
    st.markdown(planning)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown(
    """
    <hr>
    <center>
    <b>Projet réalisé par :</b><br>
    MED MBAREK – EYA ALLAH MAHMOUD – MAJDI EL BEHI – INSAF EL MATHLOUTHI
    </center>
    """,
    unsafe_allow_html=True
)







