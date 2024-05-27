import sys  # Sistem ile ilgili işlevler için sys modülünü içe aktarıyoruz
import sqlite3  # SQLite veritabanı ile çalışmak için sqlite3 modülünü içe aktarıyoruz
from PyQt5.QtCore import QTimer  # Zamanlayıcı için QTimer sınıfını içe aktarıyoruz
from PyQt5.QtGui import QMovie  # GIF animasyonu için QMovie sınıfını içe aktarıyoruz
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit,
                             QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog,
                             QFormLayout, QDialog, QDialogButtonBox, QLabel, QComboBox, QScrollArea, QGroupBox)  # PyQt5'ten gerekli widgetları içe aktarıyoruz

# SplashScreen sınıfı, başlangıçta gösterilecek bir açılış ekranı oluşturur
class SplashScreen(QDialog):
    def __init__(self, gif_path, duration=3000, parent=None):
        super().__init__(parent)  # Üst sınıfın init metodunu çağırıyoruz
        self.setWindowTitle("DATA MARİO")  # Pencere başlığını ayarlıyoruz
        self.setFixedSize(640, 480)  # Pencere boyutunu sabitliyoruz
        self.label = QLabel(self)  # QLabel oluşturup pencereye ekliyoruz
        self.movie = QMovie(gif_path)  # GIF animasyonunu yüklemek için QMovie nesnesi oluşturuyoruz
        self.label.setMovie(self.movie)  # QLabel'e filmi ayarlıyoruz
        self.movie.start()  # Animasyonu başlatıyoruz

        self.timer = QTimer(self)  # Zamanlayıcı oluşturuyoruz
        self.timer.timeout.connect(self.close_splash)  # Zamanlayıcı süresi dolduğunda close_splash metodunu çağıracak
        self.timer.start(duration)  # Zamanlayıcıyı belirli süre için başlatıyoruz

    def close_splash(self):
        self.timer.stop()  # Zamanlayıcıyı durduruyoruz
        self.accept()  # Diyaloğu kabul ediyoruz ve kapatıyoruz

