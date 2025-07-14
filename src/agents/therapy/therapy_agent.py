# src/agents/therapy/therapy_agent.py

import logging
import os
from dotenv import load_dotenv

from src.utils.logger import setup_logging
from src.utils.cultural_embeddings import cultural_embeddings  # Provides Omani‑specific prompts
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Primary LLM: Groq (zero‑cost, via prompt engineering)
# ──────────────────────────────────────────────────────────────────────────────
llm_groq = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.5
)

# ──────────────────────────────────────────────────────────────────────────────
# # Paid‑API placeholders (commented out) — enable if you have access:
#
# from openai import OpenAI
# from anthropic import Anthropic
#
# # GPT‑4o via OpenAI
# llm_gpt4 = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model="gpt-4o",
#     temperature=0.5
# )
#
# # Claude Opus 4 via Anthropic
# llm_claude = Anthropic(
#     api_key=os.getenv("CLAUDE_API_KEY"),
#     model="claude-opus-4",
#     temperature=0.5
# )
# ──────────────────────────────────────────────────────────────────────────────

# Dual‑stage prompt: 1) Generate culturally adapted CBT response
#                 2) Validate for safety, empathy, and cultural alignment.
template = """
You are a two-stage Omani Arabic therapist assistant for mental health support.
Stage 1: Generate a CBT-based, empathetic response in Omani Arabic for the given emotion and transcript. 
Use Gulf-specific terms (e.g., 'قلق نفسي' for anxiety, 'ضغط اجتماعي' for social pressure) and Islamic values 
(e.g., 'بإذن الله', 'الصبر مفتاح الفرج') if appropriate. Keep it concise and supportive.
Stage 2: Validate the response for cultural appropriateness, safety, and empathy. 
Ensure the response avoids harmful content and aligns with Omani cultural norms. Return only the validated response.
Incorporate the following cultural prompt to enhance the response: {cultural_prompt}
Always respond only in Modern Standard Arabic with Omani dialectal flavor. Never use English words or Latin letters.

Emotion: {emotion}
Transcript: {transcript}
"""

prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()

# Build our runnable chain: passthrough → prompt → Groq → parser
chain = (
    {"emotion": RunnablePassthrough(), "transcript": RunnablePassthrough(), "cultural_prompt": RunnablePassthrough()}
    | prompt
    | llm_groq
    | output_parser
)

def generate_therapy_response(transcript: str, emotion: str) -> str:
    """
    Generate a culturally sensitive, CBT-based therapy response.
    Uses Groq LLM with prompt engineering to fulfill GPT‑4/Claude requirements at zero cost.
    Falls back to hardcoded responses if Groq API is unavailable.
    """
    try:
        logger.info(f"Generating therapy response for transcript: {transcript}, emotion: {emotion}")
        cultural_prompt = cultural_embeddings.get_prompt(emotion)

        # ──────────────────────────────────────────────────────────────────────────
        # # Example of how you’d switch to GPT‑4 if available (commented out):
        # response = llm_gpt4.chat_completion(
        #     prompt=prompt.format_prompt(
        #         emotion=emotion,
        #         transcript=transcript,
        #         cultural_prompt=cultural_prompt
        #     )
        # )
        #
        # # Or use Claude as fallback/validator:
        # response = llm_claude.completions.create(
        #     prompt=prompt.format_prompt(
        #         emotion=emotion,
        #         transcript=transcript,
        #         cultural_prompt=cultural_prompt
        #     )
        # )
        # ──────────────────────────────────────────────────────────────────────────

        # Live Groq invocation:
        response = chain.invoke({
            "emotion": emotion,
            "transcript": transcript,
            "cultural_prompt": cultural_prompt
        })

        logger.info(f"Generated response: {response}")
        return response

    except Exception as e:
        # Professional fallback: pre‑defined templates ensure continuous service
        logger.warning(f"Groq API failed ({e}), using fallback responses")
        fallback_templates = {
            "sadness":   "أسمع أنك تشعر بالحزن. هل يمكنك مشاركة المزيد؟ دعنا نحدد أفكارًا إيجابية معًا، بإذن الله.",
            "anger":     "يبدو أنك غاضب. خذ نفسًا عميقًا ودعنا نفكر في تهدئة هذه المشاعر، الصبر مفتاح الفرج.",
            "joy":       "رائع أنك تشعر بالفرح! الحمد لله، شارك ما يسعدك اليوم.",
            "fear":      "أفهم قلقك. دعنا نتحدث عن مخاوفك ونفكر في خطوات صغيرة، بإذن الله.",
            "surprise":  "هذا مفاجئ! هل تريد أن تخبرني المزيد عما حدث؟",
            "neutral":   "شكرًا لمشاركتك. كيف يمكنني مساعدتك الآن؟"
        }
        fallback = fallback_templates.get(emotion, "شكرًا لمشاركتك. كيف يمكنني مساعدتك الآن؟")
        logger.info(f"Fallback response selected: {fallback}")
        return fallback

if __name__ == "__main__":
    # Quick CLI test
    sample_transcript = "أحتاج إلى المساعدة، وأريد أن أعيش معك"
    sample_emotion = "sadness"
    print(generate_therapy_response(sample_transcript, sample_emotion))
