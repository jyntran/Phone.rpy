###
#   Phone.rpy
#   Message framework with flag system 
#   
#   _script   
#     
###

init:
    image black = "#000"
    image white = "#fff"
    image red = "#f00"
    image green = "#0f0"

init python:

    nameA = "Alice"
    nameB = "Brandon"
    a = Character(nameA)
    b = Character(nameB)

label start:

    ###
    #   Phone
    ###
    python:
    
        # Set start time
        time = Time(0,0)

        # Instantiate the phone and contacts
        phone = Phone()
        contactA = Contact(nameA)
        contactB = Contact(nameB)
        

        # Game flags
        flags = set()

        # Replies sent
        replies = set()

        # Message queue   
        messages = []
        

        # Messages
        #   These will be received when receive() is called.

        # A message with no reply
        queue_message(contactB, "Hey!")


    ###
    #   BEGIN
    ###

    scene black

menu table_of_contents:
    "Please select a section to read about."
    "Debug":
        jump tutorial_debug
    "Screens":
        jump tutorial_screens
    "Flags and Points":
        jump tutorial_flags
    "Messages":
        jump tutorial_messages


label tutorial_debug():

    "In Phone.rpy, there is a screen called Phone_Debug()."
    show screen Phone_Debug
    "It's recommended to keep this open as you go through this tutorial."
    "Feel free to use it while you develop, and add more variables to it to watch."

    jump table_of_contents


label tutorial_screens():

    "First, let's open the Phone screen."
    show screen Phone
    "You can open the phone screen by clicking on 'Show Phone' in the quick menu (bottom right)."
    "Phone() is the main screen."
    "It also has the image of the phone as the background, which can be changed to a different image."
    "To do that, change the variable {i}smartphone{/i} to the image you want. You'll need to modify the styles to fit."
    "The style group for the Phone() screen is 'phone_layout'."
    "You may want to change the style group 'phone_buttons' as well if you want the images on the phone image to be usable."
    "There is the option of adding an overlay image on the phone to simulate a reflection. Change the variable {i}smartphone_overlay{/i} for this."
    "On Phone(), the default setting is {i}modal False{/i} which means the phone can be interacted with simultaneously with the say window."
    "It can be changed to {i}modal True{/i} to use the phone as a menu instead."
    "Phone() uses the screens Phone_Status() and Phone_Active()."
    "Phone_Status() is the status bar on the screen."
    "It has a showif statement for any notifications that pop up."
    "Phone_Active() determines what the active screen is."
    "Phone_Lock() is the lock screen. It contains a button to unlock the screen."
    "The predefined way of unlocking the phone is by clicking on the round phone button at the bottom."
    "Phone_Home() serves as the home screen."
    "You can add buttons to here and build the grid, or change it to look like something else completely, like using imagebuttons instead."
    "Phone_Messages() displays your contacts and will lead you to their conversation."
    "Phone_Chat() lets you view the conversation and interact with the contact."
    "Phone_Choice() displays all the choices available during the conversation."
    "More on the messaging system can be found under Messages in the table of contents, or under the label tutorial_messages."
    "Finally, Phone_New() is an example of a screen you can modify."
    "Remember to add the screen to Phone_Active()'s if statement so it displays properly, and create a link to it on Phone_Home()."

    jump table_of_contents

label tutorial_flags():

    "Available to you is a variable called {i}flags{/i}."
    "It is intended to be a set of strings to keep track of decisions made."
    "To add and remove flags, call addFlag(flagname) and remFlag(flagname) respectively."
    "Also included are the actions AddFlag(flagname) and RemFlag(flagname)."
    "You can choose to use it in your game, modify it to use something other than strings, or replace it with the system you currently have."
    "With Phone.rpy, players can earn or lose flags with the message reply system."

    "Contacts have an extra property called {i}points{/i}."
    "This can be used in multiple ways: intimacy, mood, etc."
    "To add and subtract points, call IncreasePoints(contact, amount) and DecreasePoints(contact, amount) respectively."
    "Also included are the actions increasePoints(contact, amount) and decreasePoints(contact, amount)."
    "Feel free to modify or delete it for your game."

    jump table_of_contents

