###
#   Phone.rpy
#   Message framework with flag system 
#   
#   _python   
#     
###
        
init python:

    ###
    #   Main Phone Classes and Functions
    ###
    
    # Global variables
    current_contact = None


    ###
    #   Time
    ###
    import copy

    class Time(object):
        def __init__(self, h, m):
            self.h = 0
            self.m = 0
            self.total = 0
        def __repr__(self):
            return "Time()"
        def __str__(self):
            return '{:02d}:{:02d}'.format(self.h, self.m)

        # Increments time whenever called
        #   To enable whenever the say screen shows
        #   on "show" action time.passes
        def passes(self):
            if self.m == 59:
                if self.h == 23:
                    self.h = 0
                else:
                    self.h += 1
                self.m = 0
            else:
                self.m += 1
            self.total += 1

        # Manually set the time
        #   Do NOT call if you use delays
        #   Aesthetic purposes only
        def set(self, h, m):
            self.h = h
            self.m = m
    
    # Given a contact, returns the delay time
    # between a reply and message
    def check_delay(contact):
        reply = contact.last()
        message = contact.secondlast()
        if reply and message and reply.sender == None and message.sender == contact:
            return delay(message, reply)
        else:
            return False

    # Calculates the delay
    def delay(message, reply):
        mTime = message.dateSent
        rTime = reply.dateSent
        return abs(mTime.total - rTime.total)
    
    # Simplifying check_delay func
    # ifthis = ">= 5" 
    def delayFor(contact, ifthis):
        delay = check_delay(contact)
        if delay:
            return eval("delay"+ifthis)
        else:
            return False


    ###
    #   Phone
    ###
    class Phone(object):
        def __init__(self):
            self.isLocked = False
            self.contacts = set()

        # Lock/unlock phone
        def unlock(self):
            self.isLocked = False
            renpy.restart_interaction()
        def lock(self):
            self.isLocked = True
            renpy.restart_interaction()

        # Checks if there are unread messages
        def has_unread(self):
            unread = False
            for i in self.contacts:
                if i.unread_count() > 0:
                    unread = True
            return unread
            
        # Add/remove contacts
        def add(self, Contact):
            self.contacts.add(Contact)
        def remove(self, Contact):
            self.contacts.discard(Contact)

    ###
    #   Contact
    ###
    class Contact(object):
        def __init__(self, name, messages=None):
            self.name = name
            if messages is None:
                self.messages = []
            else:
                self.messages = messages
            self.replyable = False
            self.draft = ''
            self.points = 0
        def __repr__(self):
            return self.name
        def __str__(self):
            return self.name

        # Append the message to this contact
        def append(self, Message):
            self.messages.append(Message)
        # Start/stop reply mode
        #   to reply past a certain point
        def start_reply(self):
            self.replyable = True
        def stop_reply(self):
            self.replyable = False
     
        # Returns the number of unread messages  
        def unread_count(self):
            unread = [ x for x in self.messages if not x.isRead]
            return len(unread)
        # Returns the last message with contact
        def last(self):
            if len(self.messages) > 0:
                return self.messages[len(self.messages)-1]
        # Returns the second last message with contact
        def secondlast(self):
            if len(self.messages) > 0:
                return self.messages[len(self.messages)-2]
        # Returns whether the player can reply
        def can_reply(self):
            return self.replyable and self.last() and self.last().has_replies()

    # Mark all messages with this contact as read
    def mark_read_all(contact):
        for x in contact.messages:
            x.isRead = True
    # View the contact        
    def view(contact):
        global current_contact
        current_contact = contact
        mark_read_all(contact)
        scroll_bottom(vp_chat_adj)


    ###
    #   Message 
    ###    
    class Message(object):
        def __init__(self, sender, body, replies=None):
            if sender is None:
                self.sender = None
                self.isRead = True
            else:
                self.sender = sender
                self.isRead = False
            self.body = body
            if replies is None:
                self.replies = []
            else:
                self.replies = replies
            self.dateSent = None
        def __repr__(self):
            return "{}: {}".format(self.sender, self.body)
        def __str__(self):
            return "{}: {}".format(self.sender, self.body)

        # Check if message has replies
        def has_replies(self):
            return self.replies and self.replies != []
        # Receive message from contact
        def receive(self):
            global current_contact
            global time
            if self in messages:
                messages.remove(self)
            newTime = copy.copy(time)
            self.dateSent = newTime
            sender = self.sender
            if sender == current_contact:
                self.isRead = True
            if self.has_replies:
                sender.start_reply()
            sender.append(self)
            renpy.restart_interaction()    
        # Send message to contact
        def send(self):
            global current_contact
            global time
            newTime = copy.copy(time)
            self.dateSent = newTime
            current_contact.append(self)
            reply = self.body
            effect = self.body.effect
            if effect:
                for i in effect:
                    i()
            replies.add(reply)
            current_contact.draft = ''
            renpy.restart_interaction()            


    ###
    #   Reply
    ###
    class Reply(object):
        def __init__(self, body, effect=None):
            self.body = body
            if effect is not None:
                self.effect = effect
            else:
                self.effect = False
        def __repr__(self):
            return "{}".format(self.body)
        def __str__(self):
            return "{}".format(self.body)           

    ###
    #   General message functions
    ###
    # Create a new message and queue it
    def queue_message(Contact, body, replies=None):
        msg = Message(Contact, body, replies)
        messages.append(msg)
    # Create a new message and receive it
    def receive_message(Contact, body, replies=None):
        msg = Message(Contact, body, replies)
        msg.receive()
    # Receive the next queued message
    def receive_next():
        if messages != []:
            messages[0].receive()       
    # Send a new message to contact
    def send(Contact):
        message = Message(None, Contact.draft)
        message.send()   
        
       
    ### 
    #   Viewport scrolling
    ###
    class NewAdj(renpy.display.behavior.Adjustment):
        def change(self,value):
            if value > self._range and self._value == self._range:
                return Return()
            else:
                return renpy.display.behavior.Adjustment.change(self, value)                
                                
    # Adjustment for chat viewport
    vp_chat_adj = NewAdj()
    # Add more viewports if needed
                                
    # Given an adjustment, scroll to the bottom
    def scroll_bottom(adj):
        adj.value = adj.range

    # Action equivalent
    class ChatScrollBottom(Action):
        def __init__(self):
            self.adj = vp_chat_adj
        def __call__(self):
            self.adj.value = self.adj.range

            
    ###
    #   Effects
    ###

    # Add/remove flags
    #   Call by action:
    #       AddFlag(flagname)
    class AddFlag(Action):
        def __init__(self, flagname):
            self.flagname = flagname
        def __call__(self):
            flags.add(self.flagname)
    class RemFlag(Action):  
        def __init__(self, flagname):
            self.flagname = flagname
        def __call__(self):
            flags.discard(self.flagname)
    # Function equivalent
    def addflag(flag):
        flags.append(flag)
    def remflag(flag):
        flags.discard(flag)

    # Increase/decrease points
    #   Call by action:
    #       IncreasePoints(contact, emt)
    class IncreasePoints(Action):
        def __init__(self, contact, amt):
            self.contact = contact
            self.amt = amt
        def __call__(self):
            self.contact.points += self.amt
    class DecreasePoints(Action):
        def __init__(self, contact, amt):
            self.contact = contact
            self.amt = amt
        def __call__(self):
            self.contact.points -= self.amt
    # Function equivalent
    def increasePoints(contact, amt):
        contact.points += amt
    def decreasePoints(contact, amt):
        contact.points -= amt
    

    # More can be added if necessary
    # ...

