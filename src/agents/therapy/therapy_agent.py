# src/agents/therapy/therapy_agent.py
from src.utils.logger import setup_logging
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import logging
import os
from src.utils.cultural_embeddings import cultural_embeddings  # Added for cultural prompts

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

# Initialize Groq LLM
llm_grok = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.5
)

# Prompt template for dual-role (response + validation)
template = """
You are a two-stage Omani Arabic therapist assistant for mental health support.
Stage 1: Generate a CBT-based, empathetic response in Omani Arabic for the given emotion and transcript. 
Use Gulf-specific terms (e.g., 'قلق نفسي' for anxiety, 'ضغط اجتماعي' for social pressure) and Islamic values (e.g., 'بإذن الله', 'الصبر مفتاح الفرج') if appropriate. Keep it concise and supportive.
Stage 2: Validate the response for cultural appropriateness, safety, and empathy. 
Ensure the response avoids harmful content and aligns with Omani cultural norms. Return only the validated response.
Incorporate the following cultural prompt to enhance the response: {cultural_prompt}
Always respond only in Modern Standard Arabic with Omani dialectal flavor. Never use English words or Latin letters.

Emotion: {emotion}
Transcript: {transcript}
"""

prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()

chain = (
    {"emotion": RunnablePassthrough(), "transcript": RunnablePassthrough(), "cultural_prompt": RunnablePassthrough()}
    | prompt
    | llm_grok
    | output_parser
)

def generate_therapy_response(transcript, emotion):
    try:
        logger.info(f"Generating therapy response for transcript: {transcript}, emotion: {emotion}")
        cultural_prompt = cultural_embeddings.get_prompt(emotion)  # Fetch cultural prompt
        response = chain.invoke({"emotion": emotion, "transcript": transcript, "cultural_prompt": cultural_prompt})
        logger.info(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.warning(f"Groq API failed: {str(e)}, using fallback")
        responses = {
            "sadness": "أسمع أنك تشعر بالحزن. هل يمكنك مشاركة المزيد؟ دعنا نحدد أفكارًا إيجابية معًا، بإذن الله.",
            "anger": "يبدو أنك غاضب. خذ نفسًا عميقًا ودعنا نفكر في تهدئة هذه المشاعر، الصبر مفتاح الفرج.",
            "joy": "رائع أنك تشعر بالفرح! الحمد لله، شارك ما يسعدك اليوم.",
            "fear": "أفهم قلقك. دعنا نتحدث عن مخاوفك ونفكر في خطوات صغيرة، بإذن الله.",
            "surprise": "هذا مفاجئ! هل تريد أن تخبرني المزيد عما حدث؟",
            "neutral": "شكرًا لمشاركتك. كيف يمكنني مساعدتك الآن؟"
        }
        fallback = responses.get(emotion, "شكرًا لمشاركتك. كيف يمكنني مساعدتك الآن؟")
        logger.info(f"Fallback response: {fallback}")
        return fallback

if __name__ == "__main__":
    sample_transcript = "أحتاج إلى المساعدة، وأريد أن أعيش معك"
    sample_emotion = "sadness"
    print(generate_therapy_response(sample_transcript, sample_emotion))
