;sudo apt install libxtst-dev
; linux_alt_f4.asm
; Simulates Alt + F4 and Enter keypress using X11

section .data
    display db 0                ; Pointer to X11 display structure (NULL initially)
    keysym_alt dq 0xffe9        ; Keysym for Alt (Left Alt: XK_Alt_L)
    keysym_f4 dq 0xffc1         ; Keysym for F4
    keysym_enter dq 0xff0d      ; Keysym for Enter

section .bss
    display_ptr resq 1          ; Reserve space for Display pointer

section .text
global _start

extern XOpenDisplay
extern XKeysymToKeycode
extern XTestFakeKeyEvent
extern XFlush
extern XCloseDisplay
extern sleep

_start:
    ; Open X11 display
    mov rdi, 0                  ; Pass NULL to XOpenDisplay (default display)
    call XOpenDisplay
    test rax, rax               ; Check if display opened successfully
    jz exit_program
    mov [display_ptr], rax      ; Store Display pointer

main_loop:
    ; Simulate Alt key down
    mov rdi, [display_ptr]      ; Display pointer
    mov rsi, [keysym_alt]       ; Alt keysym
    call simulate_key_down

    ; Simulate F4 key down
    mov rdi, [display_ptr]
    mov rsi, [keysym_f4]        ; F4 keysym
    call simulate_key_down

    ; Simulate F4 key up
    mov rdi, [display_ptr]
    mov rsi, [keysym_f4]
    call simulate_key_up

    ; Simulate Alt key up
    mov rdi, [display_ptr]
    mov rsi, [keysym_alt]
    call simulate_key_up

    ; Simulate Enter key down
    mov rdi, [display_ptr]
    mov rsi, [keysym_enter]     ; Enter keysym
    call simulate_key_down

    ; Simulate Enter key up
    mov rdi, [display_ptr]
    mov rsi, [keysym_enter]
    call simulate_key_up

    ; Flush X11 event queue
    mov rdi, [display_ptr]
    call XFlush

    ; Delay (sleep 1 second)
    mov rdi, 1                  ; Sleep for 1 second
    call sleep

    jmp main_loop               ; Repeat

exit_program:
    ; Close X11 display
    mov rdi, [display_ptr]
    call XCloseDisplay

    ; Exit the program
    mov rax, 60                 ; Exit syscall number
    xor rdi, rdi                ; Exit code 0
    syscall

simulate_key_down:
    ; Simulate key press
    mov rdx, 1                  ; Key press (True)
    mov rcx, 0                  ; Delay = 0
    call XTestFakeKeyEvent
    ret

simulate_key_up:
    ; Simulate key release
    mov rdx, 0                  ; Key release (False)
    mov rcx, 0                  ; Delay = 0
    call XTestFakeKeyEvent
    ret

;nasm -f elf64 linux_alt_f4.asm -o linux_alt_f4.o
;ld linux_alt_f4.o -lX11 -lXtst -o linux_alt_f4
