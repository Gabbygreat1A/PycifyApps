from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from kivy.properties import ObjectProperty

Window.size = 450, 650

kv = '''
MDBoxLayout:
    orientation: 'vertical'
    MDToolbar:
        id: tool_bar
        title: 'GP CALCULATOR'
        right_action_items: [['dots-vertical', lambda x: print('DOT'), 'DOTS']]
        left_action_items: [['menu', lambda x: nav_draw.set_state('open'), 'MENU']]
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            MDScreen:
                name: 'gp_screen'
                ScrollView:
                    MDList:
                        id: course_list
                        CourseList:
                            text: 'MATHS'
                            secondary_text: 'Mat 101'
                            tertiary_text: '3 Credit Load'
                            
                        CourseList:
                            text: 'ENGLISH'
                            secondary_text: 'Gs 101'
                            tertiary_text: '3 Credit Load'
                                                  
                MDFloatLayout:
                    md_bg_color: 0, 0, 0, .5
                    size_hint_y: .15
                    MDFillRoundFlatButton:
                        text: 'CALCULATE GP'
                        pos_hint: {'center_y': .5, 'center_x': .25}
                        size_hint: .4, .7
                        on_press: app.calculate_gp_check(course_list)
                    MDFloatingActionButton:
                        icon: 'plus'
                        pos_hint: {'center_y': .5, 'center_x': .9}
                        on_press: app.add_course_form()
            
        MDNavigationDrawer:
            id: nav_draw
            ScrollView:
                MDList:
                    OneLineIconListItem:
                        icon: 'android'
                        text: 'GP CALCULATOR'
                        on_press:
                            nav_draw.set_state('close')
                            screen_manager.current = 'gp_screen'
                            tool_bar.title = self.text
                            
<CourseList>
    IconLeftWidget:
        icon: 'book'
    CustomInput:
        id: grade_input


<DialogContainer>
    orientation: 'vertical'
    size_hint_y: None
    height: "160dp" 
    MDTextField:
        id: course_title
        hint_text: 'COURSE TITLE'
        helper_text: 'Enter The Course Title'
        helper_text_mode: 'on_focus'
    MDTextField:
        id: course_code
        hint_text: 'COURSE CODE'
        helper_text: 'Enter The Course Code'
        helper_text_mode: 'on_focus'
    MDTextField:
        id: credit_load
        hint_text: 'CREDIT LOAD'
        helper_text: 'Enter Course Credit Load'
        helper_text_mode: 'on_focus'
    
'''

class CustomInput(IRightBodyTouch, MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DialogContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CourseList(ThreeLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._no_ripple_effect = True

class CurrentGp(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        
class PycifyApp(MDApp):
    def build(self):
        return Builder.load_string(kv)

    #To Check For Valid Score Input From User
    def check_valid_score(self, score):
        try:
            int(score)
        except ValueError:
            toast('Enter A Valid Score')
            return False
        else:
            if 0<=int(score)<=100:
                return True
            else:
                toast('Your Input Must Be Between 1 and 100')
                return False

    #Use Regular Expression To Make Your Logic 
    def check_valid_data(self, row_lists):
        return True
        pass
            
    #Does Most Of The Calculations
    def calculate_gp_check(self, widget=None):
        self.state = None
        self.score_database = []
        self.load_database = []
        self.product_database = []
        for lists in widget.children:
            if self.check_valid_score(lists.ids.grade_input.text) and self.check_valid_data(lists.tertiary_text[0]):
                self.state = True
                self.score_database.append(self.subject_grade(int(lists.ids.grade_input.text)))
                self.load_database.append(int(lists.tertiary_text[0]))
            else:
                self.state = False
        self.total_load = sum(load for load in self.load_database)
        self.product_database = sum(list(map(lambda x, y: x*y, self.score_database, self.load_database)))
        self.calculate_gp()

    #To Return The Exact Grade For Each Score
    def subject_grade(self, course_grade):
        if 70<=course_grade<=100:
            return 5
        elif 60<=course_grade<=69:
            return 4
        elif 50<=course_grade<=59:
            return 3
        elif 45<=course_grade<=49:
            return 2
        elif 35<=course_grade<=44:
            return 1
        elif 0<=course_grade<=34:
            return 0

    #Displays Final CGPA On A Dialog
    def calculate_gp(self):
        if self.state:
            CurrentGp(title='CURRENT CGPA: %.2f'%(self.product_database/self.total_load)).open()
            

    #To Create A New Course List Object
    def add_new_course(self, name, code, load):
        self.root.ids.course_list.add_widget(CourseList(text=name.upper(),
                                                        secondary_text=code,
                                                        tertiary_text=load+' Credit Load'))

    #ADDS A NEW COURSE TO OUR COURSE LIST   
    def save_course(self, widget):
        title = widget.ids.course_title.text
        code = widget.ids.course_code.text
        load = widget.ids.credit_load.text
        self.add_new_course(title, code, load)
        toast('Successfully Added Course')
        self.form.dismiss()

    #The Dialog-Like Form For Adding Course
    def add_course_form(self):
        self.container = DialogContainer()
        self.form = MDDialog(title='ADD NEW COURSE',
        type='custom',
        content_cls=self.container,
        auto_dismiss=False,
        buttons=[MDFlatButton(text='CLOSE',on_press=lambda x:self.form.dismiss()),
                 MDFlatButton(text='SAVE', on_press=lambda x:self.save_course(self.container))])

        self.form.open()
        
PycifyApp().run()
