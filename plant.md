import win32gui,win32api,win32process,ctypes

PROCESS_ALL_ACCESS = (0x000F0000|0x00100000|0xFFF) 
#载入kernal32.dll，Windows读写内存的函数在这个dll里面
kernal32=ctypes.windll.LoadLibrary(r"C:\Windows\System32\kernel32.dll")

#用于通过基址获取最终的地址
def GetAddress(handle,BaseAddress,offset=[]):
    value=ctypes.c_long()
    kernal32.ReadProcessMemory(int(handle),BaseAddress,ctypes.byref(value),4,None)
    for i in range(len(offset)-1):
        kernal32.ReadProcessMemory(int(handle), value.value+offset[i], ctypes.byref(value), 4, None)
    return value.value+offset[len(offset)-1]

#获取窗口句柄
hwnd=win32gui.FindWindow("MainWindow","植物大战僵尸中文版")

#通过窗口句柄获取进程ID，该函数返回一个列表，进程ID是在第二
pid=win32process.GetWindowThreadProcessId(hwnd)[1]

#通过进程ID获取句柄
handle=win32api.OpenProcess(0x1F0FFF,False,pid)

#ctypes.c_long()返回的是一个C语言long类型的变量
showSun=ctypes.c_long()
changeSun=ctypes.c_long()

while 1:
    address = GetAddress(handle, 0x6a9ec0, offset=[0x768, 0x5560])

    #ctypes.byref(showSun)相当于取showSun的指针
    kernal32.ReadProcessMemory(int(handle),address,ctypes.byref(showSun),4,None)
    print("{}{}".format("当前阳光：",showSun.value))

    changeSun.value = int(input("要修改成多少："))
    kernal32.WriteProcessMemory(int(handle), address, ctypes.byref(changeSun), 4, None)
