register={"R0":['000',0],"R1":['001',0],"R2":['010',0],"R3":['011',0],"R4":['100',0],"R5":['101',0],"R6":['110',0],"FLAGS":["111",0]}
flag=[0,0,0,0]#equal=3,greator=2,less=1,value=0
label={}
variable={}
error=0
ind=0
finallist=[]
def type_A(instruction ,reg1,reg2,reg3 ):
    global error
    opcode_type_A={'add':'10000','sub':'10001','mul':'10110','and':'11100','xor':'11010','or':'11011'}
    if (reg1 in register.keys() and reg2 in register.keys() and reg3 in register.keys()):
        final=opcode_type_A[instruction]+'00'+register[reg1][0]+register[reg2][0]+register[reg3][0]
        finallist.append(final)
        if(instruction=="add"):
            register[reg3][1]=register[reg2][1]+register[reg1][1]
            if(register[reg3][1]<0 ):
                register[reg3][1]=0
                flag[0]=1
        elif(instruction=="sub"):
            register[reg3][1]=register[reg1][1]-register[reg2][1]
            if(register[reg3][1]<0):
                register[reg3][1]=0
                flag[0]=1
        elif(instruction=="mul"):
            register[reg3][1]=register[reg2][1]*register[reg1][1]
            if(register[reg3][1]<0):
                register[reg3][1]=0
                flag[0]=1
        elif(instruction=="and"):
            register[reg3][1]=register[reg2][1] and register[reg1][1]
            if(register[reg3][1]<0):
                register[reg3][1]=0
                flag[0]=1
        elif(instruction=="xor"):
            register[reg3][1]=register[reg2][1]^register[reg1][1]
            if(register[reg3][1]<0):
                register[reg3][1]=0
                flag[0]=1
        elif(instruction=="or"):
            register[reg3][1]=register[reg2][1] or register[reg1][1]
            if(register[reg3][1]<0):
                register[reg3][1]=0
                flag[0]=1
    else:
        error=1
def type_B(instruction,reg1,imm):
    global error
    opcode_type_B={'mov':'10010','ls':'11001','rs':"11000"}
    if(imm.isdigit()):
        val=list(bin(int(imm)))
        val1=val[2:]
        lenght=8-len(val1)
        if(lenght<=8):
            strval1="";num='0'
            for i in range(0,lenght-1):
                num=num+'0'
            if (reg1 in register.keys()):
                final=opcode_type_B[instruction]+register[reg1][0]+num+(strval1.join(val1))
                finallist.append(final)
                if(instruction=="mov"):
                    register[reg1][1]=int(imm)
                if(instruction=="ls"):
                    register[reg1][1]=register[reg1][1]<<int(imm)
                if(instruction=="rs"):
                    register[reg1][1]=register[reg1][1]>>int(imm)
            else:
                error=1  
        else:
            error=2
    else:
        error=5

def type_C(instruction ,reg1,reg2):
    opcode_type_C={'mov':'10011','div':'10111','not':'11101','cmp':'11110'}
    if(reg1 in register.keys() and reg2 in register.keys()):
        final=opcode_type_C[instruction]+'00000'+register[reg1][0]+register[reg2][0]
        finallist.append(final)
        if(instruction=="mov"):
            register[reg2][1]=register[reg1][1]
        elif(instruction=="div"):
            if(register[reg2][1]!=0):
                remainder=register[reg1][1]%register[reg2][1]
                quoetient=register[reg1][1]/register[reg2][1]
                register["R0"][1]=quoetient
                register["R1"][1]=remainder
        elif(instruction=="not"):
            register[reg2][1]= ~register[reg1][1]
        else:
            if(register[reg1][1]==register[reg2][1]):
                flag[3]=1
            elif(register[reg1][1]<register[reg2][1]):
                flag[1]=1
            elif(register[reg1][1]>register[reg2][1]):
                flag[2]=1
    else:
        global error
        error=1

def type_D(instruction ,reg1,var ):
    opcode_type_D={'ld':'10100','st':'10101'}
    if (var in variable.keys() and reg1 in register.keys()):
        val=list(bin(variable[var][0]))
        val1=val[2:]
        lenght=8-len(val1)
        strval1="";num='0'
        for i in range(0,lenght-1):
            num=num+'0'
        final=opcode_type_D[instruction]+register[reg1][0]+num+(strval1.join(val1))
        finallist.append(final)
        if(instruction=="ld"):
            register[reg1][1]=variable[var][1]
        elif(instruction=="st"):
            variable[var][1]=register[reg1][1]
    else:
        global error
        error=1

