import QtQuick
import QtQuick.Layouts
import Quickshell.Hyprland
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "omarchy.workspaces"

  function workspaceById(id) {
    var values = Hyprland.workspaces.values
    for (var i = 0; i < values.length; i++) {
      if (values[i].id === id) return values[i]
    }

    return null
  }

  function workspaceIds() {
    var ids = [1, 2, 3, 4, 5]
    var values = Hyprland.workspaces.values

    for (var i = 0; i < values.length; i++) {
      var id = values[i].id
      if (id > 0 && id <= 10 && ids.indexOf(id) === -1) ids.push(id)
    }

    ids.sort(function(left, right) { return left - right })
    return ids
  }

  function focusWorkspace(id) {
    if (!root.bar) return
    root.bar.run("hyprctl dispatch " + Util.shellQuote("hl.dsp.focus({ workspace = \"" + id + "\" })"))
  }

  readonly property real trailingGap: root.vertical ? 0 : Style.spaceReal(1.5)

  implicitWidth: grid.implicitWidth + trailingGap
  implicitHeight: grid.implicitHeight

  GridLayout {
    id: grid
    anchors.fill: parent
    anchors.rightMargin: root.trailingGap
    columns: root.vertical ? 1 : root.workspaceIds().length
    columnSpacing: root.vertical ? 0 : Style.space(3)
    rowSpacing: root.vertical ? Style.space(2) : 0

    Repeater {
      model: root.workspaceIds()

      WidgetButton {
        id: workspaceButton
        required property int modelData

        readonly property var workspace: root.workspaceById(modelData)
        readonly property bool occupied: workspace !== null && workspace.toplevels.values.length > 0
        readonly property bool focused: Hyprland.focusedWorkspace !== null && Hyprland.focusedWorkspace.id === modelData

        bar: root.bar
        text: String(modelData)
        labelVisible: false
        opacity: 1
        tooltipText: "Escritorio " + modelData + (focused ? " · actual" : "")
        fixedWidth: root.vertical ? root.barSize : Style.space(28)
        fixedHeight: root.barSize

        Rectangle {
          anchors.centerIn: parent
          width: Math.min(parent.width, Style.space(26))
          height: Math.min(parent.height, Style.space(22))
          radius: Style.space(8)
          color: workspaceButton.focused ? "#B4A1F5"
            : (workspaceButton.tooltipHovered ? "#22B4A1F5" : "transparent")

          Behavior on color {
            ColorAnimation { duration: 140 }
          }
        }

        Text {
          anchors.centerIn: parent
          text: workspaceButton.text
          textFormat: Text.PlainText
          font.family: "Adwaita Sans"
          font.pixelSize: 13
          font.weight: Font.DemiBold
          renderType: Text.NativeRendering
          color: workspaceButton.focused ? "#211B32"
            : (workspaceButton.occupied ? "#F2EFFA" : "#A69BB8")
          horizontalAlignment: Text.AlignHCenter
          verticalAlignment: Text.AlignVCenter

          Behavior on color {
            ColorAnimation { duration: 140 }
          }
        }
        onPressed: function() { root.focusWorkspace(modelData) }
      }
    }
  }
}
