###
#   Phone.rpy
#   Message framework with flag system 
#      
#   _debug
#
###

init:
    style phone_debug_window:
        xsize 0.3 ysize 0.3
    style phone_debug_text:
        size 16

screen Phone_Debug():

    drag:
        align (1.0, 0.0) 

        window:
            style_group "phone_debug"

            has vbox
            hbox:
                textbutton "Hide Debug" action Hide("Phone_Debug")
                text "Drag me!"

            viewport:
                mousewheel True
                scrollbars "vertical"
                has vbox

                # Variables to view go here

                frame:
                    has vbox
                    text "Messages"
                    text "Total queued: {}".format(len(messages))

                frame:
                    has vbox
                    text "Replies"
                    text "Total sent: {}".format(len(replies))
                    text "Sent:"
                    for x in replies:
                        text x.body

                frame:
                    has vbox
                    text "Flags:"
                    for i in flags:
                        text i
                
                null height 10
                
                if current_contact:
                    text "Current: {}".format(current_contact)
                    frame:
                        text "Check delay: {}".format(check_delay(current_contact))

                null height 10

                text "Contacts"
                for c in phone.contacts:
                    frame:
                        text "{}:\nPoints: {}\n# unread: {}".format(c.name, c.points, c.unread_count())