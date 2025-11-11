from openai import OpenAI
from django.conf import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def _clean_ai_text(text: str) -> str:
    """Normalize AI text by removing stray leading/trailing quotes and trimming whitespace.

    Handles straight and smart quotes, and removes multiple leading quote characters
    that sometimes appear at the start of the generation.
    """
    if not text:
        return text
    t = text.strip()
    # Common quote characters that might wrap or lead the content
    quotes = {'"', "'", '“', '”', '‘', '’', '«', '»', '`'}
    # If wrapped in matching quotes, strip them once
    if len(t) >= 2 and t[0] in quotes and t[-1] in quotes:
        t = t[1:-1].strip()
    # Also remove any repeated leading quote characters
    while t and t[0] in quotes:
        t = t[1:].lstrip()
    return t


def get_car_ai_bio(model, brand, year):
    message = '''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year).strip()
    response = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': message
            }
        ],
        max_tokens=1000,
        model='gpt-3.5-turbo',
    )
    raw = response.choices[0].message.content
    return _clean_ai_text(raw)
