import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import uuid

class App:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.current_job_index = 0
        self.text = tk.Text(root, wrap=tk.WORD)
        self.text.pack(expand=True, fill=tk.BOTH)

        # Navigation buttons
        prev_button = tk.Button(root, text='Previous', command=self.previous_job)
        prev_button.pack(side=tk.LEFT)
        next_button = tk.Button(root, text='Next', command=self.next_job)
        next_button.pack(side=tk.LEFT)
        
        # Save and Add Entity buttons
        save_button = tk.Button(root, text='Save Changes', command=self.save_changes)
        save_button.pack(side=tk.RIGHT)
        add_button = tk.Button(root, text='Add Entity', command=self.add_entity)
        add_button.pack(side=tk.RIGHT)

        # Load the initial job description
        self.load_job_description()

    def load_job_description(self):
        self.text.delete('1.0', tk.END)
        job = self.data[self.current_job_index]
        self.text.insert('1.0', job[0])
        self.display_entities(job[1]['entities'])

    def display_entities(self, entities):
        for i, (start, end, tag) in enumerate(entities):
            unique_tag = f"{tag}_{i}"
            self.text.tag_add(unique_tag, f'1.0+{start}c', f'1.0+{end}c')
            self.text.tag_config(unique_tag, background='yellow', foreground='black')
            self.text.tag_bind(unique_tag, '<Button-1>', lambda event, idx=i: self.remove_entity(idx))

    def remove_entity(self, index):
        if messagebox.askyesno("Confirm", "Remove this entity?"):
            entity = self.data[self.current_job_index][1]['entities'].pop(index)
            self.load_job_description()  # Refresh display to update tags
            messagebox.showinfo("Success", "Entity removed!")

    def add_entity(self):
        try:
            start_index = self.text.index(tk.SEL_FIRST)
            end_index = self.text.index(tk.SEL_LAST)
            tag = self.ask_entity_type()
            if tag:
                start = self.char_index(start_index)
                end = self.char_index(end_index)
                entity = [start, end, tag]
                self.data[self.current_job_index][1]['entities'].append(entity)
                self.load_job_description()  # Refresh display to update tags
        except tk.TclError:
            messagebox.showerror("Error", "No text selected. Please select some text to add as an entity.")

    def ask_entity_type(self):
        """ Create a dropdown dialog for selecting entity type """
        options = ['SKILL', 'QUALIFICATION', 'TOOL', 'PROGRAMMING_LANGUAGE']
        return simpledialog.askstring("Tag", "Select the entity type:", initialvalue=options[0], parent=self.root)

    def char_index(self, tk_index):
        parts = tk_index.split('.')
        line, char = int(parts[0]), int(parts[1])
        return sum(len(self.text.get(f"{i}.0", f"{i}.end")) + 1 for i in range(1, line)) + char

    def save_changes(self):
        with open('trainingData.json', 'w') as file:
            json.dump(self.data, file, indent=4)
        messagebox.showinfo("Save", "Changes saved successfully!")

    def previous_job(self):
        if self.current_job_index > 0:
            self.current_job_index -= 1
            self.load_job_description()

    def next_job(self):
        if self.current_job_index < len(self.data) - 1:
            self.current_job_index += 1
            self.load_job_description()

if __name__ == "__main__":
    with open('trainingData.json', 'r') as file:
        data = json.load(file)

    root = tk.Tk()
    root.geometry("800x600")
    app = App(root, data)
    root.mainloop()
