###
#   Phone.rpy
#   Message framework with flag system 
#      
#   _screens
#
###

init python:

    ###
    #   Images
    ###

    # Smartphone
    smartphone = "images/smartphone_640.png"
    # Smartphone overlay (eg. subtle gradient)
    smartphone_overlay = "images/smartphone_640_over.png"


init:

    ###
    #   Styles
    ###                            

    # Status bar
    style phone_status_frame:
        xfill True
        background "#000"
    style phone_status_part_frame:
        background None
    style phone_status_part_text:
        size 12


    # Phone layout     
    style phone_layout_window:
        # Position of phone
        xalign 0.075 yalign 0.5
        # Size of phone image
        xsize 328 ysize 640
        # Image of phone
        background smartphone    
    style phone_layout_frame:
        xpadding 0 ypadding 0
        # Position of screen
        xpos 33 ypos 77
        # Size of phone screen
        xsize 262 ysize 434
        # Phone wallpaper
        background None
    
    # Phone buttons
    style phone_buttons_button:
        background None
        hover_background "#fff8"

    # Phone icons
    style phone_icons_grid:
        xfill True yfill True
    style phone_icons_button:
        # Force fill entire grid block
        xfill True yfill True
        # Force size
        # xsize 100 ysize 100

    # Phone app
    style phone_app_frame:
        xpadding 0 ypadding 0
        xfill True yfill True
        background None
    style phone_app_vbox:
        xfill True
        
    # Phone message
    style phone_message_frame:
        xsize 0.8
    style phone_message_text:
        size 16
    style phone_message_incoming_frame is phone_message_frame:
        xalign 0.0
    style phone_message_incoming_text is phone_message_text
    style phone_message_outgoing_frame is phone_message_frame:
        xalign 1.0
    style phone_message_outgoing_text is phone_message_text
        
    # Phone textbox
    style phone_textbox_frame:
        xfill True
        ysize 100
        yalign 1.0
    
        
###
#   Phone
###
screen Phone():

    # Set True to disable phone use during conversations
    modal False

    default phone_active = None
        
    window:
        style_group "phone_layout"
                
        frame:
            side "t c":
                use Phone_Status
                use Phone_Active(phone_active)

        # Screen overlay image
        add smartphone_overlay


        ###
        #   Phone buttons
        ###   
        fixed:
            style_group "phone_buttons"        
            # Back
            button action If(phone_active == "chat", SetScreenVariable("phone_active", "messages"), SetScreenVariable("phone_active", None)) xpos 48 ypos 518 xsize 34 ysize 34
            # Settings
            button action ShowMenu("preferences") xpos 115 ypos 518 xsize 34 ysize 34
            # Home
            button action SetScreenVariable("phone_active", None) xpos 181 ypos 518 xsize 34 ysize 34
            # Find?
            button action Hide("Phone") xpos 247 ypos 518 xsize 34 ysize 34

            # Lock
            button action phone.lock xpos 145 ypos 571 xsize 38 ysize 38      

            
###
#   Phone_Status
###
screen Phone_Status():

    frame:
        style_group "phone_status"
        
        has hbox
        style_group "phone_status_part"
        frame:
            text "Time {}".format(str(time))
        frame:
            showif phone.has_unread() and renpy.get_screen("Phone_Chat") is None:
                text "Unread"


###
#   Phone_Active
###
screen Phone_Active(phone_active):

    frame:
        style_group "phone_app"

        if phone.isLocked:
            use Phone_Lock
        elif phone_active == "messages":
            use Phone_Messages
        elif phone_active == "chat":
            use Phone_Chat
        elif phone_active == "choice":
            use Phone_Choice
        # Add more screens
        elif phone_active == "new":
            use Phone_New
        else:
            use Phone_Home
    
        
###
#   Phone_Lock
###
screen Phone_Lock():

    vbox:
        text "Phone is Locked"
        textbutton "Unlock" action phone.unlock


###
#   Phone_Home
###
screen Phone_Home():

    # App icons
    default home_buttons = [
        ("Messages",
            [SetScreenVariable("phone_active", "messages")]),
        ("New",
            [SetScreenVariable("phone_active", "new")]),
        ("Show Debug",
            [Show("Phone_Debug")])
    ]
    
    # Customize grid numbers
    default columns = 2
    default rows = 3
    grid columns rows:
        style_group "phone_icons"

        for name, action in home_buttons:
            textbutton name action action

        for i in range(len(home_buttons), columns*rows):
            null

        
###
#   Phone_Messages
###            
screen Phone_Messages():

    vbox:
        text "Messages"
        for contact in phone.contacts:
            if contact.unread_count() > 0:
                textbutton "{} ({})".format(contact.name, contact.unread_count()) action [Function(view, contact), SetScreenVariable("phone_active", "chat")]
            else:
                textbutton contact.name action [Function(view, contact), SetScreenVariable("phone_active", "chat")]


###
#   Phone_Chat
###                 
screen Phone_Chat():

    side "t c b":
        text current_contact.name
        side "c r":
            viewport id "vp_chat":
                mousewheel True
                yinitial 1.0
                yadjustment vp_chat_adj

                has vbox
                for message in current_contact.messages:
                    frame:
                        if message.sender:
                            style_group "phone_message_incoming"
                        else:
                            style_group "phone_message_outgoing"
                        text "Sent at {}:\n {} ".format(str(message.dateSent), message.body)
            bar adjustment vp_chat_adj style 'vscrollbar' default
                           
        frame:
            style_group "phone_textbox"

            hbox:
                frame:
                    background "#fff"
                    yfill True
                    xsize 0.8
                    text "{}".format(current_contact.draft) color "#000" size 16
                frame:
                    yfill True
                    has vbox
                    textbutton "?" action SensitiveIf(current_contact.can_reply()), SetScreenVariable("phone_active", "choice")
                    textbutton u"\u27A1" action SensitiveIf(current_contact.draft), Function(send, current_contact)

                    
###
#   Phone_Choice
###
screen Phone_Choice():

    $ choices = current_contact.last().replies
           
    vbox:
        label "Select your reply:"
        for i in choices:
            button:
                action SetField(current_contact, "draft", i), SetScreenVariable("phone_active", "chat")
                text i.body
                
        button:
            action SetField(current_contact, "draft", ''), SetScreenVariable("phone_active", "chat")
            text "Don't reply"              
            


# Additional screens can be created

###
#   Phone_New
###
screen Phone_New():
    
    text "You can add another app/screen here."