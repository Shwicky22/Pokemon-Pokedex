###########################################################

    #  Computer Project #8
    #
    #  Open an input file and read it
    #   Call function to get data from csv and put it into a dictionary
    #       Inner dictionary will be every generation
    #           inner value will be dictionary types from specified input
    #               inner value will be dictionary of pokemon names
    #                   inner value will be list of pokemon data
    #       Return sorted dictionary of dictionary of dictionary of list(Pokedex)
    #    find_pokemon function
    #           loops through pokedex
    #           Finds pokemon that are in the user input set
    #    display pokemon function takes data from user and displays all pokemon that are specified
    #    find pokemon from abilities function
    #          loops through pokedex
    #          finds all pokemon who have specified ability
    #    find matchups pokemon
    #           loops through pokedex and finds pokemon effectivness
    #           then finds oppisite pokemon effectivness and returns tuple
    # loop through main until option is chosen correctly
    #      if no function is called display error message til one is
    #    display closing message

    ###########################################################
import csv, copy
from typing import List, Any

poke_types = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal',
'poison', 'psychic', 'rock', 'steel', 'water']
EFFECTIVENESS = {0.25: "super effective", 0.5: "effective", 1: "normal", 2: "weak", 4: "super weak", 0: "resistant"}
MATCHUP_TYPES = {"resistant", "super effective", "effective", "normal",
                 "weak", "super weak"}
PROMPT = '''
\nTo make a selection, please enter an option 1-3:\n
\tOPTION 1: Find Pokemon
\tOPTION 2: Find Pokemon From Abilities
\tOPTION 3: Find Matchups
\nEnter an option: '''


def open_file(s):
    ''' Opens the file and checks directory if a file is there if not displays error message'''
    file = True
    while file == True:  # Creates initial boolean to tell if file is correct
        txt = input('Please enter a {} filename: '.format(s))
        try:  # initates loop to check if true
            fp = open(txt,encoding="utf-8")
            return fp
        except FileNotFoundError:  # creates a invalid output if filenotfound error pops up
            print('This {} file does not exist. Please try again.'.format(s))


def read_file(fp):
    """This function reads the csv file line by line and puts the data into a dictionary where its kays are
    generations of pokemons and its values are dictionaries of types where its values are dictionaries of pokemon names
     where its values are a list made up of effectivness dictionary and pokemon stats"""
    reader = csv.reader(fp)
    fp.readline() # reads header
    pokedex = {} # initalizes pokedex
    reader_list = []
    for i in  reader:
        reader_list.append(i)
        if i[39] not in pokedex:
            pokedex[i[39]] = {}
        if i[37] == '':
            if (i[36],None) not in pokedex[i[39]]:
                pokedex[i[39]][(i[36], None)] = {}
                pokedex[i[39]][(i[36], None)][i[30]] = []
            else:
                pokedex[i[39]][(i[36], None)][i[30]] = []
        else:
            if (i[36],i[37]) not in pokedex[i[39]]:
                pokedex[i[39]][(i[36], i[37])] = {}
                pokedex[i[39]][(i[36], i[37])][i[30]] = []
            else:
                pokedex[i[39]][(i[36], i[37])][i[30]] = []

        count = -1
        stats = i[1:19]
        effectivness = {"super effective": None, "effective": None , "normal": None, "weak": None,"super weak": None, "resistant": None}

        sup_eff = set()
        eff = set()
        norm = set()
        weak = set()
        sup_weak = set()
        res = set()
        for x in stats:
            count += 1
            if x == '0.25':
                 sup_eff.add(poke_types[count])
                 effectivness['super effective'] = sup_eff
            if x == '0.5':
                eff.add(poke_types[count])
                effectivness["effective"] = eff
            if x == '1':
                norm.add(poke_types[count])
                effectivness["normal"] = norm
            if x == '2':
                weak.add(poke_types[count])
                effectivness["weak"] = weak
            if x == '4':
                sup_weak.add(poke_types[count])
                effectivness["super weak"] = sup_weak
            if x == '0':
                res.add(poke_types[count])
                effectivness["resistant"] = res
        for z,y in effectivness.items():
            if y == None:
                effectivness[z] = (set)

        ability = set()
        abilities = i[0].strip('[]').replace("'",'').split(',')
        for t in abilities:
            ability.add(t.strip())
        if i[37] == '':
            pokedex[i[39]][(i[36], None)][i[30]].append(effectivness)
            pokedex[i[39]][(i[36], None)][i[30]].append(ability)
            pokedex[i[39]][(i[36], None)][i[30]].append(int(i[28]))
            pokedex[i[39]][(i[36], None)][i[30]].append(int(i[23]))
            pokedex[i[39]][(i[36], None)][i[30]].append(float(i[38]))
            pokedex[i[39]][(i[36], None)][i[30]].append(int(i[35]))
            pokedex[i[39]][(i[36], None)][i[30]].append(bool(int(i[40])))
        else:
            pokedex[i[39]][(i[36], i[37])][i[30]].append(effectivness)
            pokedex[i[39]][(i[36], i[37])][i[30]].append(ability)
            pokedex[i[39]][(i[36], i[37])][i[30]].append(int(i[28]))
            pokedex[i[39]][(i[36], i[37])][i[30]].append(int(i[23]))
            pokedex[i[39]][(i[36], i[37])][i[30]].append(float(i[38]))
            pokedex[i[39]][(i[36], i[37])][i[30]].append(int(i[35]))
            pokedex[i[39]][(i[36], i[37])][i[30]].append(bool(int(i[40])))


    return pokedex


