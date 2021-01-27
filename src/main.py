import tkinter as tk
import ctypes
import ctypes.wintypes
import traceback
import atexit



WH_KEYBOARD_LL=13
PM_REMOVE=1



ctypes.wintypes.ULONG_PTR=ctypes.POINTER(ctypes.wintypes.DWORD)
ctypes.wintypes.LRESULT=ctypes.c_int
ctypes.wintypes.LowLevelKeyboardProc=ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.wintypes.KBDLLHOOKSTRUCT=type("KBDLLHOOKSTRUCT",(ctypes.Structure,),{"_fields_":[("vk_code",ctypes.wintypes.DWORD),("scan_code",ctypes.wintypes.DWORD),("flags",ctypes.wintypes.DWORD),("time",ctypes.c_int),("dwExtraInfo",ctypes.wintypes.ULONG_PTR)]})
ctypes.windll.kernel32.GetModuleHandleW.argtypes=(ctypes.wintypes.LPCWSTR,)
ctypes.windll.kernel32.GetModuleHandleW.restype=ctypes.wintypes.HMODULE
ctypes.windll.user32.CallNextHookEx.argtypes=(ctypes.POINTER(ctypes.wintypes.HHOOK),ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.windll.user32.CallNextHookEx.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.DispatchMessageW.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.DispatchMessageW.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.PeekMessageW.argtypes=(ctypes.wintypes.LPMSG,ctypes.wintypes.HWND,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint)
ctypes.windll.user32.PeekMessageW.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.SetWindowsHookExW.argtypes=(ctypes.c_int,ctypes.wintypes.LowLevelKeyboardProc,ctypes.wintypes.HINSTANCE,ctypes.wintypes.DWORD)
ctypes.windll.user32.SetWindowsHookExW.restype=ctypes.wintypes.HHOOK
ctypes.windll.user32.TranslateMessage.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.TranslateMessage.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.UnhookWindowsHookEx.argtypes=(ctypes.wintypes.HHOOK,)
ctypes.windll.user32.UnhookWindowsHookEx.restype=ctypes.wintypes.BOOL



def _handle(c,wp,lp):
	try:
		if (ctypes.cast(lp,ctypes.POINTER(ctypes.wintypes.KBDLLHOOKSTRUCT)).contents.vk_code==0x1b):
			_handle._r.destroy()
		else:
			return -1
	except Exception as e:
		traceback.print_exception(None,e,e.__traceback__)
	return ctypes.windll.user32.CallNextHookEx(None,c,wp,lp)



def _loop(r):
	if (ctypes.windll.user32.PeekMessageW(_loop._msg,None,0,0,PM_REMOVE)!=0):
		ctypes.windll.user32.TranslateMessage(_loop._msg)
		ctypes.windll.user32.DispatchMessageW(_loop._msg)
	r.after(1000//60,_loop,r)



r=tk.Tk()
r.bind("<FocusOut>",lambda _:r.focus_force())
r.attributes("-fullscreen",True)
r.attributes("-topmost",True)
r.configure(background="#000000")
r.resizable(False,False)
r.overrideredirect(True)
r.focus_force()
r.update_idletasks()
_handle._ig_alt=False
_handle._r=r
_loop._msg=ctypes.wintypes.LPMSG()
kb_cb=ctypes.wintypes.LowLevelKeyboardProc(_handle)
ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL,kb_cb,ctypes.windll.kernel32.GetModuleHandleW(None),ctypes.wintypes.DWORD(0))
atexit.register(ctypes.windll.user32.UnhookWindowsHookEx,kb_cb)
ctypes.windll.user32.ShowCursor(0)
r.after(0,_loop,r)
r.mainloop()
