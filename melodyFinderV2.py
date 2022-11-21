import musicalbeeps
import random
import copy
import time
import pickle

#Bratec martin (32 notes): F4 G4 A4 F4 F4 G4 A4 F4 A4 B4b C5:2 A4 B4b C5:2 C5:8 D5:8 C5:8 B4b:8 A4 F4 C5:8 D5:8 C5:8 B4b:8 A4 F4 F4 C4 F4:2 F4 C4 F4:2
#The Imperial March (66 notes ): A4 A4 A4 F4:8 C5:8 A4 F4:8 C5:8 A4:2 E5 E5 E5 F5:8 C5:8 A4b F4:8 C5:8 A4:2 A5 A4:8 A4:8 A5 A5b:8 G5:8 G5b:8 F5:8 G5b:8 B4b:8 E5b D5:8 D5b:8 C5:8 B4:8 C5:8 F4:8 A4b F4:8 A4b:8 C5 A4:8 C5:8 E5:2 A5 A4:8 A4:8 A5 A5b:8 G5:8 G5b:8 F5:8 G5b:8 B4b:8 E5b D5:8 D5b:8 C5:8 B4:8 C5:8 F4:8 A4b F4:8 A4b:8 C5 A4:8 C5:8 E5:2
#The Imperial March (43 notes): A4 A4 A4 F4:8 C5:8 A4 F4:8 C5:8 A4:2 E5 E5 E5 F5:8 C5:8 A4b F4:8 C5:8 A4:2 A5 A4:8 A4:8 A5 A5b:8 G5:8 G5b:8 F5:8 G5b:8 B4b:8 E5b D5:8 D5b:8 C5:8 B4:8 C5:8 F4:8 A4b F4:8 A4b:8 C5 A4:8 C5:8 E5:2
#Algorithm parameters
NUMBER_OF_GENERATIONS = 900
POPULATION = 300
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.3
MELODY_INPUT = "A4 A4 A4 F4:8 C5:8 A4 F4:8 C5:8 A4:2 E5 E5 E5 F5:8 C5:8 A4b F4:8 C5:8 A4:2 A5 A4:8 A4:8 A5 A5b:8 G5:8 G5b:8 F5:8 G5b:8 B4b:8 E5b D5:8 D5b:8 C5:8 B4:8 C5:8 F4:8 A4b F4:8 A4b:8 C5 A4:8 C5:8 E5:2"
MUTATION_RANGE = 1      #Gen value = old gen value +/- MUTATION_RANGE
MUTATIONS_PER_MELODY = 1
RECORD_EVERY_X_GENERATIONS = NUMBER_OF_GENERATIONS-1

#Note types: '1'=whole note, '2'=half note, ' '=quarter note, '8'=eight note, '16'=sixteenth note

#Setting parameters for player
PLAYER = musicalbeeps.Player(volume = 0.5, mute_output = False)
DEFAULT_NOTE_DURATION = 0.4

#Adding all playable/hearable notes to list and assigning them integer values (12 notes in each of 9 octaves = 108 notes)
ALL_NOTES = [["P",0]]   #P represents mute note, pause
for i in range(9):      
    for j in [["C0",1], ["C0#",2], ["D0b",2], ["D0",3], ["D0#",4], ["E0b",4], ["E0",5], ["F0",6], ["F0#",7], ["G0b",7], ["G0",8], ["G0#",9], ["A0b",9], ["A0",10], ["A0#",11], ["B0b",11], ["B0",12]]:
        k = j[0].replace("0", str(i))
        ALL_NOTES.append([k ,j[1]+12*i])
ALL_NOTES = ALL_NOTES + [["C",49], ["C#",50], ["Db",50], ["D",51], ["D#",52], ["Eb",52], ["E",53], ["F",54], ["F#",55], ["Gb",55], ["G",56], ["G#",57], ["Ab",57], ["A",58], ["A#",59], ["Bb",59], ["B",60]]
MELODY_LEN = len(MELODY_INPUT.split())

