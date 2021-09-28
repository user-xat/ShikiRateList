from source.ShikiOAuth import ShikiOAuth
from PyQt5 import QtCore
from source.Shikimori import Shikimori
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QInputDialog, QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem

# rates_in_table = list()

class FormFunctions:
    @staticmethod
    def update_table(table: QTableWidget, shiki: Shikimori) -> None:
        rates = shiki.get_user_rates()
        
        row = 0
        table.blockSignals(True)
        table.setRowCount(0)
        table.setRowCount(len(rates))
        for item in reversed(rates):
            #print(item['updated_at'], type(item['updated_at']))
            title = QTableWidgetItem(str(item['anime']['russian']))
            title.setWhatsThis(str(item['id']))
            # it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)
            title.setFlags(title.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(row, 0, title)

            table.setItem(row, 1, QTableWidgetItem(str(item['score'])))

            episodes = QTableWidgetItem(str(item['episodes']))
            episodes.setWhatsThis(str(item['anime']['episodes']))
            table.setItem(row, 2, episodes)

            kind = QTableWidgetItem(item['anime']['kind'])
            kind.setFlags(kind.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(row, 3, kind)
            row += 1
        table.blockSignals(False)

    @staticmethod
    def evt_change_rate_changed(table: QTableWidget, shiki: Shikimori) -> None:
        row = table.selectedIndexes()[0].row()
        row1 = table.selectedItems()[0].row()
        rate_id = table.item(row, 0).whatsThis()
        new_score = table.item(row, 1).text()
        new_episodes = table.item(row, 2).text()
        shiki.put_user_rates(rate_id, new_score, new_episodes)

    @staticmethod
    def evt_delete_rate_clicked(table: QTableWidget, shiki: Shikimori) -> None:
        rows = table.selectedIndexes()
        if rows != []:
            row = rows[0].row()
            rate_id = table.item(row, 0).whatsThis()
            shiki.delete_user_rates(rate_id)
            table.removeRow(row)

    @staticmethod
    def evt_create_rate_clicked(table: QTableWidget, cbx: QComboBox, shiki: Shikimori) -> None:
        anime_id = cbx.currentData()
        if anime_id != None:
            shiki.post_user_rates(anime_id)
            FormFunctions.update_table(table, shiki)
    
    @staticmethod
    def evt_search_anime_clicked(led: QLineEdit, cbx: QComboBox, shiki: Shikimori) -> None:
        if led.text() is not None:
            animes = shiki.search_anime(led.text())
            cbx.clear()
            for anime in animes:
                cbx.addItem(anime['russian'], anime['id'])
    
    @staticmethod
    def evt_authorization_clicked(MainWindow: QMainWindow, shiki: Shikimori, table: QTableWidget, *args) -> None:
        tokens = ShikiOAuth.load_token()
        if tokens == None:
            oauth = ShikiOAuth()
            s_res, b_ok = QInputDialog.getText(MainWindow, "Authorization code", "Введите полученный код")
            if b_ok:
                tokens = oauth.get_access_token(s_res)
                shiki = Shikimori(tokens['access_token'], tokens['refresh_token'])
                ShikiOAuth.save_tokens(tokens)
                FormFunctions.update_table(table, shiki)
                for arg in args:
                    arg.setEnabled(True)
                table.setEnabled(True)
        # else:
        #     shiki = Shikimori(tokens['access_token'], tokens['refresh_token'] )
        #     FormFunctions.update_table(table, shiki)
        #     for arg in args:
        #         arg.setEnabled(True)
        #     table.setEnabled(True)



#self.shiki = Shikimori()
#FillForm.update_table(self.tbl_rates, shiki=self.shiki)

# self.shiki = Shikimori()
# FormFunctions.update_table(self.tbl_rates, shiki=self.shiki)

        # self.tbl_rates.setColumnWidth(0, 650)
        # self.tbl_rates.setColumnWidth(1, 80)
        # self.tbl_rates.setColumnWidth(2, 80)
        # self.tbl_rates.setColumnWidth(3, 80)
        # self.tbl_rates.setEnabled(False)

        # self.shiki = None
        # self.add_functions()

    # def add_functions(self):
    #     self.btn_search.clicked.connect(lambda: FormFunctions.evt_search_anime_clicked(self.led_anime_search, self.cbx_anime_search, self.shiki))
    #     self.btn_add_rate.clicked.connect(lambda: FormFunctions.evt_create_rate_clicked(self.tbl_rates, self.cbx_anime_search, self.shiki))
    #     self.btn_delete_rate.clicked.connect(lambda: FormFunctions.evt_delete_rate_clicked(self.tbl_rates, self.shiki))
    #     self.tbl_rates.itemChanged.connect(lambda: FormFunctions.evt_change_rate_changed(self.tbl_rates, self.shiki))
    #     self.menu_sign_in.triggered.connect(lambda: FormFunctions.evt_authorization_clicked(MainWindow, self.tbl_rates, self.shiki))