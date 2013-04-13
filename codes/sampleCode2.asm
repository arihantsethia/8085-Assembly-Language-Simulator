;Code to execute division between two 16bit numbers.
JMP START

;data

;========================================
; the main function starts -----        ;|
                                        ;|
; this function calls the divide routine;|
; the quotient is finally stored in 0000;|
;----------------------------------------|
START: nop                              ;|
                                        ;|
                                        ;|
;store current state                    ;|
PUSH PSW                                ;|
PUSH B                                  ;|
PUSH D                                  ;|
PUSH H                                  ;|
;----------------------------------------|
;enter the arguments here                |
;----------------------------------------|
;push args for arg1/arg2                ;|
;arg2                                   ;|
MVI H , 00H                             ;|
MVI L , 04H                             ;|
PUSH H                                  ;|
                                        ;|
;arg1                                   ;|
MVI H , 00H                             ;|
MVI L , 28H                             ;|
PUSH H                                  ;|
;----------------------------------------|
                                        ;|
CALL DIVIDE                             ;|
                                        ;|
;----------------------------------------|
                                        ;|
;get result                             ;|
POP H                                   ;|
;store result in mem                    ;|
SHLD 0000H                              ;|
                                        ;|
;restore state                          ;|
POP H                                   ;|
POP D                                   ;|
POP B                                   ;|
POP PSW                                 ;|
RST 5                                   ;|
; the main function ends -----          ;|
                                        ;|
;========================================



;========================================
; Division routine                      ;|
                                        ;|
;employs continued subtraction          ;|
                                        ;|
; To eval A/B                           ;|
                                        ;|
;save current state                     ;|
;PUSH B                                 ;|
;PUSH A                                 ;|
;CALL DIVIDE                            ;|
;pop back original state                ;|
                                        ;|
;returns 16 bit number on stack         ;|
;----------------------------------------|
                                        ;|
DIVIDE: nop                             ;|
;pop the return address                 ;|
POP H                                   ;|
SHLD 0102H                              ;|
                                        ;|
;BC stores the quotient                 ;|
MVI B,00H                               ;|
MVI C,00H                               ;|
;get args                               ;|
POP D ; A                               ;|
POP H ; B                               ;|
repeat_sub: nop                         ;|
    ;store current state                ;|
    PUSH PSW                            ;|
    PUSH B                              ;|
    PUSH D                              ;|
    PUSH H                              ;|
                                        ;|
    ;B                                  ;|
    PUSH H                              ;|
    ;A                                  ;|
    PUSH D                              ;|
    ;A-B                                ;|
    CALL SUBTRACT                       ;|
                                        ;|
    ;get result                         ;|
    POP H                               ;|
    ;store result in mem                ;|
    SHLD 0300H                          ;|
    ;restore state                      ;|
    POP H                               ;|
    POP D                               ;|
    POP B                               ;|
    POP PSW                             ;|
    ;increment quotient                 ;|
    INX B                               ;|
    ;A = A-B                            ;|
    XCHG                                ;|
    ;load new value of A                ;|
    LHLD 0300H                          ;|
                                        ;|
    ;put it back in old reg             ;|
    XCHG                                ;|
    ;move the high bits to acc          ;|
    MOV A,D                             ;|
    ANI 80h                             ;|
    ;see if the result was negative     ;|
                                        ;|
                                        ;|
    JM sub_done                         ;|
    JMP repeat_sub                      ;|
                                        ;|
sub_done: nop                           ;|
    ;we have subtracted the             ;|
    ;dividend one extra time            ;|
    ;so the quotient is one more        ;|
    ;than correct value                 ;|
    DCX B                               ;|
    ;push answer on stack               ;|
    PUSH B                              ;|
    ;push the return address back       ;|
         LHLD 0102H                     ;|
         PUSH H                         ;|
RET                                     ;|
;div routine ends -----------------     ;|
                                        ;|
                                        ;|
;========================================


;========================================
                                        ;|
; Subtraction routine ---------         ;|
                                        ;|
; to evaluate A - B                     ;|
                                        ;|
;save current state                     ;|
;PUSH B                                 ;|
;PUSH A                                 ;|
;CALL SUBTRACT                          ;|
;pop back original state                ;|
                                        ;|
;returns 16 bit number on stack         ;|
;----------------------------------------|
                                        ;|
SUBTRACT: nop                           ;|
;pop the return address                 ;|
POP H                                   ;|
SHLD 0100H                              ;|
;get arguments (numbers)                ;|
POP D                                   ;|
POP H                                   ;|
                                        ;|
                                        ;|
;subtraction routine                    ;|
                                        ;|
     MOV A,E                            ;|
     SUB L                              ;|
     MOV L,A                            ;|
     MOV A,D                            ;|
     SBB H                              ;|
     MOV H,A                            ;|
                                        ;|
;put answer on stack                    ;|
     PUSH H                             ;|
;also set the negative bit artificially ;|
;for future use                         ;|
     ANI 80h                            ;|	
;push the return address back           ;|
     LHLD 0100H                         ;|
     PUSH H                             ;|
RET                                     ;|
; Subtraction routine ends-----         ;|
                                        ;|
;========================================
