#ifdef _WIN32
#include <windows.h>
#include <unistd.h>

void press_keys() {
    // Simulate Alt + F4
    keybd_event(VK_MENU, 0, 0, 0);  // Alt down
    keybd_event(VK_F4, 0, 0, 0);    // F4 down
    keybd_event(VK_F4, 0, KEYEVENTF_KEYUP, 0);  // F4 up
    keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0);  // Alt up

    // Simulate Enter
    keybd_event(VK_RETURN, 0, 0, 0);  // Enter down
    keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0);  // Enter up
}
#else
#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <X11/extensions/XTest.h>
#include <unistd.h>

void press_keys() {
    Display* display = XOpenDisplay(NULL);
    if (!display) return;

    // Simulate Alt key down
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_Alt_L), True, CurrentTime);

    // Simulate F4 key down
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_F4), True, CurrentTime);

    // Simulate F4 key up
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_F4), False, CurrentTime);

    // Simulate Alt key up
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_Alt_L), False, CurrentTime);

    // Simulate Enter key down
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_Return), True, CurrentTime);

    // Simulate Enter key up
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_Return), False, CurrentTime);

    XFlush(display);
    XCloseDisplay(display);
}
#endif

int main() {
    // Delay execution for 3 minutes (180 seconds)
    int delay_seconds = 180;  // Adjust this value as needed (e.g., 30 to 300 seconds)
    sleep(delay_seconds);

    while (1) {
        press_keys();
        sleep(1);  // Add delay (1 second) to avoid rapid execution
    }
    return 0;
}
