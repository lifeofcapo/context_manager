#!/usr/bin/env python3
"""
Context Manager - Professional context gathering tool for LLMs
Modern Windows 11-style dark theme UI
"""

import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
import threading

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QFileDialog,
    QMessageBox, QSplitter, QTextEdit, QComboBox, QCheckBox,
    QGroupBox, QProgressBar, QStatusBar, QMenu, QHeaderView,
    QLineEdit, QTabWidget, QListWidget, QListWidgetItem, QDialog,
    QFormLayout, QSpinBox, QDialogButtonBox, QFrame, QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread, QSize
from PyQt6.QtGui import QFont, QAction, QIcon, QColor, QTextCursor, QPalette

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

COLORS = {
    "bg_base":       "#0f0f0f",
    "bg_surface":    "#1c1c1c",
    "bg_elevated":   "#262626",
    "bg_popup":      "#2d2d2d",
    "bg_input":      "#1e1e1e",
    "accent":        "#0078d4",
    "accent_hover":  "#1a8fe3",
    "accent_press":  "#006ac1",
    "accent_muted":  "#1a3a52",
    "border":        "#3a3a3a",
    "border_focus":  "#0078d4",
    "border_subtle": "#2a2a2a",
    "text_primary":  "#e8e8e8",
    "text_secondary":"#a0a0a0",
    "text_disabled": "#5a5a5a",
    "text_accent":   "#60b8f5",
    "success":       "#4caf50",
    "error":         "#f44336",
    "sidebar_bg":    "#161616",
}


