import random

def format_hex(num):
    return bytes.fromhex(format(num,'02x'))

def get_frets_in_scale(string, scale):
    if string == '02':
        # Low E
        modifier = 0
    elif string == '04':
        # A
        modifier = -5
    elif string == '08':
        # D
        modifier = -10
    elif string == '10':
        # G
        modifier = -15
    elif string == '20':
        # B
        modifier = -19
    elif string == '40':
        # E
        modifier = -24
    # Repeat scale interval pattern over frets 0 - 48
    frets = scale_intervals[scale] + [fret + 12 for fret in scale_intervals[scale]] + [fret + 24 for fret in scale_intervals[scale]] + [fret + 36 for fret in scale_intervals[scale]]
    # Adjust frets to match string
    adj_frets = [m + modifier for m in frets]
    # Remove negative and frets greater than max_fret
    filtered_frets = [num for num in adj_frets if 0 < num < max_fret]
    return filtered_frets


def random_note():
    duration = random.choice(['04','03','02','01','00','FF','FE'])
    duration = '02'
    string = random.choice(['02','04','08','10','20','40'])
    fret_choices = get_frets_in_scale(string, 'minor arpeggio')
    fret = random.choice(fret_choices)
    fret = format(fret, '02x')
    return '00' + duration + string + '2001' + fret + '000000'

basefile = 'base.gp5'
num_notes_addr = 0x563
start_addr = 0x567
total_notes = 100
max_fret = 18
scale_intervals = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'pentatonic major': [0, 2, 4, 7, 9],
    'blues major': [0, 3, 5, 6, 7, 9],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic minor': [0, 2, 3, 5, 7, 8, 11],
    'pentatonic minor': [0, 3, 5, 7, 10],
    'blues minor': [0, 3, 5, 6, 7, 10],
    'augmented': [0, 3, 4, 7, 8, 11],
    'be-bop': [0, 2, 4, 5, 7, 9, 10, 11],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'whole-half': [0, 2, 3, 5, 6, 8, 9, 11],
    'half-whole': [0, 1, 3, 4, 6, 7, 9, 10],
    'whole tone': [0, 2, 4, 6, 8, 10],
    'augmented fifth': [0, 2, 4, 5, 7, 8, 9, 11],
    'major arpeggio': [0, 4, 7],
    'minor arpeggio': [0, 3, 7],
    'augmented arpeggio': [0, 4, 8],
    'diminished arpeggio': [0, 3, 6, 9]
}

notes = []
for i in range(total_notes):
    notes.append(random_note())
# Convert note list to byte string
all_notes = bytes.fromhex(''.join(notes))

with open(basefile, 'rb') as f:
    content = f.read()
    modified_content = content[:start_addr] + all_notes + content[start_addr:]
    with open('test.gp5', 'wb') as f:
        f.write(modified_content)
        # Write number of notes to file
        f.seek(num_notes_addr)
        f.write(format_hex(len(notes)))