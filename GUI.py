import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Brainstorming import brainstormStory, StoryGlossary
from Drafting import run_planner, write_scenes
import Initializing
import Exceptions
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
        return choice(list(E.Genre)).value
    
    @staticmethod
    def _random_audience_name() -> str: 
        return choice(list(E.Audience)).value
    
    @staticmethod
    def _random_theme_name() -> str:
        return choice(list(E.Theme)).value
    

    def __init__(self, root):
        self.root = root
        self.root.title("Geschichten-Schreib-Algorithmus")

        # Human Input
        input = Inputs.inputs[1]
        human_frame = ttk.LabelFrame(root, text="Geistiger Input")
        human_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.genre = self._add_entry_with_reroll(human_frame, "Genre", input["genre"], self._random_genre_name)
        self.audience = self._add_entry_with_reroll(human_frame, "Zielgruppe", input["audience"], self._random_audience_name)
        self.theme = self._add_entry_with_reroll(human_frame, "Thema", input["theme"], self._random_theme_name)

        # Loop-Einstellungen
        default_revisions_nr = 2
        loop_frame = ttk.LabelFrame(root, text="Loop-Einstellungen")
        loop_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        # self.character_number = self._add_spinbox(loop_frame, "Anzahl der Charakter", random.randint(1,5))
        self.character_number = self._add_spinbox(loop_frame, "Anzahl der Charakter", 2)
        self.revision_number = self._add_spinbox(loop_frame, "Anzahl der Überarbeitungen", default_revisions_nr)
        # self.scene_number = self._add_spinbox(loop_frame, "Anzahl der Szenen", random.randint(12, 24))
        self.scene_number = self._add_spinbox(loop_frame, "Anzahl der Szenen", 15)

        # Modellwahl
        model_frame = ttk.LabelFrame(root, text="KI-Modellwahl")
        model_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.model_var = tk.StringVar()
        self.model_menu = ttk.Combobox(model_frame, textvariable=self.model_var, state="readonly")
        self.model_menu['values'] = [E.Model.CHATGPT4OMINI.value, E.Model.LLAMA32.value, E.Model.MISTRAL.value, E.Model.QWEN25.value]
        self.model_menu.bind("<<ComboboxSelected>>", self._on_model_select)
        self.model_menu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.dynamic_field_label = ttk.Label(model_frame, text="")  # erscheint dynamisch
        self.dynamic_field_label.grid(row=1, column=0, sticky="w")
        self.dynamic_field = ttk.Entry(model_frame)
        self.dynamic_field.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Statusfeld
        status_frame = ttk.LabelFrame(root, text="Status")
        status_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.status_text = tk.Text(status_frame, height=2, wrap="word", state="disabled")
        self.status_text.pack(fill="both", expand=True)

        # Start Button
        self.start_button = ttk.Button(root, text="Start", command=self._start_generation)
        self.start_button.grid(row=4, column=0, padx=10, pady=10)

        # Download Buttons
        self.download_frame = ttk.LabelFrame(root, text="Ergebnisse herunterladen")
        self.download_frame.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.download_frame.grid_remove()  # wird später angezeigt

        self.download_json_btn = None
        self.download_scene_btn = None
        self.download_story_btn = None


    def _add_entry_with_reroll(self, parent, label_text, default_value, reroll_func):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text=label_text).pack(anchor="w")
        
        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill="x", pady=2)

        entry = ttk.Entry(entry_frame)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        entry.insert(0, default_value)

        reroll_btn = ttk.Button(entry_frame, text="🔄", width=3, command=lambda: entry.delete(0, "end") or entry.insert(0, reroll_func()))
        reroll_btn.pack(side="right")

        frame.pack(fill="x", padx=5, pady=2)
        return entry


    def _add_spinbox(self, parent, label_text, default_value=""):
        ttk.Label(parent, text=label_text).pack(anchor="w")
        spin = ttk.Spinbox(parent, from_=1, to=10)
        spin.pack(fill="x", padx=5, pady=2)
        spin.insert(0, default_value)
        return spin


    def _on_model_select(self, event=None):
        model = self.model_var.get()
        if model == E.Model.CHATGPT4OMINI.value:
            self.dynamic_field_label.config(text="OpenAI API Key:")
        else:
            self.dynamic_field_label.config(text="Pfad zur Ollama setup.exe:")
        self.dynamic_field.delete(0, tk.END)

    
    def _update_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")  # scrolls down automatically
        self.status_text.config(state="disabled")
        self.root.update_idletasks()


    def _show_download_buttons(self):
        for widget in self.download_frame.winfo_children():
            widget.destroy()

        for i, (label, (ftype, data)) in enumerate(self.generated_files.items()):
            btn = ttk.Button(self.download_frame,
                            text=label,
                            command=lambda d=data, t=ftype, n=label.replace(" ", "_"): self._save_generated_file(d, t, n))
            btn.grid(row=0, column=i, padx=5, pady=5)

        self.download_frame.grid()


    # Integrating the algorithm into the GUI
    def _start_generation(self):
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
            self._update_status("Starte Initialisierung ...")
            agent = Initializing.initialize_chosen_model(model, key_or_path)
            self._update_status("Initialisierung erfolgreich abgeschlossen.")
            
            self._update_status("Starte Brainstorming ...")
            brainstorm_agents: dict = Initializing.initialize_brainstorming_agents(agent)
            brainstorming_glossary = brainstormStory(brainstorm_agents["planner"], brainstorm_agents["critic"], human_input["genre"], human_input["audience"], human_input["theme"], loops["character_number"], loops["revision_number"])
            self._update_status("Brainstorming erfolgreich abgeschlossen.")
            
            self._update_status("Starte den Schreibprozess ...")
            self._update_status("Szenen werden geplant ...")
            write_agents: dict = Initializing.initialize_writing_agents(agent, brainstorming_glossary)
            scene_prompts: list[str] = run_planner(write_agents["taskmaster"], brainstorming_glossary, loops["scene_number"])
            self._update_status("Szenen wurden erfolgreich geplant.")
            
            self._update_status("Szenen werden geschrieben und überarbeitet ...")
            story_text: dict = write_scenes(write_agents["writer"], write_agents["feedback"], scene_prompts)
            self._update_status("Schreibprozess erfolgreich abgeschlossen.")
            
            self._update_status("Dateien werden zur Verfügung gestellt ...")
            self.generated_files = {
                "Brainstorming JSON": ("json", brainstorming_glossary),
                "Szenen Prompts": ("txt", scene_prompts), 
                "Fertige Geschichte": ("txt", story_text)
            }
            self._show_download_buttons()
            self._update_status("Prozess abgeschlossen.")
            self.download_frame.grid()  #show download frame
            
            end = datetime.now()

            messagebox.showinfo("Fertig", f"Die Dokumente wurden generiert.\nDas hat {((end - start)/60).total_seconds():.2f} Minuten gedauert.\nDanke für's Warten!")
            
        except RuntimeError as error:
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror("Whoops", f"{str(error)}\n\nDa scheinst du was falsch eingegeben zu haben. Überprüfe deine Eingaben besser nochmal")
            return
        except Exceptions.ModelProcessingError as error:
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror("Whoops", f"{str(error)}\n\nDa scheint was schiefgegangen zu sein. Überprüfe deine Eingaben nocheinmal.")
        except UnicodeEncodeError as error: 
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror("Whoops", f"Da ist wohl was mit deinem Eingegebenem nicht ganz korrekt. Überprüf das besser nochmal.")
        except Exception as error:
            tb = traceback.format_exc()
            self._update_status("Es ist etwas schief gelaufen ...")
            messagebox.showerror("Whoops", f"Da ist wohl ein Fehler aufgetreten, mit dem wir nicht gerechnet haben:\n{str(error)}\n\n{tb}")
            return


    def _save_generated_file(self, data, filetype: str, suggested_name: str):
        filetypes = [("JSON-Dateien", "*.json")] if filetype == "json" else [("Textdateien", "*.txt")]

        save_path = filedialog.asksaveasfilename(defaultextension=f".{filetype}",
                                                initialfile=suggested_name,
                                                filetypes=filetypes)

        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    if filetype == "json":
                        if isinstance(data, StoryGlossary): 
                            json.dump(data.to_dict(), f, indent=4, ensure_ascii=False)
                        else: 
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    elif filetype == "txt":
                        if isinstance(data, list):
                            f.write("\n\n".join(data))
                        else:
                            f.write(str(data))
                messagebox.showinfo("Gespeichert", f"{os.path.basename(save_path)} wurde gespeichert.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Datei konnte nicht gespeichert werden:\n{e}")


