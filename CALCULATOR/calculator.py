import tkinter as tk
import math
import datetime
import speech_recognition as sr
from tkinter import messagebox

# These are Theme colours for light and dark 
LIGHTTHEME = {"bg": "#f0f0f0", "fg": "#000000"}
DARKTHEME = {"bg": "#2e2e2e", "fg": "#ffffff"}

class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Calculator")
        self.root.geometry("400x550")
        self.theme = LIGHTTHEME
        self.createwidgets()
        self.applytheme()

    def createwidgets(self):
        self.display = tk.Entry(self.root, font=("Helvetica", 20), bd=10, relief=tk.RIDGE, justify="right")
        self.display.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="we")

        buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'log',
            '1', '2', '3', '-', 'sin',
            '0', '.', '=', '+', 'cos',
            'C', 'Voice', 'tan', 'Dark', 'Hist'
        ]

        row_val = 1
        col_val = 0

        for btn_text in buttons:
            tk.Button(self.root, text=btn_text, width=6, height=2, font=("Helvetica", 12),
                      command=lambda b=btn_text: self.handleclick(b)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

    def handleclick(self, key):
        if key == "=":
            self.evaluateexpression()
        elif key == "C":
            self.display.delete(0, tk.END)
        elif key == "Voice":
            self.voiceinput()
        elif key == "Dark":
            self.toggletheme()
        elif key == "Hist":
            self.showhistory()
        elif key in ["sqrt", "log", "sin", "cos", "tan"]:
            self.insertfunction(key)
        else:
            self.display.insert(tk.END, key)

    def insertfunction(self, func):
        expression = self.display.get()
        try:
            if func == "sqrt":
                result = math.sqrt(float(expression))
            elif func == "log":
                result = math.log(float(expression))
            elif func == "sin":
                result = math.sin(math.radians(float(expression)))
            elif func == "cos":
                result = math.cos(math.radians(float(expression)))
            elif func == "tan":
                result = math.tan(math.radians(float(expression)))
            else:
                result = "ERR"
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(round(result, 4)))
            self.savehistory(f"{func}({expression}) = {round(result, 4)}")
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def evaluateexpression(self):
        try:
            expression = self.display.get()
            result = eval(expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.savehistory(f"{expression} = {result}")
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def voiceinput(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Listening...")
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, text)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Voice Error")

    def savehistory(self, record):
        with open("calc_history.txt", "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {record}\n")

    def showhistory(self):
        try:
            with open("calc_history.txt", "r") as f:
                history = f.read()
            messagebox.showinfo("Calculation History", history if history else "No history found.")
        except:
            messagebox.showerror("Error", "Unable to read history file.")

    def toggletheme(self):
        self.theme = DARKTHEME if self.theme == LIGHTTHEME else LIGHTTHEME
        self.applytheme()

    def applytheme(self):
        self.root.configure(bg=self.theme["bg"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=self.theme["bg"], fg=self.theme["fg"])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="white" if self.theme == LIGHTTHEME else "#444", fg=self.theme["fg"])


if __name__ == "__main__":
    window = tk.Tk()
    calc = SmartCalculator(window)
    window.mainloop()
