# encoding: utf-8
# module win32api
# from C:\Users\afham\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\win32\win32api.pyd
# by generator 1.147
""" Wraps general API functions that are not subsumed in the more specific modules """

# imports
from pywintypes import error


# Variables with simple values

NameCanonical = 7
NameCanonicalEx = 9
NameDisplay = 3
NameFullyQualifiedDN = 1
NameSamCompatible = 2
NameServicePrincipal = 10
NameUniqueId = 6
NameUnknown = 0
NameUserPrincipal = 8

REG_NOTIFY_CHANGE_ATTRIBUTES = 2

REG_NOTIFY_CHANGE_LAST_SET = 4

REG_NOTIFY_CHANGE_NAME = 1
REG_NOTIFY_CHANGE_SECURITY = 8

STD_ERROR_HANDLE = -12

STD_INPUT_HANDLE = -10

STD_OUTPUT_HANDLE = -11

VFT_APP = 1
VFT_DLL = 2
VFT_DRV = 3
VFT_FONT = 4

VFT_STATIC_LIB = 7

VFT_UNKNOWN = 0
VFT_VXD = 5

VOS_DOS = 65536

VOS_DOS_WINDOWS16 = 65537
VOS_DOS_WINDOWS32 = 65540

VOS_NT = 262144

VOS_NT_WINDOWS32 = 262148

VOS_OS216 = 131072

VOS_OS216_PM16 = 131074

VOS_OS232 = 196608

VOS_OS232_PM32 = 196611

VOS_UNKNOWN = 0

VOS__PM16 = 2
VOS__PM32 = 3
VOS__WINDOWS16 = 1
VOS__WINDOWS32 = 4

VS_FF_DEBUG = 1
VS_FF_INFOINFERRED = 16
VS_FF_PATCHED = 4
VS_FF_PRERELEASE = 2
VS_FF_PRIVATEBUILD = 8
VS_FF_SPECIALBUILD = 32

# functions

def AbortSystemShutdown(*args, **kwargs): # real signature unknown
    pass

def Apply(*args, **kwargs): # real signature unknown
    pass

def Beep(*args, **kwargs): # real signature unknown
    pass

def BeginUpdateResource(*args, **kwargs): # real signature unknown
    pass

def ChangeDisplaySettings(*args, **kwargs): # real signature unknown
    pass

def ChangeDisplaySettingsEx(*args, **kwargs): # real signature unknown
    pass

def ClipCursor(*args, **kwargs): # real signature unknown
    pass

def CloseHandle(*args, **kwargs): # real signature unknown
    pass

def CommandLineToArgv(*args, **kwargs): # real signature unknown
    pass

def CopyFile(*args, **kwargs): # real signature unknown
    pass

def DebugBreak(*args, **kwargs): # real signature unknown
    pass

def DeleteFile(*args, **kwargs): # real signature unknown
    pass

def DragFinish(*args, **kwargs): # real signature unknown
    pass

def DragQueryFile(*args, **kwargs): # real signature unknown
    pass

def DuplicateHandle(*args, **kwargs): # real signature unknown
    pass

def EndUpdateResource(*args, **kwargs): # real signature unknown
    pass

def EnumDisplayDevices(*args, **kwargs): # real signature unknown
    pass

def EnumDisplayMonitors(*args, **kwargs): # real signature unknown
    pass

def EnumDisplaySettings(*args, **kwargs): # real signature unknown
    pass

def EnumDisplaySettingsEx(*args, **kwargs): # real signature unknown
    pass

def EnumResourceLanguages(*args, **kwargs): # real signature unknown
    pass

def EnumResourceNames(*args, **kwargs): # real signature unknown
    pass

def EnumResourceTypes(*args, **kwargs): # real signature unknown
    pass

def ExitWindows(*args, **kwargs): # real signature unknown
    pass

def ExitWindowsEx(*args, **kwargs): # real signature unknown
    pass

