import streamlit as st
from classes.Song import Song
from annotated_text import annotated_text, annotation


# A colour mapping to get colours working in Streamlit annotated text
colour_mapping = {'o' : 'orange',
                 'p' : 'purple',
                 'g' : 'green',
                 'r' : 'red',
                 'y' : 'yellow',
                 'b' : 'blue'}

def get_song_parts(user_input):
    """
    Takes the user's input and gets the song parts

    Intro
    Cmaj7 Dmin7 Emin7

    Chorus
    Cmaj7 Dmin9 Emaj7
    
    The output to this would be ['Intro\nCmaj Dmin7 Emin7', 'Chorus\nCmaj7 Dmin9 Emaj7']
    """
    song_parts = user_input.split('\n\n')
    return [song_part.strip() for song_part in song_parts if song_part.strip()]


def get_song_part_names(input_text):
    """
    Takes the user's input and gets the song part names

    Intro
    Cmaj7 Dmin7 Emin7

    Chorus
    Cmaj7 Dmin9 Emaj7
    
    The output to this would be ['Intro', 'Chorus']
    """
    song_parts = input_text.split('\n\n')
    return [song_part.strip().split('\n', 1)[0] for song_part in song_parts if song_part.strip()]


def process_user_input_to_dictionary(user_input):
    """
    Takes the user's input over multiple lines and creates the appropriate format ready for processing and chord colouring

    Example
    Cmaj7 Dmin7 Emin7
    Amaj9/#11

    Example output
    {'Section 1' : ['Cmaj7', 'Dmin7', 'Emin7'],
     'Section 2' : ['Amaj9/#11']}
    """
    # Split the users input into each line and remove the name of the input
    user_input_split_per_line = user_input.splitlines()[1:]
    
    # Convert each line into a list of chords
    lists_of_chords = [chords_in_line.split() for chords_in_line in user_input_split_per_line]

    # Take each list of chords and store them in a dictionary, each key is a section for the song
    processed_input_as_dictionary = {
        'Section ' + str(section_number + 1): collection_of_bars 
        for section_number, collection_of_bars in enumerate(lists_of_chords)
    }

    return processed_input_as_dictionary


def get_top_border_colour(chord_colour, first_extension_colour):
    """
    Get the correct top border colour. If there is no first extension colour then default to the chord's colour
    """
    if first_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[first_extension_colour]}'


def get_bottom_border_colour(chord_colour, second_extension_colour):
    """
    Get the correct bottom border colour. If there is no second extension colour then default to the chord's colour
    """
    if second_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[second_extension_colour]}'


def get_right_border_colour(chord_colour, third_extension_colour):
    """
    Get the correct right border colour. If there is no third extension colour then default to the chord's colour
    """
    if third_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[third_extension_colour]}'


## START OF THE STREAMLIT APP ##

# App title
st.title('Meta Harmony Crayon Box 🖍️')

# Example input being displayed to the user
example_input = "Intro\nCmaj7 Emin Dmin Ddom7\nCmaj7 Dmin Gdom7/#9\n\nVerse\nAmin Gmin7 Dmin9"
st.subheader("Here's an example input")
st.code(example_input, language = 'python')

# Show the example input and get the user input 
st.subheader('Input the composition of the track similar to the above example and hit "Ctrl+Enter or Cmd+Enter" to colour the chords')
song = st.text_area("Note : this app doesn't handle add, augmented or chords such as C5, C6. If you want to use your chords you can add 'maj' to the chords to get them to display.",
                    value = example_input, height = 250)


# Output the song with Meta Harmony colors if there is a song input
if song is not None:

    # Get the user-defined song parts and their names
    song_parts = get_song_parts(song)
    song_part_names = get_song_part_names(song)

    for song_part, song_part_name in zip(song_parts, song_part_names):

        # Output part name e.g. Chorus
        f"#### {song_part_name}"

        try:
            # Clean up user's chords for the song_part
            cleaned_chords = process_user_input_to_dictionary(song_part)
            s = Song(song_name = '', artist_name = '', song_structure_and_chords = cleaned_chords)
        except BaseException:
            st.error("The chord format isn't correct or the input isn't appropriate. It must match the above example.")

        # Display the chords for each part with their appropriate Meta Harmony colors
        for chords, colours_of_chords in zip(s.get_chords(), s.get_chord_colours()):
            # Separate chord colors into individual lists
            chord_main_colours, first_extension_colours, second_extension_colours, third_extension_colours = zip(*colours_of_chords)

            # Create a block of text to represent the chords in the part
            chords_as_text = []

            # Display each chord and its colors appropriately
            for chord, main_color, ext_color1, ext_color2, ext_color3 in zip(chords, chord_main_colours,
                                                                            first_extension_colours, second_extension_colours,
                                                                            third_extension_colours):
                chords_as_text.append(
                    annotation(chord, '', font_family = 'Arial', background = colour_mapping[main_color],
                               border_top = get_top_border_colour(main_color, ext_color1),
                               border_bottom = get_bottom_border_colour(main_color, ext_color2),
                               border_right = get_right_border_colour(main_color, ext_color3), color = 'white'))

            annotated_text(chords_as_text)