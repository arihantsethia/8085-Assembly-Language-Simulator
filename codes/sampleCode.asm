; program to swap data between two memory locations
jmp start
var db 7,4
start: 
swp var[0],var[1]
hlt