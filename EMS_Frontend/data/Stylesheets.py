
def GetFancySlider():
    return ("QSlider::groove:horizontal\n"
                        "{\n"
                        "border: 1px solid #bbb;\n"
                        "background: white;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::sub-page:vertical\n"
                        "{\n"
                        "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fff, stop: 0.4999 #eee, stop: 0.5 #ddd, stop: 1 #eee );\n"
                        "border: 1px solid #777;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::add-page:vertical {\n"
                        "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.4999 #46a, stop: 0.5 #45a, stop: 1 #238 );\n"
                        "\n"
                        "border: 1px solid #777;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical {\n"
                        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc);\n"
                        "border: 1px solid #777;\n"
                        "height: 13px;\n"
                        "margin-top: -2px;\n"
                        "margin-bottom: -2px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical:hover {\n"
                        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff, stop:1 #ddd);\n"
                        "border: 1px solid #444;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::sub-page:vertical:disabled {\n"
                        "background: #bbb;\n"
                        "border-color: #999;\n"
                        "}\n"
                        "\n"
                        "QSlider::add-page:vertical:disabled {\n"
                        "background: #eee;\n"
                        "border-color: #999;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical:disabled {\n"
                        "background: #eee;\n"
                        "border: 1px solid #aaa;\n"
                        "border-radius: 4px;\n"
                        "}")