MAX_OCTAVE = 6
MIN_OCTAVE = 3

########## MAIN ##########
def main():
    MELODY = Melody(inputToMelody())        #Creating input melody
    population = []                 #Creating starting population
    for i in range(POPULATION):
        population.append(Melody())
    replay = []
    solutionFound = False
    solutionGeneration = NUMBER_OF_GENERATIONS
    #Main loop
    aaa_parents = 0
    aaa_children = 0
    aaa_mutation = 0
    aaa_fitness = 0

    time1 = time.time()
    for g in range(NUMBER_OF_GENERATIONS):
        aaa_fitness1 = time.time()
        solutionFound = fitness(population, MELODY)                 #1. Check fitness value of each melody in population
        aaa_fitness += (time.time() - aaa_fitness1)



        if solutionFound==True:
            print("Solution found in ", g, ". generation.")
            solutionGeneration = g
            break
        if g%RECORD_EVERY_X_GENERATIONS==0 and g!=0: #Saving some results so it can be played later to see progress        
            bestResult = Melody()
            bestResult.fitnessScore=9999999
            for m in population:
                if m.fitnessScore<bestResult.fitnessScore:
                    bestResult=m
                    if m.fitnessScore==0:
                        bestSolutionFound = True
                        break
            replay.append(bestResult)
                
        aaa_parents1 = time.time()
        parents = selection(population)     #2. Selection function that takes the best melodies and use them as parents for crossover
        aaa_parents += (time.time() - aaa_parents1)

        aaa_children1 = time.time()
        children = crossover(parents)       #3. Crossover function - making children
        aaa_children += (time.time() - aaa_children1)
        population = parents + children     #4. Make new population out of parents and children lists
        
        aaa_mutation1 = time.time()
        population = mutation(population, MELODY)   #5. Mutation - changing some genes
        aaa_mutation += (time.time() - aaa_mutation1)
    time2 = time.time()
    print("Time: ", time2-time1, " s" )
    print("Time for: fitn:", aaa_fitness, ", selec:", aaa_parents, ", cross:", aaa_children, ", muta:", aaa_mutation)
    replayMelodies(replay, solutionGeneration, solutionFound, MELODY)     
    
def fitness(population, MELODY):
    for m in population:
        m.fitnessScore = 0
        for i in range(MELODY_LEN):
            m.fitnessScore += abs(m.melody[i].note-MELODY.melody[i].note) + abs(m.melody[i].time-MELODY.melody[i].time)
        if m.fitnessScore == 0:
            return True  

def selection(population):
    parents = population    
    parents.sort(key=lambda x: x.fitnessScore, reverse=False)    #Sorting population by fitnessScore
    parents = parents[0:int(POPULATION/2)]                      #The better rated half is saved to parents list and will be used in crossover
    return parents  

def crossover(parents):
    children = pickle.loads(pickle.dumps(parents))
    crossoverPoint = random.randint(1, MELODY_LEN)    #Randomly selecting crossover point 
    for i in range(0, len(children), 2):
        if random.random()<CROSSOVER_RATE:   
            for j in range(crossoverPoint, MELODY_LEN):
                children[i].melody[j], children[i+1].melody[j] = children[i+1].melody[j], children[i].melody[j]

    if len(children)+len(parents)!=POPULATION:         #In case the number of notes in melody is odd
        children.append(Melody(pickle.loads(pickle.dumps(parents[random.randint(0, len(parents)-1)].melody))))
    return children

def mutation(population, MELODY):
    for m in population:
        if random.random()<MUTATION_RATE:
            for r in range(MUTATIONS_PER_MELODY):
                index = random.randint(0, MELODY_LEN-1)
                m.melody[index].note += random.randint((-1) * MUTATION_RANGE, MUTATION_RANGE)
                m.melody[index].time += random.randint((-1) * MUTATION_RANGE, MUTATION_RANGE)
    return population 