label tutorial_messages():

    show screen Phone

    "This is the extra long lesson on Phone.rpy's messages."
    "First let's add some contacts."

    $ phone.add(contactA)
    $ phone.add(contactB)

    "Phone.rpy has a contact system."
    "Each contact has their own message conversation that can be viewed on the phone."
    "Let's see what happens we remove a contact."

    $ phone.remove(contactB)

    "You can no longer contact them or view their messages."

    $ receive_message(contactB, "You removed me!")
    "When you re-add a contact, their data is still retained."
    "Let's add them back."

    $ phone.add(contactB)

    "There are two ways of creating messages: receive_message() and queue_message()."

    $ receive_message(contactA, "Hey, it's Alice.")
    "receive_message() lets you create and receive a message immediately. This can make writing your script easier."

    "queue_message() does the same, but instead of receiving it immediately, it places it on the message queue."
    "This is called {i}messages{/i}, a list structure."
    $ receive_next()
    "Receiving a queued message is done with receive_next()"

    "All of these messages so far are regular messages."

    $ receive_message(contactA, "How are you?", [
        Reply("Good!"),
        Reply("Could be better.")
    ])
    "This is a message with replies."

    $ receive_message(contactA, "What do you want to eat?", [
        Reply("Burgers", [
            AddFlag("eat_burgers")
        ]),
        Reply("Salad", [
            AddFlag("eat_salad")
        ])
    ])
    "This is a message with replies. Each reply has a flag attached to it."

    "Send a reply to see what happens:"

    if "eat_burgers" in flags:
        "You want to eat burgers!"
    elif "eat_salad" in flags:
        "You want to eat a salad!"

    $ queue_message(contactA, "Want to go see a play?", [
        Reply("Sure!", [
            AddFlag("play_yes"),
            IncreasePoints(contactA, 5)
        ]),
        Reply("Why not a movie instead?", [
            AddFlag("play_no"),
            DecreasePoints(contactA, 1)
        ])
    ])
    "This is a message with replies, as well as a flag and an effect."

    "Make sure your debug screen is on so you can view the effect."

    "Now send a reply."

    if "play_yes" in flags:
        a "I'm so excited!"
    elif "play_no" in flags:
        a "Movies are okay, but they just don't match up to watching live actors on stage."

    $ receive_message(contactB, "Want to go to a fashion show?", [
        Reply("Okay!", [
            AddFlag("fashion_yes"),
            IncreasePoints(contactA, 5)
        ]),
        Reply("No thanks.", [
            AddFlag("fashion_no"),
            DecreasePoints(contactA, 1)
        ])
    ])
    "Here's another message to try."

    "Send a reply and watch the effect happen."

    if "fashion_yes" in flags:
        b "You, I like you!"
    elif "fashion_no" in flags:
        b "You're missing out!"

    "A Time object called {i}time{/i} is running by default."
    "Each time you advance the story, another 'minute' has passed."
    "This is tracked in the {i}say{/i} screen."
    "You can see how by viewing {i}screens.rpy{/i}."

    $ receive_message(contactA, "Reply in 5 minutes. Don't wait up!", [
        Reply("Ok!")    
    ])
    "Messages can depend on a delay using the Time object."
    "Depending on how soon you reply, a different effect can happen."
    "Send your reply to make sure you don't miss an important flag."
    "However, the opposite can be true: delaying your reply may have better results."
    "The same goes for not replying at all."
    "It all relies on how you want to implement the game."
    "Now let's check the delay."
    
    if delayFor(contactA, "<= 5"):
        a "Good job!"
    elif delayFor(contactA, "> 5"):
        a "You waited too long."
    else:
        a "You didn't reply."

    $ receive_message(contactB, "Reply in 5 minutes with what you want as a gift, and I'll give it! If you don't I will pick for you! Dress or skirt?", [
        Reply("Dress", [
            AddFlag("pick_dress")
        ]),
        Reply("Skirt", [
            AddFlag("pick_skirt")
        ])
    ])

    "Time can be controlled by setting it manually."
    
    "Here's another message to try."
    "This time, let's introduce the start_reply and stop_reply functions."
    "You can prevent a player for sending a reply past a certain point."
    "This gives you more control on what happens in the game."
    "Stopping replies now."

    $ contactB.stop_reply()

    "If the player hasn't replied yet, they would be prevented from doing so now."
    "Now let's check the results."

    if delayFor(contactB, "<= 5"):
        if "pick_dress" in flags:
            b "Your dress will be ballroom worthy!"
        elif "pick_skirt" in flags:
            b "Your skirt will be trendy and hip!"
    elif delayFor(contactB, "> 5"):
        b "You didn't reply!"
        b "I'll pick a short and sexy miniskirt for you then."
    else:
        b "You didn't even try."

    "Let's enable replying again for this contact."

    $ contactB.start_reply()

    "End"

    jump table_of_contents