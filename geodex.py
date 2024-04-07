import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

class FriendDatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Friend Database App")

        self.deleted_friend = None

        self.create_widgets()
        self.setup_database()

    def create_widgets(self):
        self.name_label = ttk.Label(self.master, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.city_label = ttk.Label(self.master, text="City:")
        self.city_label.grid(row=1, column=0, sticky=tk.W)
        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(self.master, textvariable=self.city_var)
        self.city_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        self.state_label = ttk.Label(self.master, text="State:")
        self.state_label.grid(row=2, column=0, sticky=tk.W)
        self.state_var = tk.StringVar()
        self.state_combobox = ttk.Combobox(self.master, textvariable=self.state_var)
        self.state_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.country_label = ttk.Label(self.master, text="Country:")
        self.country_label.grid(row=3, column=0, sticky=tk.W)
        self.country_var = tk.StringVar()
        self.country_combobox = ttk.Combobox(self.master, textvariable=self.country_var)
        self.country_combobox.grid(row=3, column=1, padx=5, pady=5)

        self.memo_label = ttk.Label(self.master, text="Memo:")
        self.memo_label.grid(row=4, column=0, sticky=tk.W)
        self.memo_entry = ttk.Entry(self.master)
        self.memo_entry.grid(row=4, column=1, padx=5, pady=5)

        self.contact_label = ttk.Label(self.master, text="Contact:")
        self.contact_label.grid(row=5, column=0, sticky=tk.W)
        self.contact_entry = ttk.Entry(self.master)
        self.contact_entry.grid(row=5, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(self.master, text="Save", command=self.save_friend)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.edit_button = ttk.Button(self.master, text="Edit", command=self.edit_friend)
        self.edit_button.grid(row=6, column=1, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.master, text="Delete", command=self.delete_friend)
        self.delete_button.grid(row=6, column=2, columnspan=2, pady=10)

        self.undo_button = ttk.Button(self.master, text="Undo Delete", command=self.undo_delete)
        self.undo_button.grid(row=6, column=3, columnspan=2, pady=10)

        self.search_label = ttk.Label(self.master, text="Search by:")
        self.search_label.grid(row=7, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(self.master)
        self.search_entry.grid(row=7, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.master, text="Search", command=self.search_friends)
        self.search_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.list_all_button = ttk.Button(self.master, text="List All Friends", command=self.load_friends)
        self.list_all_button.grid(row=8, column=1, columnspan=2, pady=10)

        self.reformat_list_button = ttk.Button(self.master, text="Reformat List", command=self.reformat_list)
        self.reformat_list_button.grid(row=8, column=2, columnspan=2, pady=10)

        self.friend_listbox = tk.Listbox(self.master, width=50)
        self.friend_listbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.friend_listbox.bind('<<ListboxSelect>>', self.select_friend)

    def setup_database(self):
        self.conn = sqlite3.connect('friends.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS friends
                            (id INTEGER PRIMARY KEY,
                            name TEXT,
                            city TEXT,
                            state TEXT,
                            country TEXT,
                            memo TEXT,
                            contact TEXT)''')
        self.conn.commit()
        self.populate_dropdowns()

    def populate_dropdowns(self):
        cities = set()
        states = set()
        countries = set()

        self.c.execute("SELECT DISTINCT city FROM friends")
        cities.update([row[0] for row in self.c.fetchall()])

        self.c.execute("SELECT DISTINCT state FROM friends")
        states.update([row[0] for row in self.c.fetchall()])

        self.c.execute("SELECT DISTINCT country FROM friends")
        countries.update([row[0] for row in self.c.fetchall()])

        self.city_combobox['values'] = sorted(cities)
        self.state_combobox['values'] = sorted(states)
        self.country_combobox['values'] = sorted(countries)

    def save_friend(self):
        name = self.name_entry.get()
        city = self.city_var.get()
        state = self.state_var.get()
        country = self.country_var.get()
        memo = self.memo_entry.get()
        contact = self.contact_entry.get()

        self.c.execute("INSERT INTO friends (name, city, state, country, memo, contact) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, city, state, country, memo, contact))
        self.conn.commit()
        self.clear_entries()
        self.load_friends()

    def load_friends(self):
        self.friend_listbox.delete(0, tk.END)
        self.c.execute("SELECT * FROM friends")
        friends = self.c.fetchall()
        for friend in friends:
            display_text = f"ID: {friend[0]}\n"
            display_text += f"Name: {friend[1]}\n"
            display_text += f"City: {friend[2]}\n"
            display_text += f"State: {friend[3]}\n"
            display_text += f"Country: {friend[4]}\n"
            if friend[5]:  # Check if memo exists
                display_text += f"Memo: {friend[5]}\n"
            if friend[6]:  # Check if contact exists
                display_text += f"Contact: {friend[6]}\n"
            self.friend_listbox.insert(tk.END, display_text)

    def select_friend(self, event):
        try:
            selected_index = self.friend_listbox.curselection()[0]
            selected_text = self.friend_listbox.get(selected_index)
            name = selected_text.split('\n')[1].split(': ')[1]
            city = selected_text.split('\n')[2].split(': ')[1]
            state = selected_text.split('\n')[3].split(': ')[1]
            country = selected_text.split('\n')[4].split(': ')[1]
            memo_index = 5 if "Memo: " in selected_text else 4
            memo = selected_text.split('\n')[memo_index].split(': ')[1] if "Memo: " in selected_text else ""
            contact_index = memo_index + 1 if memo else memo_index
            contact = selected_text.split('\n')[contact_index].split(': ')[1] if "Contact: " in selected_text else ""

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.city_var.set(city)
            self.state_var.set(state)
            self.country_var.set(country)
            self.memo_entry.delete(0, tk.END)
            self.memo_entry.insert(0, memo)
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, contact)
        except IndexError:
            pass

    def edit_friend(self):
        try:
            selected_index = self.friend_listbox.curselection()[0]
            selected_text = self.friend_listbox.get(selected_index)
            friend_id = int(selected_text.split('\n')[0].split(': ')[1])

            name = self.name_entry.get()
            city = self.city_var.get()
            state = self.state_var.get()
            country = self.country_var.get()
            memo = self.memo_entry.get()
            contact = self.contact_entry.get()

            self.c.execute("UPDATE friends SET name=?, city=?, state=?, country=?, memo=?, contact=? WHERE id=?",
                           (name, city, state, country, memo, contact, friend_id))
            self.conn.commit()

            updated_entry = f"ID: {friend_id}\nName: {name}\nCity: {city}\nState: {state}\nCountry: {country}\n"
            if memo:
                updated_entry += f"Memo: {memo}\n"
            if contact:
                updated_entry += f"Contact: {contact}\n"
                
            self.friend_listbox.delete(selected_index)
            self.friend_listbox.insert(selected_index, updated_entry)
            self.clear_entries()
            
            # Reload the friends list
            self.load_friends()
        except IndexError:
            pass

    def delete_friend(self):
        try:
            selected_index = self.friend_listbox.curselection()[0]
            selected_text = self.friend_listbox.get(selected_index)
            friend_id = int(selected_text.split('\n')[0].split(': ')[1])

            self.deleted_friend = selected_text

            self.c.execute("DELETE FROM friends WHERE id=?", (friend_id,))
            self.conn.commit()
            self.clear_entries()
            self.load_friends()
        except IndexError:
            pass

    def undo_delete(self):
        if self.deleted_friend:
            friend_details = self.deleted_friend.split('\n')
            name = friend_details[1].split(': ')[1]
            city = friend_details[2].split(': ')[1]
            state = friend_details[3].split(': ')[1]
            country = friend_details[4].split(': ')[1]
            memo_index = 5 if "Memo: " in self.deleted_friend else 4
            memo = friend_details[memo_index].split(': ')[1] if "Memo: " in self.deleted_friend else ""
            contact_index = memo_index + 1 if memo else memo_index
            contact = friend_details[contact_index].split(': ')[1] if "Contact: " in self.deleted_friend else ""

            self.c.execute("INSERT INTO friends (name, city, state, country, memo, contact) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, city, state, country, memo, contact))
            self.conn.commit()
            self.deleted_friend = None
            self.load_friends()
            self.clear_entries()

    def search_friends(self):
        search_term = self.search_entry.get()
        self.friend_listbox.delete(0, tk.END)
        self.c.execute("SELECT * FROM friends WHERE city=? OR state=? OR country=?", (search_term, search_term, search_term))
        friends = self.c.fetchall()
        for friend in friends:
            display_text = f"ID: {friend[0]}\n"
            display_text += f"Name: {friend[1]}\n"
            display_text += f"City: {friend[2]}\n"
            display_text += f"State: {friend[3]}\n"
            display_text += f"Country: {friend[4]}\n"
            if friend[5]:  # Check if memo exists
                display_text += f"Memo: {friend[5]}\n"
            if friend[6]:  # Check if contact exists
                display_text += f"Contact: {friend[6]}\n"
            self.friend_listbox.insert(tk.END, display_text)

    def reformat_list(self):
        self.c.execute("SELECT MAX(id) FROM friends")
        max_id = self.c.fetchone()[0]
        if max_id is not None:
            for i in range(1, max_id + 1):
                self.c.execute("SELECT COUNT(*) FROM friends WHERE id=?", (i,))
                count = self.c.fetchone()[0]
                if count == 0:
                    self.c.execute("SELECT * FROM friends WHERE id > ? ORDER BY id ASC LIMIT 1", (i,))
                    row = self.c.fetchone()
                    if row:
                        friend_id, name, city, state, country, memo, contact = row
                        self.c.execute("UPDATE friends SET id=? WHERE id=?", (i, friend_id))
        self.conn.commit()
        self.load_friends()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.city_var.set('')
        self.state_var.set('')
        self.country_var.set('')
        self.memo_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = FriendDatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
