import tkinter as tk
from typing import Callable, Any
from tkinter import ttk, filedialog, messagebox
from brainstorming import brainstorm_story, StoryGlossary
from sceneprompting import run_planner
from writing import write_scenes
from utility import delete_agent_list
from initializing import (
    initialize_brainstorming_agents,
    initialize_chosen_model,
    initialize_writing_agents,
)
import Enums as E
import Inputs
from random import choice
import json
import os
import traceback
from datetime import datetime


class StoryGeneratorGUI:

    @staticmethod
    def _random_genre_name() -> str:
        """Picks a random genre from the genre Enum

        Returns:
            str: the random genre
        """
        return choice(list(E.Genre)).value


    @staticmethod
    def _random_audience_name() -> str:
        """Picks a random audience from the audience Enum

        Returns:
            str: the random audience
        """
        return choice(list(E.Audience)).value


    @staticmethod
    def _random_theme_name() -> str:
        """Picks a random theme from the theme Enum

        Returns:
            str: the random theme
        """
        return choice(list(E.Theme)).value

    def __init__(self, root: tk.Tk) -> None:
        """Initializes the GUI for the story writing algorithm

        Args:
        root (tk.Tk): The main Tkinter root window that serves as the parent
            container for all GUI elements.
        """
        self.root = root
        self.root.title("Geschichten-Schreib-Algorithmus")

        # Human Input
        input = choice(Inputs.inputs)
        human_frame : ttk.LabelFrame = ttk.LabelFrame(root, text="Geistiger Input")
        human_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.genre = self._add_entry_with_reroll(
            human_frame, "Genre", input["genre"], self._random_genre_name
        )
        self.audience = self._add_entry_with_reroll(
            human_frame, "Zielgruppe", input["audience"], self._random_audience_name
        )
        self.theme = self._add_entry_with_reroll(
            human_frame, "Thema", input["theme"], self._random_theme_name
        )

        # Loop-Einstellungen
        default_revisions_nr = 2
        loop_frame : ttk.LabelFrame = ttk.LabelFrame(root, text="Loop-Einstellungen")
        loop_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.character_number = self._add_spinbox(loop_frame, "Anzahl der Charakter", 2)
        self.revision_number = self._add_spinbox(
            loop_frame, "Anzahl der Überarbeitungen", default_revisions_nr
        )
        self.scene_number = self._add_spinbox(loop_frame, "Anzahl der Szenen", 15)

        # Modellwahl
        model_frame : ttk.LabelFrame = ttk.LabelFrame(root, text="KI-Modellwahl")
        model_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.model_var = tk.StringVar()
        self.model_menu : ttk.Combobox = ttk.Combobox(
            model_frame, textvariable=self.model_var, state="readonly"
        )
        self.model_menu["values"] = [m.value for m in E.Model]
        self.model_menu.bind("<<ComboboxSelected>>", self._on_model_select)
        self.model_menu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.dynamic_field_label = ttk.Label(
            model_frame, text=""
        )  # erscheint dynamisch
        self.dynamic_field_label.grid(row=1, column=0, sticky="w")
        self.dynamic_field : ttk.Entry = ttk.Entry(model_frame)
        self.dynamic_field.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Statusfeld
        status_frame : ttk.LabelFrame = ttk.LabelFrame(root, text="Status")
        status_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.status_text : tk.Text = tk.Text(
            status_frame, height=2, wrap="word", state="disabled"
        )
        self.status_text.pack(fill="both", expand=True)

        # Start Button
        self.start_button : ttk.Button = ttk.Button(
            root, text="Start", command=self._start_generation
        )
        self.start_button.grid(row=4, column=0, padx=10, pady=10)

        # Download Buttons
        self.download_frame : ttk.LabelFrame = ttk.LabelFrame(root, text="Ergebnisse herunterladen")
        self.download_frame.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.download_frame.grid_remove()  # wird später angezeigt

        self.download_json_btn = None
        self.download_scene_btn = None
        self.download_story_btn = None


    def _add_entry_with_reroll(
        self,
        parent: tk.Widget,
        label_text: str,
        default_value: str,
        reroll_func: Callable[[], str],
    ) -> ttk.Frame:
        """Adds an entry to the GUI with a label, an entry field, and a reroll button.

        Args:
            parent (tk.Widget): the parent widget to which this entry widget will be attached.
            label_text (str): The text to display as the label next to the entry field.
            default_value (str): The initial default value to populate in the entry field.
            reroll_func (Callable[[], str]): A callback function that generates a new
                value when the reroll button is clicked.

        Returns:
            ttk.Frame: A frame containing the label, entry field, and reroll button.
        """
        frame : ttk.Frame = ttk.Frame(parent)
        ttk.Label(frame, text=label_text).pack(anchor="w")

        entry_frame : ttk.Frame = ttk.Frame(frame)
        entry_frame.pack(fill="x", pady=2)

        entry : ttk.Entry = ttk.Entry(entry_frame)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        entry.insert(0, default_value)

        reroll_btn : ttk.Button = ttk.Button(
            entry_frame,
            text="🔄",
            width=3,
            command=lambda: entry.delete(0, "end") or entry.insert(0, reroll_func()),
        )
        reroll_btn.pack(side="right")

        frame.pack(fill="x", padx=5, pady=2)
        return entry


    def _add_spinbox(
    self, 
    parent: tk.Widget, 
    label_text: str, 
    default_value=""
    ) -> ttk.Spinbox:
        """Attaches a spinbox element to the parent widget.

        Args:
            parent (tk.Widget): the parent widget to which the spinbox will be attached.
            label_text (str): the text label describing the purpose of the spinbox.
            default_value (str): the initial value for the spinbox. Defaults to "".

        Returns:
            ttk.Spinbox: the spinbox widget that was created and attached.
        """
        ttk.Label(parent, text=label_text).pack(anchor="w")
        spin : ttk.Spinbox = ttk.Spinbox(parent, from_=1, to=10)
        spin.pack(fill="x", padx=5, pady=2)
        spin.insert(0, default_value)
        return spin


    def _on_model_select(self, event=None) -> None:
        """Writes the label of the path or key variable based on what model on what platform was chosen.

        Args:
            event (tk.Event | None, optional): The event object triggered by the 
            model selection from the dropdown. Defaults to None.
        """
        model = self.model_var.get()
        if model == E.Model.CHATGPT4OMINI.value:
            self.dynamic_field_label.config(text="OpenAI API Key:")
        else:
            self.dynamic_field_label.config(text="Pfad zur Ollama setup.exe:")
        self.dynamic_field.delete(0, tk.END)

    def _update_status(self, message: str):
        """Updates the status window in the GUI. 

        Args:
            message (str): the message that should be displayed in the GUI's status window.
        """
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")  # scrolls down automatically
        self.status_text.config(state="disabled")
        self.root.update_idletasks()


    def _show_download_buttons(self) -> None:
        """
        Makes the download buttons appear in the download frame when called. 
        Each button has a file attached that was generated during the algorithm.
        """
        for widget in self.download_frame.winfo_children():
            widget.destroy()

        for i, (label, (ftype, data)) in enumerate(self.generated_files.items()):
            btn = ttk.Button(
                self.download_frame,
                text=label,
                command=lambda d=data, t=ftype, n=label.replace(
                    " ", "_"
                ): self._save_generated_file(d, t, n),
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

        self.download_frame.grid()


    # Integrating the algorithm into the GUI
    def _start_generation(self) -> None:
        """
        Starts the story generation process using the GUI inputs and the selected model.
        """
        start = datetime.now()
        self._update_status("Starte Generierung ...")
        human_input = {
            "genre": self.genre.get(),
            "audience": self.audience.get(),
            "theme": self.theme.get(),
        }
        loops = {
            "character_number": int(self.character_number.get()),
            "revision_number": int(self.revision_number.get()),
            "scene_number": int(self.scene_number.get()),
        }
        model = self.model_var.get()
        key_or_path = self.dynamic_field.get()

        try:
            # Initialize model
            self._update_status("Starte Initialisierung ...")
            agent = initialize_chosen_model(model, key_or_path)
            self._update_status("Initialisierung erfolgreich abgeschlossen.")

            # Brainstorming phase
            self._update_status("Starte Brainstorming ...")
            brainstorm_agents: dict = initialize_brainstorming_agents(agent)

            brainstorming_glossary = brainstorm_story(
                planner=brainstorm_agents["planner"],
                critic=brainstorm_agents["critic"],
                genre=human_input["genre"],
                audience=human_input["audience"],
                theme=human_input["theme"],
                character_count=loops["character_number"],
                revision_number=loops["revision_number"],
            )
            self._update_status("Brainstorming erfolgreich abgeschlossen.")

            # Scene planning phase
            self._update_status("Starte den Schreibprozess ...")
            self._update_status("Szenen werden geplant ...")
            
            write_agents: dict = initialize_writing_agents(
                model=agent, 
                story_glossary=brainstorming_glossary, 
                scene_nr=loops["scene_number"]
            )
            
            scene_prompts: list[str] = run_planner(
                write_agents["taskmaster"],
                brainstorming_glossary,
                loops["scene_number"],
            )
            self._update_status("Szenen wurden erfolgreich geplant.")

            # Writing phase
            self._update_status("Szenen werden geschrieben und überarbeitet ...")
            story_text: dict = write_scenes(
                write_agents["writer"],
                write_agents["feedback"],
                scene_prompts,
                loops["revision_number"],
            )
            self._update_status("Schreibprozess erfolgreich abgeschlossen.")

            self._update_status("Dateien werden zur Verfügung gestellt ...")
            self.generated_files = {
                "Brainstorming JSON": ("json", brainstorming_glossary),
                "Szenen Prompts": ("txt", scene_prompts),
                "Fertige Geschichte": ("txt", story_text),
            }
            self._show_download_buttons()
            self._update_status("Prozess abgeschlossen.")
            self.download_frame.grid()  # show download frame
            
            # Report duration
            end = datetime.now()
            duration = (end - start).total_seconds() /60
            messagebox.showinfo(
                "Fertig",
                f"Die Dokumente wurden generiert.\nDas hat {duration:.2f} Minuten gedauert.\nDanke für's Warten!",
            )

        except RuntimeError as error:
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror(
                "Whoops",
                f"{str(error)}\n\nDa scheinst du was falsch eingegeben zu haben. Überprüfe deine Eingaben besser nochmal",
            )
            return
        except UnicodeEncodeError as error:
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror(
                "Whoops",
                f"Da ist wohl was mit deinem Eingegebenem nicht ganz korrekt. Überprüf das besser nochmal.",
            )
        except Exception as error:
            tb = traceback.format_exc()
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror(
                "Whoops",
                f"Da ist wohl ein Fehler aufgetreten, mit dem wir nicht gerechnet haben:\n{str(error)}\n\n{tb}",
            )
            return
        

    def _save_generated_file(self, data: Any, filetype: str, suggested_name: str) -> None:
        """
        Saves the generated file associated with the pressed button. Opens a save dialog for the user.

        Args:
            data (Any): The content to save. Can be a StoryGlossary object, a list of strings, or plain text.
            filetype (str): Type of file to save. Supported values:
                - "json": Saves data as a JSON file.
                - "txt": Saves data as a plain text file.
            suggested_name (str): Default filename suggested in the save dialog.
        """
        filetypes = (
            [("JSON-Dateien", "*.json")]
            if filetype == "json"
            else [("Textdateien", "*.txt")]
        )

        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{filetype}",
            initialfile=suggested_name,
            filetypes=filetypes,
        )

        # User cancels
        if not save_path:
            return 
        
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                if filetype == "json":
                    if isinstance(data, StoryGlossary):
                        json.dump(data.to_dict(), f, indent=4, ensure_ascii=False)
                    else:
                        json.dump(data, f, indent=2, ensure_ascii=False,)
                elif filetype == "txt":
                    if isinstance(data, list):
                        f.write("\n\n".join(map(str, data)))
                    else:
                        f.write(str(data))
                        
            messagebox.showinfo(
                "Gespeichert", f"{os.path.basename(save_path)} wurde gespeichert."
            )
        except Exception as e:
            messagebox.showerror(
                "Fehler", f"Datei konnte nicht gespeichert werden:\n{e}"
            )
