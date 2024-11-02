"""
Module for defining external functions to use in Qt-interface
"""

def set_text(label, text, color = 'red'):
    """Set label text: (obj, str, str)"""
    label.setText(text)
    label.setStyleSheet(f'color: {color}')