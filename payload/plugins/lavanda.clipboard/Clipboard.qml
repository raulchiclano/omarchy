import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import QtQuick
import QtQuick.Controls as Controls
import qs.Commons
import qs.Ui
import "ClipboardHistory.js" as ClipboardHistory

Item {
  id: root

  property string omarchyPath: Quickshell.env("OMARCHY_PATH")
  property bool opened: false
  property string filterText: ""
  property int selectedIndex: 0
  property bool cursorActive: false
  property bool clearConfirmOpen: false
  property var history: []

  property string historyPath: Quickshell.env("HOME") + "/.local/state/omarchy/clipboard-history.json"
  property string captureScript: root.omarchyPath + "/shell/plugins/clipboard/capture.sh"
  // Shares the [menu] surface tokens — themes that style the menu also
  // style the clipboard. Selected-row colors composed in the
  // singleton so consumers drop them straight into Rectangle bindings.
  property color background: "#F0211E2C"
  property color foreground: "#F2EFFA"
  property color border: "#47B4A1F5"
  property var borderSpec: Border.flat(border, Math.max(1, Style.space(1)))
  property color scrim: Color.menu.scrim
  property color selectedBackground: "#393249"
  property color selectedText: "#F2EFFA"
  readonly property int cornerRadius: Style.space(14)
  property string fontFamily: "Adwaita Sans"
  property int contentMargin: Style.space(20)
  property int headerHeight: Style.space(48)
  property int contentSpacing: Style.space(16)
  property int cardWidth: Math.min(Style.space(940), panel.width - Style.gapsOut * 2)
  property int cardHeight: Math.min(Style.space(620), panel.height - Style.gapsOut * 2)
  property int rowHeight: Style.space(58)
  property int historyLimit: 300

  function open(payloadJson) {
    root.opened = true
    root.filterText = ""
    root.selectedIndex = 0
    root.cursorActive = true
    root.disarmPointer()
    root.rebuildDisplay()
    Qt.callLater(function() { keyCatcher.forceActiveFocus() })
  }

  function close() {
    root.cancelClearHistory()
    root.opened = false
  }

  function toggle() {
    if (root.opened) root.close()
    else root.open("{}")
  }

  function normalizeEntry(value) {
    return ClipboardHistory.normalizeEntry(value)
  }

  function entryKey(entry) {
    return ClipboardHistory.entryKey(entry)
  }

  function loadHistory(raw) {
    root.history = ClipboardHistory.parseHistory(raw)
    if (root.opened) root.rebuildDisplay()
  }

  function saveHistory() {
    historyFile.setText(JSON.stringify(root.history.slice(0, root.historyLimit), null, 2) + "\n")
  }

  function addClipboardEntry(entry) {
    var normalized = ClipboardHistory.normalizeEntry(entry)
    if (!normalized) return

    root.history = ClipboardHistory.addEntry(root.history, normalized, root.historyLimit)
    root.saveHistory()
    if (root.opened) root.rebuildDisplay()
  }

  function addClipboardJson(line) {
    root.addClipboardEntry(ClipboardHistory.parseEntryJson(line))
  }

  function requestClearHistory() {
    if (root.history.length === 0) return
    clearConfirm.selectedIndex = 1
    root.clearConfirmOpen = true
  }

  function cancelClearHistory() {
    root.clearConfirmOpen = false
    root.disarmPointer()
    Qt.callLater(function() { keyCatcher.forceActiveFocus() })
  }

  function confirmClearHistory() {
    root.history = ClipboardHistory.clearHistory()
    root.saveHistory()
    root.selectedIndex = 0
    root.cursorActive = false
    root.disarmPointer()
    root.clearConfirmOpen = false
    root.rebuildDisplay()
    Qt.callLater(function() { keyCatcher.forceActiveFocus() })
  }

  function removeDisplayIndex(index) {
    if (index < 0 || index >= displayModel.count) return

    var row = displayModel.get(index)
    root.history = ClipboardHistory.removeEntryAt(root.history, row.historyIndex)
    root.saveHistory()

    if (displayModel.count <= 1) {
      root.selectedIndex = 0
      root.cursorActive = false
    } else if (root.selectedIndex >= displayModel.count - 1) {
      root.selectedIndex = displayModel.count - 2
    }

    root.disarmPointer()
    root.rebuildDisplay()
  }

  function rebuildDisplay() {
    var rows = ClipboardHistory.displayRows(root.history, root.filterText, 50)

    displayModel.clear()
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i]
      displayModel.append({
        entryType: row.entryType,
        fullText: row.fullText,
        previewText: row.previewText,
        previewImage: row.previewImage ? Util.fileUrl(row.previewImage) : "",
        path: row.path,
        mime: row.mime,
        historyIndex: row.index
      })
    }

    if (displayModel.count === 0) selectedIndex = 0
    else if (selectedIndex >= displayModel.count) selectedIndex = displayModel.count - 1
    else if (selectedIndex < 0) selectedIndex = 0

    Qt.callLater(function() {
      if (displayModel.count > 0) resultList.positionViewAtIndex(root.selectedIndex, ListView.Contain)
    })
  }

  function select(delta) {
    if (displayModel.count === 0) return
    root.disarmPointer()
    if (!cursorActive) {
      cursorActive = true
      selectedIndex = delta < 0 ? displayModel.count - 1 : 0
    } else {
      selectedIndex = (selectedIndex + delta + displayModel.count) % displayModel.count
    }
    resultList.positionViewAtIndex(selectedIndex, ListView.Contain)
  }

  function selectAbsolute(index) {
    if (displayModel.count === 0) return
    root.disarmPointer()
    root.cursorActive = true
    root.selectedIndex = Math.max(0, Math.min(index, displayModel.count - 1))
    resultList.positionViewAtIndex(root.selectedIndex, ListView.Contain)
  }

  function setFilter(nextFilter) {
    root.filterText = nextFilter
    root.selectedIndex = 0
    root.cursorActive = true
    root.disarmPointer()
    root.rebuildDisplay()
  }

  function disarmPointer() {
    pointerGate.reset()
  }

  function selectFromPointer(index, item, mouse) {
    if (!pointerGate.moved(item, mouse)) return
    root.cursorActive = true
    root.selectedIndex = index
  }

  function activateIndex(index) {
    if (index < 0 || index >= displayModel.count) return
    var row = displayModel.get(index)
    root.applySelected(row)
  }

  function copyIndex(index) {
    if (index < 0 || index >= displayModel.count) return
    var row = displayModel.get(index)
    root.copySelected(row)
  }

  function openIndex(index) {
    if (index < 0 || index >= displayModel.count) return
    var row = displayModel.get(index)
    root.openSelected(row)
  }

  function applySelected(row) {
    if (!row) return
    root.opened = false
    if (row.entryType === "image") {
      Quickshell.execDetached([root.omarchyPath + "/bin/omarchy-clipboard-paste-file", row.mime, row.path])
    } else if (row.fullText) {
      Quickshell.execDetached([root.omarchyPath + "/bin/omarchy-clipboard-paste-text", "--shift-insert", "--history-index", String(row.historyIndex)])
    }
  }

  function copySelected(row) {
    if (!row) return
    root.opened = false
    if (row.entryType === "image") {
      Quickshell.execDetached([root.omarchyPath + "/bin/omarchy-clipboard-paste-file", "--copy-only", row.mime, row.path])
    } else if (row.fullText) {
      Quickshell.execDetached([root.omarchyPath + "/bin/omarchy-clipboard-paste-text", "--copy-only", "--history-index", String(row.historyIndex)])
    }
  }

  function openSelected(row) {
    if (!row) return
    root.opened = false
    Quickshell.execDetached([root.omarchyPath + "/bin/omarchy-clipboard-open", "--history-index", String(row.historyIndex)])
  }

  Component.onCompleted: initProc.running = true

  ListModel { id: displayModel }

  PointerMoveGate {
    id: pointerGate
    referenceItem: card
  }

  FileView {
    id: historyFile
    path: root.historyPath
    watchChanges: true
    atomicWrites: true
    printErrors: false
    onLoaded: root.loadHistory(text())
    onLoadFailed: root.loadHistory("[]")
    onFileChanged: reload()
  }

  // Reap watchers left behind by a previous shell instance, then start our
  // own. The pdeathsig on the watchers makes the kernel kill them whenever
  // the shell exits, however it exits, so no further lifecycle management.
  Process {
    id: initProc
    command: ["pkill", "-f", "wl-paste .*--watch .*/shell/plugins/clipboard/capture\\.sh"]
    onExited: {
      currentProc.running = true
      textWatchProc.running = true
      imageWatchProc.running = true
    }
  }

  Process {
    id: currentProc
    command: [root.captureScript]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: root.addClipboardJson(text)
    }
  }

  Process {
    id: textWatchProc
    command: ["setpriv", "--pdeathsig", "TERM", "wl-paste", "--type", "text", "--watch", root.captureScript, "text"]
    onExited: watchRestartTimer.restart()
    stdout: SplitParser {
      onRead: function(data) { root.addClipboardJson(data) }
    }
  }

  Process {
    id: imageWatchProc
    command: ["setpriv", "--pdeathsig", "TERM", "wl-paste", "--type", "image/png", "--watch", root.captureScript, "image/png"]
    onExited: watchRestartTimer.restart()
    stdout: SplitParser {
      onRead: function(data) { root.addClipboardJson(data) }
    }
  }

  // A watcher that dies takes clipboard history with it, silently: copying still
  // works, the picker still opens, and the old entries are all still there, so
  // nothing recorded until the next shell reload. Bring it back instead.
  Timer {
    id: watchRestartTimer
    interval: 1000
    repeat: false
    onTriggered: {
      if (!textWatchProc.running) textWatchProc.running = true
      if (!imageWatchProc.running) imageWatchProc.running = true
    }
  }

  PanelWindow {
    id: panel
    visible: root.opened
    anchors { top: true; bottom: true; left: true; right: true }
    color: "transparent"
    WlrLayershell.namespace: "omarchy-clipboard"
    WlrLayershell.layer: WlrLayer.Overlay
    WlrLayershell.keyboardFocus: WlrKeyboardFocus.Exclusive
    exclusionMode: ExclusionMode.Ignore

    Rectangle {
      anchors.fill: parent
      color: root.scrim
    }

    MouseArea {
      anchors.fill: parent
      onClicked: root.close()
    }

    BorderSurface {
      id: card
      width: root.cardWidth
      height: root.cardHeight
      radius: root.cornerRadius
      anchors.centerIn: parent
      color: root.background
      borderSpec: root.borderSpec
      padding: root.contentMargin

      MouseArea { anchors.fill: parent; onClicked: {} }

      Item {
        id: keyCatcher
        anchors.fill: parent
        z: root.clearConfirmOpen ? 20 : 0
        focus: true

        Keys.priority: Keys.BeforeItem
        Keys.onPressed: function(event) {
          if (root.clearConfirmOpen) {
            if (clearConfirm.handleKey(event)) event.accepted = true
            return
          }

          if (event.key === Qt.Key_Escape) {
            if (root.filterText) root.setFilter("")
            else root.close()
            event.accepted = true
          } else if (Util.editsFilter(event, root.filterText)) {
            root.setFilter(Util.editedFilter(event, root.filterText))
            event.accepted = true
          } else if (event.key === Qt.Key_Delete) {
            if (event.modifiers & Qt.ShiftModifier) root.requestClearHistory()
            else root.removeDisplayIndex(root.selectedIndex)
            event.accepted = true
          } else if (event.key === Qt.Key_Up) {
            root.select(-1)
            event.accepted = true
          } else if (event.key === Qt.Key_Down) {
            root.select(1)
            event.accepted = true
          } else if (event.key === Qt.Key_PageUp) {
            root.select(-6)
            event.accepted = true
          } else if (event.key === Qt.Key_PageDown) {
            root.select(6)
            event.accepted = true
          } else if (event.key === Qt.Key_Home) {
            root.selectAbsolute(0)
            event.accepted = true
          } else if (event.key === Qt.Key_End) {
            root.selectAbsolute(displayModel.count - 1)
            event.accepted = true
          } else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
            if (root.cursorActive && (event.modifiers & Qt.AltModifier)) root.openIndex(root.selectedIndex)
            else if (root.cursorActive && (event.modifiers & Qt.ShiftModifier)) root.copyIndex(root.selectedIndex)
            else if (root.cursorActive) root.activateIndex(root.selectedIndex)
            else if (displayModel.count > 0) root.cursorActive = true
            event.accepted = true
          } else if (event.text && event.text.length === 1 && event.text.charCodeAt(0) >= 32 && event.text.charCodeAt(0) !== 127) {
            root.setFilter(root.filterText + event.text)
            event.accepted = true
          }
        }

        ConfirmDialog {
          id: clearConfirm

          anchors.fill: parent
          opened: root.clearConfirmOpen
          z: 10
          message: "¿Eliminar todo el historial del portapapeles?"
          confirmText: "Eliminar"
          cancelText: "Cancelar"
          background: root.background
          foreground: root.foreground
          scrim: root.scrim
          selectedBackground: root.selectedBackground
          selectedText: root.selectedText
          fontFamily: root.fontFamily
          cornerRadius: root.cornerRadius
          onCanceled: root.cancelClearHistory()
          onConfirmed: root.confirmClearHistory()
        }
      }

      Column {
        anchors.fill: parent
        anchors.topMargin: card.contentTopInset
        anchors.rightMargin: card.contentRightInset
        anchors.bottomMargin: card.contentBottomInset
        anchors.leftMargin: card.contentLeftInset
        spacing: root.contentSpacing

        Rectangle {
          width: parent.width
          height: root.headerHeight
          radius: Style.space(10)
          color: "#292536"
          Text {
            anchors.left: parent.left
            anchors.leftMargin: Style.space(14)
            anchors.verticalCenter: parent.verticalCenter
            text: ""
            color: "#B4A1F5"
            font.family: "JetBrainsMono Nerd Font"
            font.pixelSize: Style.space(17)
          }
          Text {
            anchors.left: parent.left
            anchors.leftMargin: Style.space(44)
            anchors.right: parent.right
            anchors.rightMargin: Style.space(14)
            anchors.verticalCenter: parent.verticalCenter
            textFormat: Text.PlainText
            text: root.filterText || "Buscar en el portapapeles…"
            color: root.filterText ? root.foreground : "#A69BB8"
            font.family: root.fontFamily
            font.pixelSize: Style.space(17)
            elide: Text.ElideRight
          }
        }

        Item {
          width: parent.width
          height: parent.height - root.headerHeight - Style.space(26) - root.contentSpacing * 2

          Row {
            anchors.fill: parent
            spacing: Style.space(20)
            visible: displayModel.count > 0

            Column {
              id: historyColumn
              width: Math.floor((parent.width - parent.spacing) * 0.44)
              height: parent.height
              spacing: Style.space(10)
              Text {
                width: parent.width
                height: Style.space(26)
                text: "Historial · " + displayModel.count
                color: "#A69BB8"
                font.family: root.fontFamily
                font.pixelSize: Style.space(13)
                font.weight: Font.DemiBold
                verticalAlignment: Text.AlignVCenter
              }
              ListView {
                id: resultList
                width: parent.width
                height: parent.height - Style.space(36)
                model: displayModel
                clip: true
                spacing: Style.space(7)
                boundsBehavior: Flickable.StopAtBounds
                Controls.ScrollBar.vertical: Controls.ScrollBar {
                  width: Style.space(4)
                  policy: Controls.ScrollBar.AsNeeded
                }
                delegate: Rectangle {
                  id: row
                  required property int index
                  required property string entryType
                  required property string previewText
                  required property string fullText
                  required property string previewImage
                  readonly property bool hasCursor: root.cursorActive && index === root.selectedIndex
                  width: ListView.view.width - Style.space(8)
                  height: root.rowHeight
                  radius: Style.space(10)
                  color: hasCursor ? root.selectedBackground : "#142E293D"
                  border.width: 1
                  border.color: hasCursor ? "#55B4A1F5" : "transparent"
                  Rectangle {
                    id: entryIcon
                    anchors.left: parent.left
                    anchors.leftMargin: Style.space(12)
                    anchors.verticalCenter: parent.verticalCenter
                    width: Style.space(32)
                    height: width
                    radius: Style.space(7)
                    color: row.hasCursor ? "#25B4A1F5" : "#292536"
                    Text {
                      anchors.centerIn: parent
                      visible: !row.previewImage
                      text: row.entryType === "file" ? "󰈔" : "󰈙"
                      font.family: "JetBrainsMono Nerd Font"
                      font.pixelSize: Style.space(18)
                      color: "#B4A1F5"
                    }
                    Image {
                      anchors.fill: parent
                      anchors.margins: Style.space(3)
                      visible: !!row.previewImage
                      source: row.previewImage
                      fillMode: Image.PreserveAspectFit
                      asynchronous: false
                      smooth: true
                    }
                  }
                  Text {
                    anchors.left: entryIcon.right
                    anchors.leftMargin: Style.space(12)
                    anchors.right: parent.right
                    anchors.rightMargin: Style.space(14)
                    anchors.verticalCenter: parent.verticalCenter
                    textFormat: Text.PlainText
                    text: row.entryType === "image" ? row.previewText.replace(/^Screenshot from /, "Captura · ") : row.previewText.replace(/\s+/g, " ").trim()
                    color: row.hasCursor ? root.selectedText : root.foreground
                    font.family: root.fontFamily
                    font.pixelSize: Style.space(15)
                    font.weight: row.hasCursor ? Font.DemiBold : Font.Normal
                    elide: Text.ElideRight
                    wrapMode: Text.NoWrap
                  }
                  MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onPositionChanged: function(mouse) { root.selectFromPointer(row.index, row, mouse) }
                    onClicked: {
                      root.cursorActive = true
                      root.selectedIndex = row.index
                      root.activateIndex(row.index)
                    }
                  }
                }
              }
            }

            Rectangle {
              id: previewPane
              width: parent.width - historyColumn.width - parent.spacing
              height: parent.height
              radius: Style.space(12)
              color: "#292536"
              border.width: 1
              border.color: "#334A4164"
              property var activeRow: displayModel.count > 0 && root.selectedIndex >= 0 && root.selectedIndex < displayModel.count ? displayModel.get(root.selectedIndex) : null
              property string previewContent: activeRow ? activeRow.fullText : ""
              onPreviewContentChanged: previewScroll.contentY = 0
              Column {
                anchors.fill: parent
                anchors.margins: Style.space(20)
                spacing: Style.space(14)
                Item {
                  width: parent.width
                  height: Style.space(24)
                  Text {
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Vista previa"
                    color: root.foreground
                    font.family: root.fontFamily
                    font.pixelSize: Style.space(15)
                    font.weight: Font.DemiBold
                  }
                  Text {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    text: !previewPane.activeRow ? "" : previewPane.activeRow.previewImage ? "Imagen" : previewPane.activeRow.entryType === "file" ? "Archivo" : "Texto"
                    color: "#B4A1F5"
                    font.family: root.fontFamily
                    font.pixelSize: Style.space(12)
                  }
                }
                Rectangle { width: parent.width; height: 1; color: "#334A4164" }
                Item {
                  width: parent.width
                  height: parent.height - Style.space(24) - 1 - parent.spacing * 2
                  Flickable {
                    id: previewScroll
                    anchors.fill: parent
                    visible: previewPane.activeRow && !previewPane.activeRow.previewImage
                    clip: true
                    contentWidth: width
                    contentHeight: previewText.implicitHeight
                    boundsBehavior: Flickable.StopAtBounds
                    flickableDirection: Flickable.VerticalFlick
                    Controls.ScrollBar.vertical: Controls.ScrollBar {
                      width: Style.space(4)
                      policy: Controls.ScrollBar.AsNeeded
                    }
                    Text {
                      id: previewText
                      width: previewScroll.width - Style.space(12)
                      text: previewPane.previewContent
                      textFormat: Text.PlainText
                      color: "#E1DCEB"
                      font.family: root.fontFamily
                      font.pixelSize: Style.space(15)
                      wrapMode: Text.Wrap
                      lineHeight: 1.4
                    }
                  }
                  Image {
                    anchors.fill: parent
                    visible: previewPane.activeRow && !!previewPane.activeRow.previewImage
                    source: previewPane.activeRow ? previewPane.activeRow.previewImage : ""
                    fillMode: Image.PreserveAspectFit
                    asynchronous: false
                    smooth: true
                  }
                }
              }
            }
          }

          Text {
            anchors.centerIn: parent
            width: parent.width
            visible: displayModel.count === 0
            text: root.history.length === 0 ? "El portapapeles está vacío" : "Sin resultados para «" + root.filterText + "»"
            textFormat: Text.PlainText
            color: "#A69BB8"
            font.family: root.fontFamily
            font.pixelSize: Style.space(16)
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
          }
        }
        Text {
          width: parent.width
          height: Style.space(26)
          text: "↑ ↓  Elegir     ↵  Pegar     Mayús + ↵  Copiar     Supr  Eliminar     Esc  Cerrar"
          color: "#A69BB8"
          font.family: root.fontFamily
          font.pixelSize: Style.space(12)
          verticalAlignment: Text.AlignVCenter
          elide: Text.ElideRight
        }
      }
    }
  }
}
