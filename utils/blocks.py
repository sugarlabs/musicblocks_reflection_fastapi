blocks = {   
    "Start Block" : "Each Start block is a separate voice. All of the Start blocks run at the same time when the Play button is pressed.",
    "Settimbre" : "The Set instrument block selects a voice for the synthesizer, eg guitar piano violin or cello.",
    "Action" : "The Action block is used to group together blocks so that they can be used more than once. It is often used for storing a phrase of music that is repeated.",
    "Note" : "The Note block is a container for one or more Pitch blocks. The Note block specifies the duration (note value) of its contents.",
    "Pitch" : "The Pitch block specifies the pitch name and octave of a note that together determine the frequency of the note.",
    "Wrap" : "The Wrap block enables or disables screen wrapping for the graphics actions within it.",
    "Set Master BPM" : "The Master beats per minute block sets the number of 1/4 notes per minute for every voice.",
    "Arc" : "The Arc block moves the turtle in an arc.",
    "Move Forward" : "The Forward block moves the mouse forward.",
    "Move Backward" : "The Backward block moves the mouse backward.",
    "Setxy" : "The Set XY block moves the mouse to a specific position on the screen."   
}

def findBlockInfo(message):
    present_blocks = ""
    for block in blocks:
        if block in message:
            present_blocks += (f"{block} : {blocks[block]}\n")
    
    return present_blocks