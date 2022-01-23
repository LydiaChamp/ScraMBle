import random
import itertools
import letters
import json

def find_score(word):
    val = 0
    for i in range(0, len(word)): 
        let_val = letters.lets.get(word[i])[1]
        val = val + let_val
    return val

worddict={}
with open('greek7.txt', 'r', encoding="utf-8") as f7:
    for line in f7:
        word = line.strip('\n')
        worddict[word]=find_score(word)
        
class SakClass():
    
    def __init__(self):
        
        self.queue = []
        for let in letters.lets:
            num = letters.lets.get(let)[0]
            for i in range(num):
                self.queue.append(let)
        self.randomize_sak()


    def randomize_sak(self):
        random.shuffle(self.queue)


    def getletters(self, n):
        result = []
        if n > len(self.queue):
            return None
        for i in range(n):
            element = self.queue.pop()
            result.append(element)
        return result


    def putbackletters(self, letters):
        for let in letters:
            self.queue.append(let)
        self.randomize_sak()

            
        
class Player():
    score = 0;

    def takeletters(self, newletters):
        if len(newletters) == 7:
            self.letters = newletters
        else:
            self.letters.extend(newletters)

    def update_score(self, word):
        val = worddict.get(word)
        self.score = self.score + val
        return val


class Human(Player):
    def print_letters(self):
        print('Διαθέσιμα Γράμματα:', end ="")
        for let in self.letters :
            print(' '+ let + ',' + str(letters.lets.get(let)[1]) + ' -', end ="")
        print('\nΓια αλλαγή γραμμάτων πληκτρολόγησε "p"')
    def play(self):
        self.print_letters()
        print('\nΛέξη:', end =" ")
        word = input()
        if word == 'q':
            return word
        elif word == 'p':
            return word
        elif len(word) == 1:
            print('Πληκτρολόγησε μια ολόκληρη λέξη')
            self.play()
        valid = self.check_word(word)
        if not valid:
            word = self.play()
            return word
        else:
            val = self.update_score(word)
            for i in range(0, len(word)):
                self.letters.remove(word[i])
            print('Αποδεκτή Λέξη - Βαθμοί: ' + str(val) + ' - Σκορ: ' + str(self.score))
            print('Enter για Συνέχεια')
            print('-----------------------------------------------------------')
            input()
        return word
    

    def check_word(self, word):
        remaining = self.letters.copy()
        for i in range(0, len(word)):
            if word[i] in remaining:
                remaining.remove(word[i])
            else:
                print('Χρησιμοποίησε μόνο τα διαθέσιμα γράμματα. Ξαναπροσπάθησε.')
                print('\n')
                return False
        if not(word in worddict):
            print('Η λέξη δεν υπάρχει. Ξαναπροσπάθησε')
            print('\n')
            return False
        return True
        

class Computer(Player):
    level = '1'
    
    def set_level(self, level):
        self.level = level
      
    def print_letters(self):
        print('Γράμματα H/Y:', end ="")
        for let in self.letters :
            print(' '+ let + ',' + str(letters.lets.get(let)[1]) + ' -', end ="")
     
    def play(self):
        self.print_letters()
        word = ""
        if self.level == '3':
            word = self.play_smart()
        elif self.level == '1':
            word = self.play_min()
        elif self.level == '2' :
            word = self.play_max()
            return;
        else :
            print('Παρακαλώ πληκτρολόγησε έναν αριθμό')
            self.setup()
        if word == None:
            print('\nΟ Η/Υ δεν μπορεί να βρει λέξη')
            return False
        val = self.update_score(word)
        for i in range(0, len(word)):
                self.letters.remove(word[i])
        print('\nΛέξη Η/Υ: ' + word + ', Βαθμοί: ' + str(val) + ' - Σκορ Η\Υ: ' + str(self.score))
        print('----------------------------------------------------------')
        return True
            

    def play_min(self):
        word = ""
        for i in range(2, len(self.letters)):
            permutations = itertools.permutations(self.letters, i)
            for p in permutations:
                combo = ''
                for letter in p:
                    combo = combo + letter
                if combo in worddict:
                    word = combo
                    return word
        return None

    def play_max(self):
        word = ""
        i = len(self.letters)
        
        while i > 1:
            permutations = itertools.permutations(self.letters, i)
            for p in permutations:
                combo = ''
                for letter in p:
                    combo = combo + letter
                if combo in worddict:
                    word = combo
                    return word
            i = i -1
        return None
    

    def play_smart(self):
        max_score = 0
        word = ""
        for i in range(2, len(self.letters)+1):
            permutations = itertools.permutations(self.letters, i)
            for p in permutations:
                combo = ''
                for letter in p:
                    combo = combo + letter
                if combo in worddict:
                    score = worddict.get(combo)
                    if score > max_score:
                        max_score = score
                        word = combo
        if word == "":
            return None
        else:
            return word
        


