.global _start

.equ GPIO_BASE, 0x20200000         // GPIO base address for Raspberry Pi 1
.equ GPFSEL1, GPIO_BASE + 0x04     // GPIO Function Select 1
.equ GPSET0, GPIO_BASE + 0x1C      // GPIO Pin Output Set 0
.equ GPCLR0, GPIO_BASE + 0x28      // GPIO Pin Output Clear 0

_start:
    LDR R0, =GPFSEL1               // Load GPFSEL1 register address
    LDR R1, [R0]
    BIC R1, R1, #(7 << 18)         // Clear bits 18-20
    ORR R1, R1, #(1 << 18)         // Set GPIO16 as output
    STR R1, [R0]                   // Write back to GzPFSEL1

loop:
    LDR R0, =GPSET0                // Load GPSET0 register address
    MOV R1, #(1 << 16)             // Set GPIO16
    STR R1, [R0]

    BL delay                       // Call delay

    LDR R0, =GPCLR0                // Load GPCLR0 register address
    MOV R1, #(1 << 16)             // Clear GPIO16
    STR R1, [R0]

    BL delay                       // Call delay

    B loop                         // Repeat loop

delay:
    MOV R2, #0x3F0000              // Delay count
delay_loop:
    SUBS R2, R2, #1
    BNE delay_loop
    BX LR
