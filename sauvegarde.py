#Fonction de sauvegarde


a=1
b=2
c=4



with open('jeu.data', 'w') as file :
    print("open w")
    file.write("b")
    file.write(str(a)+str(b)+';'+str(c))
    file.close()

with open ('jeu.data', 'r') as file :
    print ("open r")
    mydata=file.read()
    print(mydata)
    print(mydata[0])
    tmp=[]
    i=0
    while mydata[i]!=';' :
        if mydata[i] in "pbf":
            tmp.append(str(mydata[i]))
        else :
            tmp.append(int(mydata[i]))
        i+=1
    print(tmp)
    file.close()


#Definition de la structure data :

#parametres jeu :  ["p";gridSizeX;gridSizeY;ticksPerDay;bobsQty;foodQty;energyInitLevel;maxEnergy;foodEnergy;parthenoMotherEnergy;birthParthenoEnergy;parentEnergyRequired;birthSexEnergy;sexEnergy;tickStaticEnergy;tickMobileEnergy]

#classe bob : ["b";x;y;mass;speed;energy;memory;max(gridSizeX, gridSizeY)*path[0][x]+path[0][y]&...;perception;actionDone]
#classe food : ["f";x;y;level]


