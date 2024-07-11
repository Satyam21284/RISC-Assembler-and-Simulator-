register={'000':0,'001':0,'010': 0,'011':0,'100':0,'101':0,'110':0,"111":0}#preprogram memory
flag=[0,0,0,0]#v=0,l=1,g=2,e=3
memory=["0000000000000000" for i in range(256)]#empty memory without any program
program_counter=[]


def convert(list):
    s = [str(i) for i in list]
    res = "".join(s)
    while(len(res)!=16):
        res="0"+res
    return(res)


def final(pc):
    final_output=format(pc,'08b')
    final_output=final_output+" "+format(register["000"],"016b")+" "+format(register["001"],"016b")+" "+format(register["010"],"016b")+" "+format(register["011"],"016b")+" "+format(register["100"],"016b")+" "+format(register["101"],"016b")+" "+format(register["110"],"016b")+" "
    final_output=final_output+convert(flag)
    print(final_output)
    program_counter.append(final_output)





import sys
list_of_instruction=sys.stdin.read().split("\n")

if(list_of_instruction[-1]==''):
    list_of_instruction.pop()
length=len(list_of_instruction)

count=0
i=0
while(i<length):
    count=count+1
    inst=list_of_instruction[i]
    opcode=inst[0:5]
    if(opcode=="10000"):
        
        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        register[reg3]=register[reg1]+register[reg2]
        if(register[reg3]>65535):
            flag[3]=0
            flag[1]=0
            flag[2]=0
            flag[0]=1
            register[reg3]=65535
        else:
            flag[3]=0
            flag[1]=0
            flag[2]=0
            flag[0]=0
        final(i)

        

    elif(opcode=="10001"):
        
        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        if(register[reg1]<register[reg2]):
            register[reg3]=0
            flag[3]=0
            flag[1]=0
            flag[2]=0
            flag[0]=1
            
        else:
            register[reg3]=register[reg1]-register[reg2]
            flag[3]=0
            flag[1]=0
            flag[2]=0
            flag[0]=0
        final(i)

    elif(opcode=="10010"):
        
        reg1=inst[5:8]
        imm=inst[8:]
        register[reg1]=int(imm,2)
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)


    elif(opcode=="10011"):
        
        reg1=inst[10:13]
        reg2=inst[13:]
        register[reg2]==register[reg1]
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)


    elif(opcode=="10100"):
        
        reg1=inst[5:8]
        mem_add=int(inst[8:],2)
        register[reg1]=int(memory[mem_add],2)
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)
        


    elif(opcode=="10101"):
        
        reg1=inst[5:8]
        mem_add=int(inst[8:],2)
        memory[mem_add]=format(register[reg1],"016b")
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)


    elif(opcode=="10110"):
        
        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        register[reg3]=register[reg1]*register[reg2]
        if(register[reg3]>65535):
            register[reg3]=65535
            flag[3]=0
            flag[1]=0
            flag[2]=0
            flag[0]=1
            
        else:
            flag[3]=0
            flag[2]=0
            flag[1]=0
            flag[0]=0
        final(i)
        
    elif(opcode=="10111"):
        
        reg1=inst[10:13]
        reg2=inst[13:]
        register["000"]=register[reg1]//register[reg2]
        register["001"]=register[reg1]%register[reg2]
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)
        

    elif(opcode=="11000"):
        
        reg1=inst[5:8]
        imm=inst[8:]
        register[reg1]=register[reg1]>>int(imm,2)
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)
        


    elif(opcode=="11001"):
        
        reg1=inst[5:8]
        imm=inst[8:]
        register[reg1]=register[reg1]<<int(imm,2)
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)



    elif(opcode=="11010"):
    
        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        register[reg3]=register[reg1]^register[reg2]
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)



    elif(opcode=="11011"):
    
        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        register[reg3]=register[reg1] or register[reg2]
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)



    elif(opcode=="11100"):

        reg1=inst[7:10]
        reg2=inst[10:13]
        reg3=inst[13:]
        register[reg3]=register[reg1] and register[reg2]
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)



    elif(opcode=="11101"):

        reg1=inst[10:13]
        reg2=inst[13:]
        register[reg2]= abs(~register[reg1])
        flag[3]=0
        flag[1]=0
        flag[2]=0
        flag[0]=0
        final(i)



    elif(opcode=="11110"):
        
        reg1=register[inst[10:13]]
        reg2=register[inst[13:]]


        if(reg1==reg2):
            flag[3]=1
            flag[2]=0
            flag[1]=0
            flag[0]=0
        elif(reg1>reg2):
            flag[3]=0
            flag[2]=1
            flag[1]=0
            flag[0]=0

        elif(reg1<reg2):
            flag[3]=0
            flag[2]=0
            flag[1]=1
            flag[0]=0
        final(i)

    elif(opcode=="01010"):
        
        flag[3]=0
        flag[2]=0
        flag[1]=0
        flag[0]=0
        final(i)     

    elif(opcode=="11111"):
        
        flag[0]=0
        flag[1]=0
        flag[2]=0
        flag[3]=0
        final(i)
        i=int(inst[8:],2)-1


    elif(opcode=="01100"):
        
        if(flag[1]==1):
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)
            i=int(inst[8:],2)-1
        else:
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)

    elif(opcode=="01101"):
        
        if(flag[2]==1):
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)
            i=int(inst[8:],2)-1
        else:
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)

            
    elif(opcode=="01111"):
        
        if(flag[3]==1):
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)
            i=int(inst[8:],2)-1
        else:
            flag[0]=0
            flag[1]=0
            flag[2]=0
            flag[3]=0
            final(i)
    i=i+1

program_memory=0
while(program_memory<length):
    memory[program_memory]=list_of_instruction[program_memory]
    program_memory=program_memory+1

for mem in memory:
    count=count+1
    print(mem)

