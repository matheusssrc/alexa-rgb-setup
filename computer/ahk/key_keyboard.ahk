#Persistent
SetTitleMatchMode, 2
DetectHiddenWindows, On
SendMode Input
SetKeyDelay, 30, 30
SetControlDelay, 30

winTitle := "hub.fgg.com.cn quer se conectar a um dispositivo HID"

WinWait, %winTitle%, , 10
IfWinExist, %winTitle%
{
    WinActivate
    WinWaitActive, %winTitle%, , 5
    Sleep, 500

    Send, {Tab}
    Sleep, 150

    Send, {Up}
    Sleep, 150

    Send, {Tab}
    Sleep, 150

    Send, {Tab}
    Sleep, 150

    Send, {Enter}
    Sleep, 300
}
ExitApp