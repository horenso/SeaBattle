def menu():
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_WHITE)
    screen.keypad(1)
    pos = 1
    x = None
    # I'm going to be lazy and save some typing here.
    h = curses.color_pair(1)
    n = curses.A_NORMAL
    while x != ord('\n'):
        # Gotta reset the screen from the root or lose the border, window, etc.
        screen.clear()
        screen.border(0)
        screen.addstr(2,2, "XFDL VIEWER", curses.A_STANDOUT)
        screen.addstr(4,2, "Please curect an option...", curses.A_BOLD)
        # Detect what is highlighted by the 'pos' variable.
        if pos == 1:
            screen.addstr(5,4, "1 - XFDL -> XML",h)
        else:
            screen.addstr(5,4, "1 - XFDL -> XML",n)
        if pos == 2:
            screen.addstr(6,4, "2 - XML  -> XFDL",h)
        else:
            screen.addstr(6,4, "2 - XML  -> XFDL",n)
        if pos == 3:
            screen.addstr(7,4, "3 - Show XML",h)
        else:
            screen.addstr(7,4, "3 - Show XML",n)
        if pos == 4:
            screen.addstr(8,4, "4 - Exit",h)
        else:
            screen.addstr(8,4, "4 - Exit",n)
        if pos == 5:
            screen.addstr(9,4, "5 - DEBUG", h)
        else:
            screen.addstr(9,4, "5 - DEBUG", n)
        screen.refresh()
        x = screen.getch()
        # Is 'x' 1-5 or arrow up, arrow down?
        if x == ord('1'):
            pos = 1
        elif x == ord('2'):
            pos = 2
        elif x == ord('3'):
            pos = 3
        elif x == ord('4'):
            pos = 4
        elif x == ord('5'):
            pos = 5
        # It was a pain in the ass trying to get the arrows working.
        elif x == 258:
            if pos < 5:
                pos += 1
            else:
                pos = 1
        # Since the curses.KEY_* did not work, I used the raw return value.
        elif x == 259:
            if pos > 1:
                pos += -1
            else:
                pos = 5
        elif x != ord('\n'):
            curses.flash()
            # show_error() is my custom function for displaying a message:
            # show_error(str:message, int:line#, int:seconds_to_display)
            show_error('Invalid Key',11,1)

    return ord(str(pos))