def type_E(instruction ,mem_add ):
    opcode_type_E={'jmp':'11111','jlt':'01100','jgt':'01101','je':'01111'}
    mem_add1=list(bin(int(mem_add)))
    mem_add2=mem_add1[2:]
    lenght=8-len(mem_add2)
    if(lenght<=8):
        strval1="";num='0'
        for i in range(0,lenght-1):
            num=num+'0'
    final=opcode_type_E[instruction]+"000"+num+(strval1.join(mem_add2))
    finallist.append(final)


def type_F(instruction):
    opcode_type_F={'hlt':'01010'}
    final=opcode_type_F[instruction]+'00000000000'
    finallist.append(final)

import sys
instu=sys.stdin.read().split("\n")
list_of_instruction=[]
for i in instu:
    m=i.split(" ")
    list_of_instruction.append(m)
number_of_hlt=list_of_instruction.count(["hlt"])
if(number_of_hlt>1):
    error=6
else:
    pass
index=len(list_of_instruction)
i1=0
bound=0
for instruction1 in list_of_instruction:
    if(instruction1[0]==''):
        index=index-1
        i1=i1+1
    elif(instruction1[0]=="var"):
        if(bound==0):
            index=index-1
            i1=i1+1
        else:
            i=i1
            error=8
    else:
        if(instruction1[0][-1]==":"):
            label_name1=instruction1[0][0:-1]
            a=i1
            temp=instruction1[1:]
            label[label_name1]=[temp,a]
        bound=1
        i1=i1+1

