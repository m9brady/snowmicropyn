import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDoubleValidator, QFontMetrics
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget
)

log = logging.getLogger('snowmicropyn')


class SidebarWidget(QTreeWidget):
    TEXT_COLUMN = 4

    def __init__(self, main_win, *args, **kwargs):
        self.main_window = main_win
        super().__init__(*args, **kwargs)

        # Get rid of the ugly focus rectangle and border
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setStyleSheet('outline: 0; border: 0;')

        self.doc = None
        self.marker_items = {}

        self.setColumnCount(5)
        self.setHeaderHidden(True)

        # top level items

        self.recording_item = QTreeWidgetItem(('Recording',), QTreeWidgetItem.Type)
        self.smp_item = QTreeWidgetItem(('SnowMicroPen',), QTreeWidgetItem.Type)
        self.markers_item = QTreeWidgetItem(('Markers',), QTreeWidgetItem.Type)
        self.qa_item = QTreeWidgetItem(('Quality Assurance',), QTreeWidgetItem.Type)
        self.drift_item = QTreeWidgetItem(('Drift, Offset, Noise',), QTreeWidgetItem.Type)

        self.addTopLevelItem(self.recording_item)
        self.addTopLevelItem(self.smp_item)
        self.addTopLevelItem(self.markers_item)
        self.addTopLevelItem(self.qa_item)
        self.addTopLevelItem(self.drift_item)

        self.setFirstItemColumnSpanned(self.recording_item, True)
        self.setFirstItemColumnSpanned(self.smp_item, True)
        self.setFirstItemColumnSpanned(self.markers_item, True)
        self.setFirstItemColumnSpanned(self.qa_item, True)
        self.setFirstItemColumnSpanned(self.drift_item, True)

        # recording items

        self.name_item = QTreeWidgetItem((None, None, 'Name', None, ''))
        self.timestamp_item = QTreeWidgetItem((None, None, 'Timestamp', None, ''))
        self.rec_length_item = QTreeWidgetItem((None, None, 'Length', None, ''))
        self.pnt_filename_item = QTreeWidgetItem((None, None, 'Pnt File', None, ''))
        self.coordinates_item = QTreeWidgetItem((None, None, 'Coordinates', None, ''))
        self.spatial_res_item = QTreeWidgetItem((None, None, 'Spatial Resolution', None, ''))
        self.overload_item = QTreeWidgetItem((None, None, 'Overload Force', None, ''))
        self.speed_item = QTreeWidgetItem((None, None, 'Speed', None, ''))

        self.recording_item.addChild(self.name_item)
        self.recording_item.addChild(self.pnt_filename_item)
        self.recording_item.addChild(self.timestamp_item)
        self.recording_item.addChild(self.coordinates_item)
        self.recording_item.addChild(self.rec_length_item)
        self.recording_item.addChild(self.spatial_res_item)
        self.recording_item.addChild(self.overload_item)
        self.recording_item.addChild(self.speed_item)

        # smp items

        self.smp_serial_item = QTreeWidgetItem((None, None, 'Serial Number', None, ''))
        self.smp_firmware_item = QTreeWidgetItem((None, None, 'Firmware Version', None, ''))
        self.smp_length_item = QTreeWidgetItem((None, None, 'Max. Recording Length', None, ''))
        self.smp_tipdiameter_item = QTreeWidgetItem((None, None, 'Tip Diameter', None, ''))
        self.smp_sensor_sensitivity_item = QTreeWidgetItem((None, None, 'Sensor Sensitivity', None, ''))
        self.smp_sensor_serial_item = QTreeWidgetItem((None, None, 'Sensor Serial Number', None, ''))
        self.smp_amp_item = QTreeWidgetItem((None, None, 'Amplifier Serial Number', None, ''))

        self.smp_item.addChild(self.smp_serial_item)
        self.smp_item.addChild(self.smp_firmware_item)
        self.smp_item.addChild(self.smp_length_item)
        self.smp_item.addChild(self.smp_tipdiameter_item)
        self.smp_item.addChild(self.smp_sensor_sensitivity_item)
        self.smp_item.addChild(self.smp_sensor_serial_item)
        self.smp_item.addChild(self.smp_amp_item)

        # quality assurance items

        item = QaCheckboxTreeItem(self.qa_item, 'usable')
        self.qa_item.addChild(item)
        item = QaFlagTreeItem(self.qa_item, 'quality_flag')
        self.qa_item.addChild(item)
        item = QaCommentTreeItem(self.qa_item, 'comment')
        self.qa_item.addChild(item)
        item = QaCommentTreeItem(self.qa_item, 'details')
        self.qa_item.addChild(item)
        item = QaCommentTreeItem(self.qa_item, 'experiment')
        self.qa_item.addChild(item)

        # drift items

        self.drift_begin_item = QTreeWidgetItem((None, None, 'Begin', None, ''))
        self.drift_end_item = QTreeWidgetItem((None, None, 'End', None, ''))
        self.drift_value_item = QTreeWidgetItem((None, None, 'Drift', None, ''))
        self.offset_value_item = QTreeWidgetItem((None, None, 'Offset', None, ''))
        self.noise_value_item = QTreeWidgetItem((None, None, 'Noise', None, ''))

        self.drift_item.addChild(self.drift_begin_item)
        self.drift_item.addChild(self.drift_end_item)
        self.drift_item.addChild(self.drift_value_item)
        self.drift_item.addChild(self.offset_value_item)
        self.drift_item.addChild(self.noise_value_item)

        # Tight up the columns
        self.expandAll()
        self.setColumnWidth(0, 0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)

    def set_document(self, doc):
        if doc is None:
            return

        p = doc.profile

        self.name_item.setText(self.TEXT_COLUMN, p.name)
        self.pnt_filename_item.setText(self.TEXT_COLUMN, str(p.pnt_file))
        self.timestamp_item.setText(self.TEXT_COLUMN, str(p.timestamp))
        self.rec_length_item.setText(self.TEXT_COLUMN, '{:.0f} mm ({:n} Samples)'.format(p.recording_length, len(p)))

        if p.coordinates:
            lat, long = ['{:.6f}'.format(c) for c in p.coordinates]
            url = '<a href="https://www.google.com/maps/search/?api=1&query={lat},{long}">{lat}, {long}</a>'.format(
                lat=lat, long=long)
        else:
            url = 'None'
        url_label = QLabel(url)
        url_label.setContentsMargins(5, 0, 0, 0)
        url_label.setOpenExternalLinks(True)
        self.setItemWidget(self.coordinates_item, 4, url_label)

        spatial_res = '{:.3f} µm'.format(p.spatial_resolution * 1000)
        self.spatial_res_item.setText(self.TEXT_COLUMN, spatial_res)
        overload = '{:.1f} N'.format(p.overload)
        self.overload_item.setText(self.TEXT_COLUMN, overload)
        speed = '{:.1f} mm/s'.format(p.speed)
        self.speed_item.setText(self.TEXT_COLUMN, speed)

        self.smp_serial_item.setText(self.TEXT_COLUMN, p.smp_serial)
        self.smp_firmware_item.setText(self.TEXT_COLUMN, p.smp_firmware)
        length = '{} mm'.format(p.smp_length)
        self.smp_length_item.setText(self.TEXT_COLUMN, length)
        tipdiameter = '{:.1f} mm'.format(p.smp_tipdiameter / 1000)
        self.smp_tipdiameter_item.setText(self.TEXT_COLUMN, tipdiameter)
        self.smp_sensor_serial_item.setText(self.TEXT_COLUMN, p.sensor_serial)
        self.smp_sensor_sensitivity_item.setText(self.TEXT_COLUMN, '{}  pC/N'.format(p.sensor_sensitivity))
        self.smp_amp_item.setText(self.TEXT_COLUMN, p.amplifier_serial)

        # Drop all existing markers
        for label, item in self.marker_items.items():
            self.markers_item.removeChild(item)
        self.marker_items = {}

        for label, value in p.markers.items():
            self.set_marker(label, value)

    def set_marker(self, label, value):
        if value is None:
            if label in self.marker_items:
                item = self.marker_items[label]
                self.markers_item.removeChild(item)
                del self.marker_items[label]
            return

        value = '{:.3f}'.format(value)
        if label not in self.marker_items:
            item = MarkerTreeItem(self.markers_item, label)

            # This is a bit tricky: We call the methods on main_window which
            # calls this method again...

            def set_marker():
                self.main_window.set_marker(label, item.lineedit.text())

            item.lineedit.editingFinished.connect(set_marker)

            def delete_marker(checked):
                self.main_window.set_marker(label, None)

            item.delete_button.clicked.connect(delete_marker)

            def detect_marker(checked):
                if (label == 'surface'):
                    self.main_window._detect_surface_triggered()
                else:
                    self.main_window._detect_ground_triggered()

            item.detect_button.clicked.connect(detect_marker)

            self.marker_items[label] = item
            self.markers_item.addChild(item)

        item = self.marker_items[label]
        item.lineedit.setText(value)

    def set_drift(self, begin_label, end_label, drift, offset, noise):
        self.drift_begin_item.setText(self.TEXT_COLUMN, begin_label)
        self.drift_end_item.setText(self.TEXT_COLUMN, end_label)
        self.drift_value_item.setText(self.TEXT_COLUMN, '{:.2g} mN/m'.format(drift * 1000 * 1000))
        self.offset_value_item.setText(self.TEXT_COLUMN, '{:.2f} mN'.format(offset * 1000))
        self.noise_value_item.setText(self.TEXT_COLUMN, '{:.2f} mN'.format(noise * 1000))


