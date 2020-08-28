import sqlite3


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
                         "(lot INTEGER PRIMARY KEY, date date, gun text, calibre text, powder_type text, "
                         "powder_weight float, bullet_type text, bullet_weight integer, oal float, primer_type text, "
                         "case_type text, no_made integer, rating text)")
        self.con.commit()

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

    def view_bullet_weights(self):
        self.cur.execute("SELECT * FROM bullet_weights")
        rows = self.cur.fetchall()
        return rows

    def view_bullet_types(self):
        self.cur.execute("SELECT * FROM bullet_types")
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

    def delete_component(self, table_ref, component):
        if table_ref == 0:
            pass
        elif table_ref == 1:
            self.cur.execute("DELETE FROM guns WHERE gun=?", (component,))
            self.con.commit()

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

    # def view(self):
    #     self.cur.execute("SELECT * FROM books")
    #     rows = self.cur.fetchall()
    #     return rows
    #
    # def search(self, title="", author="", year="", isbn=""):
    #     self.cur.execute("SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?",
    #                      (title.title(), author.title(), year, isbn))
    #     rows = self.cur.fetchall()
    #     return rows
    #
    # def delete(self, id):
    #     self.cur.execute("DELETE FROM books WHERE id=?", (id,))
    #     self.con.commit()
    #
    # def update(self, id, title, author, year, isbn):
    #     self.cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
    #                      (title, author, year, isbn, id))
    #     self.con.commit()

    def __del__(self):
        self.con.close()
