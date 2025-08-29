# NovelAgents
 Dieses Repository beinhaltet den Code von NovelAgents, einem Multiagentensystem, das mit fünf Agenten in drei Phasen eine Geschichte von unterschiedlicher Länge generieren kann. 
 Dieses System ist gebaut mit ([Camel AI](https://github.com/camel-ai/camel)) von Li et al., [json_repair](https://github.com/mangiucugna/json_repair) von Stefano Baccianella und [Ollama](https://ollama.com/).

# Installation Guide
Installationsguide NovelAgents

1. Überprüfe, ob Python3.10.11 bereits auf deiner Maschine vorhanden ist. Wenn nicht, lade es von der Seite https://www.python.org/downloads/release/python-31011 herunter und installiere es
	-> Version von Python kann mit python --version gecheckt werden
2. Überprüfe, ob Ollama auf deiner Maschine bereits vorhanden ist. Wenn nicht, lade es von https://www.ollama.com herunterladen und installiere es 
    --> Pass auf mit Intel GPUs! Lade hierfür Ollama mithilfe dieser Anweisung herunter! https://www.intel.de/content/www/de/de/content-details/826081/running-ollama-with-open-webui-on-intel-hardware-platform.html
	-> Über die command line kannst du mithilfe von ollama KI-Modelle lokal auf dem eigenen Rechner laufen lassen
	-> Welche KI-Modelle es gibt und mit welchen Befehlen du diese pullst, kannst du auf der Ollama Website herausfinden
	-> Der Algorithmus benutzt zu jeder Zeit maximal zwei Agenten zeitgleich. Dein Gerät sollte also zur Benutzung von OLLAMA Modellen genügend RAM haben, um zwei Modelle zeitgleich laufen lassen zu können.
3. Repository von Github herunterladen
4. Im Novel Agents Repository mit python3.10.11 ein Virtual Environment aufsetzen 
	-> Befehl auf Windows, wenn im Ordner: python3.10 -m venv
		-> Bei Problemen, PC aus und wieder an machen, bzw PowerShell schließen und wieder öffnen
		-> Wenn die Python Version noch immer nicht erkannt wird, kann mit >& "Path\to\your\python.exe" -m venv "Path\to\your\desired\locatioin\venv"< ein venv mit dem Namen venv aufgesetzt werden 
5. Das Virtual Environment muss aktiviert werden
	-> Auf Windows mit "venv/Scripts/activate" (venv durch Namen des Virtual Environments austauschen)
6. Mit pip die requirements.txt auslesen und herunterladen
	-> Auf Windows mit >pip install -r requirements.txt<
7. Zuletzt lege eine eigene .env Datei an
	-> Sie sollte unter OLLAMA_PATH den Path zur Ollama exe enthalten
	-> Sie sollte unter OPENAI_API_KEY den zu verwendenden OpenAI API Key enthalten

## Trouble-Shooting
Im Falle der nicht Erkennung der installierten packages, stelle sicher, dass deine Codingumgebung den korrekten Python Interpret benutzt! 
	-> In VSCode kannst du dazu Strg+Shift+P drücken, >Python Interpreter< in die Suchleiste eintippen und dann den Python Interpret deines Virtual Environment auswählen.

# Funktionsweise des Algorithmus
Das NovelAgents-System wird mit einer GUI gesteuert, in die BenutzerInnen Zielgruppe, Genre und Thema der gewünschten Geschichte eingeben können. Weitergehend können sie festlegen, wie viele Charaktere das System generiert, wie viele Kapitel es schreibt und welches Modell als Grundlage der Agenten dieses Multiagentensystems dient. Das System ist in drei Teile aufgeteilt: 
	1. Die Brainstorming-Phase, in der Setting, Charaktere und Plot von einem Planer und einem Kritiker geplant werden. Bei vollständiger Abschließung entsteht ein StoryGlossary-Objekt, das im weiteren Verlauf des Systems genutzt wird. 
	2. Die Scene-Prompting-Phase, in der ein TaskPlannerAgent mithilfe der in der Brainstorming-Phase erarbeiteten Informationen Szenen für die gesamte Anzahl an Szenen plant.
	3. Die Writing-Phase, in der ein Schreiber und ein Kritiker die Szenen schreiben. Der Schreiber verfasst einen ersten Draft, der Kritiker gibt Rückmeldung, der Schreiber überarbeitet das Kapitel und so weiter.
Aus der angelegten .env-Datei können der Pfad zur Ollama.exe und der OpenAI API Key herauskopiert werden. Oder die .env-Datei wird direkt an die GUI angebunden. 



