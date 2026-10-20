from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
import json
import os

DATA_FILE = "wallet_data.json"

class WalletRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(WalletRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        self.balance = 0.0
        self.transactions = []
        
        self.load_data()
        
        # 1. عنوان التطبيق
        self.add_widget(Label(
            text="Portefeuille de Poche",
            font_size=24,
            size_hint_y=None,
            height=50,
            bold=True
        ))
        
        # 2. عرض الرصيد الحالي
        self.balance_label = Label(
            text=f"Solde Actuel:\n{self.balance:.2f} DZD",
            font_size=22,
            size_hint_y=None,
            height=80,
            halign='center',
            valign='middle'
        )
        self.balance_label.bind(size=self.balance_label.setter('text_size'))
        self.add_widget(self.balance_label)
        
        # 3. حقل إدخال المبلغ
        self.amount_input = TextInput(
            hint_text="Entrer le montant",
            inputType='number',
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.amount_input)
        
        # 4. أزرار الإيداع والسحب
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        deposit_btn = Button(text="Dépôt (+)", background_color=(0.15, 0.68, 0.37, 1))
        deposit_btn.bind(on_press=lambda x: self.update_wallet('deposit'))
        btn_layout.add_widget(deposit_btn)
        
        withdraw_btn = Button(text="Retrait (-)", background_color=(0.9, 0.3, 0.25, 1))
        withdraw_btn.bind(on_press=lambda x: self.update_wallet('withdraw'))
        btn_layout.add_widget(withdraw_btn)
        
        self.add_widget(btn_layout)
        
        # 5. زر مسح الكل
        clear_btn = Button(text="Effacer tout (Réinitialiser)", size_hint_y=None, height=45, background_color=(0.5, 0.5, 0.5, 1))
        clear_btn.bind(on_press=self.clear_all_data)
        self.add_widget(clear_btn)
        
        # 6. قائمة السجل (Historique)
        self.add_widget(Label(text="Historique des transactions:", size_hint_y=None, height=30, bold=True))
        
        self.history_label = Label(
            text="",
            valign='top',
            halign='left',
            font_size=16
        )
        self.history_label.bind(size=self.history_label.setter('text_size'))
        
        # حاوية المعاملات
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.history_label)
        self.add_widget(scroll)
        
        self.update_history_display()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.balance = data.get("balance", 0.0)
                    self.transactions = data.get("transactions", [])
            except Exception:
                pass

    def save_data(self):
        data = {
            "balance": self.balance,
            "transactions": self.transactions
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_history_display(self):
        lines = []
        for tx in self.transactions:
            sign = "+" if tx['type'] == "Dépôt" else "-"
            lines.append(f"[{sign}] {tx['amount']} DZD")
        self.history_label.text = "\n".join(lines)

    def update_wallet(self, action):
        try:
            val = self.amount_input.text.strip()
            if not val:
                return
            amount = float(val)
            if amount <= 0:
                return
                
            if action == 'deposit':
                self.balance += amount
                t_type = "Dépôt"
            else:
                if amount > self.balance:
                    return
                self.balance -= amount
                t_type = "Retrait"
                
            self.transactions.insert(0, {"type": t_type, "amount": f"{amount:.2f}"})
            self.save_data()
            
            self.balance_label.text = f"Solde Actuel:\n{self.balance:.2f} DZD"
            self.update_history_display()
            self.amount_input.text = ""
        except ValueError:
            pass

    def clear_all_data(self, instance):
        self.balance = 0.0
        self.transactions = []
        self.save_data()
        self.balance_label.text = f"Solde Actuel:\n0.00 DZD"
        self.update_history_display()
        self.amount_input.text = ""

class PocketWalletApp(App):
    def build(self):
        return WalletRoot()

if __name__ == '__main__':
    PocketWalletApp().run()
