// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
	@8192
	D=A
	@temp
	M=D
	@KBD
	D=M
	@BLACK
	D; JNE
	@WHITE
	D; JEQ
	@LOOP
	0; JMP
(BLACK)
	@SCREEN
	D=M
	@LOOP
	D; JNE
	@temp
	M=M-1
	@SCREEN
	D=A
	@temp
	D=D+M
	@R0
	M=D
	@0
	D=!A
	@R0
	A=M
	M=D
	@BLACK
	0; JMP
(WHITE)
	@SCREEN
	D=M
	@LOOP
	D; JEQ
	@temp
	M=M-1
	@SCREEN
	D=A
	@temp
	A=M+D
	M=0
	@WHITE
	0; JMP
	