# CreateDatabaseDialog sınıfı, yeni bir veritabanı oluşturmak için bir diyalog kutusu sağlar
class CreateDatabaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # Üst sınıfın init metodunu çağırıyoruz
        self.initUI()  # Kullanıcı arayüzünü başlatıyoruz

    def initUI(self):
        self.setWindowTitle("Create New Database")  # Pencere başlığını ayarlıyoruz
        self.layout = QVBoxLayout()  # Dikey kutu düzeni oluşturuyoruz

        self.db_name_input = QLineEdit()  # Veritabanı adı için giriş alanı oluşturuyoruz
        self.db_name_input.setPlaceholderText("Enter database name")  # Yer tutucu metin ayarlıyoruz
        self.layout.addWidget(self.db_name_input)  # Giriş alanını düzenlemeye ekliyoruz

        self.table_count_input = QLineEdit()  # Tablo sayısı için giriş alanı oluşturuyoruz
        self.table_count_input.setPlaceholderText("Enter number of tables")  # Yer tutucu metin ayarlıyoruz
        self.layout.addWidget(self.table_count_input)  # Giriş alanını düzenlemeye ekliyoruz

        self.add_tables_btn = QPushButton("Add Tables")  # Tablo ekleme düğmesi oluşturuyoruz
        self.add_tables_btn.clicked.connect(self.add_tables)  # Düğmeye tıklama olayını add_tables metoduna bağlıyoruz
        self.layout.addWidget(self.add_tables_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.tables_layout = QVBoxLayout()  # Tablolar için dikey kutu düzeni oluşturuyoruz

        self.scroll_area = QScrollArea()  # Kaydırma alanı oluşturuyoruz
        self.scroll_area.setWidgetResizable(True)  # Kaydırma alanını yeniden boyutlandırılabilir yapıyoruz
        self.scroll_content = QWidget()  # Kaydırma alanı için içerik widget'ı oluşturuyoruz
        self.scroll_content.setLayout(self.tables_layout)  # İçeriğe tablolar düzenini ekliyoruz
        self.scroll_area.setWidget(self.scroll_content)  # Kaydırma alanına içeriği ekliyoruz
        self.layout.addWidget(self.scroll_area)  # Kaydırma alanını düzenlemeye ekliyoruz

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)  # Tamam ve İptal düğmeleri olan bir düğme kutusu oluşturuyoruz
        self.button_box.accepted.connect(self.accept)  # Kabul edilen sinyali kabul metoduna bağlıyoruz
        self.button_box.rejected.connect(self.reject)  # Reddedilen sinyali reddet metoduna bağlıyoruz
        self.layout.addWidget(self.button_box)  # Düğme kutusunu düzenlemeye ekliyoruz

        self.setLayout(self.layout)  # Diyalog düzenini ayarlıyoruz

    def add_tables(self):
        try:
            table_count = int(self.table_count_input.text())  # Girişten tablo sayısını alıyoruz
            for i in range(table_count):
                table_group = QGroupBox(f"Table {i+1}")  # Her tablo için bir grup kutusu oluşturuyoruz
                table_layout = QVBoxLayout()  # Tablolar için dikey kutu düzeni oluşturuyoruz

                table_name_input = QLineEdit()  # Tablo adı için giriş alanı oluşturuyoruz
                table_name_input.setPlaceholderText("Enter table name")  # Yer tutucu metin ayarlıyoruz
                table_layout.addWidget(table_name_input)  # Giriş alanını tablo düzenine ekliyoruz

                column_count_input = QLineEdit()  # Sütun sayısı için giriş alanı oluşturuyoruz
                column_count_input.setPlaceholderText("Enter number of columns")  # Yer tutucu metin ayarlıyoruz
                column_count_input.textChanged.connect(lambda _, table_layout=table_layout, column_count_input=column_count_input: self.add_columns(table_layout, column_count_input))  # Sütun sayısı değiştiğinde add_columns metodunu çağırıyoruz
                table_layout.addWidget(column_count_input)  # Giriş alanını tablo düzenine ekliyoruz

                table_group.setLayout(table_layout)  # Tablo düzenini grup kutusuna ayarlıyoruz
                self.tables_layout.addWidget(table_group)  # Grup kutusunu tablolar düzenine ekliyoruz
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number of tables.")  # Geçersiz giriş için uyarı mesajı gösteriyoruz

    def add_columns(self, table_layout, column_count_input):
        column_count = int(column_count_input.text()) if column_count_input.text().isdigit() else 0  # Sütun sayısını alıyoruz
        while table_layout.count() > 2:  # Önceki sütun girişlerini kaldırıyoruz
            widget = table_layout.takeAt(2).widget()
            if widget:
                widget.deleteLater()

        for j in range(column_count):
            column_group = QGroupBox(f"Column {j+1}")  # Her sütun için bir grup kutusu oluşturuyoruz
            column_layout = QFormLayout()  # Sütunlar için form düzeni oluşturuyoruz

            column_name_input = QLineEdit()  # Sütun adı için giriş alanı oluşturuyoruz
            column_name_input.setPlaceholderText("Enter column name")  # Yer tutucu metin ayarlıyoruz
            column_layout.addRow("Name:", column_name_input)  # Form düzenine sütun adını ekliyoruz

            column_type_input = QComboBox()  # Sütun türü için açılır liste oluşturuyoruz
            column_type_input.addItems(["TEXT", "INTEGER", "REAL", "BLOB"])  # Açılır listeye türleri ekliyoruz
            column_layout.addRow("Type:", column_type_input)  # Form düzenine sütun türünü ekliyoruz

            column_group.setLayout(column_layout)  # Sütun düzenini grup kutusuna ayarlıyoruz
            table_layout.addWidget(column_group)  # Grup kutusunu tablo düzenine ekliyoruz

    def getInputs(self):
        db_name = self.db_name_input.text()  # Veritabanı adını alıyoruz
        tables = []
        for i in range(self.tables_layout.count()):
            table_group = self.tables_layout.itemAt(i).widget()
            table_name_input = table_group.findChild(QLineEdit)
            table_name = table_name_input.text()
            columns = []
            for j in range(table_group.layout().count() - 2):  # Tablo adı ve sütun sayısı girişlerini atlıyoruz
                column_group = table_group.layout().itemAt(2 + j).widget()
                column_name_input = column_group.findChild(QLineEdit)
                column_name = column_name_input.text()
                column_type_input = column_group.findChild(QComboBox)
                column_type = column_type_input.currentText()
                columns.append((column_name, column_type))
            tables.append((table_name, columns))
        return db_name, tables  # Veritabanı adını ve tabloları döndürüyoruz


