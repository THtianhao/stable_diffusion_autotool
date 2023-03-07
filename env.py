import os
import platform

isWindows = False
isMac = False
if platform.system() == "Windows":
    isWindows = True
elif platform.system() == "Darwin":
    isMac = True

def getSavePath():
    if isMac:
        return os.path.expanduser('~/Desktop')
    # if isWindows:
    #     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    #     return winreg.QueryValueEx(key, "AppData")[0] + '\\Toto'

cfgPath = None
root = None

if isMac:
    root = "/AutoTool"
    cfgPath = "/config"
    ocrPath = "/ocr/"
    carPath = "/car/"
    driverPath = "/driver/"
globalRootPath = f'{getSavePath()}{root}'
globalCfgPath = f'{getSavePath()}{root}{cfgPath}'

if not os.path.exists(globalCfgPath):
    os.makedirs(globalCfgPath)

def getConfigPath():
    return r'%scfg.json' % globalCfgPath
