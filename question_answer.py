from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import json
from result import Result
from database import Database
from login import Login

Builder.load_string(
"""
#: import Custom_ProgressBar customwidgets
<QuestionPage>:
    MDLabel:
        pos_hint: {"center_x": 0.5, "top": 0.9}
        adaptive_size: True
        text: "Opto App"
        font_size: '64sp'
        font_name: 'font_names/precious.ttf'
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        
    MDAnchorLayout:
        anchor_x: "center"
        anchor_y: "center"

        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            size_hint_x: 0.7
            spacing: dp(10)

            MDLabel:
                id: label
                text: "Are the headache uniliteral or Bilaterial?"
                font_size: '18sp'
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                size_hint_y: None
                height: dp(100)
                halign: "center"

            MDRaisedButton:
                id: option1
                elevation: 2
                text: "Option 1"
                padding: [dp(100), 0, dp(100), 0]
                md_bg_color: app.theme_cls.accent_color
                pos_hint: {"center_x": 0.5}
                on_press: root.option_selection(self.text) ## Kendi text'ini alıyor. Yani 'Option 1'
            MDRaisedButton:
                id: option2
                elevation: 2
                text: "Option 2"
                padding: [dp(100), 0, dp(100), 0]
                md_bg_color: app.theme_cls.accent_color
                pos_hint: {"center_x": 0.5}
                on_press: root.option_selection(self.text) ## Kendi text'ini alıyor. Yani 'Option 2'

    Custom_ProgressBar:
        id: progressbar
        size_hint_x: 0.8
        pos_hint: {"center_x": 0.5, "y": 0.05}
        progress_value: 0
        label_text: "0%"

"""
)

class QuestionPage(MDScreen):
    data=dict()
    questions=list()
    counter=0
    process=list()
    percentage_results=list()

    @staticmethod
    def set_file(filename):
        file = open(filename)
        QuestionPage.data = json.load(file)
        QuestionPage.questions = QuestionPage.data["Questions"]
        QuestionPage.counter = 0
        QuestionPage.process = list()
    
    def next_question(self):
        question = QuestionPage.questions[QuestionPage.counter]
        keys = list(QuestionPage.data[question].keys())

        # print(question)
        # print(keys)
        self.ids.label.text = question
        self.ids.option1.text = keys[0]
        self.ids.option2.text = keys[1]

        self.ids.progressbar.progress_value = int((QuestionPage.counter / len(QuestionPage.questions)) * 100)
        self.ids.progressbar.label_text = str(int((QuestionPage.counter / len(QuestionPage.questions)) * 100)) + "%"
    def on_pre_enter(self, *args):
        self.next_question() 
    
    def option_selection(self, key):
        answer = self.ids.label.text
        value=QuestionPage.data[answer][key]
        # print(value)
        QuestionPage.process+=value

        if (QuestionPage.counter < len(QuestionPage.questions)-1):
            QuestionPage.counter += 1
            self.next_question()
        else:
            self.calculate_result()
            self.save_history()
            Result.set_result(QuestionPage.percentage_results)
            self.ids.progressbar.progress_value = 0
            self.ids.progressbar.label_text = "0%"
            self.manager.current = "result"

    def calculate_result(self):
        unique_diagnosis = set(QuestionPage.process)
        
        for diagnose in unique_diagnosis:
            percentage=f"{round((QuestionPage.process.count(diagnose) / len(QuestionPage.process)) * 100, 2)}%"
            QuestionPage.percentage_results.append((diagnose, percentage))           
        
        print(QuestionPage.percentage_results)

    def save_history(self):
        Database.insert_into_entries(Login.email, QuestionPage.data["Name"])
        entry_id = Database.get_last_entry_id(Login.email)[0]

        for item in QuestionPage.percentage_results:
            Database.insert_into_data_table(entry_id, Login.email, item[0], item[1])


