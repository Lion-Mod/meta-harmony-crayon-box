from classes.Part import Part
from PIL import Image, ImageDraw


# Define the colors corresponding to the strings
color_mapping = {
    'p': (128, 0, 128),  # Purple
    'g': (0, 255, 0),    # Green
    'o': (255, 165, 0),  # Orange
    'r': (255, 0, 0),    # Red
    'b': (0, 0, 255),    # Blue
    'y': (255, 255, 0)   # Yellow
}


# All chords in each major key (including enharmonic equivalent)
major_key_cubes = {
    'C' : ['Cmaj', 'Dmin', 'Emin', 'Fmaj', 'Gmaj', 'Amin', 'Bdim'],

    'C# / Db' : ['C#maj', 'D#min', 'Fmin', 'F#maj', 'G#maj', 'A#min', 'B#dim',
                 'Dbmaj', 'Ebmin',         'Gbmaj', 'Abmaj', 'Bbmin', 'Cdim'],

    'D' : ['Dmaj', 'Emin', 'F#min', 'Gmaj', 'Amaj', 'Bmin', 'C#dim',
                           'Gbmin',                         'Dbdim'],

    'D# / Eb' : ['D#maj', 'Fmin', 'Gmin', 'Abmaj', 'Bbmaj', 'Cmin', 'Ddim',
                 'Ebmaj',                 'G#maj', 'A#maj'],

    'E' : ['Emaj', 'F#min', 'G#min', 'Amaj', 'Bmaj', 'C#min', 'D#dim',
                   'Gbmin', 'Abmin',                 'Dbmin', 'Ebdim'],

    'F' : ['Fmaj', 'Gmin', 'Amin', 'Bbmaj', 'Cmaj', 'Dmin', 'Edim',
                                   'A#maj'],
    
    'F# / Gb' : ['F#maj', 'G#min', 'A#min', 'Bmaj', 'C#maj', 'D#min', 'E#dim',
                 'Gbmaj', 'Abmin', 'Bbmin',         'Dbmaj', 'Ebmin', 'Fdim'],
    
    'G' : ['Gmaj', 'Amin', 'Bmin', 'Cmaj', 'Dmaj', 'Emin', 'F#dim',
                                                           'Gbdim'],

    'G# / Ab' : ['Abmaj', 'Bbmin' ,'Cmin', 'Dbmaj', 'Ebmaj', 'Fmin' ,'Gdim',
                 'G#maj', 'A#min'          'C#maj', 'D#maj'],

    'A' : ['Amaj', 'Bmin', 'C#min', 'Dmaj', 'Emaj', 'F#min', 'G#dim',
                           'Dbmin',                 'Gbmin', 'Abdim'],

    'A# / Bb' : ['Bbmaj', 'Cmin', 'Dmin', 'Ebmaj', 'Fmaj', 'Gmin', 'Adim',
                 'A#maj',                 'D#maj'],

    'B' : ['Bmaj', 'C#min', 'D#min', 'Emaj', 'F#maj', 'G#min', 'A#dim',
                   'Dbmin', 'Ebmin',         'Gbmaj', 'Abmin', 'Bbdim']
}

 
# TODO
# dorian
# phrygian
# lydian
# mixolydian
# other modes...


# Corresponding alphacube colours, this helps with identifying each chords harmonic function
alphacube_colours = {
    'C' : 'o',
    'C#' : 'p',
    'Db' : 'g',
    'D' : 'g',
    'D#' : 'o',
    'Eb' : 'o',
    'E' : 'p',
    'F' : 'g',
    'F#' : 'o',
    'Gb' : 'o',
    'G' : 'p',
    'G#' : 'g',
    'Ab' : 'g',
    'A' : 'o',
    'A#' : 'p',
    'Bb' : 'p',
    'B' : 'g'
}


