from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import date
# import csv
from backend import Database

db = Database("boom_log.db")


class Window(object):

    def __init__(self, window):
        self.window = window
        self.window.geometry("1000x600")
        self.window.wm_title("*BOOM* Log")
        self.window.resizable(0, 0)
        self.window.protocol('WM_DELETE_WINDOW', exit_application)
        self.window.option_add("*Text.Font", "TkDefaultFont")

        # Create Notebook and tabs

        tab_parent = ttk.Notebook(self.window)
        view_tab = Frame(tab_parent)
        entry_tab = Frame(tab_parent)
        config_tab = Frame(tab_parent)

        tab_parent.add(view_tab, text="View log")
        tab_parent.add(entry_tab, text="Add entry")
        tab_parent.add(config_tab, text="Add components")
        tab_parent.bind("<<NotebookTabChanged>>", self.trigger_populate_log_treeview_and_reset_values)

        # App icon, attribution below
        # Icons made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from
        # <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

        self.window.iconbitmap("C:\\Users\\Yasmine\\Desktop\\ownProjects\\Python\\reloading_diary\\app_icon.ico")

        # Image for Add entry tab

        parabellum_img = Image.open(
            "C:\\Users\\Yasmine\\Desktop\\ownProjects\\Python\\reloading_diary\\parabellum_9.png")
        parabellum_img = parabellum_img.resize((550, 445), Image.ANTIALIAS)
        self.parabellum_image = ImageTk.PhotoImage(parabellum_img)

        # Image for Add component tab

        target_img = Image.open("C:\\Users\\Yasmine\\Desktop\\ownProjects\\Python\\reloading_diary\\target.jpeg")
        target_img = target_img.resize((400, 310), Image.ANTIALIAS)
        self.target_image = ImageTk.PhotoImage(target_img)

        # Configuration of View log tab
        # The user can see all loads they have made, and narrow their search, e.g. by date, specific gun etc.
        # The user can add/edit notes or add/edit a star rating for individual loads, and export the log to a CSV file.

        self.view_log_label = Label(view_tab, text="Log:")
        self.view_log_label.grid(row=0, column=0, columnspan=10, padx=20, pady=(30, 0), sticky=SW)

        self.view_log_tree = ttk.Treeview(view_tab, column=("column1", "column2", "column3", "column4", "column5",
                                                            "column6", "column7", "column8", "column9", "column10"
                                                                                                        "column11",
                                                            "column12", "column13", "column14"),
                                          show='headings', selectmode='browse')
        self.view_log_tree.heading("#1", text="Lot", anchor=W)  # ID
        self.view_log_tree.column("#1", width=0, minwidth=40)
        self.view_log_tree.heading("#2", text="Date", anchor=W)  # dd-mm-yyyy - date of entry
        self.view_log_tree.column("#2", width=0, minwidth=80)
        self.view_log_tree.heading("#3", text="Gun", anchor=W)  # text
        self.view_log_tree.column("#3", width=0, minwidth=120)
        self.view_log_tree.heading("#4", text="Calibre", anchor=W)  # text
        self.view_log_tree.column("#4", width=0, minwidth=120)
        self.view_log_tree.heading("#5", text="Powder type", anchor=W)  # text
        self.view_log_tree.column("#5", width=0, minwidth=120)
        self.view_log_tree.heading("#6", text="Powder weight (grn)", anchor=W)  # decimal
        self.view_log_tree.column("#6", width=0, minwidth=120)
        self.view_log_tree.heading("#7", text="Bullet type", anchor=W)  # text
        self.view_log_tree.column("#7", width=0, minwidth=120)
        self.view_log_tree.heading("#8", text="Bullet weight (grn)", anchor=W)  # integer
        self.view_log_tree.column("#8", width=0, minwidth=120)
        self.view_log_tree.heading("#9", text="OAL (mm)", anchor=W)  # decimal
        self.view_log_tree.column("#9", width=0, minwidth=120)
        self.view_log_tree.heading("#10", text="Primer type", anchor=W)  # text
        self.view_log_tree.column("#10", width=0, minwidth=120)
        self.view_log_tree.heading("#11", text="Case type", anchor=W)  # text
        self.view_log_tree.column("#11", width=0, minwidth=120)
        self.view_log_tree.heading("#12", text="No. made", anchor=W)  # integer
        self.view_log_tree.column("#12", width=0, minwidth=120)
        self.view_log_tree.heading("#13", text="Rating", anchor=W)  # text
        self.view_log_tree.column("#13", width=755, minwidth=70)
        self.view_log_tree.grid(row=2, column=0, rowspan=10, columnspan=10, padx=(20, 0), pady=(0, 10))
        self.view_log_tree.bind("<<TreeviewSelect>>", self.display_preparations_and_notes)

        view_scrollbar = Scrollbar(view_tab)
        view_scrollbar.grid(row=2, column=10, rowspan=10, padx=(0, 10), sticky=N + S + W)

        self.view_log_tree.configure(yscrollcommand=view_scrollbar.set)
        view_scrollbar.configure(command=self.view_log_tree.yview)

        view_horizontal_scrollbar = Scrollbar(view_tab, orient=HORIZONTAL)
        view_horizontal_scrollbar.grid(row=11, column=0, columnspan=10, padx=(15, 0), stick=E + W + S)

        self.view_log_tree.configure(xscrollcommand=view_horizontal_scrollbar.set)
        view_horizontal_scrollbar.configure(command=self.view_log_tree.xview)

        self.view_narrow_by_label = Label(view_tab, text="Narrow by:")
        self.view_narrow_by_label.grid(row=2, column=11, sticky=SW)

        narrowed_selection = StringVar()
        narrow_by = StringVar()
        self.narrow_by_combobox = ttk.Combobox(view_tab, width=22, value=narrow_by, state='readonly')
        self.narrowed_selection_combobox = ttk.Combobox(view_tab, width=22, value=narrowed_selection, state='readonly',
                                                        postcommand=self.log_fill_select_component_combobox)
        self.narrowed_selection_combobox.bind("<<ComboboxSelected>>", self.populate_log_treeview_with_selection)
        self.narrow_by_combobox['values'] = ['Select',
                                             'Date',
                                             'Gun',
                                             'Calibre',
                                             'Powder type',
                                             'Powder weight',
                                             'Bullet type',
                                             'Bullet weight',
                                             'OAL',
                                             'Primer type',
                                             'Case type',
                                             'Rating']
        self.narrow_by_combobox.current(0)
        self.narrowed_selection_combobox.set(self.log_fill_select_component_combobox()[0])
        self.narrow_by_combobox.grid(row=3, column=11, sticky=N)
        self.narrowed_selection_combobox.grid(row=5, column=11, sticky=N)
        self.narrow_by_combobox.bind("<<ComboboxSelected>>", self.narrow_by_selected)

        self.view_select_label = Label(view_tab, text="Select:")
        self.view_select_label.grid(row=4, column=11, pady=(10, 0), sticky=SW)

        view_clear_search_button = Button(view_tab, text="View all", width=22, command=self.populate_log_treeview)
        view_clear_search_button.grid(row=7, column=11)

        view_csv_button = Button(view_tab, text="Write log to CSV", width=22)
        view_csv_button.grid(row=9, column=11)

        view_delete_button = Button(view_tab, text="Delete selected entry", width=22, command=self.delete_log_entry)
        view_delete_button.grid(row=11, column=11)

        self.view_preps_label = Label(view_tab, text="Preparations:")
        self.view_preps_label.grid(row=13, column=0, padx=(20, 0), pady=(30, 0), sticky=SW)

        self.preparations_text_from_db = StringVar()
        self.view_preparations = Label(view_tab, height=3, width=106, relief="sunken", bg="white",
                                       textvariable=self.preparations_text_from_db, anchor=NW, justify=LEFT, padx=7,
                                       pady=5)
        self.view_preparations.grid(row=14, column=0, padx=(20, 0), pady=(0, 10), columnspan=10, sticky=N)

        self.view_notes_label = Label(view_tab, text="Load notes:")
        self.view_notes_label.grid(row=17, column=0, padx=(20, 0), sticky=SW)

        self.view_notes_text = Text(view_tab, height=4, width=124, padx=7, pady=5)
        self.view_notes_text.grid(row=18, column=0, padx=(20, 0), pady=(0, 20), columnspan=10)

        self.view_edit_notes_button = Button(view_tab, text="Add notes/Save changes", width=22,
                                             command=self.update_notes)
        self.view_edit_notes_button.grid(row=18, column=11, pady=(0, 20))

        self.view_add_star_rating_label = Label(view_tab, text="Add load rating:")
        self.view_add_star_rating_label.grid(row=19, column=0, padx=(20, 0), sticky=W)

        self.star_rating_combobox = ttk.Combobox(view_tab, width=22, state='readonly')
        self.star_rating_combobox['values'] = ['Select',
                                               '*',
                                               '**',
                                               '***',
                                               '****',
                                               '*****']
        self.star_rating_combobox.current(0)
        self.star_rating_combobox.grid(row=19, column=1, sticky=W)

        view_save_rating_button = Button(view_tab, text="Add/Update rating", width=22,
                                         command=self.update_rating)
        view_save_rating_button.grid(row=19, column=2, sticky=W)

        view_exit_button = Button(view_tab, text="Quit", width=22, command=exit_application)
        view_exit_button.grid(row=19, column=11)

        # Configuration of Add entry tab
        # The user can create new log entries, with both free text and selection from drop-down menus for standard
        # components that they use/own.

        self.entry_create_new_label = Label(entry_tab, text='Create a new log entry:')
        self.entry_create_new_label.grid(row=0, column=0, padx=20, pady=(40, 15))

        self.entry_gun_label = Label(entry_tab, text='Gun')
        self.entry_gun_label.grid(row=1, column=0, padx=20, pady=5, sticky=W)

        entry_gun_selection = StringVar()
        self.entry_gun_combobox = ttk.Combobox(entry_tab, width=25, value=entry_gun_selection, state='readonly',
                                               postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_gun_combobox.grid(row=1, column=1, pady=5)
        self.entry_gun_combobox.set(guns_from_repository()[0])

        self.entry_calibre_label = Label(entry_tab, text='Calibre')
        self.entry_calibre_label.grid(row=2, column=0, padx=20, pady=5, sticky=W)

        entry_calibre_selection = StringVar()
        self.entry_calibre_combobox = ttk.Combobox(entry_tab, width=25, value=entry_calibre_selection, state='readonly',
                                                   postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_calibre_combobox.grid(row=2, column=1, pady=5)
        self.entry_calibre_combobox.set(calibres_from_repository()[0])

        self.entry_powder_type_label = Label(entry_tab, text='Powder type')
        self.entry_powder_type_label.grid(row=3, column=0, padx=20, pady=5, sticky=W)

        entry_powder_type_selection = StringVar()
        self.entry_powder_type_combobox = ttk.Combobox(entry_tab, width=25, value=entry_powder_type_selection,
                                                       state='readonly',
                                                       postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_powder_type_combobox.grid(row=3, column=1, pady=5)
        self.entry_powder_type_combobox.set(powder_types_from_repository()[0])

        self.entry_powder_weight_label = Label(entry_tab, text='Powder weight (grn)')
        self.entry_powder_weight_label.grid(row=4, column=0, padx=20, pady=5, sticky=W)

        self.powder_weight = StringVar()
        self.entry_powder_weight = Entry(entry_tab, width=28, textvariable=self.powder_weight)
        self.entry_powder_weight.grid(row=4, column=1, pady=5)

        self.entry_bullet_type_label = Label(entry_tab, text='Bullet type')
        self.entry_bullet_type_label.grid(row=5, column=0, padx=20, pady=5, sticky=W)

        entry_bullet_type_selection = StringVar()
        self.entry_bullet_type_combobox = ttk.Combobox(entry_tab, width=25, value=entry_bullet_type_selection,
                                                       state='readonly',
                                                       postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_bullet_type_combobox.grid(row=5, column=1, pady=5)
        self.entry_bullet_type_combobox.set(bullet_types_from_repository()[0])

        self.entry_bullet_weight_label = Label(entry_tab, text='Bullet weight (grn)')
        self.entry_bullet_weight_label.grid(row=6, column=0, padx=20, pady=5, sticky=W)

        entry_bullet_weight_selection = StringVar()
        self.entry_bullet_weight_combobox = ttk.Combobox(entry_tab, width=25, value=entry_bullet_weight_selection,
                                                         state='readonly',
                                                         postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_bullet_weight_combobox.grid(row=6, column=1, pady=5)
        self.entry_bullet_weight_combobox.set(bullet_weights_from_repository()[0])

        self.entry_oal_label = Label(entry_tab, text='OAL (mm)')
        self.entry_oal_label.grid(row=7, column=0, padx=20, pady=5, sticky=W)

        self.oal = StringVar()
        self.entry_oal = Entry(entry_tab, width=28, textvariable=self.oal)
        self.entry_oal.grid(row=7, column=1, pady=5)

        self.entry_primer_label = Label(entry_tab, text='Primer type')
        self.entry_primer_label.grid(row=8, column=0, padx=20, pady=5, sticky=W)

        entry_primer_type_selection = StringVar()
        self.entry_primer_type_combobox = ttk.Combobox(entry_tab, width=25, value=entry_primer_type_selection,
                                                       state='readonly',
                                                       postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_primer_type_combobox.grid(row=8, column=1, pady=5)
        self.entry_primer_type_combobox.set(primers_from_repository()[0])

        self.entry_case_label = Label(entry_tab, text='Case type')
        self.entry_case_label.grid(row=9, column=0, padx=20, pady=5, sticky=W)

        entry_case_selection = StringVar()
        self.entry_case_combobox = ttk.Combobox(entry_tab, width=25, value=entry_case_selection, state='readonly',
                                                postcommand=self.keep_entry_comboboxes_refreshed)
        self.entry_case_combobox.grid(row=9, column=1, pady=5)
        self.entry_case_combobox.set(case_types_from_repository()[0])

        self.entry_no_made_label = Label(entry_tab, text='Number made')
        self.entry_no_made_label.grid(row=10, column=0, padx=20, pady=5, sticky=W)

        self.no_made = StringVar()
        self.entry_no_made = Entry(entry_tab, width=28, textvariable=self.no_made)
        self.entry_no_made.grid(row=10, column=1, pady=5)

        self.entry_preps_label = Label(entry_tab, text='Preparations')
        self.entry_preps_label.grid(row=11, column=0, padx=20, pady=5, sticky=NW)

        self.preparations_text = StringVar()
        self.entry_preparations = Entry(entry_tab, width=28, textvariable=self.preparations_text)
        self.entry_preparations.grid(row=11, column=1, pady=5)

        entry_add_entry_button = Button(entry_tab, text="Add entry", width=23,
                                        command=partial(create_new_log_entry, self.entry_gun_combobox,
                                                        self.entry_calibre_combobox, self.entry_powder_type_combobox,
                                                        self.powder_weight, self.entry_powder_weight,
                                                        self.entry_bullet_type_combobox,
                                                        self.entry_bullet_weight_combobox, self.oal,
                                                        self.entry_oal, self.entry_primer_type_combobox,
                                                        self.entry_case_combobox, self.no_made, self.entry_no_made,
                                                        self.preparations_text, self.entry_preparations))
        entry_add_entry_button.grid(row=12, column=1, pady=5)

        entry_quit_button = Button(entry_tab, text='Quit', width=23, command=exit_application)
        entry_quit_button.grid(row=13, column=1, pady=5)

        self.entry_picture_label = Label(entry_tab, bg='white', image=self.parabellum_image)
        self.entry_picture_label.image = self.parabellum_image
        self.entry_picture_label.place(x=400, y=44, relwidth=0.55, relheight=0.77)

        # Configuration of Add components tab
        # User can add standard components that they use to their repository, e.g. guns that they own. These then form
        # pre-selections for the user when logging new loads.

        self.config_components_label = Label(config_tab, text='Configure components:')
        self.config_components_label.grid(row=0, column=0, padx=20, pady=(60, 10), sticky=W)

        self.configure_combobox = ttk.Combobox(config_tab, values=['Select component',
                                                                   'Gun',
                                                                   'Calibre',
                                                                   'Powder type',
                                                                   'Bullet weight',
                                                                   'Bullet type',
                                                                   'Primer type',
                                                                   'Case type'], width=30, state="readonly",
                                               postcommand=self.clear_component_entry_and_config_tree)
        self.configure_combobox.current(0)
        self.configure_combobox.grid(row=0, column=1, pady=(60, 10))

        self.component_to_add = StringVar()
        self.component_entry = Entry(config_tab, width=30, textvariable=self.component_to_add)
        self.component_entry.grid(row=0, column=2, padx=(36, 14), pady=(60, 10))

        self.config_tree = ttk.Treeview(config_tab, column="column1", show='headings',
                                        selectmode='browse', height=15)
        self.config_tree.grid(row=3, column=0, rowspan=10, columnspan=2, padx=(20, 0), pady=(60, 0), sticky=W)
        self.config_tree.heading("#1", text="Component repository:", anchor=W)
        self.config_tree.column("#1", width=350, anchor=W)
        self.config_tree.bind("<<TreeviewSelect>>", self.fill_text_box_for_editing_component)

        config_add_button = Button(config_tab, text='Add component', width=23,
                                   command=partial(add_component, self.configure_combobox,
                                                   self.component_to_add, self.component_entry, self.config_tree))
        config_add_button.grid(row=0, column=3, padx=(16, 5), pady=(60, 10))

        config_view_all_button = Button(config_tab, text='View all', width=23,
                                        command=partial(view_components, self.config_tree,
                                                        self.configure_combobox))
        config_view_all_button.grid(row=0, column=4, pady=(60, 10))

        config_scrollbar = Scrollbar(config_tab)
        config_scrollbar.grid(row=3, column=2, rowspan=10, pady=(60, 0), sticky=N + S + W)

        self.config_tree.configure(yscrollcommand=config_scrollbar.set)
        config_scrollbar.configure(command=self.config_tree.yview)

        self.config_edit_component_label = Label(config_tab, text='Edit selected component:')
        self.config_edit_component_label.grid(row=5, column=2, padx=(34, 0), sticky=SW)

        self.component_to_edit = StringVar()
        self.edit_component_entry = Entry(config_tab, width=30, textvariable=self.component_to_edit)
        self.edit_component_entry.grid(row=6, column=2, padx=(22, 0))

        config_edit_component_button = Button(config_tab, text='Save changes', width=25,
                                              command=partial(edit_component, self.configure_combobox, self.config_tree,
                                                              self.component_to_edit, self.edit_component_entry))
        config_edit_component_button.grid(row=7, column=2, padx=(30, 10))

        config_delete_button = Button(config_tab, text='Delete selected component', width=25,
                                      command=partial(delete_selected_component, self.configure_combobox,
                                                      self.config_tree, self.edit_component_entry))
        config_delete_button.grid(row=3, column=2, padx=(30, 10), pady=(60, 0))

        config_exit_button = Button(config_tab, text="Quit", width=25, command=exit_application)
        config_exit_button.grid(row=12, column=2, padx=(30, 10))

        self.config_picture_label = Label(config_tab, bg='black', image=self.target_image)
        self.config_picture_label.image = self.target_image
        self.config_picture_label.place(x=624, y=157, relwidth=0.35, relheight=0.56)

        tab_parent.pack(expand=1, fill='both')

    def fill_text_box_for_editing_component(self, event):
        self.edit_component_entry.delete(0, END)
        item_iid = self.config_tree.selection()[0]
        if self.configure_combobox.current() == 4:
            self.edit_component_entry.insert(END, str(self.config_tree.item(item_iid)['values'])[1:-1])
        else:
            self.edit_component_entry.insert(END, str(self.config_tree.item(item_iid)['values'])[2:-2])

    def clear_component_entry_and_config_tree(self):
        self.edit_component_entry.delete(0, END)
        self.config_tree.delete(*self.config_tree.get_children())

    def keep_entry_comboboxes_refreshed(self):
        guns = guns_from_repository()
        self.entry_gun_combobox['values'] = guns
        calibres = calibres_from_repository()
        self.entry_calibre_combobox['values'] = calibres
        powder_types = powder_types_from_repository()
        self.entry_powder_type_combobox['values'] = powder_types
        bullet_types = bullet_types_from_repository()
        self.entry_bullet_type_combobox['values'] = bullet_types
        bullet_weights = bullet_weights_from_repository()
        self.entry_bullet_weight_combobox['values'] = bullet_weights
        primers = primers_from_repository()
        self.entry_primer_type_combobox['values'] = primers
        case_types = case_types_from_repository()
        self.entry_case_combobox['values'] = case_types

    def log_fill_select_component_combobox(self):
        data = []
        narrow_by_combobox_ref = self.narrow_by_combobox.current()
        if narrow_by_combobox_ref == 0:
            data = ['Select above']
        elif narrow_by_combobox_ref == 1:
            data = dates_from_repository()
        elif narrow_by_combobox_ref == 2:
            data = guns_from_repository()
        elif narrow_by_combobox_ref == 3:
            data = calibres_from_repository()
        elif narrow_by_combobox_ref == 4:
            data = powder_types_from_repository()
        elif narrow_by_combobox_ref == 5:
            data = powder_weights_from_repository()
        elif narrow_by_combobox_ref == 6:
            data = bullet_types_from_repository()
        elif narrow_by_combobox_ref == 7:
            data = bullet_weights_from_repository()
        elif narrow_by_combobox_ref == 8:
            data = oals_from_repository()
        elif narrow_by_combobox_ref == 9:
            data = primers_from_repository()
        elif narrow_by_combobox_ref == 10:
            data = case_types_from_repository()
        elif narrow_by_combobox_ref == 11:
            data = ratings_from_repository()
        self.narrowed_selection_combobox['values'] = data
        return data

    # Method bound to Narrow by combobox to reset default value of Select combobox

    def narrow_by_selected(self, event):
        self.narrowed_selection_combobox.set(self.log_fill_select_component_combobox()[0])

    # Method and event handler to return all entries from log to populate treeview on View log tab and keep updated

    def populate_log_treeview(self):
        self.view_log_tree.delete(*self.view_log_tree.get_children())
        for row in db.view_log_treeview():
            db_date = row[1]
            formatted_date = db_date[8:10] + db_date[7] + db_date[5:7] + db_date[4] + db_date[0:4]
            self.view_log_tree.insert('', END, values=(row[0], formatted_date, row[2], row[3], row[4], row[5], row[6],
                                                       row[7], row[8], row[9], row[10], row[11], row[12]))

    def trigger_populate_log_treeview_and_reset_values(self, event):
        self.populate_log_treeview()
        self.star_rating_combobox.current(0)
        self.preparations_text_from_db.set("")
        self.view_notes_text.delete('1.0', END)
        self.narrow_by_combobox.current(0)
        self.log_fill_select_component_combobox()
        self.narrowed_selection_combobox.current(0)

    # Method to populate log treeview narrowed by user selection on View log tab

    def populate_log_treeview_with_selection(self, event):
        self.view_log_tree.delete(*self.view_log_tree.get_children())
        self.star_rating_combobox.current(0)
        self.preparations_text_from_db.set("")
        self.view_notes_text.delete('1.0', END)
        search_item_type = self.narrow_by_combobox.current()
        if search_item_type == 0:
            self.populate_log_treeview()
        else:
            try:
                search_item = self.narrowed_selection_combobox.get()
                if search_item_type == 1:
                    db_date = search_item[6:10] + search_item[5] + search_item[3:5] + search_item[2] + search_item[0:2]
                    selected_search = db.selected_date(db_date)
                elif search_item_type == 2:
                    selected_search = db.selected_gun(search_item)
                elif search_item_type == 3:
                    selected_search = db.selected_calibre(search_item)
                elif search_item_type == 4:
                    selected_search = db.selected_powder_type(search_item)
                elif search_item_type == 5:
                    selected_search = db.selected_powder_weight(search_item)
                elif search_item_type == 6:
                    selected_search = db.selected_bullet_type(search_item)
                elif search_item_type == 7:
                    selected_search = db.selected_bullet_weight(search_item)
                elif search_item_type == 8:
                    selected_search = db.selected_oal(search_item)
                elif search_item_type == 9:
                    selected_search = db.selected_primer_type(search_item)
                elif search_item_type == 10:
                    selected_search = db.selected_case_type(search_item)
                elif search_item_type == 11:
                    selected_search = db.selected_rating(search_item)
                for row in selected_search:
                    db_date = row[1]
                    formatted_date = db_date[8:10] + db_date[7] + db_date[5:7] + db_date[4] + db_date[0:4]
                    self.view_log_tree.insert('', END, values=(row[0], formatted_date, row[2], row[3], row[4], row[5],
                                                               row[6], row[7], row[8], row[9], row[10], row[11],
                                                               row[12]))
            except IndexError:
                print("Index out of bounds.")

    # Method to add Preparations text from selected log entry (if available) to label in View log tab

    def display_preparations_and_notes(self, event):
        item_iid = self.view_log_tree.selection()
        ref_from_table = self.view_log_tree.item(item_iid)['values'][0]
        formatted_preps = str(db.view_preparations(ref_from_table)).replace("'", "").replace("(", "").replace(")", "")
        formatted_preps = formatted_preps.replace("[", "").replace("]", "")[:-1]
        self.preparations_text_from_db.set(formatted_preps)
        self.view_notes_text.delete('1.0', END)
        formatted_notes = str(db.view_notes(ref_from_table)).replace("'", "").replace("(", "").replace(")", "")
        formatted_notes = formatted_notes.replace("[", "").replace("]", "")[:-1]
        self.view_notes_text.insert(END, formatted_notes)

    # Method to add/edit rating in View log tab

    def update_rating(self):
        item_iid = self.view_log_tree.selection()
        if self.star_rating_combobox.current() == 0:
            messagebox.showwarning('Error', 'You must select the rating to add. No changes were made.', icon='warning')
        else:
            confirm_rating = messagebox.askquestion('Confirm Rating', 'Are you sure you want to add this rating?',
                                                    icon='warning')
            if confirm_rating == 'yes':
                try:
                    ref_from_table = self.view_log_tree.item(item_iid)['values'][0]
                    db.update_rating(ref_from_table, self.star_rating_combobox.get())
                    messagebox.showinfo('Success', 'Rating successfully added to your log.')
                    self.star_rating_combobox.current(0)
                except IndexError:
                    messagebox.showwarning('Error', 'You must select the entry you want to rate.', icon='warning')
            else:
                messagebox.showinfo('Cancelled', 'No changes were made to your log.')
        self.populate_log_treeview()

    # Method to add/edit notes in View log tab

    def update_notes(self):
        item_iid = self.view_log_tree.selection()
        confirm_notes = messagebox.askquestion('Confirm Add Notes', 'Are you sure you want to add these notes?',
                                               icon='warning')
        if confirm_notes == 'yes':
            try:
                ref_from_table = self.view_log_tree.item(item_iid)['values'][0]
                db.update_notes(ref_from_table, self.view_notes_text.get('1.0', 'end-1c'))
                messagebox.showinfo('Success', 'Notes successfully added to your log.')
            except IndexError:
                messagebox.showwarning('Error', 'You must select an entry to add notes.', icon='warning')
        else:
            messagebox.showinfo('Cancelled', 'No changes were made to your log.')

    # Method to delete log entry from View log tab

    def delete_log_entry(self):
        item_iid = self.view_log_tree.selection()
        confirm_delete_info = messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?\n'
                                                               'This action cannot be undone.', icon='warning')
        if confirm_delete_info == 'yes':
            try:
                ref_from_table = self.view_log_tree.item(item_iid)['values'][0]
                db.delete_log_entry(ref_from_table)
                self.populate_log_treeview()
                messagebox.showinfo('Deleted', 'The entry was successfully deleted from your log.')
            except IndexError:
                messagebox.showwarning('Error', 'You must select the entry you want to delete.', icon='warning')
        else:
            messagebox.showinfo('Cancelled', 'No changes were made to your log.')


# Exit application function attached to Quit button on each tab and delete window protocol


def exit_application():
    confirm_exit = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application?',
                                          icon='warning')
    if confirm_exit == 'yes':
        window.destroy()
    else:
        pass

# Add component function to add components to tables from Add components tab


def add_component(component_type_combobox, component, component_entry_widget, component_treeview):
    add_component_info = messagebox.askquestion('Add Component', 'Are you sure you want to add this component to your '
                                                                 'repository?', icon='warning')
    if add_component_info == 'yes':
        component_type = component_type_combobox.current()
        component_text = component.get()
        if len(component_text) != 0:
            try:
                if component_type != 0:
                    if component_type == 1:
                        db.insert_gun(component_text)
                    elif component_type == 2:
                        db.insert_calibre(component_text)
                    elif component_type == 3:
                        db.insert_powder_type(component_text)
                    elif component_type == 4:
                        db.insert_bullet_weight(component_text)
                    elif component_type == 5:
                        db.insert_bullet_type(component_text)
                    elif component_type == 6:
                        db.insert_primer(component_text)
                    elif component_type == 7:
                        db.insert_case_type(component_text)
                    component_entry_widget.delete(0, END)
                    messagebox.showinfo('Success', 'Component successfully added to your repository.')
                    view_components(component_treeview, component_type_combobox)
                else:
                    messagebox.showwarning('Error', 'You must specify the type of component you are adding.',
                                           icon='warning')
            except ValueError:
                messagebox.showwarning('Error', 'Something went wrong and no changes were made.', icon='warning')
            except:
                messagebox.showwarning('Error', 'Something went wrong and no changes were made. Check that the '
                                                'component does not already exist.', icon='warning')
        else:
            messagebox.showwarning('Error', 'Component text cannot be empty.')
    else:
        messagebox.showinfo('Cancelled', 'No changes were made to your repository.')


# Function to create list of selected components from repository and insert into single-column treeview on Configuration
# tab


def view_components(component_treeview, component_combobox_ref):
    component_type = component_combobox_ref.current()
    component_treeview.delete(*component_treeview.get_children())
    try:
        if component_type == 0:
            messagebox.showwarning('Error', 'You must specify the type of components you want to see.', icon='warning')
        elif component_type == 1:
            for row in db.view_guns():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 2:
            for row in db.view_calibres():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 3:
            for row in db.view_powder_types():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 4:
            for row in db.view_bullet_weights():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 5:
            for row in db.view_bullet_types():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 6:
            for row in db.view_primers():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
        elif component_type == 7:
            for row in db.view_case_types():
                component_treeview.insert("", END, text=row[0], values=(row[1],))
    except IndexError:
        print("Index not found")


# Function to edit component listed in edit component entry box on Configuration tab


def edit_component(component_combobox_ref, component_treeview, component_to_edit, edit_component_widget):
    component_type = component_combobox_ref.current()
    edited_component = component_to_edit.get()
    edit_component_info = messagebox.askquestion('Edit Component', 'Are you sure you want to save your changes?',
                                                 icon='warning')
    if edit_component_info == 'yes':
        if component_type == 0 or len(edited_component) == 0:
            messagebox.showwarning('Error', 'Something went wrong and no changes were made. \n\nCheck that the edited '
                                            'component is not blank and the correct repository is selected.',
                                   icon='warning')
        else:
            item_iid = component_treeview.selection()[0]
            id_in_table = component_treeview.item(item_iid)['text']
            try:
                if component_type == 1:
                    db.edit_gun(id_in_table, edited_component)
                elif component_type == 2:
                    db.edit_calibre(id_in_table, edited_component)
                elif component_type == 3:
                    db.edit_powder_type(id_in_table, edited_component)
                elif component_type == 4:
                    db.edit_bullet_weight(id_in_table, edited_component)
                elif component_type == 5:
                    db.edit_bullet_type(id_in_table, edited_component)
                elif component_type == 6:
                    db.edit_primer(id_in_table, edited_component)
                elif component_type == 7:
                    db.edit_case_type(id_in_table, edited_component)
                edit_component_widget.delete(0, END)
                messagebox.showinfo('Success', 'Your changes were successfully saved.')
                view_components(component_treeview, component_combobox_ref)
            except IndexError:
                print("Index out of bounds.")
    else:
        messagebox.showinfo('Cancelled', 'No changes were made to your repository.')


# Function to delete component selected from Configuration tab component repository treeview


def delete_selected_component(component_combobox_ref, component_treeview, edit_component_widget):
    component_type = component_combobox_ref.current()
    if component_type == 0:
        messagebox.showwarning('Error', 'You must select the component to delete.', icon='warning')
    else:
        confirm_delete_info = messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?',
                                                     icon='warning')
        if confirm_delete_info == 'yes':
            item_iid = component_treeview.selection()[0]
            id_in_table = component_treeview.item(item_iid)['text']
            try:
                if component_type == 1:
                    db.delete_gun(id_in_table)
                elif component_type == 2:
                    db.delete_calibre(id_in_table)
                elif component_type == 3:
                    db.delete_powder_type(id_in_table)
                elif component_type == 4:
                    db.delete_bullet_weight(id_in_table)
                elif component_type == 5:
                    db.delete_bullet_type(id_in_table)
                elif component_type == 6:
                    db.delete_primer(id_in_table)
                elif component_type == 7:
                    db.delete_case_type(id_in_table)
                messagebox.showinfo('Deleted', 'The component was successfully deleted from your repository.')
                edit_component_widget.delete(0, END)
                view_components(component_treeview, component_combobox_ref)
            except:
                messagebox.showwarning('Error', 'Something went wrong and no changes were made.', icon='warning')
        else:
            messagebox.showinfo('Cancelled', 'No changes were made to your repository.')


def confirm_delete():
    confirm_delete_info = messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?',
                                                 icon='warning')
    if confirm_delete_info == 'yes':
        pass
    else:
        pass


# Functions to return all data from databases by type to populate comboboxes/treeviews etc.


def dates_from_repository():
    dates = ['Select date']
    for row in db.view_dates():
        formatted_row = str(row)
        formatted_row = formatted_row[10:12] + formatted_row[9] + formatted_row[7:9] + formatted_row[6] + formatted_row[
                                                                                                          2:6]
        dates.append(formatted_row)
    return dates


def guns_from_repository():
    guns = ['Select component']
    for row in db.view_guns():
        guns.append(row[1])
    return guns


def calibres_from_repository():
    calibres = ['Select component']
    for row in db.view_calibres():
        calibres.append(row[1])
    return calibres


def powder_types_from_repository():
    powder_types = ['Select component']
    for row in db.view_powder_types():
        powder_types.append(row[1])
    return powder_types


def powder_weights_from_repository():
    powder_weights = ['Select weight']
    for row in db.view_powder_weights():
        powder_weights.append(row)
    return powder_weights


def bullet_types_from_repository():
    bullet_types = ['Select component']
    for row in db.view_bullet_types():
        bullet_types.append(row[1])
    return bullet_types


def bullet_weights_from_repository():
    bullet_weights = ['Select weight']
    for row in db.view_bullet_weights():
        bullet_weights.append(row[1])
    return bullet_weights


def oals_from_repository():
    oals = ['Select length']
    for row in db.view_oals():
        oals.append(row)
    return oals


def primers_from_repository():
    primers = ['Select component']
    for row in db.view_primers():
        primers.append(row[1])
    return primers


def case_types_from_repository():
    case_types = ['Select component']
    for row in db.view_case_types():
        case_types.append(row[1])
    return case_types


def ratings_from_repository():
    ratings = ['Select rating']
    for row in db.view_ratings():
        ratings.append(row)
    ratings.remove(ratings[1])
    return ratings


# Function to reset comboboxes and empty entry boxes after saving new log entry on Add entry tab


def empty_log_entry_form(gun_combobox, calibre_combobox, powder_type_combobox, powder_weight_entry_widget,
                         bullet_type_combobox, bullet_weight_combobox, oal_entry_widget, primer_type_combobox,
                         case_type_combobox, no_made_entry_widget, preps_entry_widget):
    gun_combobox.set(guns_from_repository()[0])
    calibre_combobox.set(calibres_from_repository()[0])
    powder_type_combobox.set(powder_types_from_repository()[0])
    powder_weight_entry_widget.delete(0, END)
    bullet_type_combobox.set(bullet_types_from_repository()[0])
    bullet_weight_combobox.set(bullet_weights_from_repository()[0])
    oal_entry_widget.delete(0, END)
    primer_type_combobox.set(primers_from_repository()[0])
    case_type_combobox.set(case_types_from_repository()[0])
    no_made_entry_widget.delete(0, END)
    preps_entry_widget.delete(0, END)


# Function to save new log entry on Add entry tab, all fields required except 'Preparations'


def create_new_log_entry(gun_combobox, calibre_combobox, powder_type_combobox, powder_weight,
                         powder_weight_entry_widget, bullet_type_combobox, bullet_weight_combobox, oal,
                         oal_entry_widget, primer_type_combobox, case_type_combobox, no_made, no_made_entry_widget,
                         preps, preps_entry_widget):
    new_log_entry_info = messagebox.askquestion('Save Entry', 'Are you sure you want to save this entry?',
                                                icon='warning')
    if new_log_entry_info == 'yes':
        if gun_combobox.current() == 0 \
                or calibre_combobox.current() == 0 \
                or powder_type_combobox.current() == 0 \
                or len(powder_weight.get()) == 0 \
                or bullet_type_combobox.current() == 0 \
                or bullet_weight_combobox.current() == 0 \
                or len(oal.get()) == 0 \
                or primer_type_combobox.current() == 0 \
                or case_type_combobox.current() == 0 \
                or len(no_made.get()) == 0:
            messagebox.showwarning('Error', "All fields except 'Preparations' are required. No changes were made to "
                                            "your log.", icon='warning')
        else:
            try:
                entry_date = date.today()
                gun = str(gun_combobox.get())
                calibre = str(calibre_combobox.get())
                powder_type = str(powder_type_combobox.get())
                powder_weight = float(powder_weight.get())
                bullet_type = str(bullet_type_combobox.get())
                bullet_weight = int(bullet_weight_combobox.get())
                oal = oal.get()
                primer_type = str(primer_type_combobox.get())
                case_type = str(case_type_combobox.get())
                no_made = no_made.get()
                preps = preps.get()
                notes = ""
                rating = ""
                db.create_new_log_entry(entry_date, gun, calibre, powder_type, powder_weight, bullet_type,
                                        bullet_weight, oal, primer_type, case_type, no_made, preps, notes, rating)
                messagebox.showinfo('Success', 'Your log entry was successfully saved.')
                empty_log_entry_form(gun_combobox, calibre_combobox, powder_type_combobox, powder_weight_entry_widget,
                                     bullet_type_combobox, bullet_weight_combobox, oal_entry_widget,
                                     primer_type_combobox, case_type_combobox, no_made_entry_widget, preps_entry_widget)
            except:
                messagebox.showwarning('Error', 'Something went wrong and no changes were made to your log.',
                                       icon='warning')
    else:
        messagebox.showinfo('Cancelled', 'No changes were made to your log.')


window = Tk()
Window(window)
window.mainloop()
