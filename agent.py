"""
AwaazBank — LangChain Agentic KYC Flow
Drives the full onboarding conversation autonomously.
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# ── Tools the agent can call ────────────────────────────────────────────────

@tool
def send_whatsapp_message(phone_number: str, message: str, voice: bool = True) -> str:
    """Send a message (text or voice) back to the user on WhatsApp."""
    # TODO: integrate with WhatsApp Business API
    print(f"[WhatsApp → {phone_number}] {'🔊' if voice else '💬'} {message}")
    return "Message sent"


@tool
def verify_aadhaar_otp(aadhaar_number: str, otp: str) -> str:
    """Verify Aadhaar OTP for KYC. Returns 'verified' or 'failed'."""
    # TODO: integrate with UIDAI Aadhaar OTP API
    if len(otp) == 6 and otp.isdigit():
        return "verified"
    return "failed"


@tool
def check_liveness(image_base64: str) -> str:
    """Run selfie liveness check using AWS Rekognition. Returns 'live' or 'spoof'."""
    # TODO: integrate with AWS Rekognition
    return "live"


@tool
def open_sbi_account(name: str, aadhaar: str, account_type: str) -> str:
    """Open an SBI account via Core Banking API. Returns account number."""
    # TODO: integrate with SBI Core Banking API
    import random
    account_number = f"SBI{random.randint(10000000, 99999999)}"
    return account_number


@tool
def translate_and_speak(text: str, language_code: str) -> str:
    """Translate text to target language and convert to voice using Bhashini TTS."""
    # TODO: integrate with Bhashini TTS API
    return f"[Voice in {language_code}]: {text}"


# ── Agent setup ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are AwaazBank, a friendly AI banking assistant for SBI. 
Your job is to help rural Indian users open a bank account over WhatsApp voice.

Follow this exact flow:
1. Greet the user warmly in their language
2. Ask which type of account they want (Savings / Jan Dhan)
3. Ask for their Aadhaar number
4. Send OTP and verify it
5. Ask them to take a selfie for liveness check
6. Open the account and share the account number
7. Congratulate them!

Always respond in the same language the user speaks.
Be warm, patient, and simple — your users may not be tech-savvy.
Never ask for more than one piece of information at a time.
"""

def build_agent(language_code: str = "hi") -> AgentExecutor:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    tools = [
        send_whatsapp_message,
        verify_aadhaar_otp,
        check_liveness,
        open_sbi_account,
        translate_and_speak,
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_openai_functions_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
    )


# ── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent = build_agent(language_code="hi")
    print(agent.invoke({"input": "Mujhe SBI mein khata kholna hai"}))
