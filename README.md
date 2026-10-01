# AI Agent Engineering App

Det här är huvudguiden för lektionen. Den innehåller all introduktion, installation, teori och steg för att köra workshopen. Denna fil är den huvudsakliga dokumentationen för studenter och lärare.

## Projektstruktur

Det rekommenderade upplägget är:

- [README.md](README.md) – huvudguide för hela projektet
- [setup-lesson6.ps1](setup-lesson6.ps1) – startpunkt för Windows
- [lesson6-agent](lesson6-agent) – själva appen och Python-exemplen
- [6. AI Agent Engineering.docx](6.%20AI%20Agent%20Engineering.docx) – valfri Word-version som referens

Det här är ett stabilt upplägg: roten fungerar som projekt- och undervisningsmapp, medan appen faktiskt ligger i [lesson6-agent](lesson6-agent).

## Vad installerar du själv?

Appens startscript förbereder en virtuell Python-miljö i projektet och installerar de Python-paket som behövs. Det installerar inte följande program eller tillägg:

- Visual Studio Code
- Python
- Git
- GitHub Copilot
- Codex
- LM Studio

Docker är valfritt. En OpenAI- eller Groq-API-nyckel behövs bara om du vill köra molnexemplen i block 5-9. Block 4 och 10 använder LM Studio lokalt och behöver ingen molnnyckel.

> ChatGPT och OpenAI API är separata tjänster. Ett ChatGPT-abonnemang ger inte automatiskt tillgång till API-krediter.

## 1. Installera VS Code och Python

### Installera Visual Studio Code

1. Gå till https://code.visualstudio.com/download
2. Ladda ner installationsfilen för ditt operativsystem
3. Kör installationsfilen och starta VS Code

### Installera Python

1. Gå till https://www.python.org/downloads/
2. Hämta Python 3.11 eller senare. Python 3.12 rekommenderas.
3. På Windows: markera Add Python to PATH om alternativet visas.
4. Kontrollera installationen i terminalen:

```powershell
python --version
```

eller:

```bash
python3 --version
```

Du ska se Python 3.11 eller senare.

### Lägg till Python-stöd i VS Code

1. Öppna Extensions i VS Code
2. Sök efter Python
3. Installera tillägget från Microsoft

Git behövs för Git-övningen. Docker behövs bara om du väljer Docker-alternativen i startmenyn.

## 2. Öppna och starta workshopappen

### Öppna projektet

1. Packa upp kursprojektet om du fick det som ZIP
2. I VS Code välj File → Open Folder
3. Öppna roten för projektet
4. Välj Terminal → New Terminal

Om du vill starta appen direkt från projektet, kör:

```powershell
cd .\lesson6-agent
.\start-lesson6.ps1
```

### Starta från rotmappen

```powershell
.\setup-lesson6.ps1
```

Det här scriptet hittar automatiskt projektmappen och startar appen.

