import sqlite3

# Create database, connection, and tables


class Database:

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS guns (id INTEGER PRIMARY KEY, gun text NOT NULL UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS calibres (id INTEGER PRIMARY KEY, calibre text NOT NULL UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS powder_types (id INTEGER PRIMARY KEY, powder_type text NOT NULL "
                         "UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS bullet_weights (id INTEGER PRIMARY KEY, bullet_weight integer "
                         "NOT NULL UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS bullet_types (id INTEGER PRIMARY KEY, bullet_type text NOT NULL "
                         "UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS primers (id INTEGER PRIMARY KEY, primer text NOT NULL UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS case_types (id INTEGER PRIMARY KEY, case_type text NOT NULL "
                         "UNIQUE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS log"
                         "(lot INTEGER PRIMARY KEY, date date, gun text NOT NULL, calibre text NOT NULL, "
                         "powder_type text NOT NULL, powder_weight real NOT NULL, bullet_type text NOT NULL, "
                         "bullet_weight integer NOT NULL, oal real NOT NULL, primer_type text NOT NULL, "
                         "case_type text NOT NULL, no_made integer NOT NULL, preps text, notes text, rating text)")
        self.con.commit()

# Functions to insert individual components into tables to create component repositories

    def insert_gun(self, gun):
        self.cur.execute("INSERT INTO guns VALUES (NULL, ?)", (gun.strip(),))
        self.con.commit()

    def insert_calibre(self, calibre):
        self.cur.execute("INSERT INTO calibres VALUES (NULL, ?)", (calibre.strip(),))
        self.con.commit()

    def insert_powder_type(self, powder_type):
        self.cur.execute("INSERT INTO powder_types VALUES (NULL, ?)", (powder_type.strip(),))
        self.con.commit()

    def insert_bullet_weight(self, bullet_weight):
        self.cur.execute("INSERT INTO bullet_weights VALUES (NULL, ?)", (bullet_weight.strip(),))
        self.con.commit()

    def insert_bullet_type(self, bullet_type):
        self.cur.execute("INSERT INTO bullet_types VALUES (NULL, ?)", (bullet_type.strip(),))
        self.con.commit()

    def insert_primer(self, primer):
        self.cur.execute("INSERT INTO primers VALUES (NULL, ?)", (primer.strip(),))
        self.con.commit()

    def insert_case_type(self, case_type):
        self.cur.execute("INSERT INTO case_types VALUES (NULL, ?)", (case_type.strip(),))
        self.con.commit()

# Functions to return all components from the database, for populating treeviews and comboboxes

    def view_dates(self):
        self.cur.execute("SELECT DISTINCT date FROM log ORDER BY DATE")
        rows = self.cur.fetchall()
        return rows

    def view_guns(self):
        self.cur.execute("SELECT * FROM guns")
        rows = self.cur.fetchall()
        return rows

    def view_calibres(self):
        self.cur.execute("SELECT * FROM calibres")
        rows = self.cur.fetchall()
        return rows

    def view_powder_types(self):
        self.cur.execute("SELECT * FROM powder_types")
        rows = self.cur.fetchall()
        return rows

    def view_powder_weights(self):
        self.cur.execute("SELECT DISTINCT powder_weight FROM log ORDER by powder_weight")
        rows = self.cur.fetchall()
        return rows

    def view_bullet_weights(self):
        self.cur.execute("SELECT * FROM bullet_weights")
        rows = self.cur.fetchall()
        return rows

    def view_bullet_types(self):
        self.cur.execute("SELECT * FROM bullet_types")
        rows = self.cur.fetchall()
        return rows

    def view_oals(self):
        self.cur.execute("SELECT DISTINCT oal FROM log ORDER BY oal")
        rows = self.cur.fetchall()
        return rows

    def view_primers(self):
        self.cur.execute("SELECT * FROM primers")
        rows = self.cur.fetchall()
        return rows

    def view_case_types(self):
        self.cur.execute("SELECT * FROM case_types")
        rows = self.cur.fetchall()
        return rows

    def view_ratings(self):
        self.cur.execute("SELECT DISTINCT rating FROM log ORDER BY rating")
        rows = self.cur.fetchall()
        return rows

# Functions to edit individual components from repositories in the database

    def edit_gun(self, id, gun):
        self.cur.execute("UPDATE guns SET gun=? WHERE id=?", (gun, id))
        self.con.commit()

    def edit_calibre(self, id, calibre):
        self.cur.execute("UPDATE calibres SET calibre=? WHERE id=?", (calibre, id))
        self.con.commit()

    def edit_powder_type(self, id, powder_type):
        self.cur.execute("UPDATE powder_types SET powder_type=? WHERE id=?", (powder_type, id))
        self.con.commit()

    def edit_bullet_weight(self, id, bullet_weight):
        self.cur.execute("UPDATE bullet_weights SET bullet_weight=? WHERE id=?", (bullet_weight, id))
        self.con.commit()

    def edit_bullet_type(self, id, bullet_type):
        self.cur.execute("UPDATE bullet_types SET bullet_type=? WHERE id=?", (bullet_type, id))
        self.con.commit()

    def edit_primer(self, id, primer):
        self.cur.execute("UPDATE primers SET primer=? WHERE id=?", (primer, id))
        self.con.commit()

    def edit_case_type(self, id, case_type):
        self.cur.execute("UPDATE case_types SET case_type=? WHERE id=?", (case_type, id))
        self.con.commit()

# Functions to delete individual components from the repositories

    def delete_gun(self, id):
        self.cur.execute("DELETE FROM guns WHERE id=?", (id,))
        self.con.commit()

    def delete_calibre(self, id):
        self.cur.execute("DELETE FROM calibres WHERE id=?", (id,))
        self.con.commit()

    def delete_powder_type(self, id):
        self.cur.execute("DELETE FROM powder_types WHERE id=?", (id,))
        self.con.commit()

    def delete_bullet_weight(self, id):
        self.cur.execute("DELETE FROM bullet_weights WHERE id=?", (id,))
        self.con.commit()

    def delete_bullet_type(self, id):
        self.cur.execute("DELETE FROM bullet_types WHERE id=?", (id,))
        self.con.commit()

    def delete_primer(self, id):
        self.cur.execute("DELETE FROM primers WHERE id=?", (id,))
        self.con.commit()

    def delete_case_type(self, id):
        self.cur.execute("DELETE FROM case_types WHERE id=?", (id,))
        self.con.commit()

# Function to create new log entry in log table

    def create_new_log_entry(self, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal,
                             primer_type, case_type, no_made, preps, notes, rating):
        self.cur.execute("INSERT INTO log VALUES (NULL, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, primer_type,
                          case_type, no_made, preps.strip(), notes, rating))
        self.con.commit()

# Function to return values needed to populate log treeview

    def view_log_treeview(self):
        self.cur.execute("SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, "
                         "primer_type, case_type, no_made, rating FROM log ORDER BY lot DESC")
        rows = self.cur.fetchall()
        return rows

# Function to return all log entries for CSV dump

    def all_log_entries(self):
        self.cur.execute("SELECT * from log ORDER BY lot DESC")
        rows = self.cur.fetchall()
        return rows

# Function to return preparations text

    def view_preparations(self, id):
        self.cur.execute("SELECT preps FROM log WHERE lot=?", (id,))
        data = self.cur.fetchall()
        return data

# Function to return notes

    def view_notes(self, id):
        self.cur.execute("SELECT notes FROM log WHERE lot=?", (id,))
        data = self.cur.fetchall()
        return data

# Functions to return log entries by selected date/component/measurement to populate Log treeview

    def selected_date(self, date):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE date=? ORDER BY lot DESC', (date,))
        rows = self.cur.fetchall()
        return rows

    def selected_gun(self, gun):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE gun=? ORDER BY lot DESC', (gun,))
        rows = self.cur.fetchall()
        return rows

    def selected_calibre(self, calibre):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE calibre=? ORDER BY lot DESC',
                         (calibre,))
        rows = self.cur.fetchall()
        return rows

    def selected_powder_type(self, powder_type):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE powder_type=? ORDER BY lot DESC',
                         (powder_type,))
        rows = self.cur.fetchall()
        return rows

    def selected_powder_weight(self, powder_weight):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE powder_weight=? ORDER BY lot DESC',
                         (powder_weight,))
        rows = self.cur.fetchall()
        return rows

    def selected_bullet_type(self, bullet_type):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE bullet_type=? ORDER BY lot DESC',
                         (bullet_type,))
        rows = self.cur.fetchall()
        return rows

    def selected_bullet_weight(self, bullet_weight):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE bullet_weight=? ORDER BY lot DESC',
                         (bullet_weight,))
        rows = self.cur.fetchall()
        return rows

    def selected_oal(self, oal):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE oal=? ORDER BY lot DESC', (oal,))
        rows = self.cur.fetchall()
        return rows

    def selected_primer_type(self, primer_type):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE primer_type=? ORDER BY lot DESC',
                         (primer_type,))
        rows = self.cur.fetchall()
        return rows

    def selected_case_type(self, case_type):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE case_type=? ORDER BY lot DESC',
                         (case_type,))
        rows = self.cur.fetchall()
        return rows

    def selected_rating(self, rating):
        self.cur.execute('SELECT lot, date, gun, calibre, powder_type, powder_weight, bullet_type, bullet_weight, oal, '
                         'primer_type, case_type, no_made, rating FROM log WHERE rating=? ORDER BY lot DESC', (rating,))
        rows = self.cur.fetchall()
        return rows

# Function to update load rating

    def update_rating(self, id, rating):
        self.cur.execute("UPDATE log SET rating=? WHERE lot=?", (rating, id))
        self.con.commit()

# Function to add/update notes

    def update_notes(self, id, notes):
        self.cur.execute("UPDATE log SET notes=? WHERE lot=?", (notes, id))
        self.con.commit()

# Function to delete log entry

    def delete_log_entry(self, id):
        self.cur.execute("DELETE FROM log WHERE lot=?", (id,))
        self.con.commit()

    def __del__(self):
        self.con.close()
