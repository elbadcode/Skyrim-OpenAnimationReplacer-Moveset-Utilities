import FreeSimpleGUI as sg


keycodes = {
        '<0>': 11,
        '<1>': 2,
        '<2>': 3,
        '<3>': 4,
        '<4>': 5,
        '<5>': 6,
        '<6>': 7,
        '<7>': 8,
        '<8>': 9,
        '<9>': 10,
        '<A>': 30,
        '<Apostrophe>': 40,
        '<B>': 48,
        '<BackSlash>': 43,
        '<Backspace>': 14,
        '<C>': 46,
        '<CapsLock>': 58,
        '<Comma>': 51,
        '<Console>': 41,
        '<D>': 32,
        '<Delete>': 211,
        '<DownArrow>': 208,
        '<E>': 18,
        '<End>': 207,
        '<Enter>': 28,
        '<Equals>': 13,
        '<Escape>': 1,
        '<F>': 33,
        '<F1>': 59,
        '<F10>': 68,
        '<F11>': 87,
        '<F12>': 88,
        '<F2>': 60,
        '<F3>': 61,
        '<F4>': 62,
        '<F5>': 63,
        '<F6>': 64,
        '<F7>': 65,
        '<F8>': 66,
        '<F9>': 67,
        '<ForwardSlash>': 53,
        '<G>': 34,
        '<H>': 35,
        '<Home>': 199,
        '<I>': 23,
        '<Insert>': 210,
        '<J>': 36,
        '<K>': 37,
        '<L>': 38,
        '<LeftAlt>': 56,
        '<LeftArrow>': 203,
        '<LeftBracket>': 26,
        '<LeftControl>': 29,
        '<LeftMouseButton>': 256,
        '<LeftShift>': 42,
        '<M>': 50,
        '<MiddleMouse>': 258,
        '<Minus>': 12,
        '<MouseButton3>': 259,
        '<MouseButton4>': 260,
        '<MouseButton5>': 261,
        '<MouseButton6>': 262,
        '<MouseButton7>': 263,
        '<MouseWheelDown>': 265,
        '<MouseWheelUp>': 264,
        '<N>': 49,
        '<NUM>': 181,
        '<NUM->': 74,
        '<NUM*>': 55,
        '<NUM.>': 83,
        '<NUM+>': 78,
        '<NUM0>': 82,
        '<NUM1>': 79,
        '<NUM2>': 80,
        '<NUM3>': 81,
        '<NUM4>': 75,
        '<NUM5>': 76,
        '<NUM6>': 77,
        '<NUM7>': 71,
        '<NUM8>': 72,
        '<NUM9>': 73,
        '<NUMEnter>': 156,
        '<NumLock>': 69,
        '<O>': 24,
        '<P>': 25,
        '<Pause>': 197,
        '<Period>': 52,
        '<PgDown>': 209,
        '<PgUp>': 201,
        '<PtrScr>': 183,
        '<Q>': 16,
        '<R>': 19,
        '<RightAlt>': 184,
        '<RightArrow>': 205,
        '<RightBracket>': 27,
        '<RightControl>': 157,
        '<RightMouseButton>': 257,
        '<RightShift>': 54,
        '<S>': 31,
        '<ScrollLock>': 70,
        '<Semicolon>': 39,
        '<Spacebar>': 57,
        '<T>': 20,
        '<Tab>': 15,
        '<U>': 22,
        '<UpArrow>': 200,
        '<V>': 47,
        '<W>': 17,
        '<X>': 45,
        '<Y>': 21,
        '<Z>': 44
}


layout = [[sg.Text('Press any key to get the dxscancode equivalent for things like dtrykeyutils or dkaf')],
          [sg.Input(key='-IN-')],
          [sg.Output(size=(30, 8))],
          [sg.Button('Go'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout, finalize=True)

window.bind('<0>', 11)
window.bind('<1>', 12)


while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()