### Om PowerShell blockerar scriptet

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup-lesson6.ps1
```

### macOS/Linux

```bash
cd lesson6-agent
bash ./start-lesson6.sh
```

## 3. Förstå appens två menyer

Appen har en startmeny och en lektionsmeny.

### Startmenyn

1. Start local lesson menu
2. Run automated tests
3. Build the Docker image
4. Start the lesson menu in Docker
5. Exit

### Lektionsmenyn

1. Check setup
2. Run offline tests
3. Cloud agent examples
4. LM Studio examples
5. Exit

Det här är viktigt att förstå: den första menyn startar miljön, den andra kör själva lektionen.

## 4. Skapa en OpenAI API-nyckel

Du behöver en API-nyckel för OpenAI-exemplen.

1. Gå till https://platform.openai.com/
2. Logga in eller skapa konto
3. Öppna https://platform.openai.com/api-keys
4. Skapa en ny hemlig nyckel
5. Kopiera nyckeln och förvara den privat
6. Kontrollera användnings- och betalningsinställningar innan du kör exempel

### Spara nyckeln lokalt

I terminalen i [lesson6-agent](lesson6-agent):

```powershell
Copy-Item .env.example .env
```

Öppna `.env` och skriv:

```env
OPENAI_API_KEY=din_hemliga_nyckel
```

Du kan också lämna värdet tomt och fylla i det senare i menyn.

> Dela aldrig nyckeln i kod, README eller GitHub.

## 5. Skapa en Groq API-nyckel

Groq är ett alternativ till OpenAI.

1. Gå till https://console.groq.com/
2. Logga in eller skapa konto
3. Öppna https://console.groq.com/keys
4. Skapa en ny nyckel
5. Öppna modellkatalogen https://console.groq.com/docs/models
6. Välj ett modell-ID som stöder verktygsanrop
7. Lägg in följande i `.env`:

```env
GROQ_API_KEY=din_hemliga_nyckel
GROQ_MODEL=modell-id-från-katalogen
```

## 6. Installera och prova GitHub Copilot

Copilot installeras separat från workshopappen.

1. Öppna Extensions i VS Code
2. Sök efter GitHub Copilot
3. Installera det
4. Logga in med GitHub
5. Öppna mappen `coding-agent-demo`
6. Testa Ask och Agent i Copilot Chat

Uppgift: jämför vad Copilot föreslog i Ask-läget med vad Agent faktiskt ändrade.

## 7. Installera och prova Codex

1. Öppna Extensions i VS Code
2. Sök efter Codex
3. Installera tillägget från OpenAI
4. Logga in när du blir ombedd
5. Använd en kopia av `coding-agent-demo`
6. Ge Codex samma uppgift: hantera tom lista med `ValueError`, lägg till pytest-test och kör testerna
7. Jämför resultatet med Copilot

## 8. Installera och starta LM Studio

LM Studio kör en AI-modell lokalt.

1. Gå till https://lmstudio.ai/download
2. Installera och starta LM Studio
3. Ladda ner en mindre modell som passar datorns minne
4. Ladda modellen i minnet
5. Öppna servervyn och starta den lokala API-servern
6. Standardadress: http://localhost:1234/v1
7. I lektionsmenyn välj 1 för kontroll och 4 för LM Studio-exempel

LM Studio-exemplen kräver att servern är startad.

## 9. Exempel och uppgifter i appen

### OpenAI-exempel

När du väljer 3 → OpenAI visas:

1. Basic agent
2. Agent with tools
3. Structured output
4. Human approval
5. Tool validation
6. Input guardrail
7. MCP client and server

### Groq-exempel

När du väljer 3 → Groq visas:

1. Basic agent
2. Agent with tools
3. MCP

### LM Studio-exempel

När du väljer 4 → LM Studio visas:

1. LM Studio connection test
2. Keyword retrieval / RAG demo

## 10. Säker hantering av nycklar

- Dela aldrig en OpenAI- eller Groq-nyckel i klassrummet, i en skärmbild, i en chatt eller på GitHub
- Lägg nyckeln i `.env`, aldrig i Python-koden
- Om du råkar dela en nyckel, återkalla den och skapa en ny
- Molnexemplen skickar frågor till den valda tjänsten
- LM Studio-exemplen kör lokalt på din egen dator och behöver ingen molnnyckel

## 11. Efter workshopen

Du ska kunna:

- starta appen
- förklara vad de två menyerna gör
- skilja mellan offline-tester, molnanrop och lokala modellkörningar
- visa en kodändring
- beskriva hur en agent använder ett verktyg
- förstå hur säkerhetslagren fungerar
- hålla API-nycklar privata

## 12. Officiella guider

- VS Code: https://code.visualstudio.com/download
- Python: https://www.python.org/downloads/
- Python i VS Code: https://code.visualstudio.com/docs/python/python-quick-start
- OpenAI API keys: https://platform.openai.com/api-keys
- OpenAI API quickstart: https://developers.openai.com/api/docs/quickstart
- OpenAI Help Center: https://help.openai.com/en/articles/9039756
- Groq API keys: https://console.groq.com/keys
- Groq model catalog: https://console.groq.com/docs/models
- LM Studio: https://lmstudio.ai/download
- LM Studio docs: https://lmstudio.ai/docs/app

## Kör tester

Från projektmappen:

```powershell
cd .\lesson6-agent
python -m pytest -q
```

Om bibliotek saknas, kör:

```powershell
python -m pip install -r .\lesson6-agent\requirements.txt
```

## Path-independens

Det här projektet är byggt så att det fungerar oberoende av exakt mapplats. Det använder `Path(__file__).resolve().parent` och kör subprocesser med rätt `cwd`-värde. Det betyder att appen kan köras från olika kataloger utan att behöva flyttas.

## Vanliga problem

### Python saknas

Installera Python 3.11+ och starta om terminalen.

### ModuleNotFoundError

```powershell
python -m pip install -r .\lesson6-agent\requirements.txt
```

### Docker fungerar inte

Se till att Docker Desktop är installerat och körs.

### Långa Windows-sökvägar

Använd Docker eller placera projektet i en kortare katalog om du får problem med långa sökvägar.

## Sammanfattning

Det bästa upplägget är:

- rotmappen som projekt- och dokumentationsmapp
- [lesson6-agent](lesson6-agent) som själva app-kod
- huvudguiden i [README.md](README.md)
- [6. AI Agent Engineering.docx](6.%20AI%20Agent%20Engineering.docx) som valfri referens

Detta undviker dubbel information och gör att studenterna följer en tydlig, nybörjaranpassad flow.

