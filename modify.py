import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class TranslationManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.translations = self.load_translations()

    def load_translations(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def save_translations(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.translations, file, ensure_ascii=False, indent=4)

    def get_translation_by_id(self, translation_id):
        for translation in self.translations:
            if translation['id'] == translation_id:
                return translation
        return None

    def add_translation(self, english, chinese):
        new_id = len(self.translations) + 1
        new_translation = {
            'id': new_id,
            'english': english.strip(),
            'chinese': chinese.strip()
        }
        self.translations.append(new_translation)
        self.save_translations()
        return new_id

    def update_translation(self, translation_id, new_english, new_chinese):
        for translation in self.translations:
            if translation['id'] == translation_id:
                translation['english'] = new_english.strip()
                translation['chinese'] = new_chinese.strip()
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

class TranslationEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("翻譯管理系統")
        self.master.geometry("800x600")

        self.file_var = tk.StringVar()
        self.id_var = tk.StringVar()

        self.create_widgets()

        self.load_json_files()

    def create_widgets(self):
        # 選擇檔案
        tk.Label(self.master, text="選擇翻譯檔案:").pack(pady=10)
        self.file_menu = tk.OptionMenu(self.master, self.file_var, "")
        self.file_menu.pack(pady=10)

        # 輸入欄位
        tk.Label(self.master, text="英文:").pack(pady=5)
        self.english_entry = tk.Text(self.master, height=4, width=80)
        self.english_entry.pack(pady=5)

        tk.Label(self.master, text="中文:").pack(pady=5)
        self.chinese_entry = tk.Text(self.master, height=4, width=80)
        self.chinese_entry.pack(pady=5)

        # 選擇 ID
        tk.Label(self.master, text="選擇翻譯編號:").pack(pady=10)
        self.id_menu = tk.OptionMenu(self.master, self.id_var, "")
        self.id_menu.pack(pady=10)

        # 操作按鈕
        tk.Button(self.master, text="新增例句", command=self.add_translation).pack(pady=10)
        tk.Button(self.master, text="更改例句", command=self.update_translation).pack(pady=10)
        tk.Button(self.master, text="刪除例句", command=self.delete_translation).pack(pady=10)

        # 新增/刪除 JSON 檔案
        tk.Button(self.master, text="新增翻譯檔案", command=self.add_json_file).pack(pady=5)
        tk.Button(self.master, text="刪除翻譯檔案", command=self.delete_json_file).pack(pady=5)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack(pady=10)

    def load_json_files(self):
        self.file_var.set('')
        files = [f for f in os.listdir('translations') if f.endswith('.json')]
        self.file_menu['menu'].delete(0, 'end')
        for file in files:
            self.file_menu['menu'].add_command(label=file, command=tk._setit(self.file_var, file))
        if files:
            self.file_var.set(files[0])
            self.load_translations()

    def load_translations(self):
        selected_file = self.file_var.get()
        if selected_file:
            file_path = os.path.join('translations', selected_file)
            self.manager = TranslationManager(file_path)
            self.load_translation_ids()

    def load_translation_ids(self):
        self.id_var.set('')
        self.id_menu['menu'].delete(0, 'end')
        for translation in self.manager.translations:
            translation_id = translation['id']
            self.id_menu['menu'].add_command(label=translation_id, command=tk._setit(self.id_var, translation_id))

    def add_translation(self):
        english = self.english_entry.get("1.0", tk.END).strip()
        chinese = self.chinese_entry.get("1.0", tk.END).strip()

        if english and chinese:
            new_id = self.manager.add_translation(english, chinese)
            self.status_label.config(text=f"成功新增翻譯，編號為 {new_id}。")
            self.load_translation_ids()
        else:
            self.status_label.config(text="請輸入英文和中文句子。")

    def update_translation(self):
        selected_id = self.id_var.get()
        english = self.english_entry.get("1.0", tk.END).strip()
        chinese = self.chinese_entry.get("1.0", tk.END).strip()

        if selected_id and english and chinese:
            updated = self.manager.update_translation(int(selected_id), english, chinese)
            if updated:
                self.status_label.config(text=f"成功更新編號為 {selected_id} 的翻譯。")
                self.load_translation_ids()
        else:
            self.status_label.config(text="請選擇翻譯編號並輸入中英文句子。")

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
