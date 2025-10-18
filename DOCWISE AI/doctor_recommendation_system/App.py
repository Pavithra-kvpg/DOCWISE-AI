from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.clock import Clock
from plyer import filechooser

# ------------------ Import Your Modules ------------------
from modules import pdf_analyzer
from modules.disease_mapper import predict_specialist
from modules.doctor_filtering import get_doctors_by_specialist

class ProfessionalRoleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main container with professional background
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=0,
            spacing=0,
            md_bg_color=[0.98, 0.98, 0.98, 1]
        )
        
        # Header section with professional blue
        header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(300),
            padding=[dp(40), dp(60), dp(40), dp(20)],
            md_bg_color=[0.07, 0.45, 0.87, 1]
        )
        
        # App logo and title
        logo_section = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        
        app_name = MDLabel(
            text="DOCWISE AI",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            bold=True
        )
        
        tagline = MDLabel(
            text="Advanced Healthcare Intelligence Platform",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.9]
        )
        
        logo_section.add_widget(app_name)
        logo_section.add_widget(tagline)
        header.add_widget(logo_section)
        
        main_layout.add_widget(header)
        
        # Content section
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(40), dp(40), dp(40), dp(20)],
            spacing=dp(30),
            size_hint_y=None,
            height=dp(400)
        )
        
        # Role selection card
        role_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            size_hint_y=None,
            height=dp(280),
            elevation=8,
            radius=[dp(15),],
            md_bg_color=[1, 1, 1, 1]
        )
        
        role_title = MDLabel(
            text="Select Your Role",
            halign="center",
            font_style="H5",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        role_card.add_widget(role_title)
        
        # Role options
        role_options = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=None,
            height=dp(120)
        )
        
        # Doctor option
        doctor_option = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50)
        )
        self.doctor_check = MDCheckbox(
            group="role",
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        doctor_label = MDLabel(
            text="Medical Professional",
            font_style="H6",
            theme_text_color="Primary"
        )
        doctor_option.add_widget(self.doctor_check)
        doctor_option.add_widget(doctor_label)
        
        # Patient option
        patient_option = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50)
        )
        self.patient_check = MDCheckbox(
            group="role",
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        patient_label = MDLabel(
            text="Patient",
            font_style="H6",
            theme_text_color="Primary"
        )
        patient_option.add_widget(self.patient_check)
        patient_option.add_widget(patient_label)
        
        role_options.add_widget(doctor_option)
        role_options.add_widget(patient_option)
        role_card.add_widget(role_options)
        
        # Continue button
        continue_btn = MDRaisedButton(
            text="Continue to Sign In",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            md_bg_color=[0.07, 0.45, 0.87, 1]
        )
        continue_btn.bind(on_release=self.proceed_to_login)
        role_card.add_widget(continue_btn)
        
        content.add_widget(role_card)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)

    def proceed_to_login(self, instance):
        if self.doctor_check.active:
            self.manager.get_screen("professional_login").role = "doctor"
            self.manager.current = "professional_login"
        elif self.patient_check.active:
            self.manager.get_screen("professional_login").role = "patient"
            self.manager.current = "professional_login"
        else:
            dialog = MDDialog(
                title="Selection Required",
                text="Please select your role to continue.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=[0.07, 0.45, 0.87, 1]
                    )
                ]
            )
            dialog.open()

class ProfessionalLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = None
        
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=0,
            spacing=0,
            md_bg_color=[0.98, 0.98, 0.98, 1]
        )
        
        # Top App Bar
        top_bar = MDTopAppBar(
            title="Sign In",
            elevation=4,
            md_bg_color=[0.07, 0.45, 0.87, 1],
            specific_text_color=[1, 1, 1, 1],
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        main_layout.add_widget(top_bar)
        
        # Login form container
        form_container = MDBoxLayout(
            orientation="vertical",
            padding=[dp(40), dp(20), dp(40), dp(40)],
            spacing=dp(30)
        )
        
        # Role indicator
        self.role_indicator = MDLabel(
            text="",
            halign="center",
            font_style="H5",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(self.role_indicator)
        
        # Login card
        login_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            size_hint_y=None,
            height=dp(320),
            elevation=6,
            radius=[dp(12),],
            md_bg_color=[1, 1, 1, 1]
        )
        
        # Form fields
        self.username_field = MDTextField(
            hint_text="Username",
            icon_left="account",
            size_hint_y=None,
            height=dp(60)
        )
        
        self.password_field = MDTextField(
            hint_text="Password",
            icon_left="key",
            password=True,
            size_hint_y=None,
            height=dp(60)
        )
        
        login_card.add_widget(self.username_field)
        login_card.add_widget(self.password_field)
        
        # Sign in button
        signin_btn = MDRaisedButton(
            text="Sign In",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            md_bg_color=[0.07, 0.45, 0.87, 1]
        )
        signin_btn.bind(on_release=self.authenticate)
        login_card.add_widget(signin_btn)
        
        form_container.add_widget(login_card)
        main_layout.add_widget(form_container)
        
        self.add_widget(main_layout)
    
    def go_back(self):
        self.manager.current = "professional_role"
    
    def on_enter(self):
        role_text = "Medical Professional" if self.role == "doctor" else "Patient"
        self.role_indicator.text = f"Sign In as {role_text}"
    
    def authenticate(self, instance):
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if self.role == "doctor" and username == "doctor" and password == "123":
            self.manager.current = "professional_doctor_dashboard"
        elif self.role == "patient" and username == "patient" and password == "123":
            self.manager.current = "professional_patient_dashboard"
        else:
            dialog = MDDialog(
                title="Authentication Failed",
                text="Invalid credentials. Please check your username and password.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=[0.07, 0.45, 0.87, 1]
                    )
                ]
            )
            dialog.open()

class ProfessionalDoctorDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Top App Bar
        self.top_bar = MDTopAppBar(
            title="Medical Dashboard",
            elevation=4,
            md_bg_color=[0.07, 0.45, 0.87, 1],
            specific_text_color=[1, 1, 1, 1],
            right_action_items=[["logout", lambda x: self.logout()]]
        )
        main_layout.add_widget(self.top_bar)
        
        # Content area
        content_scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10), dp(20), dp(20)],
            spacing=dp(25),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Welcome section
        welcome_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            size_hint_y=None,
            height=dp(140),
            elevation=4,
            radius=[dp(12),],
            md_bg_color=[0.95, 0.97, 1, 1]
        )
        
        welcome_card.add_widget(MDLabel(
            text="Welcome, Dr. Smith",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        ))
        welcome_card.add_widget(MDLabel(
            text="AI-Powered Medical Analysis Platform",
            theme_text_color="Secondary"
        ))
        content_layout.add_widget(welcome_card)
        
        # Upload section
        upload_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            size_hint_y=None,
            height=dp(280),
            elevation=4,
            radius=[dp(12),]
        )
        
        upload_card.add_widget(MDLabel(
            text="Medical Document Analysis",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30)
        ))
        
        upload_card.add_widget(MDLabel(
            text="Upload patient PDF reports for AI-powered analysis and insights",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Upload button
        upload_btn = MDRaisedButton(
            text="Upload Medical Report",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            md_bg_color=[0.07, 0.45, 0.87, 1]
        )
        upload_btn.bind(on_release=self.analyze_pdf)
        upload_card.add_widget(upload_btn)
        
        content_layout.add_widget(upload_card)
        
        # Results section
        self.results_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            size_hint_y=None,
            height=dp(200),
            elevation=4,
            radius=[dp(12),],
            md_bg_color=[0.98, 0.98, 0.98, 1]
        )
        
        self.results_card.add_widget(MDLabel(
            text="Analysis Results",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.results_label = MDLabel(
            text="Upload a medical report to view AI analysis results",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(120)
        )
        self.results_card.add_widget(self.results_label)
        
        content_layout.add_widget(self.results_card)
        content_scroll.add_widget(content_layout)
        main_layout.add_widget(content_scroll)
        
        self.add_widget(main_layout)
    
    def logout(self):
        self.manager.current = "professional_role"
    
    def analyze_pdf(self, instance):
        file_path = filechooser.open_file(
            title="Select Medical Report",
            filters=[("PDF Files", "*.pdf")]
        )
        if file_path:
            try:
                self.results_label.text = "🔬 Analyzing medical report...\nPlease wait, this may take a moment."
                # Schedule the PDF processing to run after a short delay
                Clock.schedule_once(lambda dt: self.process_pdf_analysis(file_path[0]), 0.1)
            except Exception as e:
                self.results_label.text = f"❌ Error: {str(e)}"
    
    def process_pdf_analysis(self, file_path):
        try:
            analysis_result = pdf_analyzer.summarize_pdf(file_path)
            self.results_label.text = analysis_result
            # Auto-adjust height based on content length
            line_count = analysis_result.count('\n') + 1
            self.results_card.height = max(dp(300), dp(50) * line_count)
        except Exception as e:
            self.results_label.text = f"❌ Analysis Failed:\n{str(e)}"

class ProfessionalPatientDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Top App Bar
        self.top_bar = MDTopAppBar(
            title="Patient Portal",
            elevation=4,
            md_bg_color=[0.07, 0.45, 0.87, 1],
            specific_text_color=[1, 1, 1, 1],
            right_action_items=[["logout", lambda x: self.logout()]]
        )
        main_layout.add_widget(self.top_bar)
        
        # Content area
        content_scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10), dp(20), dp(20)],
            spacing=dp(25),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Welcome section
        welcome_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            size_hint_y=None,
            height=dp(140),
            elevation=4,
            radius=[dp(12),],
            md_bg_color=[0.95, 0.97, 1, 1]
        )
        
        welcome_card.add_widget(MDLabel(
            text="Find Your Specialist",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        ))
        welcome_card.add_widget(MDLabel(
            text="Connect with the right medical professionals for your needs",
            theme_text_color="Secondary"
        ))
        content_layout.add_widget(welcome_card)
        
        # Search form
        search_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            size_hint_y=None,
            height=dp(240),
            elevation=4,
            radius=[dp(12),]
        )
        
        search_card.add_widget(MDLabel(
            text="Specialist Search",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.condition_input = MDTextField(
            hint_text="Enter medical condition or symptoms",
            icon_left="stethoscope",
            size_hint_y=None,
            height=dp(60)
        )
        
        self.location_input = MDTextField(
            hint_text="Preferred location (optional)",
            icon_left="map-marker",
            size_hint_y=None,
            height=dp(60)
        )
        
        search_card.add_widget(self.condition_input)
        search_card.add_widget(self.location_input)
        
        # Search button
        search_btn = MDRaisedButton(
            text="Find Specialists",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            md_bg_color=[0.07, 0.45, 0.87, 1]
        )
        search_btn.bind(on_release=self.search_specialists)
        search_card.add_widget(search_btn)
        
        content_layout.add_widget(search_card)
        content_scroll.add_widget(content_layout)
        main_layout.add_widget(content_scroll)
        
        self.add_widget(main_layout)
    
    def logout(self):
        self.manager.current = "professional_role"
    
    def search_specialists(self, instance):
        condition = self.condition_input.text.strip()
        location = self.location_input.text.strip()
        
        if condition:
            self.manager.get_screen("professional_results").update_results(condition, location)
            self.manager.current = "professional_results"
        else:
            dialog = MDDialog(
                title="Search Required",
                text="Please enter a medical condition or symptoms to search.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=[0.07, 0.45, 0.87, 1]
                    )
                ]
            )
            dialog.open()

class ProfessionalResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Top App Bar
        self.top_bar = MDTopAppBar(
            title="Specialist Results",
            elevation=4,
            md_bg_color=[0.07, 0.45, 0.87, 1],
            specific_text_color=[1, 1, 1, 1],
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        main_layout.add_widget(self.top_bar)
        
        # Results area
        self.results_scroll = MDScrollView()
        self.results_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10), dp(20), dp(20)],
            spacing=dp(20),
            size_hint_y=None
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        main_layout.add_widget(self.results_scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self):
        self.manager.current = "professional_patient_dashboard"
    
    def update_results(self, condition, location):
        self.results_layout.clear_widgets()
        
        specialist = predict_specialist(condition)
        
        if specialist:
            # Specialist recommendation card
            specialist_card = MDCard(
                orientation="vertical",
                padding=dp(25),
                size_hint_y=None,
                height=dp(120),
                elevation=4,
                radius=[dp(12),],
                md_bg_color=[0.95, 0.97, 1, 1]
            )
            
            specialist_card.add_widget(MDLabel(
                text="Recommended Specialist",
                font_style="H6",
                theme_text_color="Primary"
            ))
            specialist_card.add_widget(MDLabel(
                text=f"{specialist}",
                font_style="H5",
                theme_text_color="Primary",
                bold=True
            ))
            self.results_layout.add_widget(specialist_card)
            
            # Get matching doctors
            doctors_df = get_doctors_by_specialist(
                specialist, 
                location=location, 
                min_experience=2, 
                min_rating=3.5
            )
            
            if not doctors_df.empty:
                doctors_df = doctors_df.sort_values(by="Rating", ascending=False)
                
                results_info = MDLabel(
                    text=f"Found {len(doctors_df)} specialist(s) matching your criteria",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(40)
                )
                self.results_layout.add_widget(results_info)
                
                for _, doctor in doctors_df.iterrows():
                    doctor_card = MDCard(
                        orientation="vertical",
                        padding=dp(20),
                        size_hint_y=None,
                        height=dp(180),
                        elevation=4,
                        radius=[dp(10),]
                    )
                    
                    # Doctor header with rating
                    header_layout = MDBoxLayout(
                        orientation="horizontal",
                        size_hint_y=None,
                        height=dp(40)
                    )
                    
                    name_label = MDLabel(
                        text=f"Dr. {doctor['Name']}",
                        font_style="H6",
                        theme_text_color="Primary",
                        size_hint_x=0.7
                    )
                    
                    rating_label = MDLabel(
                        text=f"⭐ {doctor['Rating']}",
                        theme_text_color="Secondary",
                        size_hint_x=0.3,
                        halign="right"
                    )
                    
                    header_layout.add_widget(name_label)
                    header_layout.add_widget(rating_label)
                    doctor_card.add_widget(header_layout)
                    
                    # Doctor details
                    doctor_card.add_widget(MDLabel(
                        text=f"📍 {doctor['Location']}",
                        theme_text_color="Secondary"
                    ))
                    doctor_card.add_widget(MDLabel(
                        text=f"🎯 {doctor['Specialist']}",
                        theme_text_color="Secondary"
                    ))
                    doctor_card.add_widget(MDLabel(
                        text=f"💼 {doctor['Experience']} years experience",
                        theme_text_color="Secondary"
                    ))
                    doctor_card.add_widget(MDLabel(
                        text=f"📞 {doctor['Contact']}",
                        theme_text_color="Secondary"
                    ))
                    
                    self.results_layout.add_widget(doctor_card)
            else:
                no_results_card = MDCard(
                    orientation="vertical",
                    padding=dp(30),
                    size_hint_y=None,
                    height=dp(120),
                    elevation=2,
                    radius=[dp(10),]
                )
                no_results_card.add_widget(MDLabel(
                    text="No specialists found",
                    theme_text_color="Secondary",
                    halign="center",
                    font_style="H6"
                ))
                no_results_card.add_widget(MDLabel(
                    text="Try adjusting your search criteria or location",
                    theme_text_color="Secondary",
                    halign="center"
                ))
                self.results_layout.add_widget(no_results_card)
        else:
            error_card = MDCard(
                orientation="vertical",
                padding=dp(30),
                size_hint_y=None,
                height=dp(120),
                elevation=2,
                radius=[dp(10),]
            )
            error_card.add_widget(MDLabel(
                text="Condition not recognized",
                theme_text_color="Error",
                halign="center",
                font_style="H6"
            ))
            error_card.add_widget(MDLabel(
                text="Please check your input or try different symptoms",
                theme_text_color="Secondary",
                halign="center"
            ))
            self.results_layout.add_widget(error_card)

class ProfessionalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "500"
        
        sm = ScreenManager()
        sm.add_widget(ProfessionalRoleScreen(name="professional_role"))
        sm.add_widget(ProfessionalLoginScreen(name="professional_login"))
        sm.add_widget(ProfessionalDoctorDashboard(name="professional_doctor_dashboard"))
        sm.add_widget(ProfessionalPatientDashboard(name="professional_patient_dashboard"))
        sm.add_widget(ProfessionalResultsScreen(name="professional_results"))
        
        return sm

if __name__ == "__main__":
    ProfessionalApp().run()