# DatabaseBrowser sınıfı, veritabanı tarayıcı uygulamasını oluşturur
class DatabaseBrowser(QWidget):
    def __init__(self):
        super().__init__()  # Üst sınıfın init metodunu çağırıyoruz
        self.db_file = None  # Yüklü veritabanı dosyasını saklamak için değişken oluşturuyoruz
        self.initUI()  # Kullanıcı arayüzünü başlatıyoruz

    def initUI(self):
        self.layout = QVBoxLayout()  # Dikey kutu düzeni oluşturuyoruz

        self.create_db_btn = QPushButton('Create Database')  # Veritabanı oluşturma düğmesi oluşturuyoruz
        self.create_db_btn.clicked.connect(self.create_database)  # Düğmeye tıklama olayını create_database metoduna bağlıyoruz
        self.layout.addWidget(self.create_db_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.load_db_btn = QPushButton('Load Database')  # Veritabanı yükleme düğmesi oluşturuyoruz
        self.load_db_btn.clicked.connect(self.load_database)  # Düğmeye tıklama olayını load_database metoduna bağlıyoruz
        self.layout.addWidget(self.load_db_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.query_input = QLineEdit()  # SQL sorgusu için giriş alanı oluşturuyoruz
        self.query_input.setPlaceholderText("Enter SQL query")  # Yer tutucu metin ayarlıyoruz
        self.layout.addWidget(self.query_input)  # Giriş alanını düzenlemeye ekliyoruz

        self.execute_query_btn = QPushButton('Execute Query')  # Sorgu yürütme düğmesi oluşturuyoruz
        self.execute_query_btn.clicked.connect(self.execute_query)  # Düğmeye tıklama olayını execute_query metoduna bağlıyoruz
        self.layout.addWidget(self.execute_query_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.result_table = QTableWidget()  # Sorgu sonuçları için tablo widget'ı oluşturuyoruz
        self.result_table.setColumnCount(0)  # Başlangıçta sütun sayısını sıfırlıyoruz
        self.result_table.setRowCount(0)  # Başlangıçta satır sayısını sıfırlıyoruz
        self.layout.addWidget(self.result_table)  # Tablo widget'ını düzenlemeye ekliyoruz

        self.insert_record_btn = QPushButton('Insert Record')  # Kayıt ekleme düğmesi oluşturuyoruz
        self.insert_record_btn.clicked.connect(self.insert_record)  # Düğmeye tıklama olayını insert_record metoduna bağlıyoruz
        self.layout.addWidget(self.insert_record_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.delete_record_btn = QPushButton('Delete Record')  # Kayıt silme düğmesi oluşturuyoruz
        self.delete_record_btn.clicked.connect(self.delete_record)  # Düğmeye tıklama olayını delete_record metoduna bağlıyoruz
        self.layout.addWidget(self.delete_record_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.update_record_btn = QPushButton('Update Record')  # Kayıt güncelleme düğmesi oluşturuyoruz
        self.update_record_btn.clicked.connect(self.update_record)  # Düğmeye tıklama olayını update_record metoduna bağlıyoruz
        self.layout.addWidget(self.update_record_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.view_structure_btn = QPushButton('View Table Structure')  # Tablo yapısını görüntüleme düğmesi oluşturuyoruz
        self.view_structure_btn.clicked.connect(self.view_table_structure)  # Düğmeye tıklama olayını view_table_structure metoduna bağlıyoruz
        self.layout.addWidget(self.view_structure_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.show_db_btn = QPushButton('Show Loaded Database')  # Yüklü veritabanını gösterme düğmesi oluşturuyoruz
        self.show_db_btn.clicked.connect(self.show_loaded_database)  # Düğmeye tıklama olayını show_loaded_database metoduna bağlıyoruz
        self.layout.addWidget(self.show_db_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.setLayout(self.layout)  # Widget düzenini ayarlıyoruz
        self.setWindowTitle('DATA MARİO')  # Pencere başlığını ayarlıyoruz
        self.setGeometry(300, 300, 800, 600)  # Pencere boyutunu ve konumunu ayarlıyoruz

    def create_database(self):
        create_db_dialog = CreateDatabaseDialog(self)  # Yeni veritabanı oluşturma diyalogu oluşturuyoruz
        if create_db_dialog.exec_() == QDialog.Accepted:
            db_name, tables = create_db_dialog.getInputs()  # Kullanıcıdan veritabanı adı ve tabloları alıyoruz
            options = QFileDialog.Options()  # Dosya seçme diyalogu için seçenekler oluşturuyoruz
            file, _ = QFileDialog.getSaveFileName(self, "Create Database", f"{db_name}.db", "SQLite Files (*.db);;All Files (*)", options=options)
            if file:
                try:
                    conn = sqlite3.connect(file)  # Veritabanı bağlantısı oluşturuyoruz
                    cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
                    for table_name, columns in tables:
                        columns_str = ", ".join([f"{name} {type}" for name, type in columns])
                        cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")  # Tablo oluşturma sorgusu yürütüyoruz
                    conn.commit()  # Değişiklikleri kaydediyoruz
                    conn.close()  # Bağlantıyı kapatıyoruz
                    QMessageBox.information(self, "Success", f"Database {file} created successfully.")  # Başarı mesajı gösteriyoruz
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create database: {str(e)}")  # Hata mesajı gösteriyoruz

    def load_database(self):
        options = QFileDialog.Options()  # Dosya seçme diyalogu için seçenekler oluşturuyoruz
        file, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "SQLite Files (*.db);;All Files (*)", options=options)
        if file:
            self.db_file = file  # Seçilen dosya yolunu db_file değişkenine atıyoruz
            QMessageBox.information(self, "Success", f"Database {file} loaded successfully.")  # Başarı mesajı gösteriyoruz

    def execute_query(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
            return

        query = self.query_input.text()  # Giriş alanından sorguyu alıyoruz
        if not query:
            QMessageBox.warning(self, "Error", "No query entered.")  # Sorgu girilmediyse uyarı gösteriyoruz
            return

        try:
            conn = sqlite3.connect(self.db_file)  # Veritabanı bağlantısı oluşturuyoruz
            cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
            cursor.execute(query)  # Sorguyu yürütüyoruz
            conn.commit()  # Değişiklikleri kaydediyoruz

            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()  # Sorgu sonuçlarını alıyoruz
                self.show_query_results(cursor, rows)  # Sorgu sonuçlarını gösteriyoruz
            else:
                self.result_table.setColumnCount(0)  # Sütun sayısını sıfırlıyoruz
                self.result_table.setRowCount(0)  # Satır sayısını sıfırlıyoruz
                self.result_table.clearContents()  # Tablo içeriğini temizliyoruz
                QMessageBox.information(self, "Success", "Query executed successfully.")  # Başarı mesajı gösteriyoruz

            cursor.close()  # İmleci kapatıyoruz
            conn.close()  # Bağlantıyı kapatıyoruz
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to execute query: {str(e)}")  # Hata mesajı gösteriyoruz

    def show_query_results(self, cursor, rows):
        columns = [description[0] for description in cursor.description]  # Sütun adlarını alıyoruz
        self.result_table.setColumnCount(len(columns))  # Sütun sayısını ayarlıyoruz
        self.result_table.setHorizontalHeaderLabels(columns)  # Sütun başlıklarını ayarlıyoruz
        self.result_table.setRowCount(len(rows))  # Satır sayısını ayarlıyoruz

        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))  # Satır ve sütunlara öğeleri ekliyoruz

        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Sütunları eşit genişlikte yapıyoruz

    def insert_record(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
            return

        table, ok = QInputDialog.getText(self, 'Input', 'Enter table name:')  # Kullanıcıdan tablo adı alıyoruz
        if not ok or not table:
            return

        try:
            conn = sqlite3.connect(self.db_file)  # Veritabanı bağlantısı oluşturuyoruz
            cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
            cursor.execute(f"PRAGMA table_info({table})")  # Tablo bilgilerini alıyoruz
            columns = cursor.fetchall()  # Sütun bilgilerini alıyoruz

            if not columns:
                QMessageBox.warning(self, "Error", f"Table {table} does not exist.")  # Tablo yoksa uyarı gösteriyoruz
                return

            dialog = RecordDialog(columns, "Insert Record", self)  # Kayıt ekleme diyalogu oluşturuyoruz
            if dialog.exec_() == QDialog.Accepted:
                values = dialog.getValues()  # Kullanıcıdan değerleri alıyoruz
                placeholders = ', '.join(['?' for _ in values])
                cursor.execute(f"INSERT INTO {table} ({', '.join(values.keys())}) VALUES ({placeholders})", tuple(values.values()))  # Kayıt ekleme sorgusu yürütüyoruz
                conn.commit()  # Değişiklikleri kaydediyoruz
                QMessageBox.information(self, "Success", "Record inserted successfully.")  # Başarı mesajı gösteriyoruz

            cursor.close()  # İmleci kapatıyoruz
            conn.close()  # Bağlantıyı kapatıyoruz
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to insert record: {str(e)}")  # Hata mesajı gösteriyoruz

    def delete_record(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
            return

        table, ok = QInputDialog.getText(self, 'Input', 'Enter table name:')  # Kullanıcıdan tablo adı alıyoruz
        if not ok or not table:
            return

        try:
            conn = sqlite3.connect(self.db_file)  # Veritabanı bağlantısı oluşturuyoruz
            cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
            cursor.execute(f"PRAGMA table_info({table})")  # Tablo bilgilerini alıyoruz
            columns = cursor.fetchall()  # Sütun bilgilerini alıyoruz

            if not columns:
                QMessageBox.warning(self, "Error", f"Table {table} does not exist.")  # Tablo yoksa uyarı gösteriyoruz
                return

            dialog = RecordDialog(columns, "Delete Record", self)  # Kayıt silme diyalogu oluşturuyoruz
            if dialog.exec_() == QDialog.Accepted:
                values = dialog.getValues()  # Kullanıcıdan değerleri alıyoruz
                conditions = [f"{key} = '{value}'" for key, value in values.items() if value]
                if not conditions:
                    QMessageBox.warning(self, "Error", "No conditions specified for deletion.")  # Şart yoksa uyarı gösteriyoruz
                    return

                condition_str = ' AND '.join(conditions)
                cursor.execute(f"DELETE FROM {table} WHERE {condition_str}")  # Kayıt silme sorgusu yürütüyoruz
                conn.commit()  # Değişiklikleri kaydediyoruz
                QMessageBox.information(self, "Success", "Record deleted successfully.")  # Başarı mesajı gösteriyoruz

            cursor.close()  # İmleci kapatıyoruz
            conn.close()  # Bağlantıyı kapatıyoruz
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete record: {str(e)}")  # Hata mesajı gösteriyoruz

    def update_record(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
            return

        table, ok = QInputDialog.getText(self, 'Input', 'Enter table name:')  # Kullanıcıdan tablo adı alıyoruz
        if not ok or not table:
            return

        try:
            conn = sqlite3.connect(self.db_file)  # Veritabanı bağlantısı oluşturuyoruz
            cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
            cursor.execute(f"PRAGMA table_info({table})")  # Tablo bilgilerini alıyoruz
            columns = cursor.fetchall()  # Sütun bilgilerini alıyoruz

            if not columns:
                QMessageBox.warning(self, "Error", f"Table {table} does not exist.")  # Tablo yoksa uyarı gösteriyoruz
                return

            cursor.execute(f"SELECT * FROM {table}")  # Tabloyu sorguluyoruz
            rows = cursor.fetchall()  # Tablodaki kayıtları alıyoruz

            if not rows:
                QMessageBox.warning(self, "Error", f"No records found in table {table}.")  # Kayıt yoksa uyarı gösteriyoruz
                return

            # Güncellenecek kaydı seç
            items = [str(row) for row in rows]
            selected_row, ok = QInputDialog.getItem(self, "Select Record", "Select record to update:", items, 0, False)
            if not ok or not selected_row:
                return

            selected_row = eval(selected_row)

            # selected_row'u bir sözlüğe eşle
            existing_data = {columns[i][1]: str(selected_row[i]) for i in range(len(columns))}

            dialog = RecordDialog(columns, "Update Record", self, existing_data)  # Kayıt güncelleme diyalogu oluşturuyoruz
            if dialog.exec_() == QDialog.Accepted:
                values = dialog.getValues()  # Kullanıcıdan değerleri alıyoruz
                set_clauses = [f"{key} = '{value}'" for key, value in values.items() if value]

                condition_clauses = [f"{columns[i][1]} = '{selected_row[i]}'" for i in range(len(columns))]

                if not set_clauses:
                    QMessageBox.warning(self, "Error", "No values specified for update.")  # Değer yoksa uyarı gösteriyoruz
                    return

                set_str = ', '.join(set_clauses)
                condition_str = ' AND '.join(condition_clauses)
                cursor.execute(f"UPDATE {table} SET {set_str} WHERE {condition_str}")  # Kayıt güncelleme sorgusu yürütüyoruz
                conn.commit()  # Değişiklikleri kaydediyoruz
                QMessageBox.information(self, "Success", "Record updated successfully.")  # Başarı mesajı gösteriyoruz

            cursor.close()  # İmleci kapatıyoruz
            conn.close()  # Bağlantıyı kapatıyoruz
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update record: {str(e)}")  # Hata mesajı gösteriyoruz

    def view_table_structure(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
            return

        table, ok = QInputDialog.getText(self, 'Input', 'Enter table name:')  # Kullanıcıdan tablo adı alıyoruz
        if not ok or not table:
            return

        try:
            conn = sqlite3.connect(self.db_file)  # Veritabanı bağlantısı oluşturuyoruz
            cursor = conn.cursor()  # Veritabanı imleci oluşturuyoruz
            cursor.execute(f"PRAGMA table_info({table})")  # Tablo bilgilerini alıyoruz
            columns = cursor.fetchall()  # Sütun bilgilerini alıyoruz

            if not columns:
                QMessageBox.warning(self, "Error", f"Table {table} does not exist.")  # Tablo yoksa uyarı gösteriyoruz
                return

            structure_info = "\n".join([f"{col[1]} ({col[2]})" for col in columns])  # Tablo yapısını metin olarak oluşturuyoruz
            QMessageBox.information(self, "Table Structure", structure_info)  # Tablo yapısını bilgi mesajı olarak gösteriyoruz

            cursor.close()  # İmleci kapatıyoruz
            conn.close()  # Bağlantıyı kapatıyoruz
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve table structure: {str(e)}")  # Hata mesajı gösteriyoruz

    def show_loaded_database(self):
        if not self.db_file:
            QMessageBox.warning(self, "Error", "No database loaded.")  # Yüklü veritabanı yoksa uyarı gösteriyoruz
        else:
            QMessageBox.information(self, "Loaded Database", f"Currently loaded database: {self.db_file}")  # Yüklü veritabanı dosyasını bilgi mesajı olarak gösteriyoruz


# RecordDialog sınıfı, kayıt eklemek, silmek veya güncellemek için diyalog kutusu sağlar
class RecordDialog(QDialog):
    def __init__(self, columns, title, parent=None, existing_data=None):
        super().__init__(parent)  # Üst sınıfın init metodunu çağırıyoruz
        self.columns = columns  # Sütun bilgilerini alıyoruz
        self.existing_data = existing_data or {}  # Var olan verileri alıyoruz
        self.initUI(title)  # Kullanıcı arayüzünü başlatıyoruz

    def initUI(self, title):
        self.setWindowTitle(title)  # Pencere başlığını ayarlıyoruz
        self.layout = QVBoxLayout()  # Dikey kutu düzeni oluşturuyoruz

        self.form_layout = QFormLayout()  # Form düzeni oluşturuyoruz
        self.inputs = {}  # Giriş alanlarını saklamak için sözlük oluşturuyoruz

        for column in self.columns:
            column_name = column[1]
            input_field = QLineEdit()  # Giriş alanı oluşturuyoruz
            input_field.setPlaceholderText(f"Enter {column_name}")  # Yer tutucu metin ayarlıyoruz
            if column_name in self.existing_data:
                input_field.setText(self.existing_data[column_name])  # Var olan verileri giriş alanına ayarlıyoruz
            self.form_layout.addRow(column_name, input_field)  # Giriş alanını form düzenine ekliyoruz
            self.inputs[column_name] = input_field  # Giriş alanını sözlüğe ekliyoruz

        self.layout.addLayout(self.form_layout)  # Form düzenini genel düzene ekliyoruz

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)  # Tamam ve İptal düğmeleri olan bir düğme kutusu oluşturuyoruz
        self.button_box.accepted.connect(self.accept)  # Kabul edilen sinyali kabul metoduna bağlıyoruz
        self.button_box.rejected.connect(self.reject)  # Reddedilen sinyali reddet metoduna bağlıyoruz
        self.layout.addWidget(self.button_box)  # Düğme kutusunu düzene ekliyoruz

        self.setLayout(self.layout)  # Diyalog düzenini ayarlıyoruz

    def getValues(self):
        return {column: self.inputs[column].text() for column in self.inputs}  # Giriş alanlarındaki değerleri döndürüyoruz


# LoginDialog sınıfı, kullanıcı giriş ve kayıt işlemleri için diyalog kutusu sağlar
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # Üst sınıfın init metodunu çağırıyoruz
        self.initUI()  # Kullanıcı arayüzünü başlatıyoruz

    def initUI(self):
        self.setWindowTitle("Login")  # Pencere başlığını ayarlıyoruz
        self.layout = QVBoxLayout()  # Dikey kutu düzeni oluşturuyoruz

        self.email_input = QLineEdit()  # Email giriş alanı oluşturuyoruz
        self.email_input.setPlaceholderText("Enter email")  # Yer tutucu metin ayarlıyoruz
        self.layout.addWidget(self.email_input)  # Giriş alanını düzenlemeye ekliyoruz

        self.password_input = QLineEdit()  # Şifre giriş alanı oluşturuyoruz
        self.password_input.setPlaceholderText("Enter password")  # Yer tutucu metin ayarlıyoruz
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifre alanını gizli yapıyoruz
        self.layout.addWidget(self.password_input)  # Giriş alanını düzenlemeye ekliyoruz

        self.login_btn = QPushButton("Login")  # Giriş düğmesi oluşturuyoruz
        self.login_btn.clicked.connect(self.login)  # Düğmeye tıklama olayını login metoduna bağlıyoruz
        self.layout.addWidget(self.login_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.register_btn = QPushButton("Register")  # Kayıt düğmesi oluşturuyoruz
        self.register_btn.clicked.connect(self.register)  # Düğmeye tıklama olayını register metoduna bağlıyoruz
        self.layout.addWidget(self.register_btn)  # Düğmeyi düzenlemeye ekliyoruz

        self.setLayout(self.layout)  # Diyalog düzenini ayarlıyoruz

    def login(self):
        email = self.email_input.text()  # Email'i alıyoruz
        password = self.password_input.text()  # Şifreyi alıyoruz
        if self.verify_credentials(email, password):
            self.accept()  # Giriş başarılıysa diyalogu kabul ediyoruz
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")  # Geçersiz giriş bilgileri uyarısı gösteriyoruz

    def verify_credentials(self, email, password):
        try:
            with open("users.txt", "r") as file:  # Kullanıcı bilgilerini içeren dosyayı açıyoruz
                for line in file:
                    stored_email, stored_password = line.strip().split(",")  # Dosyadan email ve şifreyi alıyoruz
                    if stored_email == email and stored_password == password:
                        return True  # Email ve şifre eşleşiyorsa True döndürüyoruz
        except FileNotFoundError:
            return False  # Dosya bulunamazsa False döndürüyoruz
        return False  # Email ve şifre eşleşmezse False döndürüyoruz

    def register(self):
        email, ok = QInputDialog.getText(self, "Register", "Enter email:")  # Kullanıcıdan email alıyoruz
        if not ok or not email:
            return
        password, ok = QInputDialog.getText(self, "Register", "Enter password:")  # Kullanıcıdan şifre alıyoruz
        if not ok or not password:
            return
        with open("users.txt", "a") as file:  # Kullanıcı bilgilerini dosyaya ekliyoruz
            file.write(f"{email},{password}\n")
        QMessageBox.information(self, "Success", "User registered successfully")  # Başarı mesajı gösteriyoruz


# Ana uygulama çalıştırma kodu
if __name__ == "__main__":
    app = QApplication(sys.argv)  # PyQt uygulaması oluşturuyoruz

    splash = SplashScreen('/Mario_1-gif.gif')  # Açılış ekranı oluşturuyoruz
    if splash.exec_() == QDialog.Accepted:
        login_dialog = LoginDialog()  # Giriş diyalogu oluşturuyoruz
        if login_dialog.exec_() == QDialog.Accepted:
            ex = DatabaseBrowser()  # Veritabanı tarayıcı uygulamasını başlatıyoruz
            ex.show()  # Uygulamayı gösteriyoruz
            sys.exit(app.exec_())  # Uygulama ana döngüsünü başlatıyoruz
        else:
            sys.exit()  # Uygulamayı sonlandırıyoruz
