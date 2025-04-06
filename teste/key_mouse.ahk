#NoEnv
#SingleInstance force
SendMode Input
SetTitleMatchMode, 2

; Abre o Razer Synapse
Run, "C:\Program Files (x86)\Razer\Synapse3\WPFUI\Framework\Razer Synapse 3 Host\Razer Synapse 3.exe"
WinWaitActive, Razer Synapse
WinMaximize, Razer Synapse
Sleep, 2000

; Clica na aba STUDIO
Click, 470, 10
Sleep, 1000

; Clica no logo do mouse
Click, 950, 750
Sleep, 1000

; Clica no campo de cor HEX
Click, 1745, 360
Sleep, 300

; Aguarda o Python digitar o novo HEX
Sleep, 3000

; Clica no botão SALVAR (ajuste conforme necessário)
Click, 1804, 1013
Sleep, 1000

; Fecha o Synapse
WinClose, Razer Synapse
Sleep, 500
Process, Close, Razer Synapse 3.exe
ExitApp