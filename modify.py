import tkinter as tk
from tkinter import messagebox
import json

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
        new_id = len(self.translations) + 1
        new_translation = {
            'id': new_id,
            'english': english,
            'chinese': chinese
        }
        self.translations.append(new_translation)
        self.save_translations()
        return new_id

class TranslationEditorApp:
    def __init__(self, master, manager):
        self.master = master
        self.manager = manager
        self.master.title("翻譯管理系統")
        self.master.geometry("1200x400")

        self.create_widgets()

    def create_widgets(self):
        self.label_id = tk.Label(self.master, text="編號:", font=("標楷體", 18))
        self.label_id.grid(row=0, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.master, font=("標楷體", 12), width=20)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)

        self.label_english = tk.Label(self.master, text="英文:", font=("標楷體", 18))
        self.label_english.grid(row=1, column=0, padx=10, pady=10)
        self.entry_english = tk.Entry(self.master, font=("標楷體", 12), width=120)
        self.entry_english.grid(row=1, column=1, padx=10, pady=10)

        self.label_chinese = tk.Label(self.master, text="中文:", font=("標楷體", 18))
        self.label_chinese.grid(row=2, column=0, padx=10, pady=10)
        self.entry_chinese = tk.Entry(self.master, font=("標楷體", 12), width=120)
        self.entry_chinese.grid(row=2, column=1, padx=10, pady=10)

        self.button_search = tk.Button(self.master, text="查詢", command=self.search_translation, font=("標楷體", 18))
        self.button_search.grid(row=0, column=2, padx=10, pady=10)

        self.button_update = tk.Button(self.master, text="更新", command=self.update_translation, font=("標楷體", 18))
        self.button_update.grid(row=1, column=2, padx=10, pady=10)

        self.button_delete = tk.Button(self.master, text="刪除", command=self.delete_translation, font=("標楷體", 18))
        self.button_delete.grid(row=2, column=2, padx=10, pady=10)

        self.button_add = tk.Button(self.master, text="新增", command=self.add_translation, font=("標楷體", 18))
        self.button_add.grid(row=3, column=1, padx=10, pady=10)

        self.status_label = tk.Label(self.master, text="", font=("標楷體", 18))
        self.status_label.grid(row=4, columnspan=3, padx=10, pady=10)

    def search_translation(self):
        translation_id = int(self.entry_id.get())
        translation = self.manager.get_translation_by_id(translation_id)
        if translation:
            self.entry_english.delete(0, tk.END)
            self.entry_english.insert(0, translation['english'])
            self.entry_chinese.delete(0, tk.END)
            self.entry_chinese.insert(0, translation['chinese'])
            self.status_label.config(text=f"找到編號為 {translation_id} 的翻譯。")
        else:
            messagebox.showwarning("錯誤", f"未找到編號為 {translation_id} 的翻譯。")
            self.status_label.config(text="")

    def update_translation(self):
        translation_id = int(self.entry_id.get())
        new_english = self.entry_english.get()
        new_chinese = self.entry_chinese.get()
        if self.manager.update_translation(translation_id, new_english, new_chinese):
            self.status_label.config(text=f"成功更新編號為 {translation_id} 的翻譯。")
        else:
            messagebox.showerror("錯誤", f"更新編號為 {translation_id} 的翻譯失敗。")
            self.status_label.config(text="")

    def delete_translation(self):
        translation_id = int(self.entry_id.get())
        if self.manager.delete_translation(translation_id):
            self.status_label.config(text=f"成功刪除編號為 {translation_id} 的翻譯。")
            self.entry_id.delete(0, tk.END)
            self.entry_english.delete(0, tk.END)
            self.entry_chinese.delete(0, tk.END)
        else:
            messagebox.showerror("錯誤", f"刪除編號為 {translation_id} 的翻譯失敗。")
            self.status_label.config(text="")

    def add_translation(self):
        new_english = self.entry_english.get()
        new_chinese = self.entry_chinese.get()
        new_id = self.manager.add_translation(new_english, new_chinese)
        self.status_label.config(text=f"成功新增翻譯，編號為 {new_id}。")
        self.entry_id.delete(0, tk.END)
        self.entry_english.delete(0, tk.END)
        self.entry_chinese.delete(0, tk.END)

if __name__ == "__main__":
    file_path = 'translations.json'
    manager = TranslationManager(file_path)

    root = tk.Tk()
    app = TranslationEditorApp(root, manager)
    root.mainloop()
