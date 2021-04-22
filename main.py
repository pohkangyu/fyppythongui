from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from inputs import *
from utilities import *
from plyer import filechooser
import pandas as pd
from stationary_module import StationaryTestModule
from kivy.core.window import Window
from idtxlmodules import *
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import _thread

Window.maximize()
#Main GUI, the root class and the application display this.
#Use clock schedule to dynamically include more widget after the generation of the class
class MainGUI(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(MainGUI, self).__init__(*args, **kwargs)
        self.data = None
        Clock.schedule_once(self.ids.dataprocessing.on_tab_width, 0.1)
        Clock.schedule_once(self.ids.relationshipcheck.on_tab_width, 0.1)
        Clock.schedule_once(self.uploadData)
        Clock.schedule_once(self.getInputSettings, 5)
    #set the dataframe for processing
    def setData(self, data):
        self.data = data

    #return the dataframe for processing
    def getData(self):
        return self.data

    def getInputSettings(self, instance):
        dict1 = self.ids.dataupload.getInputDictionary()
        dict2 = self.ids.dataprocessing.ids.stationarycheck.content.getInputDictionary()
        dict3 = self.ids.relationshipcheck.ids.multivariatete.content.getInputDictionary()
        dict1.update(dict2)
        dict1.update(dict3)
        print(dict1)
        pd.DataFrame.from_dict(data=dict1, orient='index').to_csv('dict_file.csv', header=False)

    def uploadData(self, instance):
        self.ids.dataupload.setInputDictionary({'Upload Row' : "C:\\Users\\kangyu\\Desktop\\FYP\\test - Copy.csv"})
        self.ids.dataprocessing.ids.stationarycheck.content.setInputDictionary({'ADF Significant': '112%', 'Johansen Significant': '1%'})

#To get the root where it is MAINGUI class. Able to obtain DataFrame from there
def getRoot(self):
    root = self
    while (not isinstance(root,MainGUI)):
        root = root.parent
    return root

# Class to process the uploaded data
class UploadRow(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(UploadRow, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.addRunButton, 0.1)

    #add the uploadbutton
    def addRunButton(self, instance):
        #key is the text in the button, value is the information to be displayed
        value = globalInput['UploadRow']['Buttons']['Button1']
        widget = InputFactory()
        widget.generateButton(value['Text'])
        widget.generateLabelNotification(value['Information'])
        widget.returnMainController().bind(on_release = self.open_selector)
        self.add_widget(widget)

        value = globalInput['UploadRow']['Buttons']['Button2']
        widget = InputFactory()
        widget.generateButton(value['Text'])
        widget.generateLabelNotification(value['Information'])
        widget.returnMainController().bind(on_release = self.open_selector)
        self.add_widget(widget)

    #to open file selector
    def open_selector(self, instance):
        path = filechooser.open_file(title="Pick a CSV file..", filters=[("Comma-separated Values", "*.csv")])
        #if no file selected then ignored
        if (len(path) == 0):
            self.ids.uploadrowlabel.text = 'C:\\Path'
            popup = Notification("Please select a file", "File Error")
            popup.open()
            return
        else:
            self.loadFilePath(path[0])

    #to load a file and try conversion to csv
    def loadFilePath(self, path):
        self.ids.uploadrowlabel.text = path
        self.loadFileToCSV()

    def getInputDictionary(self):
        return {'Upload Row' : self.ids.uploadrowlabel.text}

    def setInputDictionary(self, dictionary):
        if 'Upload Row' in dictionary:
            self.loadFilePath(dictionary['Upload Row'])

    #actual loading of csv to df, a pop to display the results
    def loadFileToCSV(self):
        path = self.ids.uploadrowlabel.text
        try:
            data = pd.read_csv(path)
            root = getRoot(self)
            root.setData(data)
            popup = Notification("Sucessfully uploaded", "Upload Update")
        except:
            popup = Notification("Issue loading file at: " + str(path), "Upload Update")
            self.ids.uploadrowlabel.text = "Please select a file"
        popup.open()

class StationaryCheck(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(StationaryCheck, self).__init__(*args, **kwargs)
        self.inputs = []
        Clock.schedule_once(self.addInputs, 0.1)

    def addInputs(self, instance):
        for key, value in globalInput['StationaryCheck']['InputsChoice'].items():
            widget = InputFactory()
            widget.generateLabel(value['Text'])
            widget.generateLabelNotification(value['Information'])
            widget.generateChoiceInput(value['Choice'])
            self.ids.stationarycheckinput.add_widget(widget)
            self.inputs += [widget]

        for key, value in globalInput['StationaryCheck']['Buttons'].items():
            widget = InputFactory()
            widget.generateButton(value['Text'])
            widget.returnMainController().bind(on_release = self.runModule)
            self.add_widget(widget)

    def runModule(self, instance):
        module = StationaryTestModule()
        root = getRoot(self)
        dictionary = self.getInputDictionary()
        result, details = module.getResult(root.getData(), dictionary['ADF Significant'], dictionary['Johansen Significant'])
        if result:
            result = 'Success'
        else:
            result = 'Fail'
        popup = Notification(details, result)
        popup.open()


    def getInputDictionary(self, instance = None):
        dictionary = {}
        for item in self.inputs:
            dictionary[item.text] = item.returnMainController().text
        return dictionary

    def setInputDictionary(self, dictionary):
        for item in self.inputs:
            if item.text in dictionary:
                item.setText(dictionary[item.text])

class MultivariateTE(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(MultivariateTE, self).__init__(*args, **kwargs)
        self.inputs = []
        Clock.schedule_once(self.addInputs, 0.1)

    def addInputs(self, instance):
        for key, value in globalInput['MultivariateTE']['Buttons'].items():
            widget = InputFactory()
            widget.generateButton(value['Text'])
            widget.generateLabelNotification(value['Information'])
            widget.returnMainController().bind(on_release = self.runModule)
            self.ids.multivariatete.add_widget(widget)

        for key, value in globalInput['MultivariateTE']['InputsChoice'].items():
            widget = InputFactory()
            widget.generateLabel(value['Text'])
            widget.generateLabelNotification(value['Information'])
            widget.generateChoiceInput(value['Choice'])
            self.ids.multivariatete.add_widget(widget)
            self.inputs += [widget]

        for key, value in globalInput['MultivariateTE']['InputsInteger'].items():
            widget = InputFactory()
            widget.generateLabel(value['Text'])
            widget.generateLabelNotification(value['Information'])
            widget.generateIntegerInput(value['Default'])
            self.ids.multivariatete.add_widget(widget)
            self.inputs += [widget]

        for key, value in globalInput['MultivariateTE']['InputsFloat'].items():
            widget = InputFactory()
            widget.generateLabel(value['Text'])
            widget.generateLabelNotification(value['Information'])
            widget.generateFloatInput(value['Default'])
            self.ids.multivariatete.add_widget(widget)
            self.inputs += [widget]


    def runModule(self, instance):
        dictionary = self.getInputDictionary()
        root = getRoot(self)
        numpy_format = root.getData().to_numpy()
        arr_format = numpy_format.reshape((3, len(numpy_format), 1))
        # dictionary   = {'cmi_estimator': 'JidtKraskovCMI',
        #             'max_lag_sources': 5,
        #             'min_lag_sources': 1}
        _thread.start_new_thread(self.runGraph, (arr_format, dictionary))


    def runGraph(self, arr_format, dictionary):
        run = MultiVariateTime(Data(arr_format), dictionary)
        a, b = run.run()
        self.ids.graph.clear_widgets()
        self.ids.graph.add_widget(FigureCanvasKivyAgg(b))


    def getInputDictionary(self, instance = None):
        dictionary = {}
        for item in self.inputs:
            if (item.returnMainControllerText() != None):
                dictionary[item.text] = item.returnMainControllerText()
        return dictionary

    def setInputDictionary(self, dictionary):
        for item in self.inputs:
            if item.text in dictionary:
                item.setText(dictionary[item.text])

class MainApp(App):
    def build(self):
        return MainGUI()


if __name__ == '__main__':
    MainApp().run()
