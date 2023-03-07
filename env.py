import platform

host = "44.213.210.2"
# host = "127.0.0.1"
port = 7860

isWindows = False
isMac = False
if platform.system() == "Windows":
    isWindows = True
elif platform.system() == "Darwin":
    isMac = True

def getSavePath():
    if isMac:
        return '~/Desktop/AutoTool/config'
    # if isWindows:
    #     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    #     return winreg.QueryValueEx(key, "AppData")[0] + '\\Toto'

cfgPath = None

if isMac:
    picPath = "/pic/"
    cfgPath = "/config/"
    ocrPath = "/ocr/"
    carPath = "/car/"
    driverPath = "/driver/"

globalCfgPath = getSavePath() + cfgPath

def getConfigPath():
    return r'%scfg.json' % globalCfgPath
