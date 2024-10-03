import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class TranslationManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.translations = self.load_translations()

    def load_translations(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_translations(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.translations, file, ensure_ascii=False, indent=4)

    def get_translation_by_id(self, translation_id):
        for translation in self.translations:
            if translation['id'] == translation_id:
                return translation
        return None

    def update_translation(self, translation_id, new_english, new_chinese):
        for translation in self.translations:
            if translation['id'] == translation_id:
                translation['english'] = new_english
                translation['chinese'] = new_chinese
                self.save_translations()
                return True
        return False

    def delete_translation(self, translation_id):
        for idx, translation in enumerate(self.translations):
            if translation['id'] == translation_id:
                del self.translations[idx]
                self.save_translations()
                return True
        return False

    def add_translation(self, english, chinese):
        new_id = max([t['id'] for t in self.translations], default=0) + 1
        new_translation = {
            'id': new_id,
            'english': english,
            'chinese': chinese
        }
        self.translations.append(new_translation)
        self.save_translations()
        return new_id

    def get_all_ids(self):
        return [t['id'] for t in self.translations]

class TranslationEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("翻譯管理系統")
        self.master.geometry("1400x700")
        self.manager = None

        self.create_widgets()
        self.load_json_files()

    def create_widgets(self):
        # Frame for JSON file operations
        file_frame = tk.Frame(self.master)
        file_frame.pack(pady=20)

        # Dropdown for JSON files
        tk.Label(file_frame, text="選擇翻譯文件:", font=("標楷體", 14)).pack(side=tk.LEFT, padx=5)
        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(file_frame, textvariable=self.file_var, state="readonly", width=40, font=("標楷體", 12))
        self.file_dropdown.pack(side=tk.LEFT, padx=10)
        self.file_dropdown.bind("<<ComboboxSelected>>", self.load_file)

        # Button to add JSON file
        add_file_button = tk.Button(file_frame, text="新增 JSON 檔案", command=self.add_json_file, font=("標楷體", 12), width=15)
        add_file_button.pack(side=tk.LEFT, padx=10)

        # Button to delete JSON file
        delete_file_button = tk.Button(file_frame, text="刪除 JSON 檔案", command=self.delete_json_file, font=("標楷體", 12), width=15)
        delete_file_button.pack(side=tk.LEFT, padx=10)

        # Frame for translation operations
        translation_frame = tk.Frame(self.master)
        translation_frame.pack(pady=30)

        # Dropdown for translation IDs
        tk.Label(translation_frame, text="選擇例句 ID:", font=("標楷體", 14)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.id_var = tk.StringVar()
        self.id_dropdown = ttk.Combobox(translation_frame, textvariable=self.id_var, state="readonly", width=10, font=("標楷體", 12))
        self.id_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.id_dropdown.bind("<<ComboboxSelected>>", self.load_translation)

        # English entry
        tk.Label(translation_frame, text="英文句子:", font=("標楷體", 14)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.english_entry = tk.Text(translation_frame, wrap=tk.WORD, width=100, height=4, font=("標楷體", 12))
        self.english_entry.grid(row=1, column=1, padx=10, pady=10)

        # Chinese entry
        tk.Label(translation_frame, text="中文翻譯:", font=("標楷體", 14)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.chinese_entry = tk.Text(translation_frame, wrap=tk.WORD, width=100, height=4, font=("標楷體", 12))
        self.chinese_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for add/update
        button_frame = tk.Frame(translation_frame)
        button_frame.grid(row=3, column=1, pady=20)

        add_button = tk.Button(button_frame, text="新增/更新例句", command=self.add_or_update_translation, font=("標楷體", 12), width=20)
        add_button.pack(side=tk.LEFT, padx=20)

        delete_button = tk.Button(button_frame, text="刪除例句", command=self.delete_translation, font=("標楷體", 12), width=20)
        delete_button.pack(side=tk.LEFT, padx=20)

        # Status label
        self.status_label = tk.Label(self.master, text="", font=("標楷體", 12), fg="green")
        self.status_label.pack(pady=10)

    def load_json_files(self):
        folder_path = 'translations'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        self.file_dropdown['values'] = self.json_files
        if self.json_files:
            self.file_dropdown.current(0)
            self.load_file(self.json_files[0])

    def load_file(self, selected_file):
        file_path = os.path.join('translations', selected_file)
        self.manager = TranslationManager(file_path)
        self.status_label.config(text=f"成功載入文件: {selected_file}")
        self.load_translation_ids()

    def load_translation_ids(self):
        if self.manager:
            ids = self.manager.get_all_ids()
            self.id_dropdown['values'] = ids
            if ids:
                self.id_dropdown.current(0)
                self.load_translation()
            else:
                self.clear_entries()

    def load_translation(self, event=None):
        if not self.manager:
            return
        try:
            translation_id = int(self.id_var.get())
            translation = self.manager.get_translation_by_id(translation_id)
            if translation:
                self.english_entry.delete("1.0", tk.END)
                self.english_entry.insert(tk.END, translation['english'].strip())
                self.chinese_entry.delete("1.0", tk.END)
                self.chinese_entry.insert(tk.END, translation['chinese'].strip())
        except ValueError:
            pass

    def add_or_update_translation(self):
        if not self.manager:
            messagebox.showwarning("警告", "請先選擇一個 JSON 檔案。")
            return

        english = self.english_entry.get("1.0", tk.END).strip()
        chinese = self.chinese_entry.get("1.0", tk.END).strip()

        # 自動移除多餘空白和 \n
        english = ' '.join(english.split())
        chinese = ' '.join(chinese.split())

        if not english and not chinese:
            messagebox.showwarning("警告", "英文和中文欄位皆為空，無法新增或更新。")
            return

        selected_id = self.id_var.get()
        if selected_id:
            try:
                translation_id = int(selected_id)
                if english and chinese:
                    updated = self.manager.update_translation(translation_id, english, chinese)
                    if updated:
                        self.status_label.config(text=f"成功更新編號為 {translation_id} 的翻譯。")
                        self.load_translation_ids()
                    else:
                        messagebox.showerror("錯誤", "更新失敗。")
                elif not english and not chinese:
                    # 刪除該翻譯
                    confirm = messagebox.askyesno("確認刪除", f"確定要刪除編號為 {translation_id} 的翻譯嗎？")
                    if confirm:
                        deleted = self.manager.delete_translation(translation_id)
                        if deleted:
                            self.status_label.config(text=f"成功刪除編號為 {translation_id} 的翻譯。")
                            self.load_translation_ids()
                        else:
                            messagebox.showerror("錯誤", "刪除失敗。")
            except ValueError:
                messagebox.showerror("錯誤", "無效的翻譯編號。")
        else:
            new_id = self.manager.add_translation(english, chinese)
            self.status_label.config(text=f"成功新增翻譯，編號為 {new_id}。")
            self.load_translation_ids()

    def delete_translation(self):
        selected_id = self.id_var.get()
        if selected_id:
            confirm = messagebox.askyesno("確認刪除", f"確定要刪除編號為 {selected_id} 的翻譯嗎？")
            if confirm:
                deleted = self.manager.delete_translation(int(selected_id))
                if deleted:
                    self.status_label.config(text=f"成功刪除編號為 {selected_id} 的翻譯。")
                    self.load_translation_ids()

    def clear_entries(self):
        self.english_entry.delete("1.0", tk.END)
        self.chinese_entry.delete("1.0", tk.END)

    def add_json_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_name:
            open(file_name, 'w').close()
            self.load_json_files()

    def delete_json_file(self):
        selected_file = self.file_var.get()
        if selected_file:
            confirm = messagebox.askyesno("確認刪除", f"確定要刪除 {selected_file} 嗎？")
            if confirm:
                os.remove(os.path.join('translations', selected_file))
                self.load_json_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationEditorApp(root)
    root.mainloop()