def ExpandEnvironmentStrings(*args, **kwargs): # real signature unknown
    pass

def FindCloseChangeNotification(*args, **kwargs): # real signature unknown
    pass

def FindExecutable(*args, **kwargs): # real signature unknown
    pass

def FindFiles(*args, **kwargs): # real signature unknown
    pass

def FindFirstChangeNotification(*args, **kwargs): # real signature unknown
    pass

def FindNextChangeNotification(*args, **kwargs): # real signature unknown
    pass

def FormatMessage(*args, **kwargs): # real signature unknown
    pass

def FormatMessageW(*args, **kwargs): # real signature unknown
    pass

def FreeLibrary(*args, **kwargs): # real signature unknown
    pass

def GenerateConsoleCtrlEvent(*args, **kwargs): # real signature unknown
    pass

def GetAsyncKeyState(*args, **kwargs): # real signature unknown
    pass

def GetCommandLine(*args, **kwargs): # real signature unknown
    pass

def GetComputerName(*args, **kwargs): # real signature unknown
    pass

def GetComputerNameEx(*args, **kwargs): # real signature unknown
    pass

def GetComputerObjectName(*args, **kwargs): # real signature unknown
    pass

def GetConsoleTitle(*args, **kwargs): # real signature unknown
    pass

def GetCurrentProcess(*args, **kwargs): # real signature unknown
    pass

def GetCurrentProcessId(*args, **kwargs): # real signature unknown
    pass

def GetCurrentThread(*args, **kwargs): # real signature unknown
    pass

def GetCurrentThreadId(*args, **kwargs): # real signature unknown
    pass

def GetCursorPos(*args, **kwargs): # real signature unknown
    pass

def GetDateFormat(*args, **kwargs): # real signature unknown
    pass

def GetDiskFreeSpace(*args, **kwargs): # real signature unknown
    pass

def GetDiskFreeSpaceEx(*args, **kwargs): # real signature unknown
    pass

def GetDllDirectory(*args, **kwargs): # real signature unknown
    pass

def GetDomainName(*args, **kwargs): # real signature unknown
    pass

def GetEnvironmentVariable(*args, **kwargs): # real signature unknown
    pass

def GetEnvironmentVariableW(*args, **kwargs): # real signature unknown
    pass

def GetFileAttributes(*args, **kwargs): # real signature unknown
    pass

def GetFileVersionInfo(*args, **kwargs): # real signature unknown
    pass

def GetFocus(*args, **kwargs): # real signature unknown
    pass

def GetFullPathName(*args, **kwargs): # real signature unknown
    pass

def GetHandleInformation(*args, **kwargs): # real signature unknown
    pass

def GetKeyboardLayout(*args, **kwargs): # real signature unknown
    pass

def GetKeyboardLayoutList(*args, **kwargs): # real signature unknown
    pass

def GetKeyboardLayoutName(*args, **kwargs): # real signature unknown
    pass

def GetKeyboardState(*args, **kwargs): # real signature unknown
    pass

def GetKeyState(*args, **kwargs): # real signature unknown
    pass

def GetLastError(*args, **kwargs): # real signature unknown
    pass

def GetLastInputInfo(*args, **kwargs): # real signature unknown
    pass

def GetLocalTime(*args, **kwargs): # real signature unknown
    pass

def GetLogicalDrives(*args, **kwargs): # real signature unknown
    pass

def GetLogicalDriveStrings(*args, **kwargs): # real signature unknown
    pass

def GetLongPathName(*args, **kwargs): # real signature unknown
    pass

def GetLongPathNameW(*args, **kwargs): # real signature unknown
    pass

def GetModuleFileName(*args, **kwargs): # real signature unknown
    pass

def GetModuleFileNameW(*args, **kwargs): # real signature unknown
    pass

def GetModuleHandle(*args, **kwargs): # real signature unknown
    pass

def GetMonitorInfo(*args, **kwargs): # real signature unknown
    pass

def GetNativeSystemInfo(*args, **kwargs): # real signature unknown
    pass

