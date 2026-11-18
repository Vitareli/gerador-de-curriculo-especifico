"""Agent 1: semantic ATS gap analysis."""
import re
from typing import List
from pydantic import BaseModel, Field


class Analysis(BaseModel):
    ats_score: int = Field(ge=0, le=100)
    seniority: str
    role_summary: str
    critical_requirements: List[str]
    keywords: List[str]
    strengths: List[str]
    gaps: List[str]
    transferable_skills: List[str]
    recommendations: List[str]


def fallback_analysis(profile: str, job: str) -> Analysis:
    profile_low = profile.lower()
    words = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9+#.-]{2,}", job)
    stop = {"para", "com", "que", "uma", "como", "seu", "sua", "the", "and", "our", "you", "will", "with", "from", "job", "vaga"}
    counts = {}
    for word in words:
        key = word.lower().strip(".")
        if key not in stop:
            counts[key] = counts.get(key, 0) + 1
    keywords = [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:30]]
    matched = [word for word in keywords if word in profile_low]
    score = round(100 * len(matched) / max(1, len(keywords)))
    gaps = [word for word in keywords if word not in profile_low][:12]
    return Analysis(
        ats_score=score,
        seniority="Não identificado",
        role_summary="Análise local baseada em correspondência lexical.",
        critical_requirements=keywords[:12],
        keywords=keywords,
        strengths=matched[:12],
        gaps=gaps,
        transferable_skills=[],
        recommendations=["Revise os requisitos críticos sem declarar experiências que não possui."] if gaps else ["Seu perfil contém várias palavras-chave da vaga."],
    )


def analyze(profile: str, job: str, api_key: str = "", model: str = "gemini-2.0-flash") -> Analysis:
    if not api_key:
        return fallback_analysis(profile, job)
    try:
        from google import genai
        from google.genai import types
        from config import ANALYST_PROMPT, MAX_TEXT_CHARS
        client = genai.Client(api_key=api_key)
        prompt = f"""{ANALYST_PROMPT}\n\nPERFIL DO CANDIDATO:\n{profile[:MAX_TEXT_CHARS]}\n\nDESCRIÇÃO DA VAGA:\n{job[:MAX_TEXT_CHARS]}"""
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Analysis,
                temperature=0.2,
            ),
        )
        return response.parsed if isinstance(response.parsed, Analysis) else Analysis.model_validate_json(response.text)
    except Exception as exc:
        result = fallback_analysis(profile, job)
        result.recommendations.insert(0, f"Fallback local ativado: {str(exc)[:180]}")
        return result