def make_stylesheet() -> str:
    c = COLORS
    return f"""
QMainWindow, QWidget {{
    background-color: {c['bg_base']};
    color: {c['text_primary']};
    font-family: "Segoe UI", "Inter", "SF Pro Display", sans-serif;
    font-size: 12px;
}}
QMenuBar {{
    background-color: {c['bg_base']};
    color: {c['text_primary']};
    border-bottom: 1px solid {c['border_subtle']};
    padding: 2px 6px;
}}
QMenuBar::item {{
    padding: 5px 10px;
    border-radius: 4px;
    background: transparent;
}}
QMenuBar::item:selected {{ background-color: {c['bg_elevated']}; }}
QMenuBar::item:pressed {{ background-color: {c['bg_popup']}; }}
QMenu {{
    background-color: {c['bg_popup']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    padding: 4px;
    color: {c['text_primary']};
}}
QMenu::item {{
    padding: 7px 28px 7px 12px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {c['accent_muted']};
    color: {c['text_accent']};
}}
QMenu::separator {{
    height: 1px;
    background: {c['border_subtle']};
    margin: 4px 8px;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {c['border']};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {c['text_disabled']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {c['border']};
    border-radius: 4px;
    min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{ background: {c['text_disabled']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QPushButton {{
    background-color: {c['bg_elevated']};
    color: {c['text_primary']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {c['bg_popup']};
    border-color: {c['text_disabled']};
}}
QPushButton:pressed {{
    background-color: {c['bg_surface']};
}}
QPushButton:disabled {{
    color: {c['text_disabled']};
    border-color: {c['border_subtle']};
}}
QPushButton#accent {{
    background-color: {c['accent']};
    color: white;
    border: none;
    font-weight: 600;
}}
QPushButton#accent:hover {{ background-color: {c['accent_hover']}; }}
QPushButton#accent:pressed {{ background-color: {c['accent_press']}; }}
QPushButton#danger {{
    background-color: transparent;
    color: {c['error']};
    border: 1px solid {c['error']};
}}
QPushButton#danger:hover {{ background-color: rgba(244, 67, 54, 0.12); }}
QPushButton#ghost {{
    background-color: transparent;
    border: none;
    color: {c['text_secondary']};
    padding: 6px 10px;
}}
QPushButton#ghost:hover {{
    background-color: {c['bg_elevated']};
    color: {c['text_primary']};
}}
QLineEdit {{
    background-color: {c['bg_input']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    color: {c['text_primary']};
    padding: 5px 10px;
    selection-background-color: {c['accent']};
}}
QLineEdit:focus {{ border-color: {c['border_focus']}; }}
QLineEdit:hover:!focus {{ border-color: {c['text_disabled']}; }}
QComboBox {{
    background-color: {c['bg_input']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    color: {c['text_primary']};
    padding: 5px 10px;
    min-width: 80px;
}}
QComboBox:focus {{ border-color: {c['border_focus']}; }}
QComboBox:hover {{ border-color: {c['text_disabled']}; }}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox::down-arrow {{
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {c['text_secondary']};
    width: 0; height: 0;
    margin-right: 6px;
}}
QComboBox QAbstractItemView {{
    background-color: {c['bg_popup']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    color: {c['text_primary']};
    selection-background-color: {c['accent_muted']};
    selection-color: {c['text_accent']};
    padding: 4px;
    outline: none;
}}
QTreeWidget {{
    background-color: {c['bg_input']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    color: {c['text_primary']};
    alternate-background-color: {c['bg_surface']};
    outline: none;
    gridline-color: {c['border_subtle']};
    show-decoration-selected: 1;
}}
QTreeWidget::item {{ padding: 5px 4px; }}
QTreeWidget::item:hover {{ background-color: {c['bg_elevated']}; }}
QTreeWidget::item:selected {{
    background-color: {c['accent_muted']};
    color: {c['text_accent']};
}}
QHeaderView::section {{
    background-color: {c['bg_surface']};
    color: {c['text_secondary']};
    border: none;
    border-bottom: 1px solid {c['border']};
    border-right: 1px solid {c['border_subtle']};
    padding: 6px 8px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}}
QHeaderView::section:last {{ border-right: none; }}
QListWidget {{
    background-color: {c['bg_input']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    color: {c['text_primary']};
    outline: none;
}}
QListWidget::item {{
    padding: 9px 12px;
    border-bottom: 1px solid {c['border_subtle']};
}}
QListWidget::item:hover {{ background-color: {c['bg_elevated']}; }}
QListWidget::item:selected {{
    background-color: {c['accent_muted']};
    color: {c['text_accent']};
    border-left: 2px solid {c['accent']};
}}
QTextEdit {{
    background-color: {c['bg_input']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    color: {c['text_primary']};
    padding: 8px;
    selection-background-color: {c['accent']};
}}
QTextEdit:focus {{ border-color: {c['border_focus']}; }}
QLabel {{ color: {c['text_primary']}; background: transparent; }}
QLabel#section_title {{
    font-size: 11px;
    font-weight: 700;
    color: {c['text_secondary']};
    letter-spacing: 0.8px;
}}
QLabel#count_badge {{
    background-color: {c['accent_muted']};
    color: {c['text_accent']};
    border-radius: 999px;
    padding: 1px 8px;
    font-size: 11px;
    font-weight: 600;
}}
QSplitter::handle {{
    background-color: {c['border_subtle']};
    width: 1px;
}}
QSplitter::handle:hover {{ background-color: {c['border']}; }}
QStatusBar {{
    background-color: {c['bg_surface']};
    color: {c['text_secondary']};
    border-top: 1px solid {c['border_subtle']};
    font-size: 11px;
    padding: 0 8px;
}}
QProgressBar {{
    background-color: {c['bg_elevated']};
    border: none;
    border-radius: 999px;
    height: 4px;
    color: transparent;
}}
QProgressBar::chunk {{
    background-color: {c['accent']};
    border-radius: 999px;
}}
QGroupBox {{
    border: 1px solid {c['border']};
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px 8px 8px 8px;
    font-size: 11px;
    font-weight: 600;
    color: {c['text_secondary']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {c['text_secondary']};
}}
QDialog {{
    background-color: {c['bg_surface']};
    border: 1px solid {c['border']};
    border-radius: 12px;
}}
QCheckBox {{ color: {c['text_primary']}; spacing: 6px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1.5px solid {c['border']};
    border-radius: 3px;
    background: {c['bg_input']};
}}
QCheckBox::indicator:hover {{ border-color: {c['accent']}; }}
QCheckBox::indicator:checked {{
    background-color: {c['accent']};
    border-color: {c['accent']};
}}
QToolTip {{
    background-color: {c['bg_popup']};
    color: {c['text_primary']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 11px;
}}
"""

class SectionLabel(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text.upper(), parent)
        self.setObjectName("section_title")


class CountBadge(QLabel):
    def __init__(self, text: str = "0", parent=None):
        super().__init__(text, parent)
        self.setObjectName("count_badge")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setStyleSheet(f"color: {COLORS['border_subtle']}; margin: 2px 0;")
        self.setMaximumHeight(1)

