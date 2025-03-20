import json
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner  # ✅ Correct
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import requests
import psutil
import socket
import platform
import cpuinfo
import os
import winreg
import datetime
from kivymd.app import MDApp  # ✅ Assure-toi que MDApp est bien importé
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout  # ✅ MDBoxLayout pour KivyM

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar  # ✅ Correct







# Configuration de la fenêtre
Window.clearcolor = get_color_from_hex("#F5F5F5")  # Fond clair

# Couleurs modernes
PRIMARY_COLOR = get_color_from_hex("#6200EE")  # Violet
SECONDARY_COLOR = get_color_from_hex("#03DAC6")  # Turquoise
BACKGROUND_COLOR = get_color_from_hex("#FFFFFF")  # Blanc
TEXT_COLOR = get_color_from_hex("#000000")  # Noir
ERROR_COLOR = get_color_from_hex("#B00020")  # Rouge

# Variables globales pour stocker les tokens et le timer
refresh_token = None
access_token = None
inactivity_timer = None

# Classe pour l'icône de notification
class NotificationIcon(ButtonBehavior, Image):
    pass

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.selected_ticket_id = None
        self.username = None

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.tabs = TabbedPanel(do_default_tab=False, background_color=BACKGROUND_COLOR)
        self.root.add_widget(self.tabs)

        # Onglet d'inscription
        self.register_tab = TabbedPanelItem(text='Inscription', background_normal='', background_down='')
        self.register_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.register_tab.add_widget(self.register_layout)

        self.entry_username = TextInput(
            hint_text='Nom d\'utilisateur',
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.register_layout.add_widget(self.entry_username)

        self.entry_email = TextInput(
            hint_text='Email',
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.register_layout.add_widget(self.entry_email)

        self.entry_password = TextInput(
            hint_text='Mot de passe',
            password=True,
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.register_layout.add_widget(self.entry_password)

        self.entry_confirm_password = TextInput(
            hint_text='Confirmer le mot de passe',
            password=True,
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.register_layout.add_widget(self.entry_confirm_password)

        self.btn_register = Button(
            text='S\'inscrire',
            size_hint_y=None,
            height=dp(50),
            background_color=PRIMARY_COLOR,
            color=BACKGROUND_COLOR,
            background_normal='',
            bold=True
        )
        self.btn_register.bind(on_press=self.register_user)
        self.register_layout.add_widget(self.btn_register)

        self.loading_label = Label(text='', color=PRIMARY_COLOR)
        self.register_layout.add_widget(self.loading_label)

        self.tabs.add_widget(self.register_tab)

        # Onglet de connexion
        self.login_tab = TabbedPanelItem(text='Connexion', background_normal='', background_down='')
        self.login_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.login_tab.add_widget(self.login_layout)

        self.entry_login_username = TextInput(
            hint_text='Nom d\'utilisateur',
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.login_layout.add_widget(self.entry_login_username)

        self.entry_login_password = TextInput(
            hint_text='Mot de passe',
            password=True,
            size_hint_y=None,
            height=dp(40),
            background_color=BACKGROUND_COLOR,
            foreground_color=TEXT_COLOR,
            hint_text_color=get_color_from_hex("#888888")
        )
        self.login_layout.add_widget(self.entry_login_password)

        self.btn_login = Button(
            text='Se connecter',
            size_hint_y=None,
            height=dp(50),
            background_color=PRIMARY_COLOR,
            color=BACKGROUND_COLOR,
            background_normal='',
            bold=True
        )
        self.btn_login.bind(on_press=self.login_user)
        self.login_layout.add_widget(self.btn_login)

        self.loading_label_login = Label(text='', color=PRIMARY_COLOR)
        self.login_layout.add_widget(self.loading_label_login)

        self.tabs.add_widget(self.login_tab)

        return self.root

    # Méthodes existantes
    def fetch_notifications(self):
        try:
            api_url = "http://127.0.0.1:8000/api/auth/maintenance/alerts/"
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                notifications = response.json().get("alerts", [])
                return [f"{alert['equipment']} - {alert['message']}" for alert in notifications]
            else:
                print(f"Erreur lors de la récupération des notifications : {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Impossible de se connecter à l'API : {e}")

        return []

    def show_notifications(self, instance):
        notifications = self.fetch_notifications()

        # Créer une popup pour afficher les notifications
        popup = Popup(title="Notifications", size_hint=(0.8, 0.8))
        content = BoxLayout(orientation='vertical')

        if notifications:
            scroll_view = ScrollView()
            grid_layout = GridLayout(cols=1, size_hint_y=None)
            grid_layout.bind(minimum_height=grid_layout.setter('height'))

            for notification in notifications:
                notification_label = Label(text=notification, size_hint_y=None, height=40)
                grid_layout.add_widget(notification_label)

            scroll_view.add_widget(grid_layout)
            content.add_widget(scroll_view)
        else:
            content.add_widget(Label(text="Aucune notification."))

        btn_close = Button(text="Fermer", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)

        popup.content = content
        popup.open()

    def update_notification_icon(self):
        notifications = self.fetch_notifications()
        if notifications:
            self.notification_icon.opacity = 1  # Afficher l'icône
        else:
            self.notification_icon.opacity = 0  # Masquer l'icône

    def get_installed_apps(self):
        apps = []
        if platform.system() == "Windows":
            reg_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ]

            for reg_path in reg_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg_key:
                        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(reg_key, i)
                                with winreg.OpenKey(reg_key, subkey_name) as subkey:
                                    try:
                                        app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                        app_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                        app_publisher, _ = winreg.QueryValueEx(subkey, "Publisher")
                                        apps.append({
                                            "name": app_name,
                                            "version": app_version,
                                            "publisher": app_publisher
                                        })
                                    except FileNotFoundError:
                                        continue
                            except FileNotFoundError:
                                continue
                except Exception as e:
                    print(f"Erreur lors de la récupération des applications depuis {reg_path}: {e}")

            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as reg_key:
                    for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(reg_key, i)
                            with winreg.OpenKey(reg_key, subkey_name) as subkey:
                                try:
                                    app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                    app_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                    app_publisher, _ = winreg.QueryValueEx(subkey, "Publisher")
                                    apps.append({
                                        "name": app_name,
                                        "version": app_version,
                                        "publisher": app_publisher
                                    })
                                except FileNotFoundError:
                                    continue
                        except FileNotFoundError:
                            continue
            except Exception as e:
                print(f"Erreur lors de la récupération des applications depuis HKEY_CURRENT_USER: {e}")

        else:
            self.show_popup("Attention", "Cette fonctionnalité est uniquement disponible sur Windows.")
        return apps

    def update_online_status(self, username, is_online):
        try:
            api_url = "http://127.0.0.1:8000/api/auth/update_online_status/"
            data = {
                "username": username,
                "is_online": is_online
            }
            response = requests.post(api_url, json=data, timeout=10)

            if response.status_code != 200:
                print(f"Erreur lors de la mise à jour de l'état en ligne : {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Impossible de se connecter à l'API : {e}")

    def refresh_access_token(self):
        global refresh_token, access_token

        try:
            api_url = "http://127.0.0.1:8000/api/auth/api/token/refresh/"
            data = {"refresh": refresh_token}
            response = requests.post(api_url, json=data, timeout=10)

            if response.status_code == 200:
                # Mettre à jour les tokens
                access_token = response.json().get("access")
                refresh_token = response.json().get("refresh")
                return True
            else:
                self.show_popup("Erreur", f"Échec du rafraîchissement du token : {response.json()}")
                return False
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")
            return False

    def logout_user(self):
        global refresh_token, access_token, inactivity_timer
        username = self.entry_login_username.text.strip()
        try:
            # Rafraîchir le token avant la déconnexion
            if not self.refresh_access_token():
                self.show_popup("Erreur", "Impossible de rafraîchir le token. Déconnexion impossible.")
                return

            # Envoyer une requête POST à l'API pour déconnecter l'utilisateur
            api_url = "http://127.0.0.1:8000/api/auth/logout/"
            headers = {
                "Authorization": f"Bearer {access_token}"  # Inclure le token d'accès pour l'authentification
            }
            data = {"refresh": refresh_token}  # Utilisez le refresh token rafraîchi
            response = requests.post(api_url, json=data, headers=headers, timeout=10)

            if response.status_code == 205:  # HTTP 205 Reset Content
                self.return_to_login()  # Rediriger vers la page de connexion
                # Mettre à jour l'état en ligne dans Django
                self.update_online_status(username, False)
            else:
                self.show_popup("Erreur", f"Échec de la déconnexion : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")
        finally:
            # Réinitialiser le timer d'inactivité
            if inactivity_timer:
                Clock.unschedule(inactivity_timer)
            inactivity_timer = None

    def reset_inactivity_timer(self):
        global inactivity_timer

        # Annuler le timer existant
        if inactivity_timer:
            Clock.unschedule(inactivity_timer)

        # Obtenir l'heure actuelle
        now = datetime.datetime.now()

        # Définir l'heure de déconnexion à 15h30
        logout_time = now.replace(hour=15, minute=30, second=0, microsecond=0)

        # Si l'heure de déconnexion est déjà passée pour aujourd'hui, la définir pour le lendemain
        if now >= logout_time:
            logout_time += datetime.timedelta(days=1)

        # Calculer le temps restant en secondes
        time_remaining = (logout_time - now).total_seconds()

        # Redémarrer le timer pour l'heure de déconnexion
        inactivity_timer = Clock.schedule_once(lambda dt: self.logout_user(), time_remaining)

    def show_welcome_page(self, username, installed_apps):
        self.root.clear_widgets()

        # Récupérer les tickets
        self.fetch_tickets()  # Cette méthode définit maintenant self.tickets

        self.category = "Choisir une catégorie"
        self.status = "Ouvert"  # Statut par défaut
        self.priorite = "Moyenne"  # Priorité par défaut

        # ✅ Création du Layout principal
        main_layout = MDBoxLayout(orientation='horizontal', padding=10, spacing=10)
        self.root.add_widget(main_layout)

        # ------------------------ PARTIE GAUCHE : Applications ------------------------
        left_layout = MDBoxLayout(orientation='vertical', size_hint=(0.5, 1), padding=10, spacing=10)
        main_layout.add_widget(left_layout)

        # ✅ Barre d'outils avec MDTopAppBar
        toolbar = MDTopAppBar(
            title=f"Bienvenue {username} - JESSMI",
            right_action_items=[["bell", lambda x: self.show_notifications()]],
            elevation=4
        )
        left_layout.add_widget(toolbar)

        # ✅ Liste des applications installées
        apps_label = MDLabel(text="📌 Applications installées", font_style="H6", bold=True, theme_text_color="Primary")
        left_layout.add_widget(apps_label)

        scroll_view = ScrollView()
        grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for app in installed_apps:
            card = MDCard(size_hint=(1, None), height=80, padding=10)
            card_layout = MDBoxLayout(orientation='vertical')

            app_info = f"[b]{app['name']}[/b]\nVersion: {app['version']} - Éditeur: {app['publisher']}"
            label = MDLabel(text=app_info, markup=True, theme_text_color="Secondary")
            card_layout.add_widget(label)

            card.add_widget(card_layout)
            grid_layout.add_widget(card)

        scroll_view.add_widget(grid_layout)
        left_layout.add_widget(scroll_view)

        # ✅ Boutons d'action
        button_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        left_layout.add_widget(button_layout)

        btn_logout = MDRaisedButton(text="Déconnexion", md_bg_color=(1, 0.3, 0.3, 1))
        btn_logout.bind(on_press=lambda instance: [self.logout_user(), self.reset_inactivity_timer()])
        button_layout.add_widget(btn_logout)

        btn_return = MDRaisedButton(text="Retour", md_bg_color=(0.2, 0.6, 1, 1))
        btn_return.bind(on_press=self.return_to_login)
        button_layout.add_widget(btn_return)

        # ------------------------ PARTIE DROITE : Tickets ------------------------
        right_layout = MDBoxLayout(orientation='vertical', size_hint=(0.5, 1), padding=10, spacing=10)
        main_layout.add_widget(right_layout)

        ticket_label = MDLabel(text="🎫 Tickets", font_style="H6", bold=True, theme_text_color="Primary")
        right_layout.add_widget(ticket_label)

        self.ticket_title_input = MDTextField(hint_text='Titre du ticket', mode="rectangle")
        right_layout.add_widget(self.ticket_title_input)

        self.ticket_description_input = MDTextField(hint_text='Description du ticket', multiline=True, mode="rectangle")
        right_layout.add_widget(self.ticket_description_input)

        # ✅ Sélecteur de catégorie avec MDDropdownMenu
        categories = ["réseau", "logiciel", "matériel", "sécurité"]

        # Champ de texte qui affiche la catégorie sélectionnée
        self.ticket_categorie_input = MDTextField(
            hint_text='Catégorie du ticket',
            mode="rectangle",
            readonly=True  # Empêche la saisie manuelle
        )
        right_layout.add_widget(self.ticket_categorie_input)

        # Création du menu déroulant
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": category,
                "on_release": lambda x=category: self.set_category(x),
            } for category in categories
        ]

        self.ticket_categorie_menu = MDDropdownMenu(
            caller=self.ticket_categorie_input,
            items=menu_items,
            width_mult=4
        )

        # Ajout d'un événement au champ pour ouvrir le menu
        self.ticket_categorie_input.bind(focus=self.open_category_menu)

        # ✅ Sélecteur de statut avec MDDropdownMenu:

        statuts = ["ouvert", "en_cours", "résolu", "fermé"]

        # Champ de texte qui affiche la catégorie sélectionnée
        self.ticket_statut_input = MDTextField(
            hint_text='Statut du ticket',
            mode="rectangle",
            readonly=True  # Empêche la saisie manuelle
        )
        right_layout.add_widget(self.ticket_statut_input)

        # Création du menu déroulant
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": status,
                "on_release": lambda x=status: self.set_status(x),
            } for status in statuts
        ]

        self.ticket_statut_menu = MDDropdownMenu(
            caller=self.ticket_statut_input,
            items=menu_items,
            width_mult=4
        )

        # Ajout d'un événement au champ pour ouvrir le menu
        self.ticket_statut_input.bind(focus=self.open_status_menu)

        # ✅ Sélecteur de priorité avec MDDropdownMenu:

        prioriti = ["faible", "normal", "élevé", "urgent"]

        # Champ de texte qui affiche la catégorie sélectionnée
        self.ticket_priorite_input = MDTextField(
            hint_text='Priorite du ticket',
            mode="rectangle",
            readonly=True  # Empêche la saisie manuelle
        )
        right_layout.add_widget(self.ticket_priorite_input)

        # Création du menu déroulant
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": prioriti,
                "on_release": lambda x=prioriti: self.set_priority(x),
            } for prioriti in prioriti
        ]

        self.ticket_priority_menu = MDDropdownMenu(
            caller=self.ticket_priorite_input,
            items=menu_items,
            width_mult=4
        )

        # Ajout d'un événement au champ pour ouvrir le menu
        self.ticket_priorite_input.bind(focus=self.open_priority_menu)

        # ✅ Boutons d'action pour tickets
        btn_create_ticket = MDRaisedButton(text="Créer un ticket", md_bg_color=(0.2, 0.6, 1, 1))
        btn_create_ticket.bind(on_press=self.create_ticket)
        right_layout.add_widget(btn_create_ticket)

        """btn_show_comments = MDRaisedButton(text="Afficher les commentaires", md_bg_color=(0.2, 0.8, 0.2, 1))
        btn_show_comments.bind(on_press=self.show_comments)
        right_layout.add_widget(btn_show_comments)"""

        # Bouton pour afficher les commentaires
        btn_show_commentaires = MDRaisedButton(
            text="Afficher les commentaires",
            md_bg_color=(0.2, 0.8, 0.2, 1)
        )
        btn_show_commentaires.bind(on_press=self.show_all_commentaires)  # Lier à la méthode show_all_commentaires
        right_layout.add_widget(btn_show_commentaires)

        btn_show_attachments = MDRaisedButton(text="Afficher les pièces jointes", md_bg_color=(0.8, 0.2, 0.2, 1))
        btn_show_attachments.bind(on_press=self.show_attachments)
        right_layout.add_widget(btn_show_attachments)

        """btn_select_ticket = MDRaisedButton(text="Sélectionner un ticket", md_bg_color=(1, 0.6, 0.2, 1))
        btn_select_ticket.bind(on_press=self.select_ticket)
        right_layout.add_widget(btn_select_ticket)"""

        # ✅ Liste des tickets existants
        ticket_scroll_view = ScrollView()
        self.ticket_grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.ticket_grid_layout.bind(minimum_height=self.ticket_grid_layout.setter('height'))
        ticket_scroll_view.add_widget(self.ticket_grid_layout)
        right_layout.add_widget(ticket_scroll_view)

        # ✅ Icône de notification cachée au départ
        self.notification_icon = MDIconButton(
            icon="bell",
            pos_hint={"center_x": 0.9, "center_y": 0.9},
            on_release=lambda x: self.show_notifications()
        )
        self.notification_icon.opacity = 0

        # ✅ Redémarrer le timer d'inactivité et récupérer les tickets
        self.reset_inactivity_timer()
        self.update_notification_icon()
        Clock.schedule_interval(lambda dt: self.update_notification_icon(), 300)
        self.fetch_tickets()

    def show_all_commentaires(self, instance):
        # Vérifier si des tickets existent
        if not hasattr(self, 'tickets') or not self.tickets:
            self.show_popup("Aucun commentaire", "Aucun ticket disponible.")
            return

        # Récupérer tous les commentaires de tous les tickets
        all_commentaires = []
        for ticket in self.tickets:
            ticket_id = ticket['id']
            commentaires = self.get_commentaires_for_ticket(ticket_id)  # Récupérer les commentaires pour ce ticket
            all_commentaires.extend(commentaires)

        # Créer un layout pour le popup
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Ajouter un label pour le titre
        title_label = Label(text="Commentaires", size_hint_y=None, height=40, font_size=20, bold=True)
        popup_layout.add_widget(title_label)

        # Créer un ScrollView pour contenir les commentaires
        scroll_view = ScrollView()
        commentaires_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        commentaires_layout.bind(minimum_height=commentaires_layout.setter('height'))

        # Ajouter chaque commentaire dans le layout
        for commentaire in all_commentaires:
            commentaire_label = Label(text=commentaire, size_hint_y=None, height=40, halign='left', valign='middle')
            commentaires_layout.add_widget(commentaire_label)

        scroll_view.add_widget(commentaires_layout)
        popup_layout.add_widget(scroll_view)

        # Créer le popup
        popup = Popup(title='Commentaires', content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

    def get_selected_ticket(self):
        # Simule la récupération du ticket sélectionné
        if self.ticket_grid_layout.children:
            return {"title": "Exemple de ticket", "status": "Ouvert", "priority": "Moyenne"}
        return None

    def create_ticket(self, instance):
        title = self.ticket_title_input.text
        description = self.ticket_description_input.text
        category = self.ticket_categorie_input.text
        status = self.ticket_statut_input.text
        priority = self.ticket_priorite_input.text


        if not title or not description or category == "Sélectionner une catégorie":
            print("Veuillez remplir tous les champs obligatoires.")
            return

        print(f"✅ Ticket créé : {title} | {category} | {status} | {priority}")



    def open_category_menu(self, instance, value):
        """Ouvre le menu déroulant quand le champ est sélectionné"""
        if value:  # Si l'utilisateur clique sur le champ
            self.ticket_categorie_menu.open()

    def set_category(self, category):
        """Définit la catégorie sélectionnée dans le champ"""
        self.ticket_categorie_input.text = category
        self.ticket_categorie_menu.dismiss()

    """statut"""
    def open_status_menu(self, instance, value):
        """Ouvre le menu déroulant quand le champ est sélectionné"""
        if value:  # Si l'utilisateur clique sur le champ
            self.ticket_statut_menu.open()

    def set_status(self, status):
        """Définit la catégorie sélectionnée dans le champ"""
        self.ticket_statut_input.text = status
        self.ticket_statut_menu.dismiss()

    """priorite"""

    def open_priority_menu(self, instance, value):
        """Ouvre le menu déroulant quand le champ est sélectionné"""
        if value:  # Si l'utilisateur clique sur le champ
            self.ticket_priority_menu.open()

    def set_priority(self, priority):
        """Définit la catégorie sélectionnée dans le champ"""
        self.ticket_priorite_input.text = priority
        self.ticket_priority_menu.dismiss()


    """def show_comments(self, instance):
        if not self.selected_ticket_id:
            self.show_popup("Erreur", "Aucun ticket sélectionné.")
            return

        # Créer une popup pour afficher les commentaires
        popup = Popup(title="Commentaires", size_hint=(0.8, 0.8))
        content = BoxLayout(orientation='vertical')

        scroll_view = ScrollView()
        grid_layout = GridLayout(cols=1, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Récupérer les commentaires depuis l'API
        try:
            api_url = f"http://127.0.0.1:8000/api/auth/tickets/{self.selected_ticket_id}/commentaires/"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                commentaires = response.json()
                for commentaire in commentaires:
                    # Afficher uniquement les commentaires de l'utilisateur connecté
                    if commentaire['auteur'] == self.username:
                        commentaire_info = (
                            f"Commentaire sur le ticket {commentaire['ticket_titre']}:\n"  # Utiliser ticket_titre
                            f"{commentaire['contenu']}\n"
                            f"Date: {commentaire['date_creation']}"
                        )
                        commentaire_label = Label(text=commentaire_info, size_hint_y=None, height=100)
                        grid_layout.add_widget(commentaire_label)
            else:
                self.show_popup("Erreur", f"Échec de la récupération des commentaires : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")

        scroll_view.add_widget(grid_layout)
        content.add_widget(scroll_view)

        btn_close = Button(text="Fermer", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)

        popup.content = content
        popup.open()"""

    def show_commentaires(self, instance, ticket_id):
        commentaires = self.get_commentaires_for_ticket(ticket_id)  # Récupérer les commentaires pour ce ticket

        # Créer un layout pour le popup
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Ajouter un label pour le titre
        title_label = Label(text="Commentaires", size_hint_y=None, height=40, font_size=20, bold=True)
        popup_layout.add_widget(title_label)

        # Créer un ScrollView pour contenir les commentaires
        scroll_view = ScrollView()
        commentaires_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        commentaires_layout.bind(minimum_height=commentaires_layout.setter('height'))

        # Ajouter chaque commentaire dans le layout
        for commentaire in commentaires:
            commentaire_label = Label(text=commentaire, size_hint_y=None, height=40, halign='left', valign='middle')
            commentaires_layout.add_widget(commentaire_label)

        scroll_view.add_widget(commentaires_layout)
        popup_layout.add_widget(scroll_view)

        # Créer le popup
        popup = Popup(title='Commentaires', content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

    def get_commentaires_for_ticket(self, ticket_id):
        # URL de l'API Django pour récupérer les commentaires d'un ticket
        api_url = f"http://127.0.0.1:8000/api/auth/tickets/{ticket_id}/commentaires/"
        headers = {
            "Authorization": f"Bearer {access_token}"  # Utiliser le token d'accès pour l'authentification
        }

        try:
            # Faire une requête GET à l'API Django
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Vérifier si la requête a réussi

            # Convertir la réponse JSON en liste de commentaires
            commentaires_data = response.json()
            commentaires = [
                f"{commentaire['auteur']} ({commentaire['date_creation']}): {commentaire['contenu']}"
                for commentaire in commentaires_data
            ]
            return commentaires
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des commentaires : {e}")
            return []


    def show_attachments(self, instance):
        if not self.selected_ticket_id:
            self.show_popup("Erreur", "Aucun ticket sélectionné.")
            return

        # Créer une popup pour afficher les pièces jointes
        popup = Popup(title="Pièces jointes", size_hint=(0.8, 0.8))
        content = BoxLayout(orientation='vertical')

        scroll_view = ScrollView()
        grid_layout = GridLayout(cols=1, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Récupérer les pièces jointes depuis l'API
        try:
            api_url = f"http://127.0.0.1:8000/api/auth/tickets/{self.selected_ticket_id}/pieces_jointes/"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                pieces_jointes = response.json()
                for piece_jointe in pieces_jointes:
                    # Afficher uniquement les pièces jointes de l'utilisateur connecté
                    if piece_jointe['auteur'] == self.username:
                        piece_jointe_info = f"Pièce jointe: {piece_jointe['fichier']}"
                        piece_jointe_label = Label(text=piece_jointe_info, size_hint_y=None, height=50)
                        grid_layout.add_widget(piece_jointe_label)
            else:
                self.show_popup("Erreur", f"Échec de la récupération des pièces jointes : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")

        scroll_view.add_widget(grid_layout)
        content.add_widget(scroll_view)

        btn_close = Button(text="Fermer", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)

        popup.content = content
        popup.open()

    def get_machine_info(self):
        try:
            os_name = platform.system()  # Windows, Linux, Mac
            os_version = platform.release()  # Version (ex: 10 pour Windows)
            hostname = socket.gethostname()  # Nom de la machine
            ip_address = socket.gethostbyname(hostname)  # Adresse IP locale

            # Récupérer l'adresse MAC de la première interface réseau
            mac_address = None
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        mac_address = addr.address
                        break
                if mac_address:
                    break

            # Récupérer le nombre de cœurs du CPU
            cpu_cores = psutil.cpu_count(logical=False)  # Nombre de cœurs physiques

            # Récupérer les informations détaillées du processeur
            cpu_info_data = cpuinfo.get_cpu_info()
            cpu_brand = cpu_info_data.get('brand_raw', 'Unknown')  # Exemple: "Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz"
            cpu_freq = psutil.cpu_freq().current / 1000  # Fréquence en GHz

            # Extraire le modèle et la génération du processeur
            cpu_model = "Unknown"
            cpu_generation = "Unknown"
            if "Intel" in cpu_brand:
                parts = cpu_brand.split()
                for part in parts:
                    if part.startswith("i3") or part.startswith("i5") or part.startswith("i7") or part.startswith("i9"):
                        cpu_model = part
                    if "Gen" in part:
                        cpu_generation = part

            # Ajouter le nombre de cœurs à os_name
            os_name = f"{os_name} {cpu_cores}C {cpu_model} {cpu_generation}"  # Exemple : "Windows 4C i5 8th Gen"

            # Récupérer la quantité de RAM en Go
            ram_info = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # RAM en Go

            # Récupérer le nombre de cartes réseau et Wi-Fi
            network_cards = 0
            wifi_cards = 0
            for interface, addrs in psutil.net_if_addrs().items():
                if "wifi" in interface.lower() or "wireless" in interface.lower():
                    wifi_cards += 1
                else:
                    network_cards += 1

            return {
                "hostname": hostname,
                "os_name": os_name,
                "os_version": os_version,
                "ip_address": ip_address,
                "mac_address": mac_address,
                "cpu_info": cpu_brand,  # Nom du processeur (optionnel)
                "cpu_freq": cpu_freq,  # Fréquence en GHz (optionnel)
                "ram_info": ram_info,
                "network_cards": network_cards,
                "wifi_cards": wifi_cards,
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des infos machine: {e}")
            return None

    def clear_fields(self):
        self.entry_username.text = ''
        self.entry_email.text = ''
        self.entry_password.text = ''
        self.entry_confirm_password.text = ''

    def register_user(self, instance):
        username = self.entry_username.text.strip()
        email = self.entry_email.text.strip()
        password = self.entry_password.text.strip()
        confirm_password = self.entry_confirm_password.text.strip()

        # Vérification des champs obligatoires
        if not username or not email or not password or not confirm_password:
            self.show_popup("Erreur", "Tous les champs sont obligatoires !")
            return

        # Vérification de la correspondance des mots de passe
        if password != confirm_password:
            self.show_popup("Erreur", "Les mots de passe ne correspondent pas !")
            return

        # Désactiver le bouton pour éviter les clics multiples
        self.btn_register.disabled = True
        self.loading_label.text = "Envoi en cours..."
        self.loading_label.color = (0, 0, 1, 1)

        # Récupération des infos de la machine
        machine_info = self.get_machine_info()
        if not machine_info:
            self.show_popup("Erreur", "Impossible de récupérer les infos de la machine.")
            self.btn_register.disabled = False
            self.loading_label.text = ""
            return

        # 📤 Envoi des données à l'API Django
        api_url = "http://127.0.0.1:8000/api/auth/register/"  # URL de l'API Django
        data = {
            "username": username,
            "email": email,
            "password": password,
            "hostname": machine_info["hostname"],
            "os_name": machine_info["os_name"],
            "os_version": machine_info["os_version"],
            "ip_address": machine_info["ip_address"],
            "mac_address": machine_info["mac_address"],
            "cpu_info": machine_info["cpu_info"],
            "cpu_freq": machine_info["cpu_freq"],
            "ram_info": machine_info["ram_info"],
            "network_cards": machine_info["network_cards"],
            "wifi_cards": machine_info["wifi_cards"],
        }

        try:
            response = requests.post(api_url, json=data, timeout=40)  # Augmenter le timeout à 10 secondes
            if response.status_code == 201:
                self.show_popup("Succès", "Utilisateur enregistré avec succès !")
                self.clear_fields()  # Vider les champs après un enregistrement réussi
            else:
                self.show_popup("Erreur", f"Échec de l'enregistrement : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")
        finally:
            self.btn_register.disabled = False
            self.loading_label.text = ""

    def return_to_login(self, instance=None):
        # Masquer tous les widgets de la fenêtre actuelle
        self.root.clear_widgets()
        self.root.add_widget(self.tabs)

    def login_user(self, instance):
        global refresh_token, access_token  # Déclarer les variables globales au début de la fonction

        username = self.entry_login_username.text.strip()
        password = self.entry_login_password.text.strip()

        if not username or not password:
            self.show_popup("Erreur", "Tous les champs sont obligatoires !")
            return

        self.btn_login.disabled = True
        self.loading_label_login.text = "Connexion en cours..."
        self.loading_label_login.color = (0, 0, 1, 1)

        # Récupérer les applications installées
        installed_apps = self.get_installed_apps()

        # Données à envoyer à l'API
        data = {
            "username": username,
            "password": password,
            "installed_apps": installed_apps  # Inclure les applications installées
        }

        try:
            # Envoyer les données à l'API Django
            api_url = "http://127.0.0.1:8000/api/auth/login/"
            response = requests.post(api_url, json=data, timeout=10)

            if response.status_code == 200:
                # Stocker le refresh token et le token d'accès
                refresh_token = response.json().get("refresh")
                access_token = response.json().get("access")

                # Stocker le nom d'utilisateur dans l'attribut de la classe
                self.username = username

                # Afficher la page de bienvenue après une connexion réussie
                self.show_welcome_page(username, installed_apps)
                # Mettre à jour l'état en ligne dans Django
                self.update_online_status(username, True)

                # Redémarrer le timer d'inactivité
                self.reset_inactivity_timer()
            else:
                self.show_popup("Erreur", f"Échec de la connexion : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")
        finally:
            self.btn_login.disabled = False
            self.loading_label_login.text = ""

    def create_ticket(self, instance):
        # Vérifier que self.username est défini
        if not hasattr(self, 'username') or not self.username:
            self.show_popup("Erreur", "Utilisateur non connecté.")
            return

        # Récupérer le titre sélectionné et la description du ticket
        title = self.ticket_title_input.text.strip()
        description = self.ticket_description_input.text.strip()
        self.selected_categorie = ""  # Stocke la catégorie sélectionnée
        self.selected_statut = ""  # Stocke le statut sélectionné
        self.selected_priorite = ""  # Stocke la priorité sélectionnée

        # Vérifier que les champs ne sont pas vides
        if (title == 'Choisir une catégorie' or not description or
                self.ticket_categorie_input.text == 'Choisir une catégorie' or
                self.ticket_statut_input.text == 'Choisir un statut' ):
            self.show_popup("Erreur", "Veuillez remplir tous les champs.")
            return

        # Données du ticket à envoyer à l'API
        ticket_data = {
            "title": title,
            "description": description,
            "categorie": self.ticket_categorie_input.text,  # Catégorie sélectionnée
            "statut": self.ticket_statut_input.text,  # Statut sélectionné
            "priorite": self.ticket_priorite_input.text,  # Priorité sélectionnée

            "owner": self.username,  # Utilisateur connecté
        }

        try:
            api_url = "http://127.0.0.1:8000/api/auth/tickets/"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.post(api_url, json=ticket_data, headers=headers, timeout=10)

            if response.status_code == 201:
                self.show_popup("Succès", "Ticket créé avec succès !")
                self.ticket_title_input.text = ''  # Effacer le champ titre
                self.ticket_description_input.text = ''  # Effacer le champ description
                self.fetch_tickets()  # Rafraîchir la liste des tickets
            else:
                self.show_popup("Erreur", f"Échec de la création du ticket : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")

    def fetch_tickets(self):
        try:
            # Récupérer les tickets depuis l'API Django
            api_url = "http://127.0.0.1:8000/api/auth/tickets/"
            headers = {
                "Authorization": f"Bearer {access_token}"  # Utiliser le token d'accès pour l'authentification
            }
            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                self.tickets = response.json()
                print(f"Tickets récupérés : {self.tickets}")  # Débogage
            else:
                self.show_popup("Erreur", f"Échec de la récupération des tickets : {response.json()}")
        except requests.exceptions.RequestException as e:
            self.show_popup("Erreur", f"Impossible de se connecter à l'API : {e}")

    """def display_tickets(self, tickets):
        # Effacer les tickets actuels
        self.ticket_grid_layout.clear_widgets()

        # Ajouter chaque ticket à l'interface utilisateur
        for ticket in tickets:
            ticket_info = (
                f"Titre: {ticket['title']}\n"
                f"Description: {ticket['description']}\n"
                f"Catégorie: {ticket['categorie']}\n"
                f"Statut: {ticket['statut']}\n"
                f"Priorité: {ticket['priorite']}\n"
                f"Créé par: {ticket['owner']}\n"
                f"Date: {ticket['date_creation']}"
            )
            ticket_label = Label(text=ticket_info, size_hint_y=None, height=150)

            # Ajouter un bouton pour sélectionner le ticket
            btn_select_ticket = Button(
                text="Sélectionner ce ticket",
                size_hint_y=None,
                height=40,
                background_color=(0.2, 0.6, 1, 1),  # Couleur de fond (bleu clair)
                color=(1, 1, 1, 1)  # Couleur du texte (blanc)
            )
            btn_select_ticket.bind(on_press=lambda instance, t=ticket: self.select_ticket(t))

            # Ajouter le label et le bouton au layout
            self.ticket_grid_layout.add_widget(ticket_label)
            self.ticket_grid_layout.add_widget(btn_select_ticket)"""

    def display_tickets(self, tickets):
        # Vérifier si la liste des tickets est vide
        if not tickets:
            print("Aucun ticket à afficher.")
            return

        # Parcourir chaque ticket et l'afficher
        for ticket in tickets:
            print(f"Ticket ID: {ticket['id']}, Titre: {ticket['title']}, Description: {ticket['description']}")

    """def select_ticket(self, ticket):
        if isinstance(ticket, str):  # Vérifie si c'est une chaîne JSON
            try:
                ticket = json.loads(ticket)  # Convertir en dict
            except json.JSONDecodeError:
                print("Erreur : Ticket JSON invalide :", ticket)
                self.show_popup("Erreur", "Format JSON invalide.")
                return

        if isinstance(ticket, dict) and 'id' in ticket and 'title' in ticket:
            self.selected_ticket_id = ticket['id']
            self.show_popup("Ticket sélectionné", f"Ticket {ticket['title']} sélectionné.")
        else:
            print("Données du ticket invalides :", ticket)  # Afficher les données invalides
            self.show_popup("Erreur", "Données du ticket invalides.")"""

    def show_popup(self, title, message):
        popup = Popup(title=title, size_hint=(0.8, 0.4))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        btn_close = Button(text="Fermer", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)
        popup.content = content
        popup.open()

if __name__ == '__main__':
    MyApp().run()