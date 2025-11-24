from dotenv import load_dotenv
from openai import OpenAI

# Carica le variabili dal file .env
load_dotenv()

# Crea il client OpenAI (usa OPENAI_API_KEY dal .env)
client = OpenAI()

def main():
    print("Invio una richiesta di test a OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # modello economico e veloce
        messages=[
            {"role": "system", "content": "Sei un assistente utile che risponde in italiano."},
            {"role": "user", "content": "Scrivi una frase di test in massimo 10 parole."}
        ],
        max_tokens=50,
    )

    print("\nRisposta dal modello:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()