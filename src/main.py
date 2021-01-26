import tkinter as tk
import pynput.keyboard
import ctypes



r=tk.Tk()
r.bind("<FocusOut>",lambda _:r.focus_force())
r.attributes("-fullscreen",True)
r.attributes("-topmost",True)
r.configure(background="#000000")
r.resizable(False,False)
r.overrideredirect(True)
r.focus_force()
r.update_idletasks()
c=pynput.keyboard.Controller()
ctypes.windll.user32.ShowCursor(0)
with pynput.keyboard.Listener(on_press=lambda k:((r.destroy(),False) if k==pynput.keyboard.Key.esc else (c.release(k),None))[1]):
	r.mainloop()