class Game():

    def __init__(self):
        self.human = Human()
        self.computer = Computer()
        self.sak = SakClass()
        self.setup()
        
        
    def setup(self):
        print('*****SCRAMBLE*****\n1: Σκορ\n2: Ρυθμίσεις\n3: Παιχνίδι\nq: Έξοδος')
        choice = input()
        if choice == '1' :
            try:
                with open('data.txt') as json_file:
                    data = json.load(json_file)
                    for p in data['info']:
                        print('ΟΝΟΜΑ: ' + p['NAME'])
                        print('ΣΚΟΡ: ' + p['SCORE'])
                        print('')
            except FileNotFoundError:
                print('Δεν υπάρχουν προηγούμενα σκορ')
            print('----------------------------------------------------------')
            self.setup()
        elif choice == '2' :
            print('Ποιο θες να είναι το επίπεδο του Η/Υ;\n1.MIN(ΕΥΚΟΛΟ)\n2.MAX(ΜΕΤΡΙΟ)\n3.SMART(ΔΥΣΚΟΛΟ)')
            level = input()
            self.computer.set_level(level)
            self.setup()
        elif choice == '3' :
            self.run()
        elif choice == 'q':
            return;
        else :
            print('Παρακαλώ διάλεξε μια έγκυρη επιλογή')
            self.setup()

    def run(self):
        human_letters = self.sak.getletters(7).copy()
        self.human.takeletters(human_letters)
        comp_letters = self.sak.getletters(7).copy()
        self.computer.takeletters(comp_letters)

        while(True):
            print('Στο σακουλάκι: ' + str(len(self.sak.queue)) + ' - Παιζεις:')
            word = self.human.play()
            if word == 'p':
                res = self.sak.getletters(7)
                if res == None:
                    print('Δεν υπάρχουν αρκετά διαθέσιμα γράμματα για να γίνει αλλαγή')
                    self.end()
                    return
                else:
                    new_letters = res.copy()
                    self.sak.putbackletters(self.human.letters)
                    self.human.takeletters(new_letters)
                continue
            elif word == 'q':
                self.end()
                return
            else:
                res = self.sak.getletters(7-len(self.human.letters))
                if res == None:
                    self.end()
                    return
                new_letters = res.copy()
                self.human.takeletters(new_letters)
                    
                if self.computer.play():
                    res = self.sak.getletters(7-len(self.computer.letters))
                    if res == None:
                        self.end()
                        return
                    new_letters = res.copy()
                    self.computer.takeletters(new_letters)
                else:
                    self.end()
                    return

    def end(self):
        print('\nΤο σκορ σου: ' + str(self.human.score) )
        print('Το σκορ του Η\Υ: ' + str(self.computer.score))
        if self.human.score > self.computer.score :
            print('Είσαι ο νικητής!')
        elif self.human.score < self.computer.score :
            print('Έχασες...')
        else:
            print('Ισοπαλία')
        data = {}
        data['info'] = []
        data['info'].append({
            'NAME': 'ΠΑΙΚΤΗΣ',
            'SCORE': str(self.human.score),
        })
        data['info'].append({
            'NAME': 'ΥΠΟΛΟΓΙΣΤΗΣ',
            'SCORE': str(self.computer.score),
        })


        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

        print('----------------------------------------------------------------')
        print('Επόμενος γύρος')
        self.setup()
