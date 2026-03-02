import streamlit as st
import pandas as pd
st.set_page_config(page_title="AI Drug Repurposing Portal")

st.title(" AI-Driven Drug Repurposing Portal")
st.markdown("### Identifying new uses for existing FDA-approved drugs.")


data = {
    'Disease': ['Hypertension', 'Type 2 Diabetes', 'Alzheimer\'s', 'Rheumatoid Arthritis', 'COVID-19'],
    'Candidate Drug': ['Propranolol', 'Metformin', 'Donepezil', 'Adalimumab', 'Dexamethasone'],
    'Mechanism': ['Beta-blocker', 'AMPK Activator', 'AChE Inhibitor', 'TNF Inhibitor', 'Corticosteroid'],
    'Confidence Score': [0.95, 0.88, 0.72, 0.91, 0.85]
}
df = pd.DataFrame(data)


st.sidebar.header("Search Parameters")
selected_disease = st.sidebar.selectbox("Select Target Disease", df['Disease'].unique())

st.subheader(f"Top Candidates for: {selected_disease}")

result = df[df['Disease'] == selected_disease]

if not result.empty:
    st.success(f"Found Candidate: **{result.iloc[0]['Candidate Drug']}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Confidence Score", f"{result.iloc[0]['Confidence Score'] * 100}%")
    with col2:
        st.info(f"Mechanism: {result.iloc[0]['Mechanism']}")

    st.write("---")
    st.write("### Full Data Insight")
    st.table(result)
else:
    st.error("No candidates found in current database.")
st.caption("Disclaimer: This is an AI-generated prototype for research purposes only.")
