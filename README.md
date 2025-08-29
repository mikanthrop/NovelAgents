# NovelAgents
 Dieses Repository beinhaltet den Code von NovelAgents, einem Multiagentensystem, das mit fünf Agenten in drei Phasen eine Geschichte von unterschiedlicher Länge generieren kann. 
 Dieses System ist gebaut mit ([Camel AI](https://github.com/camel-ai/camel)) von Li et al., [json_repair](https://github.com/mangiucugna/json_repair) von Stefano Baccianella und [Ollama](https://ollama.com/).

# Installation Guide
Installationsguide NovelAgents

1. Python3.10.11 von der Seite www.python.org/downloads/release/python-31011 herunterladen und installieren oder überprüfen, ob es auf der Maschine bereits vorhanden ist
2. von www.ollama.com den ollama server herunterladen und installieren oder überprüfen, ob es auf der Maschine bereits Vorhanden ist 
    --> aufpassen mit Intel GPUs! Hierfür ollama mithilfe dieser Anweisung herunterladen! https://www.intel.de/content/www/de/de/content-details/826081/running-ollama-with-open-webui-on-intel-hardware-platform.html
	-> über die command line können mithilfe von ollama ki-modelle lokal auf dem eigenenRrechner laufen
	-> welche KI-modelle es gibt und mit welchen befehlen, du diese pullst, kannst du auf der Ollama Website herausfinden
	-> der Algorithmus benutzt zu jeder zeit maximal zwei Agenten zeitgleich. dein Gerät sollte also zur Benutzung von OLLAMA Modellen genügend RAM haben, um zwei Modelle zeitgleich laufen lassen zu können. Das können verschiedene Modelle sein
3. Repository von Github herunterladen (hierfür kann GitHub desktop genutzt werden)
4. in Novel Agents repository mit python3.10.11 ein virtualenvironment aufsetzen 
	-> Befehl auf Windows, wenn im Ordner: python3.10 -m venv
		-> Version von Python kann mit python --version gecheckt werden
		-> Bei Problemen, PC aus und wieder an machen, bzw PowerShell schließen und wieder öffnen
		-> wenn die python version noch immer nicht erkannt wird, kann mit >& "Path\to\your\python.exe" -m venv "Path\to\your\desired\locatioin\venv"< ein venv mit dem Namen venv aufgesetzt werden (um Namen zu ändern, ändere den letzten Teil des zweiten Paths
5. das virtual environment aktivieren
	-> auf Windows mit "venv/Scripts/activate" (venv durch Namen des Virtual Environments austauschen)
6. mit pip die requirements.txt auslesen und herunterladen
	-> auf Windows mit pip install -r requirements.txt
		-> so wird alles notwendige in das virtual environment geladen
7. eine eigene .env Datei anlegen	
	-> sollte unter OLLAMA_PATH den Path zur Ollama exe enthalten
	-> sollte unter OPENAI_API_KEY den zu verwendenden OpenAI API Key enthalten

## Trouble-Shooting
Im Falle der nicht Erkennung von der installierten packages, gehen Sie sicher, dass iIhre Coding Umgebung den korrekten python Interpret benutzt! 
	-> In VSCode können Sie dazu Strg+Shift+P drücken, Python Interpreter in die Suchleiste eintippen und dann den python Interpret Ihres virtual environment auswählen.

# Funktionsweise des Algorithmus
Das NovelAgents-System wird mit einer GUI gesteuert, in die BenutzerInnen Zielgruppe, Genre und Thema der gewünschten Geschichte eingeben können. Weitergehend können sie festlegen, wie viele Charaktere das System generiert, wie viele Kapitel es schreibt und welches Modell als Grundlage der Agenten dieses Multiagentensystems dient. Das System ist in drei Teile aufgeteilt: 
1. Die Brainstorming-Phase, in der Setting, Charaktere und Plot von einem Planer und einem Kritiker geplant werden. Bei vollständiger Abschließung entsteht ein StoryGlossary-Objekt, das im weiteren Verlauf des Systems genutzt wird. 
2. Die Scene-Prompting-Phase, in der ein TaskPlannerAgent mithilfe der in der Brainstorming-Phase erarbeiteten Informationen Szenen für die gesamte Anzahl an Szenen plant.
3. Die Writing-Phase, in der ein Schreiber und ein Kritiker die Szenen schreiben. Der Schreiber verfasst einen ersten Draft, der Kritiker gibt Rückmeldung, der Schreiber überarbeitet das Kapitel und so weiter.



