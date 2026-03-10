import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Drug Repurposing Portal", page_icon="💊", layout="wide")

st.title(" AI-Driven Drug Repurposing Portal")
st.markdown("### Identifying new uses for existing FDA-approved drugs.")
st.write("---")

st.sidebar.header(" Data Management")
uploaded_file = st.sidebar.file_uploader("Upload Open Targets Data (TSV or CSV)", type=["tsv", "csv"])

if uploaded_file is not None:
    file_name = uploaded_file.name


    if file_name.endswith('.tsv'):
        df_raw = pd.read_csv(uploaded_file, sep='\t')
        st.sidebar.info("Format Detected: TSV (Tab Separated)")
    else:
        df_raw = pd.read_csv(uploaded_file)
        st.sidebar.info("Format Detected: CSV (Comma Separated)")


    df = df_raw.rename(columns={
        'diseaseName': 'Disease',
        'targetSymbol': 'Candidate Drug',
        'overallScore': 'Confidence Score'
    })


    df['Confidence Score'] = pd.to_numeric(df['Confidence Score'], errors='coerce')


    if 'Mechanism' not in df.columns:
        df['Mechanism'] = "Biological Target Interactor"

    st.sidebar.success(f"Loaded: {file_name}")

else:

    st.sidebar.warning("No file uploaded. Showing demo dataset.")
    demo_data = {
        'Disease': ['Hypertension', 'Type 2 Diabetes', 'Alzheimer\'s', 'Rheumatoid Arthritis', 'COVID-19'],
        'Candidate Drug': ['Propranolol', 'Metformin', 'Donepezil', 'Adalimumab', 'Dexamethasone'],
        'Mechanism': ['Beta-blocker', 'AMPK Activator', 'AChE Inhibitor', 'TNF Inhibitor', 'Corticosteroid'],
        'Confidence Score': [0.95, 0.88, 0.72, 0.91, 0.85]
    }
    df = pd.DataFrame(demo_data)


st.sidebar.header("🔍 Search Parameters")

disease_list = sorted(df['Disease'].dropna().unique())
selected_disease = st.sidebar.selectbox("Select Target Disease", disease_list)


st.subheader(f"Top Candidates for: {selected_disease}")


result = df[df['Disease'] == selected_disease].sort_values(by='Confidence Score', ascending=False)

if not result.empty:

    top_hit = result.iloc[0]

    st.success(f"Primary Therapeutic Candidate: **{top_hit['Candidate Drug']}**")


    col1, col2, col3 = st.columns(3)
    with col1:

        score_val = float(top_hit['Confidence Score']) * 100
        st.metric("AI Confidence Score", f"{score_val:.1f}%")

    with col2:
        st.info(f"**Predicted Mechanism:**\n{top_hit['Mechanism']}")

    with col3:
        st.metric("Total Matches Found", len(result))

    st.write("---")

    st.write("###  Complete Discovery Ranking")
    st.markdown("The table below ranks all identified targets based on genomic association strength.")


    cols_to_show = ['Candidate Drug', 'Mechanism', 'Confidence Score']

    st.dataframe(result[cols_to_show], use_container_width=True)

else:
    st.error("No candidates found in the current database for this selection.")

st.write("---")
st.caption(
    " **Project Status:** AI-Enhanced Drug Repurposing Prototype. Data sourced from Open Targets & DrugBank logic.")