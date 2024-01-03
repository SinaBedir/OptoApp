from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from login import Login
from database import Database
from question_answer import QuestionPage
from customwidgets import CustomItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog

Builder.load_string(
"""
<Home>:
    MDTopAppBar:
        pos_hint: {"top": 1}
        md_bg_color: app.theme_cls.accent_light
        right_action_items: [["logout", lambda x: root.logout()]]
        specific_text_color: app.theme_cls.primary_color
        elevation: 0
    
    MDBottomNavigation:
        id: navigation
        on_size: self.switch_tab("main_menu")
        MDBottomNavigationItem:
            name: "account"
            icon: "account-circle"
            text: "Account"
            on_tab_press: root.get_info()

            MDBoxLayout:
                orientation: "vertical"

                MDLabel:
                    adaptive_height: True
                    text: "Opto App"
                    halign: "center"
                    font_size: '64sp'
                    font_name: 'font_names/precious.ttf'
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_size: True

                        MDLabel:
                            text: "Personal Information"
                            adaptive_height: True
                            halign: "center"
                        MDTextField:
                            id: name
                            hint_text: "Name"
                            size_hint_x: None
                            width: dp(300)
                        MDTextField:
                            id: email
                            hint_text: "Email"
                            size_hint_x: None
                            width: dp(300)
                            disabled: True
                        MDTextField:
                            id: password
                            hint_text: "Password"
                            size_hint_x: None
                            width: dp(300)
                        MDRaisedButton:
                            text: "Update"
                            pos_hint: {"right": 1}
                            on_press: root.update()
                
        MDBottomNavigationItem:
            name: "main_menu"
            icon: "home-account"
            text: "Home"
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                MDLabel:
                    adaptive_height: True
                    text: "Opto App"
                    halign: "center"
                    font_size: '64sp'
                    font_name: 'font_names/precious.ttf'
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "top"
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(30)
                        adaptive_width: True
                        MDLabel:
                            text: "More Information"
                            halign: "center"
                            adaptive_height: True
                        MDScrollView:
                            size_hint_x:None
                            width: dp(300)
                            MDGridLayout:
                                cols: 2
                                adaptive_height: True
                                spacing: dp(20)
                                padding: [dp(20), dp(20), dp(20), dp(90)]
                                DCard:
                                    name: "Headache"
                                    icon_name: "head-plus"
                                    on_press: root.headache()
                                DCard:
                                    name: "Eye Flash"
                                    icon_name: "flash-red-eye"
                                    on_press: root.flashes()
                                DCard:
                                    name: "Red Eye"
                                    icon_name: "eye"
                                    on_press: root.headache()
                                DCard:
                                    name: "More Diseases"
                                    icon_name: "plus"
                                    on_press: root.flashes()
        MDBottomNavigationItem:
            name: "history"
            icon: "history"
            text: "History"
            on_tab_press: root.getHistory()

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(20), 0, dp(20), dp(70)

                MDLabel:
                    adaptive_height: True
                    text: "History"
                    halign: "center"
                    font_size: '24sp'
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                
                MDScrollView:
                    MDList:
                        id: list

"""
)

class Home(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.navigation.switch_tab("main_menu")
        
    def logout(self):
        self.manager.current = "login"

    def get_info(self):
        email = Login.email
        result = Database.get_user_info(email)
        self.ids.name.text = result[2] # Name bilgisi tuple'ın 3.elemanı
        self.ids.email.text = result[0] # Email bilgisi tuple'ın 1.elemanı
        self.ids.password.text = result[1] # Paassword bilgisi tuple'ın 2.elemanı
    
    def update(self):
        name = self.ids.name.text
        email = self.ids.email.text
        password = self.ids.password.text
        Database.update_user_info(name, email, password)
    
    def headache(self):
        QuestionPage.set_file("json/headache.json")
        self.manager.current = "qa_page"
    
    def flashes(self):
        QuestionPage.set_file("json/flashes.json")
        self.manager.current = "qa_page"

    def getHistory(self):
        self.ids.list.clear_widgets()
        results = Database.get_all_entries(Login.email)

        for index, result in enumerate(results):
            item = CustomItem(text=f"{result[-1]} - {index + 1}", entry_id=result[0])
            item.bind(on_press=self.show_details)
            self.ids.list.add_widget(item)
        
    def show_details(self, obj):
        boxLayout = MDBoxLayout(orientation="vertical", adaptive_size=True)

        column_data = [("Name", dp(30)), ("Percentage", dp(30))]

        row_data = list()
        data = Database.get_data(Login.email, obj.entry_id)

        for row in data:
            row_data.append((row[-2], row[-1]))
        
        data_table = MDDataTable(
                                rows_num=15,
                                column_data=column_data,
                                row_data=row_data,
                                size_hint=(None, None),
                                size=(dp(350), dp(300)),
                                pos_hint={"center_x":0.5,
                                          "center_y":0.5},
                                elevation=2,
                                background_color_header="#E91E63"
                                 )

        boxLayout.add_widget(data_table)

        dialogBox = MDDialog(title="Details", 
                             type="custom",
                             size_hint=(None, None),
                             size=(dp(400), dp(400)),
                             content_cls=boxLayout)
        dialogBox.open()