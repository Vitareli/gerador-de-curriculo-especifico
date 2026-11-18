# TailorCV — Gerador de Currículo Específico

[![Repositório GitHub](https://img.shields.io/badge/GitHub-TailorCV-181717?logo=github&logoColor=white)](https://github.com/Vitareli/tailorcv)
[![Deploy Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com)


> Interface web pública destinada à análise de vagas, compatibilidade ATS e geração de currículos personalizados.

Aplicativo agêntico em Streamlit que analisa uma vaga e um perfil profissional, produz um currículo em Markdown otimizado para ATS e exporta um `.docx` simples e profissional.

## Instalação

```bash
cd tailor-cv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Opcional para navegadores bloqueados:
python -m playwright install chromium
```

Configure `GOOGLE_API_KEY` no arquivo `.env`. Sem chave, o TailorCV executa uma análise local de fallback baseada em palavras-chave.

## Executar

```bash
streamlit run app.py
```

## Fluxo

1. Informe uma URL ou cole o texto da vaga.
2. Cole o perfil, envie `.txt` ou `.pdf`.
3. Execute a análise. Revise score, lacunas e pontos fortes.
4. Gere o currículo personalizado e baixe Markdown ou DOCX.

O conteúdo é processado localmente; textos são enviados ao Gemini apenas quando uma chave é configurada.

## Implantação no Render

1. Crie um novo **Web Service** no Render e conecte este repositório.
2. Use Python como ambiente de execução.
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
4. Adicione `GOOGLE_API_KEY` nas Environment Variables do serviço.
5. Opcionalmente, defina `GEMINI_MODEL=gemini-2.0-flash`.

O arquivo [`render.yaml`](render.yaml) permite implantar o projeto como Blueprint.

## Funcionalidades

- Extração resiliente de vagas por URL com BeautifulSoup, Trafilatura e fallback Playwright
- Upload de perfil em TXT ou PDF
- Análise lexical local ou análise estruturada com Gemini
- Score ATS, senioridade, lacunas, pontos fortes e palavras-chave
- Geração de currículo fiel ao perfil em Markdown
- Exportação `.docx` com uma única coluna e formatação simples para ATS
