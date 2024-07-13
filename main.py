import tkinter as tk
import random
from tkinter import scrolledtext
import difflib
from ReadJson import TranslationManager

def compare_sentences(original, user_input):
    original_words = original.split()
    user_input_words = user_input.split()
    diff = difflib.ndiff(original_words, user_input_words)
    result = []
    errors = 0
    for word in diff:
        if word.startswith('-'):
            # 原句中有，但使用者沒輸入
            result.append(('blue', word[2:]))
            errors += 1
        elif word.startswith('+'):
            # 使用者輸入錯誤的字
            result.append(('red', word[2:]))
            errors += 1
        elif word.startswith(' '):
            # 正確的字
            result.append(('lightgreen', word[2:]))
    return result, errors

def check_translation():
    user_input = input_text.get("1.0", tk.END).strip()
    comparison, errors = compare_sentences(english_sentence, user_input)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    for color, word in comparison:
        output_text.insert(tk.END, word + ' ', (color,))
    output_text.config(state=tk.DISABLED)

    # Provide feedback based on errors
    feedback = get_feedback(errors)
    feedback_label.config(text=feedback)

def get_feedback(errors):
    if errors == 0:
        output = ["你居然全對了，太神了吧！", "♪ All My People ~ All My People ~ ♫", "很厲害，繼續保持","不會吧，你真的全對了?"]
        return output[random.randint(0, 3)]
    
    elif errors == 1:
        output = ["唉阿，差點就全對了，可惜。", "【WA : 99%】", "是不是又少加甚麼了? 下次注意點阿","一失足成千古恨阿"]
        return output[random.randint(0, 3)]
    
    elif errors == 2:
        output = ["再加把勁，你快全對了 !", "勝敗乃兵家常事焉", "哎呀，錯了兩個","不宜妄自菲薄、引喻失義，誠宜開張聖聽、宜付有司"]
        return output[random.randint(0, 3)]
    
    elif 3 <= errors <= 4:
        output = ["還不錯，你可以在努力點", "再加把勁吧", "人有五名，錯誤有三個","你又錯哪裡了 ? 來，讓我康康 !"]
        return output[random.randint(0, 3)]
    
    elif 5 <= errors <= 10:
        output = ["往好處想，你還有很大的進步空間", "出題者只要出題就好了，而考生要考慮的就多了", "有一間私立大學推薦給你 : 南山幼兒園","零分，下一位"]
        return output[random.randint(0, 3)]
    
    else:
        output = ["負分，給我滾 !", "我甚至要向蠢材說明何謂蠢材", "你確定你在學測真的要這麼寫 ?","( 你的英文老師將在 30 秒後抵達現場 )"]
        return output[random.randint(0, 3)]

def get_new_translation():
    global english_sentence, chinese_sentence
    translation = manager.get_random_translation()
    english_sentence = translation['english']
    chinese_sentence = translation['chinese']
    chinese_label.config(text=f"中文: {chinese_sentence}")
    input_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    feedback_label.config(text="")  # Clear feedback when getting new translation

# Initialize
file_path = 'translations.json'
manager = TranslationManager(file_path)
english_sentence = ""
chinese_sentence = ""

# GUI Setup
root = tk.Tk()
root.title("英語翻譯學習輔助")
root.geometry("1600x900")

# Centralize content
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

chinese_label = tk.Label(frame, text="", wraplength=1500, font=("標楷體", 24))
chinese_label.pack(pady=20)

input_label = tk.Label(frame, text="請輸入英文翻譯:", font=("標楷體", 18))
input_label.pack()

input_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=5, font=("標楷體", 16))
input_text.pack(pady=20)

output_label = tk.Label(frame, text="翻譯檢查結果:", font=("標楷體", 18))
output_label.pack()

output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=10, font=("標楷體", 16), state=tk.DISABLED)
output_text.pack(pady=10)

output_text.tag_configure("red", foreground="red")
output_text.tag_configure("blue", foreground="blue")
output_text.tag_configure("lightgreen", foreground="lightgreen")

button_frame = tk.Frame(frame)
button_frame.pack(pady=20)

check_button = tk.Button(button_frame, text="檢查翻譯", command=check_translation, font=("標楷體", 18))
check_button.pack(side=tk.LEFT, padx=10)

new_translation_button = tk.Button(button_frame, text="新的翻譯", command=get_new_translation, font=("標楷體", 18))
new_translation_button.pack(side=tk.LEFT, padx=10)

feedback_label = tk.Label(frame, text="", font=("標楷體", 18))
feedback_label.pack()

get_new_translation()
root.mainloop()
