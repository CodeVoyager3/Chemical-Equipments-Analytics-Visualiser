from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, 
    QSizePolicy, QFileDialog, QMessageBox, QScrollArea, QListWidget,
    QListWidgetItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from theme import Theme
from ui.components import Card, ModernButton
from api_client import APIClient

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        # Apply Theme
        self.apply_theme()

        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        SizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(SizePolicy)

    def apply_theme(self):
        self.fig.patch.set_facecolor(Theme.CARD)
        self.axes.set_facecolor(Theme.CARD)
        
        self.axes.tick_params(colors=Theme.FOREGROUND, which='both')
        for spine in self.axes.spines.values():
            spine.set_edgecolor(Theme.BORDER)
            
        self.axes.xaxis.label.set_color(Theme.FOREGROUND)
        self.axes.yaxis.label.set_color(Theme.FOREGROUND)
        self.axes.title.set_color(Theme.FOREGROUND)

class Dashboard(QWidget):
    def __init__(self, parent=None, api_client=None):
        super().__init__(parent)
        # Use provided api_client or create a new one
        self.api_client = api_client if api_client else APIClient()
        self.stats = None
        self.batch_id = None  # Store batch_id for PDF export
        
        # Main Layout (Scrollable)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet(f"background-color: {Theme.BACKGROUND};")
        self.layout = QVBoxLayout(self.content_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(25)
        
        self.setup_hero_section()
        self.setup_upload_section()
        self.setup_stats_section()
        self.setup_charts_section()
        self.setup_recent_uploads_section()
        
        self.layout.addStretch()
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        
        # Load recent uploads on startup
        self.load_recent_uploads()

    def setup_hero_section(self):
        hero_frame = QFrame()
        hero_frame.setObjectName("HeroFrame")
        hero_frame.setStyleSheet(f"""
            #HeroFrame {{
                background-color: {Theme.CARD};
                border-radius: 12px;
                border: 1px solid {Theme.BORDER};
            }}
        """)
        hero_layout = QHBoxLayout(hero_frame)
        hero_layout.setContentsMargins(30, 30, 30, 30)
        
        # Text Content
        text_layout = QVBoxLayout()
        title = QLabel("Chemical Equipment Analytics Dashboard")
        title.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {Theme.FOREGROUND}; background: transparent; border: none;")
        
        subtitle = QLabel("Upload a CSV file to generate summary analytics including total equipment count, average operating values, and equipment type distribution.")
        subtitle.setStyleSheet(f"font-size: 14px; color: {Theme.MUTED}; background: transparent; border: none;")
        subtitle.setWordWrap(True)
        
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        hero_layout.addLayout(text_layout)
        
        # Simple Stats indicators in Hero (Right side)
        stats_layout = QHBoxLayout()
        
        # Helper to style stats without borders
        def style_stat_labels(lbl, desc):
            lbl.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {lbl.property('color')}; background: transparent; border: none;")
            desc.setStyleSheet(f"color: {Theme.MUTED}; background: transparent; border: none;")

        self.hero_count_lbl = QLabel("—")
        self.hero_count_lbl.setProperty("color", Theme.PRIMARY)
        self.hero_count_desc = QLabel("Equipment")
        style_stat_labels(self.hero_count_lbl, self.hero_count_desc)
        
        hero_stat1 = QVBoxLayout()
        hero_stat1.addWidget(self.hero_count_lbl, 0, Qt.AlignCenter)
        hero_stat1.addWidget(self.hero_count_desc, 0, Qt.AlignCenter)
        
        self.hero_types_lbl = QLabel("—")
        self.hero_types_lbl.setProperty("color", Theme.CHART_2)  # Blue
        self.hero_types_desc = QLabel("Types")
        style_stat_labels(self.hero_types_lbl, self.hero_types_desc)
        
        hero_stat2 = QVBoxLayout()
        hero_stat2.addWidget(self.hero_types_lbl, 0, Qt.AlignCenter)
        hero_stat2.addWidget(self.hero_types_desc, 0, Qt.AlignCenter)
        
        stats_layout.addLayout(hero_stat1)
        stats_layout.addSpacing(20)
        stats_layout.addLayout(hero_stat2)
        
        hero_layout.addLayout(stats_layout)
        
        self.layout.addWidget(hero_frame)

    def setup_upload_section(self):
        self.upload_card = QFrame()
        self.upload_card.setProperty("class", "Card")
        self.upload_card.setStyleSheet(f"""
            QFrame[class="Card"] {{
                background-color: {Theme.CARD};
                border: 2px dashed {Theme.PRIMARY};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self.upload_card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        icon_lbl = QLabel("⬆")
        icon_lbl.setStyleSheet(f"font-size: 40px; color: {Theme.PRIMARY}; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignCenter)
        
        title_lbl = QLabel("Upload Equipment Data")
        title_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Theme.FOREGROUND}; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        
        desc_lbl = QLabel("Upload CSV to analyze summary statistics")
        desc_lbl.setStyleSheet(f"color: {Theme.MUTED}; background: transparent;")
        desc_lbl.setAlignment(Qt.AlignCenter)
        
        # Button container for horizontal layout
        btn_container = QHBoxLayout()
        btn_container.setSpacing(15)
        
        self.upload_btn = ModernButton("Upload CSV", is_primary=True)
        self.upload_btn.setObjectName("UploadBtn")
        self.upload_btn.setFixedWidth(160)
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: {Theme.PRIMARY_FG};
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #5fd69a;
            }}
        """)
        self.upload_btn.clicked.connect(self.browse_file)
        
        # Export PDF Button
        self.pdf_btn = ModernButton("Export PDF", is_primary=False)
        self.pdf_btn.setObjectName("PdfBtn")
        self.pdf_btn.setFixedWidth(160)
        self.pdf_btn.setEnabled(False)  # Disabled until data is uploaded
        self.pdf_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT};
                color: {Theme.FOREGROUND};
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid {Theme.BORDER};
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
            QPushButton:disabled {{
                background-color: #f0f0f0;
                color: #a0a0a0;
            }}
        """)
        self.pdf_btn.clicked.connect(self.download_pdf)
        
        btn_container.addStretch()
        btn_container.addWidget(self.upload_btn)
        btn_container.addWidget(self.pdf_btn)
        btn_container.addStretch()
        
        layout.addWidget(icon_lbl)
        layout.addWidget(title_lbl)
        layout.addWidget(desc_lbl)
        layout.addSpacing(15)
        layout.addLayout(btn_container)
        
        self.layout.addWidget(self.upload_card)

    def setup_stats_section(self):
        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(15)
        
        # Placeholders to be updated
        self.card_total = Card("Total Equipment", "—", "Units registered in system")
        self.card_flow = Card("Avg Flowrate", "—", "m³/hr average flow")
        self.card_pressure = Card("Avg Pressure", "—", "Pa average pressure")
        self.card_temp = Card("Avg Temperature", "—", "°C average temp")
        
        self.stats_layout.addWidget(self.card_total)
        self.stats_layout.addWidget(self.card_flow)
        self.stats_layout.addWidget(self.card_pressure)
        self.stats_layout.addWidget(self.card_temp)
        
        self.stats_container.setVisible(False)  # Hidden until data loaded
        self.layout.addWidget(self.stats_container)

    def setup_charts_section(self):
        self.charts_container = QWidget()
        charts_layout = QHBoxLayout(self.charts_container)  # Side by side like React
        charts_layout.setContentsMargins(0, 0, 0, 0)
        charts_layout.setSpacing(25)
        
        # 1. Bar Chart (Distribution)
        bar_frame = QFrame()
        bar_frame.setProperty("class", "Card")
        bar_layout = QVBoxLayout(bar_frame)
        bar_header = QLabel("Equipment Count by Type")
        bar_header.setProperty("class", "CardTitle")
        bar_layout.addWidget(bar_header)
        
        self.bar_canvas = MplCanvas(self, width=5, height=4)
        bar_layout.addWidget(self.bar_canvas)
        
        # 2. Pie Chart (Share)
        pie_frame = QFrame()
        pie_frame.setProperty("class", "Card")
        pie_layout = QVBoxLayout(pie_frame)
        pie_header = QLabel("Equipment Type Share")
        pie_header.setProperty("class", "CardTitle")
        pie_layout.addWidget(pie_header)
        
        self.pie_canvas = MplCanvas(self, width=5, height=4)
        pie_layout.addWidget(self.pie_canvas)
        
        charts_layout.addWidget(bar_frame)
        charts_layout.addWidget(pie_frame)
        
        self.charts_container.setVisible(False)
        self.layout.addWidget(self.charts_container)

    def setup_recent_uploads_section(self):
        """Setup the recent uploads section showing last 5 uploads."""
        self.recent_uploads_frame = QFrame()
        self.recent_uploads_frame.setProperty("class", "Card")
        self.recent_uploads_frame.setStyleSheet(f"""
            QFrame[class="Card"] {{
                background-color: {Theme.CARD};
                border-radius: 8px;
                border: 1px solid {Theme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(self.recent_uploads_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Recent Uploads")
        header.setProperty("class", "CardTitle")
        header.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Theme.FOREGROUND}; background: transparent;")
        layout.addWidget(header)
        
        self.recent_uploads_list = QListWidget()
        self.recent_uploads_list.setMaximumHeight(200)
        self.recent_uploads_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Theme.BACKGROUND};
                border: 1px solid {Theme.BORDER};
                border-radius: 6px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Theme.BORDER};
                color: {Theme.FOREGROUND};
            }}
            QListWidget::item:selected {{
                background-color: rgba(114, 227, 173, 0.2);
            }}
            QListWidget::item:hover {{
                background-color: rgba(114, 227, 173, 0.1);
            }}
        """)
        self.recent_uploads_list.itemClicked.connect(self.on_recent_upload_clicked)
        layout.addWidget(self.recent_uploads_list)
        
        self.layout.addWidget(self.recent_uploads_frame)

    def load_recent_uploads(self):
        """Fetch and display recent uploads."""
        try:
            uploads = self.api_client.get_recent_uploads()
            self.recent_uploads_list.clear()
            
            if not uploads:
                item = QListWidgetItem("No recent uploads")
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                self.recent_uploads_list.addItem(item)
                return
            
            for upload in uploads:
                filename = upload.get('filename', 'Unknown')
                uploaded_at = upload.get('uploaded_at', '')
                equipment_count = upload.get('equipment_count', 0)
                batch_id = upload.get('id')
                
                # Format the date
                if uploaded_at:
                    from datetime import datetime
                    try:
                        dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                        date_str = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        date_str = uploaded_at[:16]
                else:
                    date_str = 'Unknown date'
                
                item_text = f"📄 {filename}  •  {date_str}  •  {equipment_count} items"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, batch_id)  # Store batch_id
                self.recent_uploads_list.addItem(item)
                
        except Exception as e:
            print(f"Failed to load recent uploads: {e}")

    def on_recent_upload_clicked(self, item):
        """Handle click on a recent upload item."""
        batch_id = item.data(Qt.UserRole)
        if batch_id:
            self.load_batch_stats(batch_id)

    def load_batch_stats(self, batch_id):
        """Load statistics for a specific batch."""
        try:
            data = self.api_client.get_batch_stats(batch_id)
            self.batch_id = batch_id
            self.stats = data.get("statistics", {})
            self.update_ui_with_stats()
            self.pdf_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load batch data:\n{str(e)}")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.upload_file(file_path)

    def upload_file(self, file_path):
        self.upload_btn.setText("Processing...")
        self.upload_btn.setEnabled(False)
        
        try:
            data = self.api_client.upload_csv(file_path)
            self.batch_id = data.get("batch_id")
            self.stats = data.get("statistics", {})
            self.update_ui_with_stats()
            self.pdf_btn.setEnabled(True)
            self.load_recent_uploads()  # Refresh recent uploads
            QMessageBox.information(self, "Success", "File uploaded and processed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to upload file:\n{str(e)}")
        finally:
            self.upload_btn.setText("Upload CSV")
            self.upload_btn.setEnabled(True)

    def download_pdf(self):
        """Download PDF report for the current batch."""
        if not self.batch_id:
            QMessageBox.warning(self, "No Data", "Please upload data first before exporting PDF.")
            return
        
        # Open file save dialog
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save PDF Report", 
            f"batch_{self.batch_id}_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not save_path:
            return
        
        self.pdf_btn.setText("Exporting...")
        self.pdf_btn.setEnabled(False)
        
        try:
            self.api_client.download_pdf(self.batch_id, save_path)
            QMessageBox.information(self, "Success", f"PDF report saved to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download PDF:\n{str(e)}")
        finally:
            self.pdf_btn.setText("Export PDF")
            self.pdf_btn.setEnabled(True)

    def update_ui_with_stats(self):
        if not self.stats:
            return
            
        # 1. Hero
        total_count = self.stats.get("total_count", 0)
        type_dist = self.stats.get("type_distribution", {})
        
        self.hero_count_lbl.setText(str(total_count))
        self.hero_types_lbl.setText(str(len(type_dist)))
        
        # 2. Cards
        self.card_total.value_lbl.setText(str(total_count))
        self.card_flow.value_lbl.setText(str(self.stats.get("average_flowrate", 0)))
        self.card_pressure.value_lbl.setText(str(self.stats.get("average_pressure", 0)))
        self.card_temp.value_lbl.setText(str(self.stats.get("average_temperature", 0)))
        
        self.stats_container.setVisible(True)
        self.charts_container.setVisible(True)
        
        # 3. Charts
        self.plot_bar_chart(type_dist)
        self.plot_pie_chart(type_dist)

    def plot_bar_chart(self, type_dist):
        labels = list(type_dist.keys())
        values = list(type_dist.values())
        
        self.bar_canvas.axes.clear()
        
        TEXT_COLOR = Theme.FOREGROUND 
        
        self.bar_canvas.axes.bar(labels, values, color=Theme.CHART_1, alpha=0.9)
        self.bar_canvas.axes.set_title("Count per Type", color=TEXT_COLOR, fontsize=12, fontweight='bold')
        self.bar_canvas.axes.tick_params(colors=TEXT_COLOR, labelcolor=TEXT_COLOR, axis='x', rotation=45)
        self.bar_canvas.axes.tick_params(colors=TEXT_COLOR, labelcolor=TEXT_COLOR, axis='y')
        
        # Style spines
        for spine in self.bar_canvas.axes.spines.values():
            spine.set_edgecolor(Theme.BORDER)
            
        self.bar_canvas.axes.patch.set_alpha(0)
        self.bar_canvas.fig.subplots_adjust(bottom=0.25)
        
        self.bar_canvas.draw()

    def plot_pie_chart(self, type_dist):
        labels = list(type_dist.keys())
        values = list(type_dist.values())
        
        # React-matching color palette
        colors = [
            Theme.CHART_1, Theme.CHART_2, Theme.CHART_3, Theme.CHART_4, Theme.CHART_5,
            Theme.CHART_6, Theme.CHART_7, Theme.CHART_8, Theme.CHART_9, Theme.CHART_10
        ]
        
        color_map = [colors[i % len(colors)] for i in range(len(values))]
        
        self.pie_canvas.axes.clear()
        
        TEXT_COLOR = Theme.FOREGROUND
        
        wedges, texts, autotexts = self.pie_canvas.axes.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=color_map,
            textprops={'color': TEXT_COLOR},
            wedgeprops={'edgecolor': Theme.CARD, 'linewidth': 1}
        )
        
        for text in texts:
            text.set_color(TEXT_COLOR)
            text.set_fontsize(9)
            
        for autotext in autotexts:
            autotext.set_color("#ffffff")
            autotext.set_fontweight('bold')
        
        self.pie_canvas.axes.set_title("Type Share", color=TEXT_COLOR, fontsize=12, fontweight='bold')
        self.pie_canvas.draw()