def GetProcAddress(*args, **kwargs): # real signature unknown
    pass

def GetProfileSection(*args, **kwargs): # real signature unknown
    pass

def GetProfileVal(*args, **kwargs): # real signature unknown
    pass

def GetPwrCapabilities(*args, **kwargs): # real signature unknown
    pass

def GetShortPathName(*args, **kwargs): # real signature unknown
    pass

def GetStdHandle(*args, **kwargs): # real signature unknown
    pass

def GetSysColor(*args, **kwargs): # real signature unknown
    pass

def GetSystemDefaultLangID(*args, **kwargs): # real signature unknown
    pass

def GetSystemDefaultLCID(*args, **kwargs): # real signature unknown
    pass

def GetSystemDirectory(*args, **kwargs): # real signature unknown
    pass

def GetSystemFileCacheSize(*args, **kwargs): # real signature unknown
    pass

def GetSystemInfo(*args, **kwargs): # real signature unknown
    pass

def GetSystemMetrics(*args, **kwargs): # real signature unknown
    pass

def GetSystemPowerStatus(*args, **kwargs): # real signature unknown
    pass

def GetSystemTime(*args, **kwargs): # real signature unknown
    pass

def GetTempFileName(*args, **kwargs): # real signature unknown
    pass

def GetTempPath(*args, **kwargs): # real signature unknown
    pass

def GetThreadLocale(*args, **kwargs): # real signature unknown
    pass

def GetTickCount(*args, **kwargs): # real signature unknown
    pass

def GetTimeFormat(*args, **kwargs): # real signature unknown
    pass

def GetTimeZoneInformation(*args, **kwargs): # real signature unknown
    pass

def GetUserDefaultLangID(*args, **kwargs): # real signature unknown
    pass

def GetUserDefaultLCID(*args, **kwargs): # real signature unknown
    pass

def GetUserName(*args, **kwargs): # real signature unknown
    pass

def GetUserNameEx(*args, **kwargs): # real signature unknown
    pass

def GetVersion(*args, **kwargs): # real signature unknown
    pass

def GetVersionEx(*args, **kwargs): # real signature unknown
    pass

def GetVolumeInformation(*args, **kwargs): # real signature unknown
    pass

def GetWindowLong(*args, **kwargs): # real signature unknown
    pass

def GetWindowsDirectory(*args, **kwargs): # real signature unknown
    pass

def GlobalMemoryStatus(*args, **kwargs): # real signature unknown
    pass

def GlobalMemoryStatusEx(*args, **kwargs): # real signature unknown
    pass

def HIBYTE(*args, **kwargs): # real signature unknown
    pass

def HIWORD(*args, **kwargs): # real signature unknown
    pass

def InitiateSystemShutdown(*args, **kwargs): # real signature unknown
    pass

def keybd_event(*args, **kwargs): # real signature unknown
    pass

def LoadCursor(*args, **kwargs): # real signature unknown
    pass

def LoadKeyboardLayout(*args, **kwargs): # real signature unknown
    pass

def LoadLibrary(*args, **kwargs): # real signature unknown
    pass

def LoadLibraryEx(*args, **kwargs): # real signature unknown
    pass

def LoadResource(*args, **kwargs): # real signature unknown
    pass

def LoadString(*args, **kwargs): # real signature unknown
    pass

def LOBYTE(*args, **kwargs): # real signature unknown
    pass

def LOWORD(*args, **kwargs): # real signature unknown
    pass

def MAKELANGID(*args, **kwargs): # real signature unknown
    pass

def MAKELONG(*args, **kwargs): # real signature unknown
    pass

def MAKEWORD(*args, **kwargs): # real signature unknown
    pass

def MapVirtualKey(*args, **kwargs): # real signature unknown
    pass

def MessageBeep(*args, **kwargs): # real signature unknown
    pass

def MessageBox(*args, **kwargs): # real signature unknown
    pass