def intToStrMelody(intMelody):    #Converting string of notes to list of integer notes
    strMelody = ""
    for i in intMelody:
        for j in ALL_NOTES:
            if(j[1]==i):
                strMelody = strMelody + j[0] + " "
                break
    return strMelody

def strToIntMelody(strMelody):    #Converting list of integer notes to string of notes
    intMelody = []
    for note in strMelody.split():
        for i in ALL_NOTES:
            if i[0]==note:
                intMelody.append(i[1])
                break
    return intMelody

def intToStrNote(integer):
    for i in ALL_NOTES:
        if(i[1]==integer):
            return i[0]
    return "P"

def strToIntNote(string):
    for i in ALL_NOTES:
        if(i[0]==string):
            return i[1]

def printIntMelody(melody):
    printMe = ""
    for n in melody.melody:
        printMe += str(n.note) + ":" + str(n.time) + "\t"
    print(printMe)

def printStrMelody(melody):
    printMe = ""
    for n in melody.melody:
        printMe += intToStrNote(n.note) + ":" + str(n.time) + "\t"
    print(printMe)

def replayMelodies(replay, solutionGeneration, solutionFound, MELODY):
    generationCounter = 0
    for m in replay:
        print("\nGen: ", generationCounter, "\tFit: ", m.fitnessScore)
        printStrMelody(m)
        generationCounter+=RECORD_EVERY_X_GENERATIONS
        m.play()
        PLAYER.play_note("pause", 2)
    if solutionFound==True:
        print("\nSOLUTION FOUND:\nGen: ", solutionGeneration, "\tFit: 0")
        MELODY.play()

def inputToMelody():
    noteNote = []
    noteTime = []
    for note in MELODY_INPUT.split():
        for i in ALL_NOTES:
            stringNoteTime = note.split(":")
            if len(stringNoteTime)==2:
                if i[0]==stringNoteTime[0]:
                    noteNote.append(stringNoteTime[0])
                    if int(stringNoteTime[1])==1:
                        noteTime.append(1)
                    elif int(stringNoteTime[1])==2:
                        noteTime.append(2)
                    elif int(stringNoteTime[1])==4:
                        noteTime.append(3)
                    elif int(stringNoteTime[1])==8:
                        noteTime.append(4)
                    elif int(stringNoteTime[1])==16:
                        noteTime.append(5)
                    break
            else:
                if i[0]==stringNoteTime[0]:
                    noteNote.append(stringNoteTime[0])
                    noteTime.append(3)
                    break
    temporary = []
    for i in range(MELODY_LEN):
        temporary.append(Note(noteTime[i], strToIntNote(noteNote[i])))  
    return temporary    

class Note:
    def __init__(self, time=None, note=None):
        if(time==None):
            self.time = random.randint(1,5)
        else:
            self.time = time

        if(note == None):
            self.note = random.randint(MIN_OCTAVE*12, MAX_OCTAVE*12)
        else:
            self.note = note

    def play(self):
        timeToPlay = DEFAULT_NOTE_DURATION
        if self.time==1:
            timeToPlay = DEFAULT_NOTE_DURATION*4
        elif self.time==2:
            timeToPlay = DEFAULT_NOTE_DURATION*2
        elif self.time==3:
            timeToPlay = DEFAULT_NOTE_DURATION
        elif self.time==4:
            timeToPlay = DEFAULT_NOTE_DURATION/2
        elif self.time==5:
            timeToPlay = DEFAULT_NOTE_DURATION/4
            
        PLAYER.play_note(intToStrNote(self.note), timeToPlay)

class Melody:                               
        def __init__(self, inputMelody=None):
            self.fitnessScore = None
            if(inputMelody==None):              #Setting random notes to melody list
                self.melody = []
                for i in range(MELODY_LEN):
                    self.melody.append(Note())
            else:
                self.melody = inputMelody
        
        def play(self, m = None):       #Play melody
            if m==None:
                for n in self.melody:
                    n.play()
            else:
                for n in m.melody:
                    n.play()

        

if __name__=="__main__":
    main()