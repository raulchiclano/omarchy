import QtQuick
import qs.Ui

BarWidget {
  id: root
  moduleName: "lavanda.applications"
  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight
  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    fixedWidth: 32
    text: " "
    labelVisible: false
    tooltipText: "Aplicaciones y ajustes"
    Grid {
      anchors.centerIn: parent
      columns: 3
      spacing: 3
      Repeater {
        model: 9
        Rectangle { width: 3; height: 3; radius: 1.2; color: "#F2EFFA" }
      }
    }
    onPressed: function(button) {
      if (!root.bar) return
      if (button === Qt.RightButton) root.bar.run("xdg-terminal-exec")
      else root.bar.run("omarchy-shell shell toggle omarchy.menu '{\"menu\":\"root\"}'")
    }
  }
}
