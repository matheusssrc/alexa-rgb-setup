#NoEnv
#SingleInstance force
SendMode Input
SetTitleMatchMode, 2
CoordMode, Mouse, Screen

; Abre o Razer Synapse
Run, "C:\Program Files (x86)\Razer\Synapse3\WPFUI\Framework\Razer Synapse 3 Host\Razer Synapse 3.exe"
WinWait, Razer Synapse
WinActivate, Razer Synapse
WinWaitActive, Razer Synapse
Sleep, 600

; Move a janela para a tela principal
WinMove, Razer Synapse,, 0, 0, 1920, 1080
Sleep, 300

; Maximiza
WinMaximize, Razer Synapse
Sleep, 300

; Clica na aba STUDIO
Click, 470, 10
Sleep, 500

; Clica no logo do mouse
Click, 950, 750
Sleep, 500

; Clica no campo de cor HEX
Click, 1745, 360
Sleep, 300

; Apaga o valor atual com Duplo Clique e Delete
Click, 1745, 360, 2
Sleep, 100
Send, {Delete}
Sleep, 4000  ; Aguarda digitação pelo Python

; Clica no botão SALVAR
Click, 1804, 1013
Sleep, 500

; Fecha o Synapse
WinClose, Razer Synapse
Sleep, 300
Process, Close, Razer Synapse 3.exe
ExitApp