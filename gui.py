import streamlit as st
import io
import contextlib

from orco_nmr.stats import load_stats
from orco_nmr.core import assign_spin, assign_spin_probs

# Optional: logo
st.image("orco_logo.png", width=300)
st.title(" ORCO: Residue Classifier")

# Input fields
st.markdown("### 🧪 Input Chemical Shifts")
N  = st.number_input("N", value=120.5)
CA = st.number_input("CA", value=60.2)
CO = st.number_input("CO", value=175.8)

CX_vals = []
for i in range(4):
    val = st.number_input(f"CX{i+1}", value=1e6)
    CX_vals.append(val)

# Load stats
stats = load_stats()
spin = { "N": N, "CA": CA, "CO": CO, "CX": CX_vals }

# On Predict button
if st.button("🚀 Predict"):
    st.markdown("### 🔢 Probability Ranking")
    probs = assign_spin_probs(spin, stats)

    if not probs:
        st.warning("⚠️ No residue predictions returned. Check your inputs.")
    else:
        top5 = sorted(probs.items(), key=lambda x: -x[1])[:5]
        st.table(top5)

        st.markdown("### 📋 CLI-style Output")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            assign_spin(spin, stats)
        st.text(f.getvalue())