class FileWatcherSignals(QObject):
    file_changed = pyqtSignal(str, str)
    project_updated = pyqtSignal(str)


class ProjectFileHandler(FileSystemEventHandler):
    def __init__(self, project_id, signals, ignored_patterns):
        self.project_id = project_id
        self.signals = signals
        self.ignored_patterns = ignored_patterns

    def on_modified(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.signals.file_changed.emit(event.src_path, 'modified')
            self.signals.project_updated.emit(self.project_id)

    def on_created(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.signals.file_changed.emit(event.src_path, 'created')
            self.signals.project_updated.emit(self.project_id)

    def on_deleted(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.signals.file_changed.emit(event.src_path, 'deleted')
            self.signals.project_updated.emit(self.project_id)

    def _should_ignore(self, path):
        return any(p in path for p in self.ignored_patterns)


class ProjectWatcher(QThread):
    def __init__(self, project_id, project_path, ignored_patterns):
        super().__init__()
        self.project_id = project_id
        self.project_path = project_path
        self.ignored_patterns = ignored_patterns
        self.observer = None
        self.signals = FileWatcherSignals()

    def run(self):
        self.observer = Observer()
        handler = ProjectFileHandler(self.project_id, self.signals, self.ignored_patterns)
        self.observer.schedule(handler, self.project_path, recursive=True)
        self.observer.start()
        try:
            while True:
                self.msleep(1000)
        except Exception:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()


class ContextBuilder:
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
        '.hpp', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.kts',
        '.sql', '.html', '.css', '.scss', '.sass', '.less', '.json', '.xml',
        '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.md', '.txt',
        '.sh', '.bash', '.zsh', '.ps1', '.dockerfile', '.gitignore'
    }

    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024

    def build(self, project_path, selected_files, ignored_patterns, format_type):
        context = {
            'project_path': project_path,
            'timestamp': datetime.now().isoformat(),
            'files': [], 'total_files': 0, 'total_size': 0
        }
        total_size = file_count = 0
        for fp in selected_files:
            if not os.path.exists(fp):
                continue
            fs = os.path.getsize(fp)
            if fs > self.max_file_size:
                continue
            if any(p in fp for p in ignored_patterns):
                continue
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                context['files'].append({
                    'path': os.path.relpath(fp, project_path),
                    'absolute_path': fp,
                    'extension': os.path.splitext(fp)[1].lower(),
                    'size': fs, 'content': content
                })
                total_size += fs
                file_count += 1
            except Exception as e:
                print(f"Error reading {fp}: {e}")
        context['total_files'] = file_count
        context['total_size'] = total_size
        return context

    def export_to_format(self, context, format_type):
        if format_type == 'markdown':
            return self._export_markdown(context)
        elif format_type == 'json':
            return self._export_json(context)
        elif format_type == 'xml':
            return self._export_xml(context)
        return self._export_markdown(context)

    def _export_markdown(self, context):
        out = [
            f"# Project Context Export\n",
            f"**Project Path:** `{context['project_path']}`\n",
            f"**Export Date:** {context['timestamp']}\n",
            f"**Total Files:** {context['total_files']}\n",
            f"**Total Size:** {self._format_size(context['total_size'])}\n",
            "---\n\n",
        ]
        for fi in context['files']:
            out += [
                f"## File: `{fi['path']}`\n",
                f"**Extension:** {fi['extension']}\n",
                f"**Size:** {self._format_size(fi['size'])}\n",
                "\n```" + self._get_language(fi['extension']) + "\n",
                fi['content'], "\n```\n\n---\n\n"
            ]
        return ''.join(out)

    def _export_json(self, context):
        return json.dumps({
            'metadata': {
                'project_path': context['project_path'],
                'export_date': context['timestamp'],
                'total_files': context['total_files'],
                'total_size': context['total_size']
            },
            'files': [{'path': fi['path'], 'extension': fi['extension'],
                        'size': fi['size'], 'content': fi['content']}
                      for fi in context['files']]
        }, indent=2, ensure_ascii=False)

    def _export_xml(self, context):
        import xml.etree.ElementTree as ET
        from xml.dom import minidom
        root = ET.Element('context')
        meta = ET.SubElement(root, 'metadata')
        ET.SubElement(meta, 'project_path').text = context['project_path']
        ET.SubElement(meta, 'export_date').text = context['timestamp']
        ET.SubElement(meta, 'total_files').text = str(context['total_files'])
        ET.SubElement(meta, 'total_size').text = str(context['total_size'])
        files_el = ET.SubElement(root, 'files')
        for fi in context['files']:
            fe = ET.SubElement(files_el, 'file')
            ET.SubElement(fe, 'path').text = fi['path']
            ET.SubElement(fe, 'extension').text = fi['extension']
            ET.SubElement(fe, 'size').text = str(fi['size'])
            ET.SubElement(fe, 'content').text = fi['content']
        return minidom.parseString(ET.tostring(root, encoding='unicode')).toprettyxml(indent='  ')

    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _get_language(self, ext):
        m = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript',
             '.jsx': 'jsx', '.tsx': 'tsx', '.java': 'java', '.cpp': 'cpp',
             '.c': 'c', '.cs': 'csharp', '.go': 'go', '.rs': 'rust',
             '.rb': 'ruby', '.php': 'php', '.html': 'html', '.css': 'css',
             '.json': 'json', '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml',
             '.md': 'markdown', '.sh': 'bash', '.sql': 'sql'}
        return m.get(ext, 'text')

class GlobalIgnoreDialog(QDialog):
    def __init__(self, current_patterns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Global Ignore Patterns")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.setMinimumHeight(460)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Global Ignore Patterns")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['text_primary']};")
        layout.addWidget(title)

        desc = QLabel("These patterns apply to ALL projects. Matched against file paths (partial match).")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(desc)

        layout.addWidget(Divider())

        self.patterns_edit = QTextEdit()
        self.patterns_edit.setPlaceholderText("node_modules\n__pycache__\n.env\n*.log\n.git")
        self.patterns_edit.setText('\n'.join(current_patterns))
        self.patterns_edit.setMinimumHeight(180)
        layout.addWidget(self.patterns_edit)

        quick_group = QGroupBox("Quick Add")
        quick_layout = QHBoxLayout(quick_group)
        quick_layout.setSpacing(6)
        quick_layout.setContentsMargins(10, 14, 10, 10)
        chip_style = f"""
            QPushButton {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['border']};
                border-radius: 999px;
                color: {COLORS['text_secondary']};
                padding: 3px 10px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_muted']};
                color: {COLORS['text_accent']};
                border-color: {COLORS['accent']};
            }}
        """
        for p in ["node_modules", "__pycache__", ".env", "*.log", ".git",
                  ".vscode", ".idea", "dist", "build", "*.pyc", ".DS_Store"]:
            btn = QPushButton(p)
            btn.setStyleSheet(chip_style)
            btn.clicked.connect(lambda checked, pat=p: self.add_pattern(pat))
            quick_layout.addWidget(btn)
        quick_layout.addStretch()
        layout.addWidget(quick_group)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        reset_btn = QPushButton("Reset to defaults")
        reset_btn.setObjectName("ghost")
        reset_btn.clicked.connect(self.reset_patterns)
        btn_row.addWidget(reset_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        ok_btn = QPushButton("Save Changes")
        ok_btn.setObjectName("accent")
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def add_pattern(self, pattern):
        lines = [p.strip() for p in self.patterns_edit.toPlainText().split('\n') if p.strip()]
        if pattern not in lines:
            lines.append(pattern)
            self.patterns_edit.setText('\n'.join(lines))

    def reset_patterns(self):
        self.patterns_edit.setText('\n'.join([
            "node_modules", "__pycache__", ".env", "*.log", ".git",
            ".vscode", ".idea", "dist", "build", "*.pyc", ".DS_Store",
            "Thumbs.db", "*.tmp", "*.swp", ".sass-cache"
        ]))

    def get_patterns(self):
        return [p.strip() for p in self.patterns_edit.toPlainText().strip().split('\n') if p.strip()]


class ProjectManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.projects = {}
        self.watchers = {}
        self.global_ignore_patterns = [
            "node_modules", "__pycache__", ".env", "*.log", ".git",
            ".vscode", ".idea", "dist", "build", "*.pyc", ".DS_Store",
            "Thumbs.db", "*.tmp", "*.swp"
        ]
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.projects = data.get('projects', {})
                    self.global_ignore_patterns = data.get('global_ignore_patterns', self.global_ignore_patterns)
            except Exception:
                self.projects = {}

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump({'projects': self.projects,
                       'global_ignore_patterns': self.global_ignore_patterns}, f, indent=2, ensure_ascii=False)

    def add_project(self, project_id, path):
        self.projects[project_id] = {
            'id': project_id, 'name': os.path.basename(path),
            'path': path, 'enabled': True,
            'created_at': datetime.now().isoformat()
        }
        self.save_config()

    def remove_project(self, project_id):
        if project_id in self.projects:
            del self.projects[project_id]
            self.save_config()

    def update_project(self, project_id, **kwargs):
        if project_id in self.projects:
            self.projects[project_id].update(kwargs)
            self.save_config()

    def get_project(self, project_id):
        return self.projects.get(project_id)

    def get_all_projects(self):
        return list(self.projects.values())

    def get_combined_ignored_patterns(self, project_id):
        project = self.get_project(project_id)
        if not project:
            return self.global_ignore_patterns
        return list(set(self.global_ignore_patterns + project.get('ignored_patterns', [])))

    def update_global_ignore_patterns(self, patterns):
        self.global_ignore_patterns = patterns
        self.save_config()

    def start_watching(self, project_id, signals_handler):
        project = self.get_project(project_id)
        if not project or not project.get('enabled'):
            return
        ignored = set(self.get_combined_ignored_patterns(project_id))
        watcher = ProjectWatcher(project_id, project['path'], ignored)
        watcher.signals.file_changed.connect(signals_handler)
        watcher.signals.project_updated.connect(signals_handler)
        watcher.start()
        self.watchers[project_id] = watcher

    def stop_watching(self, project_id):
        if project_id in self.watchers:
            self.watchers[project_id].stop()
            del self.watchers[project_id]

    def stop_all_watching(self):
        for w in self.watchers.values():
            w.stop()
        self.watchers.clear()

class ContextManagerPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.context_builder = ContextBuilder()
        self.current_project = None
        self.current_files = []

        self.setWindowTitle("Context Manager")
        self.setMinimumSize(1060, 640)
        self.resize(1280, 760)

        self.init_ui()
        self.setup_menu()
        self.start_project_watching()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            background-color: {COLORS['sidebar_bg']};
            border-right: 1px solid {COLORS['border_subtle']};
        """)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setSpacing(8)
        sb_layout.setContentsMargins(12, 16, 12, 12)

        brand = QLabel("Context Manager")
        brand.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {COLORS['text_primary']}; padding-bottom: 8px;")
        sb_layout.addWidget(brand)
        sb_layout.addWidget(Divider())

        sb_layout.addWidget(SectionLabel("Projects"))
        self.projects_list = QListWidget()
        self.projects_list.setMaximumHeight(240)
        self.projects_list.itemClicked.connect(self.on_project_selected)
        sb_layout.addWidget(self.projects_list)

        pb = QHBoxLayout()
        pb.setSpacing(6)
        add_btn = QPushButton("＋ Add")
        add_btn.setObjectName("accent")
        add_btn.clicked.connect(self.add_project)
        rem_btn = QPushButton("Remove")
        rem_btn.setObjectName("danger")
        rem_btn.clicked.connect(self.remove_project)
        pb.addWidget(add_btn)
        pb.addWidget(rem_btn)
        sb_layout.addLayout(pb)

        sb_layout.addSpacing(4)
        sb_layout.addWidget(Divider())
        sb_layout.addSpacing(4)

        ignore_btn = QPushButton("⚙  Ignore Patterns")
        ignore_btn.clicked.connect(self.configure_global_ignore)
        sb_layout.addWidget(ignore_btn)
        sb_layout.addStretch()

        ver = QLabel("v1.0  •  Context Manager")
        ver.setStyleSheet(f"color: {COLORS['text_disabled']}; font-size: 10px;")
        sb_layout.addWidget(ver)
        root.addWidget(sidebar)
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setSpacing(0)
        cl.setContentsMargins(0, 0, 0, 0)
        root.addWidget(content, 1)

        # Top bar
        topbar = QWidget()
        topbar.setFixedHeight(48)
        topbar.setStyleSheet(f"""
            background-color: {COLORS['bg_surface']};
            border-bottom: 1px solid {COLORS['border_subtle']};
        """)
        tbl = QHBoxLayout(topbar)
        tbl.setContentsMargins(16, 0, 16, 0)
        tbl.setSpacing(10)
        self.project_name_label = QLabel("No project selected")
        self.project_name_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {COLORS['text_primary']};")
        tbl.addWidget(self.project_name_label)
        tbl.addStretch()
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("  Search files...")
        self.filter_edit.setFixedWidth(220)
        self.filter_edit.setFixedHeight(32)
        self.filter_edit.textChanged.connect(self.filter_files)
        tbl.addWidget(self.filter_edit)
        self.ext_filter = QComboBox()
        self.ext_filter.setFixedWidth(100)
        self.ext_filter.setFixedHeight(32)
        self.ext_filter.addItem("All types")
        self.ext_filter.addItems(['.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.md'])
        self.ext_filter.currentTextChanged.connect(self.filter_files)
        tbl.addWidget(self.ext_filter)
        refresh_btn = QPushButton("↺  Refresh")
        refresh_btn.setFixedHeight(32)
        refresh_btn.clicked.connect(self.refresh_files)
        tbl.addWidget(refresh_btn)
        cl.addWidget(topbar)

        # File panel
        fp_widget = QWidget()
        fp_widget.setStyleSheet(f"background-color: {COLORS['bg_base']};")
        fpl = QVBoxLayout(fp_widget)
        fpl.setSpacing(8)
        fpl.setContentsMargins(16, 12, 16, 8)

        hdr = QHBoxLayout()
        hdr.setSpacing(8)
        hdr.addWidget(SectionLabel("Project Files"))
        hdr.addStretch()
        self.file_count_label = CountBadge("0 files")
        hdr.addWidget(self.file_count_label)
        fpl.addLayout(hdr)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["File Path", "Size", "Modified"])
        self.file_tree.setIndentation(16)
        self.file_tree.setAlternatingRowColors(True)
        self.file_tree.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.file_tree.header().setStretchLastSection(False)
        self.file_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.file_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.file_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        fpl.addWidget(self.file_tree)

        sel_row = QHBoxLayout()
        sel_row.setSpacing(8)
        sa = QPushButton("✓  Select All")
        sa.setFixedHeight(30)
        sa.clicked.connect(self.select_all_files)
        da = QPushButton("✕  Deselect All")
        da.setFixedHeight(30)
        da.clicked.connect(self.deselect_all_files)
        sel_row.addWidget(sa)
        sel_row.addWidget(da)
        sel_row.addStretch()
        fpl.addLayout(sel_row)
        cl.addWidget(fp_widget, 1)

        # Export bar
        export_bar = QWidget()
        export_bar.setFixedHeight(52)
        export_bar.setStyleSheet(f"""
            background-color: {COLORS['bg_surface']};
            border-top: 1px solid {COLORS['border_subtle']};
        """)
        ebl = QHBoxLayout(export_bar)
        ebl.setContentsMargins(16, 0, 16, 0)
        ebl.setSpacing(12)
        fl = QLabel("Export format:")
        fl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        ebl.addWidget(fl)
        self.format_combo = QComboBox()
        self.format_combo.addItems(['markdown', 'json', 'xml'])
        self.format_combo.setFixedWidth(110)
        self.format_combo.setFixedHeight(34)
        ebl.addWidget(self.format_combo)
        ebl.addStretch()
        self.export_btn = QPushButton("  Export Context  ↗")
        self.export_btn.setFixedHeight(36)
        self.export_btn.setMinimumWidth(160)
        self.export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_hover']}; }}
            QPushButton:pressed {{ background-color: {COLORS['accent_press']}; }}
        """)
        self.export_btn.clicked.connect(self.export_context)
        ebl.addWidget(self.export_btn)
        cl.addWidget(export_bar)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(24)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(160)
        self.progress_bar.setFixedHeight(4)
        self.status_bar.addPermanentWidget(self.progress_bar)

        self.load_projects()

    def setup_menu(self):
        mb = self.menuBar()
        file_menu = mb.addMenu("File")
        ea = QAction("Export Context", self)
        ea.setShortcut("Ctrl+E")
        ea.triggered.connect(self.export_context)
        file_menu.addAction(ea)
        file_menu.addSeparator()
        qa = QAction("Quit", self)
        qa.setShortcut("Ctrl+Q")
        qa.triggered.connect(self.close)
        file_menu.addAction(qa)
        settings_menu = mb.addMenu("Settings")
        gia = QAction("Global Ignore Patterns…", self)
        gia.triggered.connect(self.configure_global_ignore)
        settings_menu.addAction(gia)
        help_menu = mb.addMenu("Help")
        aa = QAction("About", self)
        aa.triggered.connect(self.show_about)
        help_menu.addAction(aa)

    def load_projects(self):
        self.projects_list.clear()
        for p in self.project_manager.get_all_projects():
            item = QListWidgetItem(f"  {p['name']}")
            item.setData(Qt.ItemDataRole.UserRole, p['id'])
            if not p.get('enabled', True):
                item.setForeground(QColor(COLORS['text_disabled']))
            self.projects_list.addItem(item)

    def add_project(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory", os.path.expanduser("~"))
        if path:
            for p in self.project_manager.get_all_projects():
                if p['path'] == path:
                    QMessageBox.warning(self, "Duplicate", "This project is already in the list.")
                    return
            pid = hashlib.md5(path.encode()).hexdigest()[:8]
            self.project_manager.add_project(pid, path)
            self.load_projects()
            self.start_project_watching()
            self.status_bar.showMessage(f"Added: {os.path.basename(path)}", 3000)

    def remove_project(self):
        item = self.projects_list.currentItem()
        if item:
            pid = item.data(Qt.ItemDataRole.UserRole)
            p = self.project_manager.get_project(pid)
            if QMessageBox.question(self, "Remove Project", f"Remove '{p['name']}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    ) == QMessageBox.StandardButton.Yes:
                self.project_manager.stop_watching(pid)
                self.project_manager.remove_project(pid)
                self.load_projects()
                if self.current_project == pid:
                    self.current_project = None
                    self.file_tree.clear()
                    self.file_count_label.setText("0 files")
                    self.project_name_label.setText("No project selected")
                self.status_bar.showMessage(f"Removed: {p['name']}", 3000)

    def configure_global_ignore(self):
        dialog = GlobalIgnoreDialog(self.project_manager.global_ignore_patterns, self)
        if dialog.exec():
            patterns = dialog.get_patterns()
            self.project_manager.update_global_ignore_patterns(patterns)
            self.status_bar.showMessage(f"Ignore patterns updated ({len(patterns)} entries)", 3000)
            if self.current_project:
                self.refresh_files()

    def on_project_selected(self, item):
        self.current_project = item.data(Qt.ItemDataRole.UserRole)
        p = self.project_manager.get_project(self.current_project)
        if p:
            self.project_name_label.setText(p['name'])
        self.refresh_files()

    def refresh_files(self):
        if not self.current_project:
            return
        p = self.project_manager.get_project(self.current_project)
        if not p:
            return
        self.file_tree.clear()
        self.current_files = []
        ignored = set(self.project_manager.get_combined_ignored_patterns(self.current_project))
        root_path = p['path']
        count = 0
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if not any(pat in os.path.join(root, d) for pat in ignored)]
            for file in files:
                fp = os.path.join(root, file)
                if any(pat in fp for pat in ignored):
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext not in self.context_builder.SUPPORTED_EXTENSIONS:
                    continue
                try:
                    stat = os.stat(fp)
                    size = stat.st_size
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    size = 0; modified = "Unknown"
                rel = os.path.relpath(fp, root_path)
                item = QTreeWidgetItem([rel, self._format_size(size), modified])
                item.setData(0, Qt.ItemDataRole.UserRole, fp)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(0, Qt.CheckState.Unchecked)
                self.file_tree.addTopLevelItem(item)
                self.current_files.append(fp)
                count += 1
        self.file_count_label.setText(f"{count} files")
        self.status_bar.showMessage(f"Loaded {count} files", 2000)

    def filter_files(self):
        search = self.filter_edit.text().lower()
        ext = self.ext_filter.currentText()
        visible = 0
        for i in range(self.file_tree.topLevelItemCount()):
            item = self.file_tree.topLevelItem(i)
            name = item.text(0).lower()
            fext = os.path.splitext(name)[1]
            show = True
            if search and search not in name:
                show = False
            if ext != "All types" and fext != ext:
                show = False
            item.setHidden(not show)
            if show:
                visible += 1
        total = self.file_tree.topLevelItemCount()
        self.file_count_label.setText(f"{visible} / {total} files")

    def select_all_files(self):
        for i in range(self.file_tree.topLevelItemCount()):
            item = self.file_tree.topLevelItem(i)
            if not item.isHidden():
                item.setCheckState(0, Qt.CheckState.Checked)

    def deselect_all_files(self):
        for i in range(self.file_tree.topLevelItemCount()):
            self.file_tree.topLevelItem(i).setCheckState(0, Qt.CheckState.Unchecked)

    def get_selected_files(self):
        return [
            self.file_tree.topLevelItem(i).data(0, Qt.ItemDataRole.UserRole)
            for i in range(self.file_tree.topLevelItemCount())
            if self.file_tree.topLevelItem(i).checkState(0) == Qt.CheckState.Checked
        ]

    def export_context(self):
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        selected = self.get_selected_files()
        if not selected:
            QMessageBox.warning(self, "No Files", "Please select at least one file to export.")
            return
        p = self.project_manager.get_project(self.current_project)
        fmt = self.format_combo.currentText()
        ignored = self.project_manager.get_combined_ignored_patterns(self.current_project)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Building context…")
        QApplication.processEvents()
        try:
            context = self.context_builder.build(p['path'], selected, ignored, fmt)
            output = self.context_builder.export_to_format(context, fmt)
            ext = 'md' if fmt == 'markdown' else fmt
            default_name = f"context_{p['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            fp, _ = QFileDialog.getSaveFileName(self, "Save Context", default_name,
                                                 f"{fmt.upper()} Files (*.{ext})")
            if fp:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(output)
                self.status_bar.showMessage(f"Exported → {os.path.basename(fp)}", 5000)
                QMessageBox.information(self, "Export Complete",
                    f"✅  {context['total_files']} files exported\n"
                    f"📦  {self.context_builder._format_size(context['total_size'])} total")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export:\n{e}")
        finally:
            self.progress_bar.setVisible(False)
            self.status_bar.showMessage("Ready")

    def start_project_watching(self):
        self.project_manager.stop_all_watching()

        def on_change(path, event_type):
            self.status_bar.showMessage(f"↺ {event_type}: {os.path.basename(path)}", 2000)
            if self.current_project:
                QTimer.singleShot(500, self.refresh_files)

        for p in self.project_manager.get_all_projects():
            if p.get('enabled', True):
                self.project_manager.start_watching(p['id'], on_change)

    def show_about(self):
        QMessageBox.about(self, "About Context Manager", """
            <div style="font-family:'Segoe UI',sans-serif;">
            <h3 style="margin-bottom:4px;">Context Manager</h3>
            <p style="color:#888;margin-top:0;">Version 2.0</p>
            <p>Professional tool for gathering project context for LLMs and AI assistants.</p>
            <ul>
              <li>Automatic project name from folder</li>
              <li>Global ignore patterns for all projects</li>
              <li>Real-time file change monitoring</li>
              <li>Export to Markdown, JSON, XML</li>
            </ul>
            </div>
        """)

    def _format_size(self, size):
        return self.context_builder._format_size(size)

    def closeEvent(self, event):
        self.project_manager.stop_all_watching()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Context Manager")
    app.setOrganizationName("ContextManager")

    app.setStyleSheet(make_stylesheet())

    p = QPalette()
    p.setColor(QPalette.ColorRole.Window,          QColor(COLORS['bg_surface']))
    p.setColor(QPalette.ColorRole.WindowText,      QColor(COLORS['text_primary']))
    p.setColor(QPalette.ColorRole.Base,            QColor(COLORS['bg_input']))
    p.setColor(QPalette.ColorRole.AlternateBase,   QColor(COLORS['bg_elevated']))
    p.setColor(QPalette.ColorRole.ToolTipBase,     QColor(COLORS['bg_popup']))
    p.setColor(QPalette.ColorRole.ToolTipText,     QColor(COLORS['text_primary']))
    p.setColor(QPalette.ColorRole.Text,            QColor(COLORS['text_primary']))
    p.setColor(QPalette.ColorRole.Button,          QColor(COLORS['bg_elevated']))
    p.setColor(QPalette.ColorRole.ButtonText,      QColor(COLORS['text_primary']))
    p.setColor(QPalette.ColorRole.BrightText,      QColor('#ffffff'))
    p.setColor(QPalette.ColorRole.Link,            QColor(COLORS['accent']))
    p.setColor(QPalette.ColorRole.Highlight,       QColor(COLORS['accent']))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor('#ffffff'))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
               QColor(COLORS['text_disabled']))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
               QColor(COLORS['text_disabled']))
    app.setPalette(p)

    window = ContextManagerPro()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()