class MarkerTreeItem(QTreeWidgetItem):

    def __init__(self, parent, name, deletable=True):
        super(MarkerTreeItem, self).__init__(parent)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon(':/icons/delete.png'))
        self.detect_button = QPushButton()

        self.lineedit = QLineEdit(self.treeWidget())
        self.lineedit.setValidator(QDoubleValidator())

        if deletable:
            self.treeWidget().setItemWidget(self, 1, self.delete_button)
        self.setText(2, name)
        if name in ['surface', 'ground']:
            self.detect_button.setIcon(QIcon(f':/icons/detect_{name}.png'))
            self.treeWidget().setItemWidget(self, 3, self.detect_button)
        self.treeWidget().setItemWidget(self, 4, self.lineedit)

    @property
    def name(self):
        return self.text(2)

    @property
    def value(self):
        return self.lineedit.value()

    def lineedit_focused(self):
        pass

class QaFlagTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setText(2, name)
        self.picker = QaPicker(self.treeWidget())
        self.treeWidget().setItemWidget(self, 4, self.picker)

class QaCommentTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super(QaCommentTreeItem, self).__init__(parent)

        self.lineedit = QLineEdit(self.treeWidget())

        self.setText(2, name)
        self.treeWidget().setItemWidget(self, 4, self.lineedit)

