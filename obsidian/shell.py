import os
import sys
import subprocess
from pathlib import Path
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
 QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
 QPushButton, QTextEdit, QLineEdit, QFileSystemModel, QTreeView,
 QTabWidget, QMessageBox, QSplitter, QListWidget, QFrame
)
from eden import answer

STYLE = """
QWidget {background:#030917;color:#dcefff;font-family:'DejaVu Sans';font-size:12px}
QMainWindow {background:#030917}
QFrame#panel {background:#081a35;border:1px solid #1165a4;border-radius:12px}
QPushButton {background:#0b2c54;border:1px solid #1689ca;border-radius:8px;padding:9px;color:#e2f6ff}
QPushButton:hover {background:#10558b;border-color:#00d9ff}
QLineEdit,QTextEdit,QTreeView,QListWidget,QTabWidget {background:#07152b;border:1px solid #125783;border-radius:8px;padding:7px}
QTabBar::tab {background:#0b2b4c;color:#bde8ff;padding:10px;border:1px solid #125783}
QTabBar::tab:selected {background:#09517f;color:#fff}
QLabel#heading {font-size:26px;font-weight:bold;color:#00d9ff}
"""
APPS = [
 ("Explorer","Files"), ("Terminal","Terminal"), ("EDEN AI","EDEN"),
 ("Security Center","Security"), ("Network Center","Network"),
 ("System Monitor","Monitor"), ("Developer Studio","Developer"),
 ("OBS Package Manager","Packages"), ("Financial Integrity","Finance"),
 ("Identity Guardian","Identity"), ("Settings","Settings")
]

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OBSIDIAN OS — Native Desktop")
        self.resize(1280, 800)
        root=QWidget(); self.setCentralWidget(root)
        outer=QVBoxLayout(root)
        head=QHBoxLayout()
        brand=QLabel("◈  OBSIDIAN OS"); brand.setObjectName("heading"); head.addWidget(brand)
        head.addStretch()
        self.clock=QLabel(QDateTime.currentDateTime().toString("ddd dd MMM yyyy · hh:mm"))
        head.addWidget(self.clock); outer.addLayout(head)
        splitter=QSplitter(); outer.addWidget(splitter,1)
        side=QFrame(); side.setObjectName("panel"); side.setMinimumWidth(205)
        left=QVBoxLayout(side); left.addWidget(QLabel("SYSTEM APPLICATIONS"))
        for title,key in APPS:
            btn=QPushButton(title);btn.clicked.connect(lambda _,k=key:self.open_app(k));left.addWidget(btn)
        left.addStretch(); splitter.addWidget(side)
        self.tabs=QTabWidget(); self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        splitter.addWidget(self.tabs);splitter.setStretchFactor(1,1)
        self.open_app("EDEN")
    def page(self,title):
        panel=QWidget();layout=QVBoxLayout(panel)
        h=QLabel(title.upper());h.setObjectName("heading");layout.addWidget(h)
        self.tabs.addTab(panel,title);self.tabs.setCurrentWidget(panel)
        return layout
    def open_app(self,key):
        l=self.page(key)
        if key=="Files":
            bar=QLineEdit(str(Path.home()));l.addWidget(bar)
            model=QFileSystemModel();model.setRootPath(str(Path.home()))
            view=QTreeView();view.setModel(model);view.setRootIndex(model.index(str(Path.home())))
            bar.returnPressed.connect(lambda:view.setRootIndex(model.index(bar.text())))
            l.addWidget(view)
        elif key=="Terminal":
            l.addWidget(QLabel("Launch the system terminal as a separate Linux window."))
            b=QPushButton("Open XFCE Terminal")
            b.clicked.connect(lambda:subprocess.Popen(["xfce4-terminal"]))
            l.addWidget(b)
        elif key=="EDEN":
            history=QTextEdit();history.setReadOnly(True);history.setText("EDEN AI — Local-first interface\nNo inference model connected yet.")
            l.addWidget(history)
            entry=QLineEdit();entry.setPlaceholderText("Ask EDEN...");l.addWidget(entry)
            def send():
                q=entry.text().strip()
                if q: history.append("YOU: "+q+"\nEDEN: "+answer(q));entry.clear()
            entry.returnPressed.connect(send)
        elif key=="Developer":
            l.addWidget(QLabel("Native OBS SDK · Python / GCC / Node.js / Rust"))
            l.addWidget(QLabel("CLI: obs init APPNAME | obs build APPDIR | obs inspect FILE.obs"))
            b=QPushButton("Open development terminal")
            b.clicked.connect(lambda:subprocess.Popen(["xfce4-terminal"]))
            l.addWidget(b)
        elif key=="Packages":
            l.addWidget(QLabel(".obs package validation is available via the obs CLI."))
            l.addWidget(QLabel("Installation and publisher signing are not implemented."))
        elif key=="Monitor":
            import shutil
            total,used,free=shutil.disk_usage(Path.home())
            l.addWidget(QLabel(f"Home filesystem usage: {used//(1024**3)} / {total//(1024**3)} GiB"))
            l.addWidget(QLabel("For live system monitoring, launch the system task manager."))
            b=QPushButton("Open Task Manager");b.clicked.connect(lambda:subprocess.Popen(["xfce4-taskmanager"]))
            l.addWidget(b)
        elif key=="Network":
            l.addWidget(QLabel("Network configuration is managed by NetworkManager."))
            b=QPushButton("Open Network Connections");b.clicked.connect(lambda:subprocess.Popen(["nm-connection-editor"]))
            l.addWidget(b)
        elif key=="Settings":
            l.addWidget(QLabel("OBSIDIAN appearance · native Linux configuration"))
            b=QPushButton("Open XFCE Settings");b.clicked.connect(lambda:subprocess.Popen(["xfce4-settings-manager"]))
            l.addWidget(b)
        else:
            l.addWidget(QLabel("Module: "+key))
            l.addWidget(QLabel("Integration pending. No live security or financial monitoring is active."))
        l.addStretch()

if __name__=="__main__":
    app=QApplication(sys.argv);app.setStyleSheet(STYLE)
    window=Desktop();window.show();sys.exit(app.exec())
