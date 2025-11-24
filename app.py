import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Carica le variabili dal file .env (solo in locale)
load_dotenv()


def get_openai_client() -> OpenAI:
    """
    Recupera la API key da:
    1. st.secrets["OPENAI_API_KEY"] (quando sei su Streamlit Cloud)
    2. variabile ambiente OPENAI_API_KEY (quando sei in locale con .env)
    """
    api_key = None

    # 1. Prova a leggere dai secrets di Streamlit (sul cloud)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    # 2. Se non trovata, prova dalla variabile ambiente (.env in locale)
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error(
            "❌ OPENAI_API_KEY non trovata.\n\n"
            "➜ In locale: assicurati di avere un file `.env` con `OPENAI_API_KEY=...`.\n"
            "➜ Su Streamlit Cloud: imposta la chiave in *Settings → Secrets*."
        )
        st.stop()

    # Crea il client OpenAI usando la chiave trovata
    client = OpenAI(api_key=api_key)
    return client


def build_system_prompt(
    business_type: str,
    business_name: str,
    business_city: str,
    business_description: str,
    main_goal: str,
    tone: str,
) -> str:
    """
    Crea il messaggio di sistema che definisce il ruolo dell'assistente.
    """
    prompt = f"""
Sei un consulente di business e marketing specializzato in piccole attività locali italiane.

DATI ATTIVITÀ:
- Tipo di attività: {business_type}
- Nome: {business_name}
- Città / zona: {business_city}
- Descrizione: {business_description}
- Obiettivo principale: {main_goal}

STILE RISPOSTE:
- Tono: {tone}
- Linguaggio semplice e pratico, adatto a imprenditori e commercianti
- Fornisci risposte strutturate con punti elenco e passi concreti
- Quando utile, suggerisci esempi di messaggi, post social, email, offerte specifiche
- Mantieni le risposte focalizzate su risultati misurabili (clienti, fatturato, prenotazioni, ecc.)

COSA PUOI FARE:
- Idee di promozioni e offerte
- Strategie per aumentare clienti e fatturato
- Messaggi per WhatsApp, SMS, email
- Idee per contenuti social
- Migliorare l'esperienza clienti
- Consigli su automazioni semplici (es. risposte automatiche, reminder)

Rispondi sempre in ITALIANO.
Adatta le risposte alla tipologia di attività e alla città indicata.
    """.strip()

    return prompt


def generate_response(client: OpenAI, system_prompt: str, conversation: list[dict]) -> str:
    """
    Manda la conversazione al modello OpenAI e restituisce la risposta testuale.
    """
    # Partiamo dal messaggio di sistema
    messages = [{"role": "system", "content": system_prompt}]

    # Aggiungiamo tutti i messaggi della chat (user/assistant)
    for msg in conversation:
        role = msg.get("role")
        content = msg.get("content", "")
        if role in ("user", "assistant"):
            messages.append({"role": role, "content": content})

    # Chiamata al modello
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # modello veloce ed economico
        messages=messages,
        temperature=0.6,       # 0 = molto rigoroso, 1 = creativo
        max_tokens=800,
    )

    return response.choices[0].message.content


def main():
    # Impostazioni pagina Streamlit
    st.set_page_config(
        page_title="AI Business Assistant",
        page_icon="💼",
        layout="centered",
    )

    st.title("💼 AI Business Assistant per attività locali")
    st.write(
        "Fai domande su **marketing, offerte, messaggi ai clienti, contenuti social, automazioni semplici**, "
        "pensate per piccoli business locali."
    )

    # Inizializza il client OpenAI
    client = get_openai_client()

    # SIDEBAR: impostazioni dell'attività
    with st.sidebar:
        st.header("⚙️ Impostazioni business")

        business_type = st.selectbox(
            "Tipo di attività",
            [
                "Ristorante / Bar",
                "Negozio al dettaglio",
                "Professionista (avvocato, consulente, coach, ecc.)",
                "Centro estetico / Parrucchiere",
                "Palestra / Centro sportivo",
                "Altro",
            ],
        )

        business_name = st.text_input("Nome dell'attività", value="La tua attività")
        business_city = st.text_input("Città / zona", value="La tua città")

        business_description = st.text_area(
            "Descrizione breve",
            value=(
                "Descrivi cosa vendi, chi sono i tuoi clienti ideali, "
                "fascia di prezzo, punti di forza, ecc."
            ),
            height=100,
        )

        main_goal = st.selectbox(
            "Obiettivo principale",
            [
                "Aumentare i clienti",
                "Aumentare lo scontrino medio",
                "Aumentare le prenotazioni",
                "Lanciare un nuovo servizio/prodotto",
                "Migliorare la fidelizzazione dei clienti",
            ],
        )

        tone = st.selectbox(
            "Tono delle risposte",
            ["Professionale", "Amichevole", "Molto diretto"],
        )

        st.markdown("---")
        if st.button("🔄 Reset conversazione"):
            st.session_state.messages = []
            st.experimental_rerun()

    # Crea il system prompt in base alle impostazioni
    system_prompt = build_system_prompt(
        business_type=business_type,
        business_name=business_name,
        business_city=business_city,
        business_description=business_description,
        main_goal=main_goal,
        tone=tone,
    )

    # Inizializza la cronologia dei messaggi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra la cronologia della chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input utente (campo in basso)
    user_input = st.chat_input("Scrivi una domanda per l'assistente business...")

    if user_input:
        # Aggiungi il messaggio dell'utente alla cronologia
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Mostra il messaggio utente
        with st.chat_message("user"):
            st.markdown(user_input)

        # Genera la risposta del modello
        with st.chat_message("assistant"):
            with st.spinner("Sto pensando a una strategia per il tuo business..."):
                response_text = generate_response(
                    client=client,
                    system_prompt=system_prompt,
                    conversation=st.session_state.messages,
                )
                st.markdown(response_text)

        # Salva la risposta nella cronologia
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )


if __name__ == "__main__":
    main()