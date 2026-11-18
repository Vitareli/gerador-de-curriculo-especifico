import streamlit as st
from pathlib import Path
import base64

import config
from modules.parser import parse_profile
from modules.scraper import scrape_job_url
from modules.analyzer import analyze
from modules.generator import generate_resume
from modules.exporter import markdown_to_docx

st.set_page_config(page_title="Gerador de Currículo Específico", page_icon="📄", layout="wide")

def font_data(filename):
    font_path = Path(__file__).parent / "assets" / filename
    return base64.b64encode(font_path.read_bytes()).decode("ascii")

regular_font = font_data("Cocogoose-Pro-Regular-trial.ttf")
bold_font = font_data("Cocogoose-Pro-Bold-trial.ttf")

st.markdown(f"""
<style>
@font-face {{ font-family: 'Cocogoose'; src: url('data:font/ttf;base64,{regular_font}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: 'Cocogoose'; src: url('data:font/ttf;base64,{bold_font}') format('truetype'); font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root { --gold: #FCA311; --navy: #14213D; --ink: #000000; --grey: #E5E5E5; --white: #FFFFFF; }
html, body, [class*="css"] { font-family: 'Cocogoose', 'Segoe UI', sans-serif; }
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #080b12 0%, #111827 55%, #18284a 100%); color: var(--white); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: rgba(5, 8, 15, .94); border-right: 1px solid rgba(252,163,17,.18); }
[data-testid="stSidebar"] * { color: #f7f7f7; }
.block-container { max-width: 1500px; padding: 1.2rem 3.5rem 4rem; }
.hero { position: relative; overflow: hidden; border: 1px solid rgba(252,163,17,.24); border-radius: 20px; padding: 2.2rem 2.5rem; margin-bottom: 1.4rem; background: linear-gradient(118deg, rgba(252,163,17,.16), rgba(20,33,61,.72)); box-shadow: 0 18px 45px rgba(0,0,0,.24); }
.hero:after { content:''; position:absolute; width:260px; height:260px; border:1px solid rgba(252,163,17,.20); border-radius:50%; right:-80px; top:-130px; box-shadow: 0 0 80px rgba(252,163,17,.10); }
.hero h1 { font-family:'Cocogoose'; font-size: clamp(2rem, 4vw, 3.7rem); line-height:1.05; margin:0 0 .7rem; letter-spacing:-1px; }
.hero p { max-width:760px; color:#dbe3ef; font-size:1.05rem; margin:0; }
.gold { color: var(--gold); }
.feature-grid { display:grid; grid-template-columns: repeat(3,1fr); gap:12px; margin: 1rem 0 1.4rem; }
.feature { border:1px solid rgba(229,229,229,.11); border-radius:14px; padding:1.1rem; background:rgba(255,255,255,.035); transition:.25s ease; }
.feature:hover { transform:translateY(-3px); border-color:rgba(252,163,17,.48); background:rgba(252,163,17,.055); }
.feature span { display:block; color:var(--gold); font-size:.76rem; letter-spacing:1.5px; margin-bottom:.35rem; }
.feature b { color:white; font-size:.92rem; }
[data-testid="stMetric"] { background:rgba(255,255,255,.055); border:1px solid rgba(252,163,17,.16); border-radius:14px; padding:1rem; }
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color:white !important; }
.stProgress > div > div > div > div { background:linear-gradient(90deg, var(--gold), #ffd166); }
.stButton > button, [data-testid="stDownloadButton"] button { border-radius:10px; border:1px solid rgba(252,163,17,.65); background:var(--gold); color:#080b12; font-weight:700; box-shadow:0 8px 22px rgba(252,163,17,.12); transition:.2s ease; }
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover { transform:translateY(-2px); background:#ffb238; border-color:#ffb238; color:#080b12; }
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { background:rgba(255,255,255,.06) !important; border:1px solid rgba(229,229,229,.16) !important; border-radius:10px; color:white !important; }
[data-testid="stFormSubmitButton"] button { border-radius:10px; }
.panel { border:1px solid rgba(229,229,229,.12); border-radius:16px; background:rgba(255,255,255,.045); padding:1.2rem; backdrop-filter:blur(8px); }
.footer { margin-top:3rem; border-top:1px solid rgba(252,163,17,.22); padding:1.8rem 0 1rem; color:#bac3d0; }
.footer-grid { display:grid; grid-template-columns:2fr 1fr; gap:20px; align-items:start; }
.socials a { display:inline-block; margin:.35rem .55rem .35rem 0; padding:.55rem .75rem; border:1px solid rgba(252,163,17,.22); border-radius:9px; color:#ffc66d; text-decoration:none; transition:.2s; }
.socials a:hover { border-color:var(--gold); background:rgba(252,163,17,.08); color:white; }
hr { border-color:rgba(229,229,229,.10); }
@media (max-width: 900px) { .block-container {padding:1rem;} .feature-grid {grid-template-columns:1fr;} .footer-grid {grid-template-columns:1fr;} }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <span class="gold" style="font-size:.78rem;letter-spacing:2px">INTELIGÊNCIA · PRECISÃO · POSICIONAMENTO</span>
  <h1>Gerador de <span class="gold">Currículo Específico</span></h1>
  <p>Transforme seu perfil profissional em uma candidatura estratégica, legível por sistemas ATS e construída com linguagem de negócio.</p>
</div>
<div class="feature-grid">
  <div class="feature"><span>01 · ANÁLISE</span><b>Compatibilidade ATS e lacunas</b></div>
  <div class="feature"><span>02 · POSICIONAMENTO</span><b>Estrutura STAR e palavras-chave</b></div>
  <div class="feature"><span>03 · RESULTADO</span><b>Exportação Markdown e DOCX</b></div>
</div>
""", unsafe_allow_html=True)

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
            st.download_button("Baixar Markdown", resume, file_name="curriculo-especifico.md", mime="text/markdown")
            docx_file = markdown_to_docx(resume)
            st.download_button("Baixar DOCX", docx_file, file_name="curriculo-especifico.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.divider()
            st.markdown(resume)
else:
    st.info("Informe os dados na barra lateral e execute a análise para visualizar o painel ATS.")

st.markdown("""
<div class="footer">
  <div class="footer-grid">
    <div>
      <span class="gold" style="letter-spacing:1.5px;font-size:.72rem">GABRIEL VITARELI</span>
      <p style="margin:.45rem 0 0">Gerador de Currículo Específico · Inteligência aplicada ao posicionamento profissional</p>
    </div>
    <div class="socials">
      <a href="https://github.com/Vitareli" target="_blank">GitHub</a>
      <a href="https://www.linkedin.com/in/gabrielvitareli/" target="_blank">LinkedIn</a>
      <a href="https://instagram.com/_Vitareli" target="_blank">Instagram</a>
      <a href="https://wa.me/5519991712007" target="_blank">WhatsApp</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
