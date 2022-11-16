from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
import sys
import os
import os.path
import configparser
import json
import requests
import logger
from jadepy import JadeAPI


class AppWindow():
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        bundle_dir = getattr(
            sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_dialog_ui = os.path.abspath(
            os.path.join(bundle_dir, 'dialog.ui'))
        self.ui = loader.load(path_to_dialog_ui, None)

        self.ui.btn_connect.clicked.connect(self.on_btn_connect_clicked_send)
        self.ui.btn_pinserver_reset.clicked.connect(self.on_btn_pinserver_reset_clicked_send)
        self.ui.btn_pinserver_set.clicked.connect(self.on_btn_pinserver_set_clicked_send)

        self.ui.btn_otp_settimestamp.clicked.connect(self.on_btn_otp_settimestamp_clicked_send)
        self.ui.btn_otp_registerotp.clicked.connect(self.on_btn_otp_registerotp_clicked_send)
        self.ui.btn_otp_getotp.clicked.connect(self.on_btn_otp_getotp_clicked_send)

    def on_btn_connect_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=10) as jade:
            version_info = jade.get_version_info()
            self.ui.txt_info_version.setText(version_info.get('JADE_VERSION', ''))
            self.ui.txt_info_otamaxchunk.setText(str(version_info.get('JADE_OTA_MAX_CHUNK', '')))
            self.ui.txt_info_config.setText(version_info.get('JADE_CONFIG', ''))
            self.ui.txt_info_board.setText(version_info.get('BOARD_TYPE', ''))
            self.ui.txt_info_features.setText(version_info.get('JADE_FEATURES', ''))
            self.ui.txt_info_idfversion.setText(version_info.get('IDF_VERSION', ''))
            self.ui.txt_info_chip.setText(version_info.get('CHIP_FEATURES', ''))
            self.ui.txt_info_efusemac.setText(version_info.get('EFUSEMAC', ''))
            self.ui.txt_info_battery.setText(str(version_info.get('BATTERY_STATUS', '')))
            self.ui.txt_info_state.setText(version_info.get('JADE_STATE', ''))
            self.ui.txt_info_networks.setText(version_info.get('JADE_NETWORKS', ''))
            self.ui.txt_info_haspin.setText(str(version_info.get('JADE_HAS_PIN', '')))
            # enable guis objects
            self.ui.btn_connect.setEnabled(False);
            self.ui.grp_info.setEnabled(True);
            self.ui.grp_totp.setEnabled(True);
            self.ui.grp_pinserver.setEnabled(True);
            self.ui.txt_info_version.setEnabled(True);
            # debug
            self.ui.txt_results.setText(json.dumps(version_info) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_pinserver_reset_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=10) as jade:
            res = jade.reset_pinserver(reset_details=True, reset_certificate=True)
            # debug
            self.ui.txt_results.setText(json.dumps(res) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_pinserver_set_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=120) as jade:
            urlA = self.ui.txt_pinserver_urla.text()
            if len(urlA) < 3:
                urlA = None
            urlB = self.ui.txt_pinserver_urlb.text()
            if len(urlB) < 3:
                urlB = None
            pubkey = self.ui.txt_pinserver_pubkey.text()
            if len(pubkey) < 3:
                pubkey = None
            certificate = self.ui.txt_pinserver_certificate.text()
            if len(certificate) < 3:
                certificate = None
            res = jade.set_pinserver(urlA=urlA, urlB=urlB, pubkey=pubkey, cert=certificate)
            # debug
            self.ui.txt_results.setText(json.dumps(res) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_otp_settimestamp_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=10) as jade:
            res = jade.set_epoch()
            # debug
            self.ui.txt_results.setText(json.dumps(res) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_otp_registerotp_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=10) as jade:
            otp_name = self.ui.txt_otp_name.text()
            otp_uri = self.ui.txt_otp_uri.text()
            res = jade.register_otp(otp_name, otp_uri)
            # debug
            self.ui.txt_results.setText(json.dumps(res) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_otp_getotp_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=10) as jade:
            otp_name = self.ui.txt_otp_name.text()
            res = jade.get_otp_code(otp_name)
            # debug
            self.ui.txt_results.setText(json.dumps(res) + '\n' + self.ui.txt_results.toPlainText())


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = AppWindow()
    w.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AppWindow()
    w.ui.show()
    sys.exit(app.exec_())
