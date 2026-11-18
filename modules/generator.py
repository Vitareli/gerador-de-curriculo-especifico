"""Agent 2: tailored resume generation."""


def fallback_resume(profile: str, job: str) -> str:
    return f"""# CURRÍCULO PERSONALIZADO

{profile.strip()}

## Alinhamento com a vaga

Currículo baseado no perfil fornecido. Palavras relevantes da vaga foram consideradas sem alterar experiências ou competências existentes.

### Texto da vaga analisada

{job[:2500].strip()}
"""


def generate_resume(profile: str, job: str, analysis, api_key: str = "", model: str = "gemini-2.0-flash") -> str:
    if not api_key:
        return fallback_resume(profile, job)
    try:
        from google import genai
        from google.genai import types
        from config import WRITER_PROMPT, MAX_TEXT_CHARS
        client = genai.Client(api_key=api_key)
        prompt = f"""{WRITER_PROMPT}

RETORNAR APENAS UM CURRÍCULO EM MARKDOWN LIMPO.
Estrutura sugerida:
# Nome
## Contato
## Resumo Profissional
## Competências
## Experiência Profissional
## Formação
## Certificações (somente se constarem no perfil)
## Idiomas

PERFIL:
{profile[:MAX_TEXT_CHARS]}

VAGA:
{job[:MAX_TEXT_CHARS]}

ANÁLISE ATS:
{analysis.model_dump_json(indent=2, ensure_ascii=False)}

Regras finais:
- Preserve a verdade factual.
- Use bullets em formato STAR quando apropriado.
- Não adicione seções vazias.
- Não use tabelas, duas colunas, links com sintaxe complexa ou caixas de texto.
"""
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.35),
        )
        text = (response.text or "").strip()
        return text or fallback_resume(profile, job)
    except Exception as exc:
        return fallback_resume(profile, job).replace("\n\n", f"\n\n_Fallback por erro de geração: {str(exc)[:180]}_\n\n", 1)