def MessageBoxEx(*args, **kwargs): # real signature unknown
    pass

def MonitorFromPoint(*args, **kwargs): # real signature unknown
    pass

def MonitorFromRect(*args, **kwargs): # real signature unknown
    pass

def MonitorFromWindow(*args, **kwargs): # real signature unknown
    pass

def mouse_event(*args, **kwargs): # real signature unknown
    pass

def MoveFile(*args, **kwargs): # real signature unknown
    pass

def MoveFileEx(*args, **kwargs): # real signature unknown
    pass

def OpenProcess(*args, **kwargs): # real signature unknown
    pass

def OpenThread(*args, **kwargs): # real signature unknown
    pass

def OutputDebugString(*args, **kwargs): # real signature unknown
    pass

def PostMessage(*args, **kwargs): # real signature unknown
    pass

def PostQuitMessage(*args, **kwargs): # real signature unknown
    pass

def PostThreadMessage(*args, **kwargs): # real signature unknown
    pass

def RegCloseKey(*args, **kwargs): # real signature unknown
    pass

def RegConnectRegistry(*args, **kwargs): # real signature unknown
    pass

def RegCopyTree(*args, **kwargs): # real signature unknown
    pass

def RegCreateKey(*args, **kwargs): # real signature unknown
    pass

def RegCreateKeyEx(*args, **kwargs): # real signature unknown
    pass

def RegDeleteKey(*args, **kwargs): # real signature unknown
    pass

def RegDeleteKeyEx(*args, **kwargs): # real signature unknown
    pass

def RegDeleteTree(*args, **kwargs): # real signature unknown
    pass

def RegDeleteValue(*args, **kwargs): # real signature unknown
    pass

def RegEnumKey(*args, **kwargs): # real signature unknown
    pass

def RegEnumKeyEx(*args, **kwargs): # real signature unknown
    pass

def RegEnumKeyExW(*args, **kwargs): # real signature unknown
    pass

def RegEnumValue(*args, **kwargs): # real signature unknown
    pass

def RegFlushKey(*args, **kwargs): # real signature unknown
    pass

def RegGetKeySecurity(*args, **kwargs): # real signature unknown
    pass

def RegisterWindowMessage(*args, **kwargs): # real signature unknown
    pass

def RegLoadKey(*args, **kwargs): # real signature unknown
    pass

def RegNotifyChangeKeyValue(*args, **kwargs): # real signature unknown
    pass

def RegOpenCurrentUser(*args, **kwargs): # real signature unknown
    pass

def RegOpenKey(*args, **kwargs): # real signature unknown
    pass

def RegOpenKeyEx(*args, **kwargs): # real signature unknown
    pass

def RegOpenKeyTransacted(*args, **kwargs): # real signature unknown
    pass

def RegOverridePredefKey(*args, **kwargs): # real signature unknown
    pass

def RegQueryInfoKey(*args, **kwargs): # real signature unknown
    pass

def RegQueryInfoKeyW(*args, **kwargs): # real signature unknown
    pass

def RegQueryValue(*args, **kwargs): # real signature unknown
    pass

def RegQueryValueEx(*args, **kwargs): # real signature unknown
    pass

def RegRestoreKey(*args, **kwargs): # real signature unknown
    pass

def RegSaveKey(*args, **kwargs): # real signature unknown
    pass

def RegSaveKeyEx(*args, **kwargs): # real signature unknown
    pass

def RegSetKeySecurity(*args, **kwargs): # real signature unknown
    pass

def RegSetValue(*args, **kwargs): # real signature unknown
    pass

def RegSetValueEx(*args, **kwargs): # real signature unknown
    pass

def RegUnLoadKey(*args, **kwargs): # real signature unknown
    pass

def RGB(*args, **kwargs): # real signature unknown
    pass

def SearchPath(*args, **kwargs): # real signature unknown
    pass

def SendMessage(*args, **kwargs): # real signature unknown
    pass

