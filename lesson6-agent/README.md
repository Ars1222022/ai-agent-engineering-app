# Lektion 6 — AI Agent Engineering

Den här guiden visar steg för steg hur du förbereder och genomför workshopen i VS Code. Följ blocken i ordning. Menynamn är skrivna som de vanligtvis visas i VS Code och programmen.

**Lektionsflöde:** Block 0 setup → Block 1 kontroll → Block 2–4 manuell installation och inloggning → Block 5–10 Python-exempel och elevuppgifter. LangGraph och multi-agent hör till Lektion 7, inte den här workshopen.

## 1. Installera och öppna projektet

### Program som behövs

- **Visual Studio Code:** [Ladda ner för Windows, macOS eller Linux](https://code.visualstudio.com/download) och installera.
- **Python 3.12 rekommenderas**, minst 3.11 för lokal körning: [python.org/downloads](https://www.python.org/downloads/). I Windows-installationen väljer du alternativet att lägga Python i PATH om det visas.
- **Git:** [git-scm.com/downloads](https://git-scm.com/downloads). Behövs för Git-övningen och för att jämföra kodändringar.
- **Docker Desktop eller Docker Engine är valfritt**. Det behövs för Docker-körning, inte när lokal Python fungerar: [Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [macOS](https://docs.docker.com/desktop/setup/install/mac-install/), [Linux](https://docs.docker.com/engine/install/).

`setup-lesson6.ps1` och startskripten installerar inte Python, Git, VS Code eller tillägg globalt. Projektets venv, paket, nyckelfil, markör och temporära installationsfiler ligger i `lesson6-agent`-mappen. Lokal körning använder Python-runtime som redan finns på datorn; den kopieras inte till projektet. Docker kan användas i stället.

### Öppna kursprojektet i VS Code

1. Hämta kursens repo eller ZIP från läraren. Packa upp ZIP-filen.
2. Starta VS Code.
3. Välj **File → Open Folder** och öppna `lesson6-agent`. Om du ska köra hela workshopens Windows-setup öppnar du i stället den överordnade workshopmappen.
4. Öppna **Terminal → New Terminal**. Terminalen ska stå i mappen du tänker köra scriptet från.

## 2. Starta projektet

### Windows: full workshopmapp

Kör från workshopmappens rot:

```powershell
.\setup-lesson6.ps1
```

Det här är Block 0:s workshop-setup. Om det färdiga `lesson6-agent` redan finns öppnar setupscriptet dess startmeny i stället för att skriva över projektfilerna.

### Windows: endast `lesson6-agent`

Kör från `lesson6-agent`:

```powershell
.\start-lesson6.ps1
```

Om PowerShell blockerar scriptet kan du tillåta script för den aktuella terminalsessionen och försöka igen:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\start-lesson6.ps1
```

### macOS/Linux

Kör från `lesson6-agent` i VS Codes terminal:

```bash
bash ./start-lesson6.sh
```

### Välj lokal Python eller Docker

Startmenyn har dessa val:

1. **Starta lokal meny:** skapar projektets `venv` och installerar dess paket om det behövs, och öppnar sedan lektionsmenyn.
2. **Kör automatiska tester:** samma projektmiljö, sedan körs offline-tester.
3. **Bygg Docker-imagen:** bygger projektets container.
4. **Starta lektionsmenyn i Docker:** kör menyn i containern. Containern tas bort när du avslutar; imagen ligger kvar.

Docker måste vara installerat och startat innan du väljer 3 eller 4. Docker innehåller Python-paketen men inte OpenAI-/Groq-nycklar eller en AI-modell. Docker Desktop lagrar imagen i sin egen dataplats, inte i projektmappen. Om även Docker-data måste ligga på D: behöver Docker Desktop konfigureras separat. Välj lokal meny (1) om venv och paket ska ligga i projektmappen.

**Viktigt för den här Windows-workspace-sökvägen:** den är lång. Startscriptet använder vid behov en ledig tillfällig enhetsbokstav som pekar på samma `lesson6-agent`-mapp. Det flyttar eller kopierar inte projektet. Venv, installerade paket och temporära installationsfiler sparas fysiskt i projektmappen på D:. En liten `.lesson6-drive`-markör i projektet hjälper startscriptet hitta samma mapp nästa gång. `python lab_launcher.py` visar bara menyn och installerar inte paket; använd startscriptet första gången.

## 3. Block 1 — Kontrollera installationen

I lektionsmenyn:

- Välj **1** för paket-, fil-, nyckelstatus- och LM Studio-kontroll.
- Välj **2** för de automatiska testerna.

En saknad OpenAI/Groq-nyckel är normal tills du väljer den tjänsten. En LM Studio-varning är normal om LM Studio inte är installerat eller servern inte är startad.

Testerna kör lokala hjälpfunktioner och provider-konfiguration. De kontaktar inte OpenAI, Groq eller LM Studio och kan därför inte bevisa att en API-nyckel eller modell fungerar.

## 4. Skaffa en moln-API-nyckel (valfritt)

Molnnyckel behövs för molnexemplen i Block 5–9. Välj **OpenAI eller Groq**. LM Studio i Block 4 och 10 kör lokalt och behöver ingen molnnyckel. OpenAI API debiteras separat från ChatGPT-abonnemang; kontrollera konto, pris och eventuell kredit innan du kör exempel.

### OpenAI

1. Logga in eller skapa konto på [OpenAI API Platform](https://platform.openai.com/).
2. Gå till [API keys](https://platform.openai.com/api-keys) och välj att skapa en ny hemlig nyckel.
3. Kopiera nyckeln när den visas. Förvara den privat; visa eller skicka den inte till någon.
4. I VS Code Explorer kopierar du `.env.example` till en ny fil som heter `.env`.
   - PowerShell: `Copy-Item .env.example .env`
   - macOS/Linux: `cp .env.example .env`
5. Öppna `.env` och klistra nyckeln efter `OPENAI_API_KEY=`. Spara filen.
6. I menyn välj **3 → OpenAI**. Du kan i stället lämna raden tom och klistra in nyckeln när den dolda frågan visas. Den nyckeln sparas inte mellan körningar.

OpenAI:s [API quickstart](https://developers.openai.com/api/docs/quickstart) beskriver konto, nyckel och API-användning. API-användning kan kräva betalningsuppgifter/krediter.

### Groq (valfritt alternativ)

1. Logga in eller skapa konto i [Groq Console](https://console.groq.com/).
2. Öppna [API Keys](https://console.groq.com/keys), skapa en ny nyckel och kopiera den privat.
3. Öppna Groqs [modellkatalog](https://console.groq.com/docs/models). Välj ett modell-ID som är tillgängligt för ditt konto och stöder verktygsanrop.
4. I `.env`, fyll i `GROQ_API_KEY=` med nyckeln och `GROQ_MODEL=` med modell-ID:t.
5. Välj **3 → Groq** i menyn. Groq-menyn erbjuder grundagent, verktygsagent och MCP. Stöd för andra Agents SDK-funktioner varierar mellan modeller.

Lägg aldrig en riktig nyckel i Python-filer, README eller GitHub. `.env` ignoreras av Git. Om en nyckel råkar delas, återkalla den hos leverantören och skapa en ny.

## 5. Block 2–4 — Installera och logga in manuellt

Dessa program installeras och konfigureras separat. Lektionsmenyn installerar eller loggar inte in åt dig.

### Block 2 — GitHub Copilot i VS Code

1. Starta VS Code och öppna `coding-agent-demo/`.
2. Klicka Copilot-ikonen i statusfältet och välj **Use AI Features**. Om ikonen saknas, följ [VS Codes Copilot-startguide](https://code.visualstudio.com/docs/copilot/setup).
3. Välj **Sign in with GitHub**. Logga in i webbläsaren och godkänn anslutningen till VS Code.
4. Kontrollera din plans tillgänglighet och användningsgräns. Behöriga konton kan erbjudas Copilot Free; se den officiella guiden för aktuella villkor.
5. Öppna Copilot Chat. Välj **Ask** och be den förklara `calculate_average`, beskriva vad som händer med en tom lista och föreslå saknade tester. Ask ska bara analysera.
6. Byt till **Agent**. Be den hantera tom lista med ett tydligt `ValueError`, lägga till pytest-test och köra testerna. Granska filerna den ändrar.

### Block 3 — Codex i VS Code

1. Behåll en orörd kopia av `coding-agent-demo/` innan Copilot gör ändringar. Använd en kopia för Codex så verktygen får samma startkod.
2. I VS Code öppna **Extensions** (`Ctrl+Shift+X`; på Mac `Cmd+Shift+X`). Sök efter **Codex – OpenAI's coding agent**, utgivare OpenAI. Alternativt öppna [Codex på VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt).
3. Installera extensionen och öppna Codex-ikonen. Om ikonen inte syns, öppna Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) och kör **Codex: Open Codex Sidebar**.
4. Logga in med ChatGPT-kontot och kontrollera planåtkomst enligt [Codex IDE-guiden](https://learn.chatgpt.com/docs/codex/ide).
5. Öppna kopian av `coding-agent-demo/` och ge Codex samma uppgift som Copilot.
6. Jämför filer, tester, felhantering och hur mycket styrning du behövde ge. **Copilot och Codex är produkter; agent är ett arkitekturkoncept.**

### Block 4 — LM Studio och lokal modell

1. Hämta LM Studio för ditt operativsystem från [lmstudio.ai/download](https://lmstudio.ai/download) och installera appen.
2. Starta LM Studio. Öppna **Discover**, sök efter en liten modell och välj en variant som passar datorns minne. En kvantiserad Q4-variant är ofta en rimlig början; se [LM Studios modellguide](https://lmstudio.ai/docs/app/basics/download-model).
3. Ladda ner modellen och vänta tills nedladdningen är färdig.
4. Öppna **Developer**, ladda modellen om det behövs och slå på **Start server**. Projektets standardadress är `http://localhost:1234/v1`. Se [LM Studio serverguide](https://lmstudio.ai/docs/developer/core/server).
5. I lektionsmenyn välj **1**. Kontrollera att LM Studio-modellen hittas.
6. Välj **4 → LM Studio connection test**. Förväntat: ett svar från den lokala modellen.
7. Välj sedan **4 → Keyword retrieval / RAG demo**.

`test-lmstudio.ps1` är en extra Windows-kontroll. Den fungerar inte i macOS/Linux; använd lektionsmenyn där. I Docker Desktop på Windows/macOS används normalt `host.docker.internal`. På Linux kan Docker behöva extra värdkoppling för att nå LM Studio; om det inte fungerar, kör LM Studio-exemplen lokalt på värden.

## 6. Block 5–10 — Kör och ändra Python-exemplen

1. **Block 5 — Första agenten:** välj **3 → OpenAI → Basic agent**. Ändra frågan i `app.py` till exempelvis `Explain function calling to a beginner.` och kör igen.
2. **Block 6 — Agent + Tools:** välj **Agent with tools**. Se hur agenten använder kursinfo och addition. Övning: lägg till `reverse_text(text: str) -> str` i `tools/course_tools.py`, importera funktionen och lägg den i agentens `tools` i `app_tool.py`. Lägg till en fråga som ber agenten vända ordet `Python`.
3. **Block 7 — Structured Output:** kör exemplet. Lägg till `beginner_friendly: bool` i `CourseAnswer` i `app_structured.py`, skriv ut fältet och kör igen. Schemat styr formatet, inte om svaret är sant. `confidence` är modellens uppskattning, inte en kalibrerad sannolikhet.
4. **Block 8 — Security:** från OpenAI-menyn kör **Human approval**, **Tool validation** och **Input guardrail**. Godkänn/neka den simulerade e-posten. Kontrollera att filoperationen bara simuleras och att osäker sökväg blockeras. Se att guardrailen stoppar testfrasen. Inget riktigt mejl skickas och ingen fil raderas. Exemplen är pedagogiska, inte produktionssäkerhet.
5. **Block 9 — MCP:** välj **MCP client and server**. Klienten startar servern automatiskt och frågar efter kursinfo samt använder räknaren. Starta inte MCP-servern manuellt. Jämför MCP med det direkta Python-verktyget.
6. **Block 10 — Mini-RAG:** välj **LM Studio → Keyword retrieval / RAG demo**. Programmet söker efter nyckelord i `knowledge/course_notes.txt` och skickar den hittade texten till modellen som kontext. Ändra gärna frågan i `app_rag_demo.py` och kör igen.

Den här mini-RAG-demon använder inte embeddings eller vector database. De delarna, LangGraph och multi-agent byggs i Lektion 7 och ingår inte i denna workshop.

## Vad testar menyn?

- **Meny 1 — Kontroll:** visar vilken Python som kör, saknade paket/filer, om API-nycklar verkar konfigurerade och om LM Studio svarar. En saknad nyckel är inte ett fel om du inte ska använda den providern.
- **Meny 2 — Offline-tester:** fem tester av verktygsfunktioner och provider-konfiguration. Inga moln- eller LM Studio-anrop görs och inga kostnader uppstår.
- **Meny 3 — OpenAI/Groq:** gör ett riktigt modell-anrop. Kräver fungerande nyckel, tillgänglig modell och eventuellt credits/kvot hos leverantören.
- **Meny 4 — LM Studio:** gör ett riktigt lokalt modell-anrop. Kräver installerad LM Studio, nedladdad/laddad modell och startad API-server.

Om menyn säger `MISSING package` har du sannolikt startat `lab_launcher.py` med systemets Python. Avsluta den och kör startscriptet igen så används projektets venv, eller välj Docker. Vid Windows `WinError 206` i den här långa sökvägen ska du välja Docker eller flytta projektet till en kortare sökväg.

## Officiella länkar

- [VS Code](https://code.visualstudio.com/download) · [Python](https://www.python.org/downloads/) · [Git](https://git-scm.com/downloads)
- [Docker för Windows](https://docs.docker.com/desktop/setup/install/windows-install/) · [macOS](https://docs.docker.com/desktop/setup/install/mac-install/) · [Linux](https://docs.docker.com/engine/install/)
- [Copilot i VS Code](https://code.visualstudio.com/docs/copilot/setup) · [Codex IDE](https://learn.chatgpt.com/docs/codex/ide)
- [OpenAI API keys](https://platform.openai.com/api-keys) · [OpenAI API guide](https://developers.openai.com/api/docs/quickstart)
- [Groq API keys](https://console.groq.com/keys) · [Groq model catalog](https://console.groq.com/docs/models)
- [LM Studio download](https://lmstudio.ai/download) · [Ladda ner modell](https://lmstudio.ai/docs/app/basics/download-model) · [Starta API server](https://lmstudio.ai/docs/developer/core/server)