end=len(list_of_instruction)
i=0
j=end
cout=0
while(i<end and error==0):
    inst=list_of_instruction[i]
    if (inst[0]==""):
        i=i+1
    else:
        temp=inst[0]
        if(temp=='var'):
            if(len(inst)==2):
                data=inst[1]
                variable[data]=[index,0]
                index=index+1
            else:
                error=6
        elif(temp[-1]==":"):
            inst=inst[1:]
            while(cout==0 ):
                size=len(inst)
                opcode=inst[0]
                if(len(opcode)==2):
                    if(opcode=='or'):
                        if(size==4):
                            reg1=inst[1]
                            reg2=inst[2]
                            reg3=inst[3]
                            type_A(opcode,reg1,reg2,reg3)
                        else:
                            error=6
                        cout=1
                    elif (opcode=='ls' or opcode=='rs'):
                        if(size==3):
                            reg1=inst[1]
                            val=inst[2][1:]
                            type_B(opcode,reg1,val)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='ld' or opcode=='st'):
                        if(size==3):
                            reg1=inst[1]
                            var=inst[2]
                            type_D(opcode,reg1,var)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='je'):
                        if(flag[3]==1):
                            a1=inst[1]
                            if(a1 in label.keys()):
                                i=int(label[a1][1])
                                type_E(opcode,i)
                                command=label[a1][0]
                                inst=command
                                flag[3]=0
                            else:
                                error=1
                        else:
                            cout=1
                elif(len(opcode)==3 and opcode=='hlt'):
                    type_F(opcode)
                    cout=1
                    ind=1
                    i=end
                else:
                    if(opcode=='add' or opcode=='sub' or opcode=='mul' or opcode=='xor' or opcode=='and' ):
                        if(size==4):
                            reg1=inst[1]
                            reg2=inst[2]
                            reg3=inst[3]
                            type_A(opcode,reg1,reg2,reg3)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='mov' and inst[2] not in register.keys() ):
                        if(size==3):
                            reg1=inst[1]
                            val=inst[2][1:]
                            type_B(opcode,reg1,val)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='div' or opcode=='not' or opcode=='cmp' or opcode=='mov'):
                        if(size==3):
                            reg1=inst[1]
                            reg2=inst[2]
                            type_C(opcode,reg1,reg2)
                        else:
                            error=6
                        cout=1
                    elif (opcode=='jmp' or opcode=='jlt' or opcode=='jgt'):
                        if(opcode=="jmp"):
                            a1=inst[1]
                            if(a1 in label.keys()):
                                i=int(label[a1][1])
                                type_E(opcode,i)
                                command=label[a1][0]
                                inst=command
                            else:
                                error=1
                        elif(opcode=='jlt'):
                            if(flag[1]==1):
                                a1=inst[1]
                                if(a1 in label.keys()):
                                    i=int(label[a1][1])
                                    type_E(opcode,i)
                                    command=label[a1][0]
                                    inst=command
                                    flag[1]=0
                                else:
                                    error=1
                            else:
                                cout=1
                        elif(opcode=="jgt"):
                            if(flag[2]==1):
                                a1=inst[1]
                                if(a1 in label.keys()):
                                    i=int(label[a1][1])
                                    type_E(opcode,i)
                                    command=label[a1][0]
                                    inst=command
                                    flag[2]=0
                                else:
                                    error=1
                            else:
                                cout=1
                    elif (opcode=='hlt'):
                        type_F(opcode)
                        cout=1
                        ind=1
                        i=end
                    else:
                        error=3
                        cout=1
        else: 
            while(cout==0):
                size=len(inst)
                opcode=inst[0]
                if(len(opcode)==2):
                    if(opcode=='or'):
                        if(size==4):
                            reg1=inst[1]
                            reg2=inst[2]
                            reg3=inst[3]
                            type_A(opcode,reg1,reg2,reg3)
                        else:
                            error=6
                        cout=1
                    elif (opcode=='ls' or opcode=='rs'):
                        if(size==3):
                            reg1=inst[1]
                            val=inst[2][1:]
                            type_B(opcode,reg1,val)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='ld' or opcode=='st'):
                        if(size==3):
                            reg1=inst[1]
                            var=inst[2]
                            type_D(opcode,reg1,var)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='je'):
                        if(flag[3]==1):
                            a1=inst[1]
                            if(a1 in label.keys()):
                                i=int(label[a1][1])
                                type_E(opcode,i)
                                command=label[a1][0]
                                inst=command
                                flag[3]=0
                            else:
                                error=1
                        else:
                            cout=1
                elif(len(opcode)==3 and opcode=='hlt'):
                    type_F(opcode)
                    cout=1
                    ind=1
                    i=end
                else:
                    if(opcode=='add' or opcode=='sub' or opcode=='mul' or opcode=='xor' or opcode=='and' ):
                        if(size==4):
                            reg1=inst[1]
                            reg2=inst[2]
                            reg3=inst[3]
                            type_A(opcode,reg1,reg2,reg3)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='mov' and inst[2] not in register.keys() ):
                        if(size==3):
                            reg1=inst[1]
                            val=inst[2][1:]
                            type_B(opcode,reg1,val)
                        else:
                            error=6
                        cout=1
                    elif(opcode=='div' or opcode=='not' or opcode=='cmp' or opcode=='mov'):
                        if(size==3):
                            reg1=inst[1]
                            reg2=inst[2]
                            type_C(opcode,reg1,reg2)
                        else:
                            error=6
                        cout=1
                    elif (opcode=='jmp' or opcode=='jlt' or opcode=='jgt'):
                        if(opcode=="jmp"):
                            a1=inst[1]
                            if(a1 in label.keys()):
                                i=int(label[a1][1])
                                type_E(opcode,i)
                                command=label[a1][0]
                                inst=command
                            else:
                                error=1
                        elif(opcode=='jlt'):
                            if(flag[1]==1):
                                a1=inst[1]
                                if(a1 in label.keys()):
                                    i=int(label[a1][1])
                                    type_E(opcode,i)
                                    command=label[a1][0]
                                    inst=command
                                    flag[1]=0
                                else:
                                    error=1
                            else:
                                cout=1
                        elif(opcode=="jgt"):
                            if(flag[2]==1):
                                a1=inst[1]
                                if(a1 in label.keys()):
                                    i=int(label[a1][1])
                                    type_E(opcode,i)
                                    command=label[a1][0]
                                    inst=command
                                    flag[2]=0
                                else:
                                    error=1
                            else:
                                cout=1
                    elif (opcode=='hlt'):
                        type_F(opcode)
                        cout=1
                        ind=1
                        i=end
                    else:
                        error=3
                        cout=1
        cout=0
        i=i+1
if(error==1):
    print("LINE "+str(i)+" NAME ERROR")
elif(error==2):
    print("LINE "+str(i)+" VALUE EXCEED")
elif(error==3):
    print("LINE "+str(i)+" KEY WORD ERROR")
elif(error==5):
    print("LINE "+str(i)+" VALUE ERROR")
elif(error==6):
    print("LINE "+str(i)+" SYNTAX ERROR\n")
elif(ind==0):
    print("LINE "+str(i)+" OVER FLOW\n")
elif(error==8):
    i=i1
    print("LINE "+str(i)+" SYNTAX ERROR\n")
else:
    for p in finallist:
        print(p)