class QaCheckboxTreeItem(QTreeWidgetItem):

    def __init__(self, parent, name):
        super(QaCheckboxTreeItem, self).__init__(parent)

        self.checkbox = QCheckBox(self.treeWidget())

        self.setText(2, name)
        self.treeWidget().setItemWidget(self, 4, self.checkbox)

    @property
    def name(self):
        return self.text(2)

    @property
    def value(self):
        return self.checkbox.value()

    def lineedit_focused(self):
        pass

class QaPicker(QWidget):
    _colors = {0: "black", 1: "green", 2: "#8B8000", 3: "orange", 4: "red", 9: "#630700"}
    _flags = {0: "not set", 1: "excellent", 2: "good", 3: "satisfying", 4: "sufficient", 9: "unsatisfactory"}

    def __init__(self, parent):
        super(QaPicker, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        for idx in self._colors.keys():
            button = QToolButton()
            button.setCheckable(True)
            button.setText(str(idx))
            button.clicked.connect(lambda state, index=idx: self.on_qa_click(index, state))
            button.setStyleSheet(f"background-color: {self._colors[idx]}; color: white; font-weight: normal")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            font_height = QFontMetrics(button.font()).height() + 5
            font_width = QFontMetrics(button.font()).width("X") * 3
            button.setMinimumSize(font_width, font_height)
            button_layout.addWidget(button, 0, Qt.AlignLeft)
        layout.addLayout(button_layout)

        self.qa_label = QLabel()
        layout.addWidget(self.qa_label)
        self.setLayout(layout)

    def on_qa_click(self, index, state):
        self.qa_label.setText(str(index) + ": " + self._flags[index])
        self.qa_label.setStyleSheet(f"background-color: {self._colors[index]}; color: white")
