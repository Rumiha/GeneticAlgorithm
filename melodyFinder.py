import musicalbeeps
import random
import copy


#Algorithm parameters
NUMBER_OF_GENERATIONS = 200
POPULATION = 200
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.3
MELODY_INPUT = "C4 E4 G4 C5"
MUTATION_RANGE = 5      #Gen value = old gen value +/- MUTATION_RANGE
#Max notes = (TOP_OCTAVE - BOTTOM_OCTAVE + 1) * 12
HIGHEST_NOTE = "D5"          #Max is 8
LOWEST_NOTE = "F4"      #Min is 0
RECORD_EVERY_X_GENERATIONS = 40

#Setting parameters for player
PLAYER = musicalbeeps.Player(volume = 0.3, mute_output = False)
PLAYER_NOTE_DURATION = 0.5

#Adding all playable/hearable notes to list and assigning them integer values (12 notes in each of 9 octaves = 108 notes)
ALL_NOTES = [["P",0]]   #P represents mute note, pause
for i in range(9):      
    for j in [["C0",1], ["C0#",2], ["D0b",2], ["D0",3], ["D0#",4], ["E0b",4], ["E0",5], ["F0",6], ["F0#",7], ["G0b",7], ["G0",8], ["G0#",9], ["A0b",9], ["A0",10], ["A0#",11], ["B0b",11], ["B0",12]]:
        k = j[0].replace("0", str(i))
        ALL_NOTES.append([k ,j[1]+12*i])
ALL_NOTES = ALL_NOTES + [["C",49], ["C#",50], ["Db",50], ["D",51], ["D#",52], ["Eb",52], ["E",53], ["F",54], ["F#",55], ["Gb",55], ["G",56], ["G#",57], ["Ab",57], ["A",58], ["A#",59], ["Bb",59], ["B",60]]

#Converting input string of notes to integer list that is used for comparison with melodies in population (represents the best chromosome/ideal solution)
MELODY = []
for note in MELODY_INPUT.split():
    for i in ALL_NOTES:
        if i[0]==note:
            MELODY.append(i[1])
            break

#Setting min and max notes
min = 0
max = 108
for j in ALL_NOTES:
    if j[0]==HIGHEST_NOTE:
        max = j[1]
        break
for j in ALL_NOTES:
    if j[0]==LOWEST_NOTE:
        min = j[1]
        break

########## MAIN ##########
def main():
    #Creating first population
    population = []
    for i in range(POPULATION):
        population.append(Melody())

    evolution = []
    #Generations loop
    bestSolutionFound = False
    for gen in range(NUMBER_OF_GENERATIONS):
        
        #1. Check fitness value of each melody in population
        for m in population:
            m.fitness()

        if gen%RECORD_EVERY_X_GENERATIONS==0:   #Saving best result in generation so it can be played later
            bestResult = Melody()
            bestResult.fitnessScore=9999999
            for m in population:
                if m.fitnessScore<bestResult.fitnessScore:
                    bestResult=m
                    if m.fitnessScore==0:
                        bestSolutionFound = True
                        break
            evolution.append(bestResult)

        if(bestSolutionFound == True):
            print("Solution in ", gen, ". generation!")
            break

        #2. Selection function that takes the best results and use them as parents for crossover
        parents = selection(population)

        #3. Crossover function - making children
        children = crossover(population)

        #4. Since the lists of parents and children are half the size of the population, we combine them into new population
        population = parents + children

        #5. Mutation - changing some genes
        population = mutation(population)

    
    #Print best result
    bestResult = Melody()
    bestResult.fitnessScore=9999999
    for m in population:
        m.fitness()
        if m.fitnessScore<bestResult.fitnessScore:
            bestResult=m

            
    print(bestResult)
    print("Fitness score: ", bestResult.fitnessScore)

    for e in evolution:
        e.playMelody()
        PLAYER.play_note("pause", PLAYER_NOTE_DURATION)

    print("bestResult playing")
    bestResult.playMelody()
        

    
    


def selection(population):
    parents = population    
    parents.sort(key=lambda x: x.fitnessScore, reverse=True)    #Sorting population by fitnessScore
    parents = parents[0:int(POPULATION/2)]                      #The better rated half is saved to parents list and will be used in crossover
    return parents  

def crossover(parents):
    children = []
    crossoverPoint = random.randint(1, len(MELODY))    #Randomly selecting crossover point 

    for i in range(0, len(parents), 2):
        temp1 = copy.deepcopy(parents[i].melody)
        temp2 = copy.deepcopy(parents[i+1].melody)
    
        for j in range(crossoverPoint, len(MELODY)):
            temp1[j], temp2[j] = temp2[j], temp1[j]

        if random.random()<CROSSOVER_RATE:             #Return children only if crossover chance is hit, otherwise return one of parents
            children.append(Melody(temp1))
        else:
            children.append(Melody(copy.deepcopy(parents[i].melody)))
        if random.random()<CROSSOVER_RATE:
            children.append(Melody(temp2))
        else:
            children.append(Melody(copy.deepcopy(parents[i+1].melody)))
        if i+2>=len(parents)-1:
            break

    if len(children)+len(parents)!=POPULATION:         #In case the number of notes in melody is odd
        children.append(Melody(copy.deepcopy(parents[random.randint(0, len(parents)-1)].melody)))
    return children

def mutation(population):
    for m in population:
        if random.random()<MUTATION_RATE:
            index = random.randint(0, len(MELODY)-1)
            m.melody[index] += random.randint((-1) * MUTATION_RANGE, MUTATION_RANGE)
    return population 

class Melody:                               
        def __init__(self, input_melody=None):
            self.fitnessScore = None
            if(input_melody==None):              #Setting random notes to melody list
                self.melody = [0] * len(MELODY)
                for i in range(len(MELODY)):
                    self.melody[i] = random.randint(min, max)

            else:
                self.melody = input_melody

        def __str__(self):                      #Print melody as default print for class
            return self.intToStrMelody(self.melody)

        def fitness(self):                      #Fitness function
            self.fitnessScore = 0
            for i in range(len(MELODY)):
                self.fitnessScore += abs(self.melody[i]-MELODY[i])
                
        def intToStrMelody(self, intMelody):    #Converting string of notes to list of integer notes
            strMelody = ""
            for i in intMelody:
                for j in ALL_NOTES:
                    if(j[1]==i):
                        strMelody = strMelody + j[0] + " "
                        break
            return strMelody

        def strToIntMelody(strMelody):          #Converting list of integer notes to string of notes
            intMelody = []
            for note in strMelody.split():
                for i in ALL_NOTES:
                    if i[0]==note:
                        intMelody.append(i[1])
                        break
            return intMelody
        
        def playMelody(self):                   #Play melody
            for note in Melody.intToStrMelody(self, self.melody).split():
                PLAYER.play_note(note, PLAYER_NOTE_DURATION)

        

if __name__=="__main__":
    main()