def SetClassLong(*args, **kwargs): # real signature unknown
    pass

def SetClassWord(*args, **kwargs): # real signature unknown
    pass

def SetConsoleCtrlHandler(*args, **kwargs): # real signature unknown
    pass

def SetConsoleTitle(*args, **kwargs): # real signature unknown
    pass

def SetCursor(*args, **kwargs): # real signature unknown
    pass

def SetCursorPos(*args, **kwargs): # real signature unknown
    pass

def SetDllDirectory(*args, **kwargs): # real signature unknown
    pass

def SetEnvironmentVariable(*args, **kwargs): # real signature unknown
    pass

def SetEnvironmentVariableW(*args, **kwargs): # real signature unknown
    pass

def SetErrorMode(*args, **kwargs): # real signature unknown
    pass

def SetFileAttributes(*args, **kwargs): # real signature unknown
    pass

def SetHandleInformation(*args, **kwargs): # real signature unknown
    pass

def SetLastError(*args, **kwargs): # real signature unknown
    pass

def SetLocalTime(*args, **kwargs): # real signature unknown
    pass

def SetStdHandle(*args, **kwargs): # real signature unknown
    pass

def SetSysColors(*args, **kwargs): # real signature unknown
    pass

def SetSystemFileCacheSize(*args, **kwargs): # real signature unknown
    pass

def SetSystemPowerState(*args, **kwargs): # real signature unknown
    pass

def SetSystemTime(*args, **kwargs): # real signature unknown
    pass

def SetThreadLocale(*args, **kwargs): # real signature unknown
    pass

def SetTimeZoneInformation(*args, **kwargs): # real signature unknown
    pass

def SetWindowLong(*args, **kwargs): # real signature unknown
    pass

def ShellExecute(*args, **kwargs): # real signature unknown
    pass

def ShowCursor(*args, **kwargs): # real signature unknown
    pass

def Sleep(*args, **kwargs): # real signature unknown
    pass

def SleepEx(*args, **kwargs): # real signature unknown
    pass

def TerminateProcess(*args, **kwargs): # real signature unknown
    pass

def ToAsciiEx(*args, **kwargs): # real signature unknown
    pass

def Unicode(*args, **kwargs): # real signature unknown
    pass

def UpdateResource(*args, **kwargs): # real signature unknown
    pass

def VkKeyScan(*args, **kwargs): # real signature unknown
    pass

def VkKeyScanEx(*args, **kwargs): # real signature unknown
    pass

def WinExec(*args, **kwargs): # real signature unknown
    pass

def WinHelp(*args, **kwargs): # real signature unknown
    pass

def WriteProfileSection(*args, **kwargs): # real signature unknown
    pass

def WriteProfileVal(*args, **kwargs): # real signature unknown
    pass

# classes

class PyDISPLAY_DEVICEType(object):
    # no doc
    def Clear(self, *args, **kwargs): # real signature unknown
        pass

    def __delattr__(self, *args, **kwargs): # real signature unknown
        """ Implement delattr(self, name). """
        pass

    def __getattribute__(self, *args, **kwargs): # real signature unknown
        """ Return getattr(self, name). """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(*args, **kwargs): # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __setattr__(self, *args, **kwargs): # real signature unknown
        """ Implement setattr(self, name, value). """
        pass

    DeviceID = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """String of at most 128 chars"""

    DeviceKey = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """String of at most 128 chars"""

    DeviceName = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """String of at most 32 chars"""

    DeviceString = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """String of at most 128 chars"""

    Size = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Size of structure"""

    StateFlags = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Bitmask of DISPLAY_DEVICE_* constants indicating current device status"""



# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001A5EA80C090>'

__spec__ = None # (!) real value is "ModuleSpec(name='win32api', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001A5EA80C090>, origin='C:\\\\Users\\\\afham\\\\Desktop\\\\Custom\\\\Samples\\\\venv\\\\Lib\\\\site-packages\\\\win32\\\\win32api.pyd')"

