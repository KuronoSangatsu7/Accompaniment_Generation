from typing import List, Tuple
from random import *
import mido
import random
import math
import music21

#Some global variables to be used later on
Genome = List[int]
Population = List[Genome]
tpb = 0
note_indexes = []
beats = 0
input_track = mido.MidiTrack()

#Differences between notes which cause Dissonance
dissonance_diff = [1, 2, 6, 10, 11]

keys = ['C# minor', 'D minor', 'F major', 'E minor']

#Some popular keys to be used later on
key_dict = {
    'C# minor' : [25, 27, 28, 30, 32, 33, 35],
    'D minor' : [26, 28, 29, 31, 33, 34, 36],
    'F major' : [29, 31, 33, 34, 36, 38, 40],
    'E minor' : [28, 30, 31, 33, 35, 36, 38]
}

#Functions to generate random chords from the previous list of keys
def generate_major_chord(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start)
    chord.append(start + 4)
    chord.append(start + 7)

    return chord

def generate_first_inversion_major_triad(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start + 4)
    chord.append(start + 7)
    chord.append(start + 12)

    return chord

def generate_second_inversion_major_triad(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start + 7)
    chord.append(start + 12)
    chord.append(start + 16)

    return chord

def generate_minor_chord(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start)
    chord.append(start + 3)
    chord.append(start + 7)

    return chord

def generate_first_inversion_minor_triad(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start + 3)
    chord.append(start + 7)
    chord.append(start + 12)

    return chord

def generate_second_inversion_minor_triad(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start + 7)
    chord.append(start + 12)
    chord.append(start + 15)

    return chord

def generate_diminished_chord(start: int) -> List:
    chord = []
    start = start + 12
    chord.append(start)
    chord.append(start + 3)
    chord.append(start + 6)

    return chord

#A function to generate a random chord given a key using the functions above
def generate_chord(music_key: str) -> Genome:
    rand_start = random.randint(0, 6)
    generated_chord = []

    if 'minor' in music_key and rand_start == 1:
        generated_chord = generate_diminished_chord(key_dict[music_key][rand_start])
    elif 'major' in music_key and rand_start == 7:
        generated_chord = generate_diminished_chord(key_dict[music_key][rand_start])
    else:
        rand_major_minor = random.randint(0, 5)
        if rand_major_minor == 0:
            generated_chord = generate_major_chord(key_dict[music_key][rand_start])
        elif rand_major_minor == 1:
            generated_chord = generate_minor_chord(key_dict[music_key][rand_start])
        elif rand_major_minor == 2:
            generated_chord = generate_first_inversion_major_triad(key_dict[music_key][rand_start])
        elif rand_major_minor == 3:
            generated_chord = generate_first_inversion_minor_triad(key_dict[music_key][rand_start])
        elif rand_major_minor == 4:
            generated_chord = generate_second_inversion_major_triad(key_dict[music_key][rand_start])
        else:
            generated_chord = generate_second_inversion_minor_triad(key_dict[music_key][rand_start])

    return generated_chord

#Generates a genome (The number of chords suitable for the track) using the previous function
def generate_genome(music_key: str, no_of_chords: int) -> Genome:
    final_chords = []

    for i in range(no_of_chords):
        final_chords.extend(generate_chord(music_key))
    
    return final_chords

#Generates a number of genomes
def populate(size: int, music_key: str, no_of_chords: int) -> Population:
    return [generate_genome(music_key, no_of_chords) for i in range(size)]
    
#Checks the given genome for dissonance with the melody track
def check_dissonance(genome: Genome, track: mido.MidiTrack) -> int:
    ret = 0
    relevant_notes = [None] * beats
    dtime = 0
    for message in track:
        if message.is_meta or message.type == 'program_change':
            continue
        dtime += message.time
        if message.type == 'note_on':
            if dtime % tpb == 0:
                relevant_notes[int(dtime / tpb)] = message.note

    j = 0
    i = 0
    while i < len(relevant_notes):
        if relevant_notes[i] is None:
            i += 2
            j += 3
            continue
        if abs(relevant_notes[i]%12 - genome[j]%12) in dissonance_diff or abs(relevant_notes[i]%12 - genome[j+1]%12) in dissonance_diff or abs(relevant_notes[i]%12 - genome[j+2]%12) in dissonance_diff:
            ret += 1
        
        j += 3
        i += 2

    return ret

