from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
import re

#Custom label that is mainly defined in the kivy file
class WrapLabel(Label):
    pass

#Custom notification that is mainly defined in the kivy file
class Notification(Popup):
    def __init__(self, text, title = None, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)
        self.ids.text.text = text

        if title != None:
            self.title = title

#Button that generates a dropdown on click
class ChoiceButton(Button):
    def __init__(self, choices, *args, **kwargs):
        super(ChoiceButton, self).__init__(*args, **kwargs)
        self.choices = choices
        self.text = self.choices[0]
        self.bind(on_release = self.dropdown_callback)

    def dropdown_callback(self, instance):
        dropdown = DropDown()

        for item in self.choices:
            btn = Button(text=item, size_hint_y=None, height=44, background_color = (0.5,0.5,0.5,0.5))
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        def onSelect(selfIgnore, instance):
            self.text = instance
            self.clear_widgets()

        dropdown.bind(on_select=onSelect)
        dropdown.open(self)

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def __init__(self, default = None, *args, **kwargs):
        super(FloatInput, self).__init__(*args, **kwargs)
        if default != None:
            self.text = default
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class IntegerInput(TextInput):
    pat = re.compile('[^0-9]')
    def __init__(self, default = None, *args, **kwargs):
        super(IntegerInput, self).__init__(*args, **kwargs)
        if default != None:
            self.text = default
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(IntegerInput, self).insert_text(s, from_undo=from_undo)

#Button that generates a notification on click
class NotificationButton(Button):
    def __init__(self, notification, title = None, *args, **kwargs):
        super(NotificationButton, self).__init__(*args, **kwargs)
        self.notification = notification
        self.title = None
        self.text = '(i)'
        self.pos_hint = {'top': 1, 'right' : 1}
        self.bind(on_release = self.notification_callback)

    def notification_callback(self, instance):
        notification = Notification(self.notification, self.title)
        notification.open()

class InputFactory(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(InputFactory, self).__init__(*args, **kwargs)
        self.maincontroller = None

    #to get button or input to bind actions / etc
    def returnMainController(self):
        return self.maincontroller

    def returnMainControllerText(self):
        if (self.maincontroller.text == ''):
            return None
        elif (isinstance(self.maincontroller,IntegerInput)):
            return int(self.maincontroller.text)
        elif (isinstance(self.maincontroller,FloatInput)):
            return float(self.maincontroller.text)
        else:
            return self.maincontroller.text

    def setText(self, text):
        if (isinstance(self.maincontroller,ChoiceButton)):
            if (text in self.maincontroller.choices):
                self.maincontroller.text = text
        else:
            self.maincontroller.text = text

    #to add a label
    def generateLabel(self, text):
        self.removeLabel()
        self.text = text
        self.label = RelativeLayout()
        self.label.add_widget(WrapLabel(text = self.text))
        self.add_widget(self.label)

    #to add a button
    def generateButton(self, text):
        self.removeLabel()
        self.text = text
        self.label = RelativeLayout()
        button = Button(text = self.text)
        self.label.add_widget(button)
        self.add_widget(self.label)
        self.maincontroller = button

    #need to call generateLabel before calling this
    def generateLabelNotification(self, notification):
        if hasattr(self, 'label') and self.label != None:
            self.notification = notification
            secondaryButton = NotificationButton(self.notification, size_hint = (0.1, 0.3))
            self.label.add_widget(secondaryButton)
        else:
            print("No Label Generated Yet")

    def removeLabel(self):
        if hasattr(self, 'label') and self.label != None:
            self.remove_widget(self.label)

    #generate float input
    def generateFloatInput(self, default = None):
        self.removeInput()
        self.input = RelativeLayout()
        floatField = FloatInput(default)
        self.input.add_widget(floatField)
        self.add_widget(self.input)
        self.maincontroller = floatField

    #generate integer input
    def generateIntegerInput(self, default = None):
        self.removeInput()
        self.input = RelativeLayout()
        integerField = IntegerInput(default)
        self.input.add_widget(integerField)
        self.add_widget(self.input)
        self.maincontroller = integerField

    #to add a choiceinput
    def generateChoiceInput(self, choices):
        self.removeInput()
        self.choices = choices
        self.input = RelativeLayout()
        choiceField = ChoiceButton(self.choices)
        self.input.add_widget(choiceField)
        self.add_widget(self.input)
        self.maincontroller = choiceField

    #need to call generateChoiceInput / Input before calling this
    def generateInputNotification(self, choices):
        if hasattr(self, 'input') and self.input != None:
            self.notification = notification
            secondaryButton = NotificationButton(self.notification, size_hint = (0.3, 0.3))
            self.input.add_widget(secondaryButton)
        else:
            print("No Input Generated Yet")

    def removeInput(self):
        if hasattr(self, 'input') and self.input != None:
            self.remove_widget(self.input)
