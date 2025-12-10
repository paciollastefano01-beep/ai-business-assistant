# 💼 AI Business Assistant

Assistente AI personalizzato per piccole attività locali italiane.

Fornisce consulenza su marketing, promozioni, messaggi clienti, social media e automazioni semplici.

---

## 🚀 Features

- **Configurazione business personalizzata**: tipo attività, città, obiettivi
- **Consulenza AI mirata**: risposte adattate al tuo business specifico
- **Tono personalizzabile**: professionale, amichevole o diretto
- **Cronologia conversazione**: mantiene il contesto della chat
- **Deploy facile**: funziona sia in locale che su Streamlit Cloud

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**: UI interattiva
- **OpenAI API (GPT-4.1-mini)**: motore AI
- **python-dotenv**: gestione variabili ambiente

---

## 📦 Installazione locale

```bash
# Clone repository
git clone https://github.com/paciollastefano01-beep/ai-business-assistant.git
cd ai-business-assistant

# Crea ambiente virtuale
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Crea file .env con la tua API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Avvia app
streamlit run app.py
```

---

## 🌐 Deploy su Streamlit Cloud

1. Pusha il repository su GitHub
2. Vai su [Streamlit Cloud](https://share.streamlit.io/)
3. Collega il repository
4. Aggiungi `OPENAI_API_KEY` in Settings → Secrets:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

5. Deploy automatico

---

## 💡 Casi d'uso

- **Ristoranti**: idee promozioni, messaggi WhatsApp clienti, post social
- **Negozi**: strategie aumento vendite, offerte stagionali, fidelizzazione
- **Professionisti**: contenuti marketing, email campagne, automazioni
- **Centri estetici/palestre**: gestione prenotazioni, reminder automatici

---

## 📄 License

MIT

---

## 👤 Author

**Stefano Paciolla**

[GitHub](https://github.com/paciollastefano01-beep)
