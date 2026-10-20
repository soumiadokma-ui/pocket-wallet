import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "wallet_data.json"

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portefeuille de Poche")
        self.root.geometry("440x560")
        self.root.config(bg="#f4f6f9")
        self.root.resizable(False, False)
        
        self.balance = 0.0
        self.transactions = []
        
        self.load_data()
        self.create_widgets()
        self.populate_history()
        
    def create_widgets(self):
        # 1. En-tête
        header_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Portefeuille de Poche", fg="white", bg="#2c3e50", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # 2. Carte du Solde
        balance_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        balance_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(balance_frame, text="Solde Actuel:", fg="#7f8c8d", bg="#ffffff", font=("Arial", 11)).pack(anchor="w")
        self.balance_label = tk.Label(balance_frame, text=f"{self.balance:.2f} DZD", fg="#27ae60", bg="#ffffff", font=("Arial", 24, "bold"))
        self.balance_label.pack(anchor="w", pady=5)
        
        # 3. حقل إدخال المبلغ فقط
        input_frame = tk.Frame(self.root, bg="#f4f6f9", padx=10)
        input_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(input_frame, text="Montant:", bg="#f4f6f9", font=("Arial", 11, "bold"), fg="#34495e").grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 12), bd=1, relief="solid", justify="left")
        self.amount_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # 4. Boutons d'action (Dépôt / Retrait)
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        deposit_btn = tk.Button(btn_frame, text="Dépôt (+)", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", padx=15, pady=8, command=lambda: self.update_wallet('deposit'))
        deposit_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        withdraw_btn = tk.Button(btn_frame, text="Retrait (-)", bg="#c0392b", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", padx=15, pady=8, command=lambda: self.update_wallet('withdraw'))
        withdraw_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
        
        # زر مسح كل المعاملات والبيانات
        clear_btn = tk.Button(self.root, text="Effacer tout (Réinitialiser)", bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", pady=6, command=self.clear_all_data)
        clear_btn.pack(fill=tk.X, padx=20, pady=5)
        
        # 5. Historique (عرض بالإشارتين + و -)
        history_frame = tk.Frame(self.root, bg="#f4f6f9", padx=20)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(history_frame, text="Historique des transactions:", bg="#f4f6f9", fg="#34495e", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)
        
        list_container = tk.Frame(history_frame, bg="#ffffff", bd=1, relief="solid")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.history_listbox = tk.Listbox(list_container, font=("Courier New", 11, "bold"), bg="#ffffff", fg="#2c3e50", bd=0, highlightthickness=0, height=5)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.history_listbox.yview)
        
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.balance = data.get("balance", 0.0)
                    self.transactions = data.get("transactions", [])
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier: {e}")

    def save_data(self):
        data = {
            "balance": self.balance,
            "transactions": self.transactions
        }
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")

    def populate_history(self):
        self.history_listbox.delete(0, tk.END)
        for tx in self.transactions:
            sign = "+" if tx['type'] == "Dépôt" else "-"
            line = f"[{sign}] {tx['amount']} DZD"
            self.history_listbox.insert(0, line)

    def update_wallet(self, action):
        try:
            amount_text = self.amount_entry.get().strip()
            
            if not amount_text:
                messagebox.showwarning("Avertissement", "Veuillez entrer un montant!")
                return
                
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être supérieur à zéro!")
                return
                
            if action == 'deposit':
                self.balance += amount
                trans_type = "Dépôt"
                sign = "+"
            elif action == 'withdraw':
                if amount > self.balance:
                    messagebox.showerror("Erreur", "Solde insuffisant!")
                    return
                self.balance -= amount
                trans_type = "Retrait"
                sign = "-"
                
            tx_data = {
                "type": trans_type,
                "amount": f"{amount:.2f}"
            }
            self.transactions.append(tx_data)
            
            self.save_data()
            
            self.balance_label.config(text=f"{self.balance:.2f} DZD")
            
            line = f"[{sign}] {amount:.2f} DZD"
            self.history_listbox.insert(0, line)
            
            self.amount_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide!")

    def clear_all_data(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir tout effacer ? (Solde et historique)"):
            self.balance = 0.0
            self.transactions = []
            self.save_data()
            
            self.balance_label.config(text="0.00 DZD")
            self.history_listbox.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            messagebox.showinfo("Succès", "Toutes les données ont été effacées.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