class Song():
    """
    Stores data for the Song.

    This class initializes a Song object with a song name, artist name, and a dictionary
    representing the song's parts and chords in each part. It creates a list of Part objects based on
    the provided song structure and chords.

    The structure is Song has multiple Parts. Each Part has multiple ColouredChords

    Attributes:
        song_name (str): The name of the song.
        artist_name (str): The name of the artist who performed the song.
        song_structure_and_chords (dict): A dictionary representing the song structure and chords. 
        The keys of the dictionary are part names e.g. 'intro', and the values are lists of raw chord names for each part.

    Properties:
        parts (list): A list of Part objects created based on the song structure and chords.
    """

    def __init__(self, song_name, artist_name, song_structure_and_chords):
        self.song_name = song_name
        self.artist_name = artist_name
        self.parts = [Part(name = part_name, raw_chords = chords_of_part) for part_name, chords_of_part in song_structure_and_chords.items()]        


    def get_chord_colours(self):
        """
        Get all the chord colours (and any extension colours) for each part e.g. ['o', 'o', 'o', 'o'] is a part of a song with 4 orange chords
        """
        song_chord_colours = []

        for p in self.parts:
        
            part_chord_colours = []
            
            for c in p.coloured_chords:
                part_chord_colours.append([c.chord_colour, c.extension_one_colour, c.extension_two_colour, c.extension_three_colour])
            
            song_chord_colours.append(part_chord_colours)
        
        return song_chord_colours


    def get_chords(self):
        """
        Get all the chords
        """
        song_chords = []

        for p in self.parts:
        
            part_chords = []
            
            for c in p.coloured_chords:
                part_chords.append(c.chord)
            
            song_chords.append(part_chords)
        
        return song_chords


    def get_most_likely_major_key_cube_per_part(self):
        """
        Get the most likely major key cube of each part of the Song given the chords E.g. ['Cmaj', 'Dmin', 'Emin'] is most likely C major
        """
        chords_in_parts = self.get_chords()

        for chords_in_part in chords_in_parts:
            for mode, key_cubes in zip(['major keys'], [major_key_cubes]):
                
                # Dictionary to store the count for each key_cube a chord is in
                counts = {}  
                
                # For each chord see which keys it falls in e.g. Cmaj is in Cmaj (or Amin), Fmaj (or Dmin), Gmaj
                for chord in chords_in_part:
                    for key_cube, chords_in_key_cube in key_cubes.items():
                        if chord in chords_in_key_cube:
                            counts[key_cube] = counts.get(key_cube, 0) + 1
                
                # Get the most likely keys but taking the keys that had the most chords
                most_likely_keys = [lst_name for lst_name, count in counts.items() if count == max(counts.values())]
                
                # Get the most likely keys with their alphacube colours
                most_likely_keys_with_colours = {key: alphacube_colours[key] for key in alphacube_colours if key in most_likely_keys}
             
                print(mode)
                print(counts)
                print(most_likely_keys_with_colours)


    def create_coloured_chords_image(self):
        """
        Creates an image of a song's chords with the appropriate Meta Harmony colours
        """
        song_chord_colours = self.get_chord_colours()

        image_width = 150 * 3
        image_height = 50 * max(len(part_chord_colours) for part_chord_colours in song_chord_colours)
        square_width = 25

        # Create a new image with a white background that the coloured chords will be drawn on
        image = Image.new('RGB', (image_width, image_height), 'white')
        draw = ImageDraw.Draw(image)

        # Initialise y and section number to assist with correct formatting
        y = 0
        section_number = 0

        # Create squares for each section's chords and colour it with the secondary colour appropriately
        for coloured_section in song_chord_colours:

            # Get the main chord colour and the extension colours
            chord_main_colours = [chord[0] for chord in coloured_section]
            first_extension_colours = [chord[1] for chord in coloured_section]
            second_extension_colours = [chord[2] for chord in coloured_section]
            third_extension_colours = [chord[3] for chord in coloured_section]
    
            # The 3 variables below ensure chords are drawn correctly
            chord_number_in_section = 0
            section_number += 1
            number_of_chords_in_sections = len(coloured_section)

            # Output each chord's colours as a square one at a time
            for (chord_main_colour, first_extension_colour, 
                second_extension_colour, third_extension_colour) in zip(chord_main_colours, first_extension_colours, 
                                                                        second_extension_colours, third_extension_colours):

                # Set the correct x origin
                x_origin = (chord_number_in_section % 4) * square_width

                # Get the chord RGB colour (if not know then default to black) and draw the chord as a square
                chord_main_colour = color_mapping.get(chord_main_colour, (0, 0, 0))
                draw.rectangle((x_origin, y, x_origin + square_width, y + square_width), fill = chord_main_colour)
                
                # Add the colours of the extensions (if applicable) as a smaller rectangle within the main chord's square
                for i, extension_colour in enumerate([first_extension_colour, second_extension_colour, third_extension_colour], start = 1):
                    if extension_colour != '':
                        extension_colour = color_mapping.get(extension_colour, (0, 0, 0))
                        draw.rectangle((x_origin + square_width * (i - 1) / 3, y,
                                        x_origin + square_width * i / 3, y + square_width / 4), fill = extension_colour)
                    else:
                        AssertionError(f'Colouring extensions failed on extension number {i}')

                # Add one to the chord counter to ensure formatting of chords being drawn is correct
                chord_number_in_section += 1
                
                # When 4 chords have been drawn increase y (new line) and reset chord_number_in_section i.e. new line of chords
                if (chord_number_in_section % 4 == 0 and chord_number_in_section != 0) or (number_of_chords_in_sections == chord_number_in_section):
                    y += square_width

            # After each section of the song reset the y to create a gap
            y += square_width

        return image