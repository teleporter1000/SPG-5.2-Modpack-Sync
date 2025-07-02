from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve
import sys

class MinecraftLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Launcher")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #312D2C;")

        base_path = r"C:\\Users\\telep\\Desktop\\SPG Launcher\\recursos\\"

        icon_path = base_path + "launcherlogo.png"
        self.setWindowIcon(QIcon(icon_path))

        bar_path = base_path + "bar\\"
        self.paths = {
            "account": [base_path + "btn_account.png", base_path + "selected_btn_account.png"],
            "inicio": [base_path + "btn_inicio.png", base_path + "selected_btn_inicio.png"],
            "java": [base_path + "btn_java.png", base_path + "selected_btn_java.png", base_path + "cursor_btn_java.png"],
            "novedades": [base_path + "btn_novedades.png", base_path + "selected_btn_novedades.png", base_path + "cursor_btn_novedades.png"],
            "ajustes": [base_path + "btn_ajustes.png", base_path + "selected_btn_ajustes.png", base_path + "cursor_btn_ajustes.png"],
            "jugar": [bar_path + "jugar_lbl_minecraft_java.png", bar_path + "selected_btn_jugar.png"],
            "instalaciones": [bar_path + "instalaciones_lbl_minecraft_java.png", bar_path + "selected_btn_instalaciones.png"],
            "body": bar_path + "body_photo.png",
            "body2": bar_path + "body_photo2.png",
            "body3": bar_path + "body_photo3.png",
            "down_body": bar_path + "down_body_photo.png",
            "java_header": bar_path + "java_header.png",
            "spg_logo": bar_path + "spg_logo.png",
            "jugar_grande": [base_path + "btn_jugar.png", base_path + "selected_btn_jugar2.png"]
        }

        self.logo_scale = 0.2
        self.logo_offset_y = 70
        self.logo_animation = None
        self.current_section = None
        self.setup_ui()
        self.setup_version_label()

    def setup_ui(self):
        self.account_btn = self.create_sidebar_button("account", 0, lambda e: self.switch_section("account"))
        self.inicio_btn = self.create_sidebar_button("inicio", self.account_btn.y() + self.account_btn.pixmap().height(), lambda e: self.switch_section("inicio"))

        self.java_btn = QLabel(self)
        self.java_pix_default = QPixmap(self.paths["java"][0])
        self.java_pix_selected = QPixmap(self.paths["java"][1])
        self.java_pix_hover = QPixmap(self.paths["java"][2])
        self.java_btn.setPixmap(self.java_pix_default)
        self.java_btn.move(0, self.inicio_btn.y() + self.inicio_btn.pixmap().height())
        self.java_btn.enterEvent = self.java_hover_enter
        self.java_btn.leaveEvent = self.java_hover_leave
        self.java_btn.mousePressEvent = self.java_click

        self.body_label = QLabel(self)
        self.body_label.setPixmap(QPixmap(self.paths["body"]))
        self.body_label.move(0, self.java_btn.y() + self.java_btn.pixmap().height())

        self.body2_label = QLabel(self)
        self.body2_label.setPixmap(QPixmap(self.paths["body2"]))
        self.body2_label.move(0, self.body_label.y() + self.body_label.pixmap().height())

        self.down_body_label = QLabel(self)
        self.down_body_label.setPixmap(QPixmap(self.paths["down_body"]))
        self.down_body_label.move(self.body2_label.x() + self.body2_label.pixmap().width(), self.body2_label.y())

        self.novedades_btn = QLabel(self)
        self.novedades_pix_default = QPixmap(self.paths["novedades"][0])
        self.novedades_pix_selected = QPixmap(self.paths["novedades"][1])
        self.novedades_pix_hover = QPixmap(self.paths["novedades"][2])
        self.novedades_btn.setPixmap(self.novedades_pix_default)
        self.novedades_btn.move(0, self.body2_label.y() + self.body2_label.pixmap().height())
        self.novedades_btn.enterEvent = self.novedades_hover_enter
        self.novedades_btn.leaveEvent = self.novedades_hover_leave
        self.novedades_btn.mousePressEvent = self.novedades_click

        self.ajustes_btn = QLabel(self)
        self.ajustes_pix_default = QPixmap(self.paths["ajustes"][0])
        self.ajustes_pix_selected = QPixmap(self.paths["ajustes"][1])
        self.ajustes_pix_hover = QPixmap(self.paths["ajustes"][2])
        self.ajustes_btn.setPixmap(self.ajustes_pix_default)
        self.ajustes_btn.move(0, self.novedades_btn.y() + self.novedades_btn.pixmap().height())
        self.ajustes_btn.enterEvent = self.ajustes_hover_enter
        self.ajustes_btn.leaveEvent = self.ajustes_hover_leave
        self.ajustes_btn.mousePressEvent = self.ajustes_click

        self.body3_label = QLabel(self)
        self.body3_label.setPixmap(QPixmap(self.paths["body3"]))
        self.body3_label.move(0, self.ajustes_btn.y() + self.ajustes_btn.pixmap().height())

        self.java_header_label = QLabel(self)
        java_header_pix = QPixmap(self.paths["java_header"])
        if java_header_pix.width() > self.width():
            java_header_pix = java_header_pix.scaled(self.width(), java_header_pix.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.java_header_label.setPixmap(java_header_pix)
        self.java_header_label.move(self.down_body_label.x(), self.down_body_label.y() - java_header_pix.height())

        self.spg_logo_label = QLabel(self)
        spg_logo_pix = QPixmap(self.paths["spg_logo"]).scaledToWidth(
            int(QPixmap(self.paths["spg_logo"]).width() * self.logo_scale),
            Qt.SmoothTransformation
        )
        self.spg_logo_label.setPixmap(spg_logo_pix)
        self.spg_logo_label.setAttribute(Qt.WA_TranslucentBackground)

        header_x = self.java_header_label.x()
        header_w = self.java_header_label.pixmap().width()
        logo_w = self.spg_logo_label.pixmap().width()
        self.spg_logo_final_pos = QPoint(header_x + (header_w - logo_w) // 2, self.java_header_label.y() + self.logo_offset_y)
        self.spg_logo_label.move(self.spg_logo_final_pos.x(), -logo_w)

        self.jugar_pix = [QPixmap(p) for p in self.paths["jugar"]]
        self.instalaciones_pix = [QPixmap(p) for p in self.paths["instalaciones"]]

        self.jugar_btn = QLabel(self)
        self.jugar_btn.setPixmap(self.jugar_pix[0])
        self.jugar_btn.move(self.account_btn.pixmap().width(), 0)
        self.jugar_btn.mousePressEvent = self.toggle_jugar
        self.jugar_btn.enterEvent = self.jugar_hover_enter
        self.jugar_btn.leaveEvent = self.jugar_hover_leave

        self.instalaciones_btn = QLabel(self)
        self.instalaciones_btn.setPixmap(self.instalaciones_pix[0])
        self.instalaciones_btn.move(self.jugar_btn.x() + self.jugar_btn.pixmap().width(), 0)
        self.instalaciones_btn.mousePressEvent = self.toggle_instalaciones
        self.instalaciones_btn.enterEvent = self.instalaciones_hover_enter
        self.instalaciones_btn.leaveEvent = self.instalaciones_hover_leave

        self.jugar_grande_pix = [QPixmap(p) for p in self.paths["jugar_grande"]]
        self.jugar_grande_btn = QLabel(self)
        self.jugar_grande_btn.setPixmap(self.jugar_grande_pix[0])
        self.jugar_grande_btn.setCursor(Qt.PointingHandCursor)
        self.jugar_grande_btn.enterEvent = lambda e: self.jugar_grande_btn.setPixmap(self.jugar_grande_pix[1])
        self.jugar_grande_btn.leaveEvent = lambda e: self.jugar_grande_btn.setPixmap(self.jugar_grande_pix[0])
        self.jugar_grande_btn.mousePressEvent = self.on_jugar_grande_click
        self.jugar_grande_btn.move(self.down_body_label.x() + 425, self.down_body_label.y() - 15)
        self.jugar_grande_btn.hide()

        self.pantalla_inicio_label = QLabel("INICIO", self)
        self.pantalla_inicio_label.setStyleSheet("background-color: black; color: white; font-size: 40px;")
        self.pantalla_inicio_label.setAlignment(Qt.AlignCenter)
        self.pantalla_inicio_label.setGeometry(self.account_btn.pixmap().width(), 0, self.width() - self.account_btn.pixmap().width(), self.height())

        self.pantalla_instalaciones_label = QLabel("INSTALACIONES", self)
        self.pantalla_instalaciones_label.setStyleSheet("background-color: black; color: white; font-size: 40px;")
        self.pantalla_instalaciones_label.setAlignment(Qt.AlignCenter)
        self.pantalla_instalaciones_label.setGeometry(self.account_btn.pixmap().width(), 0, self.width() - self.account_btn.pixmap().width(), self.height())

        self.switch_section("inicio")

    def setup_version_label(self):
        self.version_label = QLabel("v.0.00.00-0.0.1", self)
        self.version_label.setAutoFillBackground(False)
        self.version_label.setStyleSheet("color: #A3A1A1;")


        self.version_label.setFont(QFont("Segoe UI", 9.5, QFont.Bold))
        self.version_label.move(15, self.height() - 17)

    def create_sidebar_button(self, name, y, handler):
        btn = QLabel(self)
        btn.pix_default, btn.pix_selected = [QPixmap(p) for p in self.paths[name]]
        btn.setPixmap(btn.pix_default)
        btn.move(0, y)
        btn.mousePressEvent = handler
        return btn

    def switch_section(self, section):
        self.current_section = section
        for btn, name, default, selected in [
            (self.account_btn, "account", self.paths["account"][0], self.paths["account"][1]),
            (self.inicio_btn, "inicio", self.paths["inicio"][0], self.paths["inicio"][1]),
        ]:
            btn.setPixmap(QPixmap(selected if section == name else default))

        self.java_btn.setPixmap(self.java_pix_selected if section == "java" else self.java_pix_default)
        self.novedades_btn.setPixmap(self.novedades_pix_selected if section == "novedades" else self.novedades_pix_default)
        self.ajustes_btn.setPixmap(self.ajustes_pix_selected if section == "ajustes" else self.ajustes_pix_default)

        self.jugar_btn.hide()
        self.instalaciones_btn.hide()
        self.jugar_grande_btn.hide()
        self.java_header_label.hide()
        self.spg_logo_label.hide()
        self.down_body_label.hide()
        self.pantalla_inicio_label.hide()
        self.pantalla_instalaciones_label.hide()

        if section == "java":
            self.jugar_selected = False
            self.instalaciones_selected = False
            self.jugar_btn.show()
            self.instalaciones_btn.show()
            self.toggle_jugar(None)
        elif section == "inicio":
            self.pantalla_inicio_label.show()

    def java_hover_enter(self, event):
        if self.current_section != "java":
            self.java_btn.setPixmap(self.java_pix_hover)
            self.java_btn.setCursor(Qt.PointingHandCursor)

    def java_hover_leave(self, event):
        if self.current_section != "java":
            self.java_btn.setPixmap(self.java_pix_default)
        self.java_btn.setCursor(Qt.ArrowCursor)

    def java_click(self, event):
        if self.current_section != "java":
            self.switch_section("java")
            self.java_btn.setCursor(Qt.ArrowCursor)

    def novedades_hover_enter(self, event):
        if self.current_section != "novedades":
            self.novedades_btn.setPixmap(self.novedades_pix_hover)
            self.novedades_btn.setCursor(Qt.PointingHandCursor)

    def novedades_hover_leave(self, event):
        if self.current_section != "novedades":
            self.novedades_btn.setPixmap(self.novedades_pix_default)
        self.novedades_btn.setCursor(Qt.ArrowCursor)

    def novedades_click(self, event):
        if self.current_section != "novedades":
            self.switch_section("novedades")
            self.novedades_btn.setCursor(Qt.ArrowCursor)

    def ajustes_hover_enter(self, event):
        if self.current_section != "ajustes":
            self.ajustes_btn.setPixmap(self.ajustes_pix_hover)
            self.ajustes_btn.setCursor(Qt.PointingHandCursor)

    def ajustes_hover_leave(self, event):
        if self.current_section != "ajustes":
            self.ajustes_btn.setPixmap(self.ajustes_pix_default)
        self.ajustes_btn.setCursor(Qt.ArrowCursor)

    def ajustes_click(self, event):
        if self.current_section != "ajustes":
            self.switch_section("ajustes")
            self.ajustes_btn.setCursor(Qt.ArrowCursor)

    def jugar_hover_enter(self, event):
        if not getattr(self, "jugar_selected", False):
            self.jugar_btn.setCursor(Qt.PointingHandCursor)
        else:
            self.jugar_btn.setCursor(Qt.ArrowCursor)

    def jugar_hover_leave(self, event):
        self.jugar_btn.setCursor(Qt.ArrowCursor)

    def instalaciones_hover_enter(self, event):
        if not getattr(self, "instalaciones_selected", False):
            self.instalaciones_btn.setCursor(Qt.PointingHandCursor)
        else:
            self.instalaciones_btn.setCursor(Qt.ArrowCursor)

    def instalaciones_hover_leave(self, event):
        self.instalaciones_btn.setCursor(Qt.ArrowCursor)

    def toggle_jugar(self, event):
        if getattr(self, "jugar_selected", False):
            return
        self.jugar_selected = True
        self.instalaciones_selected = False
        self.jugar_btn.setPixmap(self.jugar_pix[1])
        self.instalaciones_btn.setPixmap(self.instalaciones_pix[0])

        self.java_header_label.show()
        self.spg_logo_label.show()
        self.down_body_label.show()
        self.pantalla_instalaciones_label.hide()
        self.jugar_grande_btn.show()

        self.jugar_btn.raise_()
        self.instalaciones_btn.raise_()
        self.jugar_grande_btn.raise_()

        self.spg_logo_label.move(self.spg_logo_final_pos.x(), -self.spg_logo_label.pixmap().height())
        self.logo_animation = QPropertyAnimation(self.spg_logo_label, b"pos")
        self.logo_animation.setDuration(800)
        self.logo_animation.setStartValue(self.spg_logo_label.pos())
        self.logo_animation.setEndValue(self.spg_logo_final_pos)
        self.logo_animation.setEasingCurve(QEasingCurve.OutBounce)
        self.logo_animation.start()

        self.jugar_btn.setCursor(Qt.ArrowCursor)

    def toggle_instalaciones(self, event):
        if getattr(self, "instalaciones_selected", False):
            return
        self.jugar_selected = False
        self.instalaciones_selected = True
        self.instalaciones_btn.setPixmap(self.instalaciones_pix[1])
        self.jugar_btn.setPixmap(self.jugar_pix[0])

        self.java_header_label.hide()
        self.spg_logo_label.hide()
        self.down_body_label.hide()
        self.jugar_grande_btn.hide()
        self.pantalla_instalaciones_label.show()

        self.instalaciones_btn.raise_()
        self.jugar_btn.raise_()

        self.instalaciones_btn.setCursor(Qt.ArrowCursor)

    def on_jugar_grande_click(self, event):
        print("¡Botón JUGAR presionado!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = MinecraftLauncher()
    launcher.show()
    sys.exit(app.exec_())