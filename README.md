# Intro to AI - Assignment 2

- ### Problem description:
The task was to create an AI which uses an Evolutionary Algorithm to generate musical accompaniments for a number of input files which contain melodies.

- ### Solution steps:
- The input tracks were first analyzed to find the key used for the melody, determine the number of chords which will be used in the generated accompaniment as well as their length.
- The EA(Evolutionary Algorithm) then randomly generates a number of accompaniments by putting together chords at random from a previously defined pool(more on later). These accompaniments will then be used as the base specimens for the Evolution.
- The specimens then undergo the process of natural selection in order to generate more refined results and provide the most optimal solution to the problem.

- ### The algorithm:
The EA used was a `Genetic Algorithm` as follows:
  - **Population**: The algorithm first generates a population of 100 accompaniments by randomly putting together chords from a pool of predefined chords which fit the previously analyzed criteria(number of cords, key, length of notes) from the original melody.
  - **Variation Operators**: The algorithm then chooses 2 members of the population at random, but uses weights which will make members with the highest `Fitness` more likely candidates to be used for reproduction. These 2 candidates will then be used to create future generations using 2 operators.
    - **Crossover**: Which takes the `Genomes` (which are notes in our case) of the 2 candidates and chooses a cutting point at random. The Genomes of the 2 candidates will then be swapped at that point to create new accompaniments. The previous technique, however, limits our sample pool to only a few chords which have been used in the 2 original members of the population. The next technique is used in conjunction with the previous to overcome the limitation.
    - **Mutation**: Mutation then swaps out one chord at random from each result of the `Crossover` to introduce new genes and guarantee that our population maintains a certain amount of variety, which is necessary in the process of finding the best solutions possible.
    - **Elitism**: The new population consists of the newly generated accompaniments as well as 2 of the best performing members of the previous generation.
  -  **Stopping Criteria**: The generation stops after a number of generations which is given manually to the program. 200 proved to be a good number for most cases.
 - The `Fitness Function`: The function used to determine the competence of members of the population. The function gives `points` to accompaniments according to the following criteria:
    - Accompaniments gain points for using notes that were present in the original melody in its corresponding chord.
    - Accompaniments lose points for committing `Dissonance`, that is, playing 2 or more notes which cause a "harsh" sound and a feeling of tension when played together.

- ### Music:
- A number of predefined chords was used for the generation, namely:
  - Major and Minor Triads.
  - First and second inversions of Major and Minor Triads.
  - Diminished chords.
- The chords were taken from a number of popular keys stored in the program.

- ### Tech:
The program was written in `Python` and uses a number of libraries to assist in finding the solution.

- ### Requirements:
  - Python 3.10.2
  - Python libraries:
    - `typing` used for technical necessities.
    - `random` used for the generation of samples.
    - `math` used for... math.
    - `mido` used to manipulate and generate `.mid` files.
    - `music21` used to find the key used in the given melody.
  - Most of the libraries used are standard python packages. The libraries related to music can be installed by running:

        pip3 install mido
        pip3 install music21

- ### Acknowledgements:
The code for the Genetic Algorithms was inspired by a template written by *kiecodes* which can be found at the following link:

  https://github.com/kiecodes/genetic-algorithms/blob/master/algorithms/genetic.py

- ### Contact info:
      Author: Jaffar Totanji
      E-mail: j.totanji@innopolis.university
      Telegram: @KuroHata7
