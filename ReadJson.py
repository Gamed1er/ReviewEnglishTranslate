import json

class TranslationManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.translations = self.load_translations()

    def load_translations(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def display_translations(self):
        for translation in self.translations:
            english = translation['english']
            chinese = translation['chinese']
            print(f"English: {english}\nChinese: {chinese}\n")

    def get_random_translation(self):
        import random
        return random.choice(self.translations)

if __name__ == "__main__":
    file_path = 'translations.json'
    manager = TranslationManager(file_path)
    manager.display_translations()