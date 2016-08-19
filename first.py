"""does the thing."""


def rude():
    """
    Be rude to the caller.

    Does so by being generally rude and stuff.
    """
    print('lalalalal')
    myname = input()
    typed = ''
    if myname == 'peyton':
        while typed != 'stop':
            print('no you')
            while True:
                print(typed + '?')
                typed = input()
                if typed == 'no':
                    break
                break
            typed = input()
    else:
        print('up yours ' + myname)

if __name__ == '__main__':
    rude()
