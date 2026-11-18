import streamlit as st
from pathlib import Path

import config
from modules.parser import parse_profile
from modules.scraper import scrape_job_url
from modules.analyzer import analyze
from modules.generator import generate_resume
from modules.exporter import markdown_to_docx

st.set_page_config(page_title="TailorCV", page_icon="📄", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1450px;}
.metric-card {border: 1px solid #e6e6e6; border-radius: 12px; padding: 1rem; background: #fafafa;}
.stProgress > div > div > div > div {background-color: #2563eb;}
</style>
""", unsafe_allow_html=True)

st.title("TailorCV — Gerador de Currículo Específico")
st.caption("Perfil + vaga → análise ATS → currículo estratégico → Markdown/DOCX")

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "resume_md" not in st.session_state:
    st.session_state.resume_md = None

with st.sidebar:
    st.header("Dados de entrada")
    job_url = st.text_input("URL da vaga", placeholder="https://...")
    job_text = st.text_area("Texto da vaga", height=220, placeholder="Cole aqui caso a URL esteja bloqueada...")
    st.divider()
    if "profile_base" not in st.session_state:
        st.session_state.profile_base = ""
    profile_text = st.text_area("Perfil base", height=260, key="profile_base",
                                 placeholder="Cole seu LinkedIn, experiências e formação...")
    uploaded_profile = st.file_uploader("Ou envie perfil (.txt, .pdf)", type=["txt", "pdf"])

    sample = Path(__file__).parent / "assets" / "sample_profile.txt"

    def load_sample():
        st.session_state.profile_base = sample.read_text(encoding="utf-8")

    st.button("Carregar exemplo", on_click=load_sample)

    run = st.button("Analisar compatibilidade", type="primary", use_container_width=True)

profile = parse_profile(profile_text, uploaded_profile)

if run:
    if not profile:
        st.error("Informe o perfil do candidato ou envie um arquivo.")
    else:
        with st.spinner("Extraindo vaga e analisando compatibilidade..."):
            extracted = scrape_job_url(job_url) if job_url.strip() else ""
            job = job_text.strip() or extracted
            if not job:
                st.error("Informe o texto da vaga ou uma URL válida.")
            else:
                st.session_state.analysis = analyze(profile, job, config.GOOGLE_API_KEY, config.GEMINI_MODEL)
                st.session_state.job = job
                st.session_state.profile = profile

analysis = st.session_state.analysis

if analysis:
    left, right = st.columns([0.78, 1.22], gap="large")
    with left:
        st.subheader("Painel ATS")
        st.metric("Score de compatibilidade", f"{analysis.ats_score}/100")
        st.progress(analysis.ats_score / 100)
        st.caption(f"Senioridade sugerida: {analysis.seniority}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Pontos fortes**")
            for item in analysis.strengths:
                st.markdown(f"- {item}")
        with c2:
            st.markdown("**Lacunas**")
            for item in analysis.gaps:
                st.markdown(f"- {item}")

        st.markdown("**Palavras-chave críticas**")
        st.write(" · ".join(analysis.keywords[:20]))
        st.markdown("**Recomendações**")
        for item in analysis.recommendations:
            st.markdown(f"- {item}")

    with right:
        st.subheader("Currículo personalizado")
        if st.button("Gerar currículo", type="primary"):
            with st.spinner("Reestruturando experiências e aplicando estratégia STAR..."):
                st.session_state.resume_md = generate_resume(
                    st.session_state.profile,
                    st.session_state.job,
                    analysis,
                    config.GOOGLE_API_KEY,
                    config.GEMINI_MODEL,
                )

        resume = st.session_state.resume_md
        if resume:
            st.download_button("Baixar Markdown", resume, file_name="curriculo_tailorcv.md", mime="text/markdown")
            docx_file = markdown_to_docx(resume)
            st.download_button("Baixar DOCX", docx_file, file_name="curriculo_tailorcv.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.divider()
            st.markdown(resume)
else:
    st.info("Informe os dados na barra lateral e execute a análise para visualizar o painel ATS.")
