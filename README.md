# NovelAgents
 Code for my Bachelor Thesis on a Multi-Agent System writing a novel.
 
 # The Idea
 The idea is to seperate each stage of writing a novel into a task completable by two or more AI agents. 
 The tasks are: 
 - Brainstorming for characters, setting, plot and conflict into readable json strings
 - Plotting what's to happen with the material from the brainstorming stage into a scene structure
 - Writing the given scenes
 - Revising the written scenes

 # Installation Guide
 Installationsguide NovelAgents

1. Python3.10.11 von der Seite www.python.org/downloads/release/python-31011 herunterladen und installieren oder überprüfen, ob es auf der Maschine bereits vorhanden ist
2. von www.ollama.com den ollama server herunterladen und installieren oder überprüfen, ob es auf der Maschine bereits Vorhanden ist 
    --> aufpassen mit Intel GPUs! Hierfür ollama mithilfe dieser Anweisung herunterladen! https://www.intel.de/content/www/de/de/content-details/826081/running-ollama-with-open-webui-on-intel-hardware-platform.html
	-> über die command line können mithilfe von ollama ki-modelle lokal auf dem eigenen rechner laufen
	-> welche ki-modelle es gibt und mit welchen befehlen, du sie pullst, kannst du auf der ollama website herausfinden
	-> der Algorithmus benutzt zu jeder zeit maximal zwei Agenten zeitgleich. dein Gerät sollte also zur Benutzung von OLLAMA Modellen genügend RAM haben, um zwei Modelle zeitgleich laufen lassen zu können. Das können verschiedene Modelle sein
3. Node.js installieren (nodejs.org/en/download) oder überprüfen, ob es auf der Maschine verfügbar ist 
	-> für die Dokumentation tippe ollama in die cmd
4. Repository von Github herunterladen (hierfür kann GitHub desktop genutzt werden)
5. in Novel Agents repository mit python3.10.11 ein virtualenvironment aufsetzen 
	-> Befehl auf Windows, wenn im Ordner: python3.10 -m venv
		-> Version von Python kann mit python --version gecheckt werden
		-> Bei Problemen, PC aus und wieder an machen, bzw PowerShell schließen und wieder öffnen
		-> wenn die python version noch immer nicht erkannt wird, kann mit >& "Path\to\your\python.exe" -m venv "Path\to\your\desired\locatioin\venv"< ein venv mit dem Namen venv aufgesetzt werden (um Namen zu ändern, ändere den letzten Teil des zweiten Paths
6. das virtual environment aktivieren
	-> auf Windows mit "venv/Scripts/activate" (venv durch Namen des Virtual Environments austauschen)
7. mit pip die requirements.txt auslesen und herunterladen
	-> auf Windows mit pip install -r requirements.txt
		-> so wird alles notwendige in das virtual environment geladen
8. installiere die packages aus der package.json
	-> benutze npm install
9. eine eigene .env Datei anlegen	
	-> sollte unter OLLAMA_PATH den Path zur Ollama exe enthalten
	-> sollte unter OPENAI_API_KEY den zu verwendenden OpenAI API Key enthalten

## Trouble-Shooting
Im Falle der nicht Erkennung von der installierten packages, gehen Sie sicher, dass ihre Coding Umgebung den korrekten python Interpret benutzt! 
	-> In VSCode können Sie dazu Strg+Shift+P drücken, Python Interpreter in die Such-leiste eintippen und dann den python Interpret Ihres virtual environment auswählen.



 # What I have so far
 I have two agents who brainstorm characters together. One writes a character into a pre-defined json string, 
 the other gives feedback and tries to make the general statements of the first agent more specific. 
 On my Laptop with 16GB of RAM with two 4.2GB models (olmo2) this takes approximately 10 minutes per character. 
 I can try to improve effiency by not letting the critic give free-form feedback but also write into the json 
 string directly and then reducing the loops needed. 
 Brainstorming two characters needed 1158.61 seconds (~19,3 minutes) during my last trial. I hope I can bring this down somehow. 
 Maybe I can try if an AI society would be faster with this. 
 I also do not know, if the characters are generated with knowledge of the characters generated previously. But for further generation
 of Plot and the like I should load the memory json file into the brainstorming agents. 

 # Open Issues
 - Fallback for repeated answers has to be implemented: If an answer towards the end of the cycle fails to load into a pydanctic model it should instead use an earlier functioning answer instead to write to memory.
 - SavingIssueExpection from StoryGlossary.py isn't declared anywhere 
 - Problem with running the same model for too long. when tasked to write ten scenes, it crashes after four to five scenes because of time out. I have to figure out, if that is only because of my machine or if that also happens on other machines. 
 
 # Tasks for Tomorrow
 - Refactoring of Code
 - Isn't checking if OpenAI API key or OLLAMA path are actually working. Maybe it does that when they get initialized? That means, I'll have to move the try except statements to the initialize_agent_tasks() method. 
- schlaf drüber, ob du wirklich einen Regler für jede Überarbeitung brauchst. Für so ein generelles Tool sollte eines doch auch reichen. Wenn schon ein KI Modell reicht ...