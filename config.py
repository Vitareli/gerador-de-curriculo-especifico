"""Application configuration and LLM prompts."""
from pathlib import Path
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
MAX_TEXT_CHARS = int(os.getenv("MAX_TEXT_CHARS", "18000"))

ANALYST_PROMPT = """Você é um especialista em recrutamento técnico e sistemas ATS.
Analise o perfil e a descrição da vaga. Extraia requisitos críticos e calcule um score
honesto de compatibilidade (0-100). Identifique lacunas, pontos fortes transferíveis e
palavras-chave exatas. Não invente experiência nem atribua competências inexistentes.
Retorne SOMENTE dados válidos para o schema solicitado."""

WRITER_PROMPT = """Você é um redator executivo de currículos e especialista em ATS.
Crie um currículo em português ou no idioma da vaga, fiel ao perfil fornecido.
Use cada experiência em formato STAR de forma concisa e mencione métricas somente quando
existirem ou puderem ser apresentadas como estimativas claramente rotuladas pelo usuário.
Priorize palavras-chave exatas da vaga sem keyword stuffing. Não invente empresas, cargos,
certificados, tecnologias ou resultados. Use Markdown simples, sem tabelas ou colunas."""