#Checks the given genome for notes that are similar to the corresponding notes in the melody
def check_similar_notes(genome: Genome, track: mido.MidiTrack) -> int:
    ret = 0
    relevant_notes = [None] * beats
    dtime = 0
    for message in track:
        if message.is_meta or message.type == 'program_change':
            continue
        dtime += message.time
        if message.type == 'note_on':
            if dtime % tpb == 0:
                relevant_notes[int(dtime / tpb)] = message.note

    j = 0
    i =0
    while i < len(relevant_notes):
        if relevant_notes[i] is None:
            i += 2
            j += 3
            continue
        if relevant_notes[i]%12 == genome[j]%12 or relevant_notes[i]%12 == genome[j+1]%12 or relevant_notes[i]%12 == genome[j+2]%12:
            ret += 1
        
        j += 3
        i += 2

    return ret

#The fitness function which uses the 2 functions above to determine the fitness of a given genome
def fitness(genome: Genome) -> int:
    score = 1000
    score -= check_dissonance(genome, input_track) * 10
    score += check_similar_notes(genome, input_track) * 5
    return score

#Selects a pair of genomes from the population at random with a higher probability given to genomes with higher fitness
def selection_pair(population: Population) -> Population:
    return choices(
        population = population,
        weights = [fitness(genome) for genome in population],
        k = 2
    )

#Performs the crossover operation as described in the report
def crossover(first_genome: Genome, second_genome: Genome) -> Tuple[Genome, Genome]:
    cut = 1
    while cut%3 !=0:
        cut = randint(1, len(first_genome)-1)
    return first_genome[0:cut] + second_genome[cut:], second_genome[0:cut] + first_genome[cut:]

#Performs mutation as described in the report
def mutate(genome: Genome, music_key: str) -> Genome:
    mutation_point = 1
    while mutation_point%3 != 0:
        mutation_point = random.randint(0, len(genome) - 3)
    
    gene = generate_chord(music_key)

    genome = genome[0: mutation_point] + gene + genome[mutation_point + 3 :]

    return genome

#The main loop for the evolution procedure which stops at the given limit and returns the last generation with the best performance
def run_evolution(limit: int, key: str, no_of_chords: int) -> Population:

    population = populate(100, key, no_of_chords)

    for i in range(limit):
        population = sorted(
            population,
            key = lambda genome: fitness(genome),
            reverse = True
        )

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population)
            offspring_a, offspring_b = crossover(parents[0], parents[1])
            offspring_a = mutate(offspring_a, key)
            offspring_b = mutate(offspring_b, key)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(
            population,
            key = lambda genome: fitness(genome),
            reverse = True
        )
    
    return population

#Generates a MIDI track given a list of notes
def generate_track(music: List) -> mido.MidiTrack:
    track = mido.MidiTrack()
    meta = mido.MetaMessage('track_name', name = 'Elec. Piano (Classic)', time=0)
    first_message = mido.Message('program_change', channel = 0, program = 0, time = 0)
    track.append(meta)
    track.append(first_message)

    ite = 0
    while ite < len(music) - 2:

        chord = []

        chord.append(mido.Message('note_on', note = music[ite], time = 0))
        chord.append(mido.Message('note_on', note = music[ite + 1], time = 0))
        chord.append(mido.Message('note_on', note = music[ite + 2], time = 0))

        chord.append(mido.Message('note_off', note = music[ite], time = tpb * 2))
        chord.append(mido.Message('note_off', note = music[ite + 1], time = 0))
        chord.append(mido.Message('note_off', note = music[ite + 2], time = 0))

        for msg in chord:
            track.append(msg)

        ite = ite + 3

    return track

#The main loop of the porgram
def init():
    mid = mido.MidiFile('input3.mid', clip = True)

    global input_track
    input_track = mid.tracks[1]

    #Calulcating the number of beats to determine the number of chords to be in the accompaniment
    dtime = 0
    for msg in mid.tracks[1]:
        if msg.is_meta or msg.type == 'program_change':
            continue
        dtime = dtime + msg.time

    global tpb 
    tpb = mid.ticks_per_beat
    
    global beats
    beats = math.ceil(dtime/tpb)

    no_of_chords = beats
    no_of_chords = math.ceil(no_of_chords/2)

    #Finding the key of the melody
    score = music21.converter.parse('input3.mid')
    key_details = score.analyze('key')
    key = key_details.tonic.name + ' ' + key_details.mode

    population = run_evolution(200, key, no_of_chords)

    track = generate_track(population[0])

    mid.tracks.append(track)

    mid.save('JaffarTotanjiOutput3.mid')

init()