def find_pokemon(pokedex, names):
    """This function takes a set of pokemon names and searches through the pokedex and returns the data for each pokemon given"""
    dis = {}
    for i in pokedex:
        for x in pokedex[i]:
            for y in pokedex[i][x]:
                if y in names:
                    pokemon = pokedex[i][x][y]
                    dis[y] = [pokemon[1],pokemon[2],pokemon[3],pokemon[4],pokemon[5],pokemon[6],int(i),x]
    return dis




def display_pokemon(name, info):
    """Display takes the data from find pokemon and displays it for each pokemon given"""
    dis = ''
    pokemon = info
    if pokemon[7][1] == None:
        types = '\n\tTypes: ' + pokemon[7][0]
    else:
        types = '\n\tTypes: ' + pokemon[7][0] + ', ' +  pokemon[7][1]
    abilities = list(pokemon[0])
    abilities.sort()
    gen = '\n\tGen: ' + str(pokemon[6])
    abil = '\n\tAbilities: ' + ', '.join(str(i) for i in abilities)
    HP = '\n\tHP: ' + str(pokemon[1])
    cap = '\n\tCapture Rate: ' +  str(pokemon[2])
    weight = '\n\tWeight: ' +  str(pokemon[3])
    speed = '\n\tSpeed: '+ str(pokemon[4])
    if pokemon[5] == False:
        leg = '\n\tNot Legendary'
    else:
        leg = '\n\tLegendary'
    dis = '\n' + name + gen + types + abil + HP + cap + weight + speed + leg
    return dis

def find_pokemon_from_abilities(pokedex, abilities):
    """This function takes abilities from user and finds all the poemon who use those abilities returns set of pokemon names"""
    poke = set()
    for i in pokedex:
        for x in pokedex[i]:
            for y in pokedex[i][x]:
                    abil = pokedex[i][x][y][1]
                    if abilities.issubset(abil):
                        poke.add(y)
    return poke


def find_matchups(pokedex, name, matchup_type):
    """This function takes the effectivness given by user and determines which pokemon is best suited for matchups against one another and returns a set of pokemon"""
    if matchup_type not in MATCHUP_TYPES:
        return None
    types = set()
    matchups = []
    for i in pokedex:
        for x in pokedex[i]:
            for y in pokedex[i][x]:
                if name == y:
                    effect = pokedex[i][x][y][0]
                    types = effect[matchup_type]
                    continue
    if types == set():
        return None
    else:
        for n in pokedex:
            for m in pokedex[n]:
                for l in pokedex[n][m]:
                    if m[0] in types:
                        if m[1] != None:
                            matchups.append((l, (m[0], m[1])))
                        else:
                            matchups.append((l, (m[0],)))
                    if m[1] in types:
                        matchups.append((l, (m[0], m[1])))
        matchups.sort()
        return matchups

def main():
    print("Welcome to your personal Pokedex!\n")
    fp = open_file("pokemon")
    pokedex = read_file(fp)
    usr_input = input(PROMPT)
    while usr_input.lower() not in ('1','2','3','4','q'):
        print('Invalid option {}'.format(usr_input))
        usr_input = input(PROMPT)
    while usr_input.lower() != 'q':
        if usr_input == '1':
            poke_input = input("\nEnter a list of pokemon names, separated by commas: ")
            poke_names = [i.strip() for i in poke_input.split(',')]
            lol = find_pokemon(pokedex,set(poke_names))
            poke_list = []
            for x,y in lol.items():
                poke_list.append((x,y))
            for k,v in sorted(poke_list):
                print(display_pokemon(k,v))
        if usr_input == '2':
            abilities = input('Enter a list of abilities, separated by commas: ')
            list_abil = [i.strip() for i in abilities.split(',')]
            lol = find_pokemon_from_abilities(pokedex,set(list_abil))
            pokemon = list(lol)
            pokemon.sort()
            print("Pokemon: " + ', '.join(pokemon))
        if usr_input == '3':
            poke_name = input("Enter a pokemon name: ")
            matchup = input('Enter a matchup type: ')
            matchups = find_matchups(pokedex,poke_name,matchup)
            if matchups == None:
                print('Invalid input')
            else:
                for i in matchups:
                    if len(i[1]) == 2:
                        print(i[0] + ': ' + i[1][0] + ', ' + i[1][1])
                    else:
                        print(i[0] + ': ' + i[1][0])
        usr_input = input(PROMPT)
        if usr_input.lower() == 'q':
            break
        while usr_input.lower() not in ('1', '2', '3', '4', 'q'):
            print('Invalid option {}'.format(usr_input))
if __name__ == "__main__":
    main()