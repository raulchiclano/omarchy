import QtQuick
import Quickshell
import Quickshell.Io
import QtQuick.Effects
import qs.Commons
import qs.Ui

Item {
  id: root

  property string backgroundPath: ""
  property int backgroundVersion: 0
  property bool fingerprintConfigured: false
  property bool authenticatingPassword: false
  property string failureMessage: ""
  property int failedAttempts: 0
  property bool inputEnabled: true
  property bool loadBackground: true
  property string passwordText: ""
  property bool syncingPasswordText: false

  readonly property string accountName: Quickshell.env("USER") || Quickshell.env("LOGNAME")
  property string displayName: accountName
  readonly property string uiFont: "Adwaita Sans"
  readonly property string placeholderText: "Contraseña"

  SystemClock {
    id: clock
    precision: SystemClock.Minutes
  }

  // Resolve the current account's GECOS full name through NSS (also works
  // with directory-backed accounts). Keep the login name if it is absent.
  Process {
    command: ["getent", "passwd", root.accountName]
    running: root.accountName.length > 0
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        var fields = String(text || "").trim().split(":")
        if (fields.length >= 5 && fields[0] === root.accountName) {
          var fullName = fields[4].split(",")[0].trim()
          root.displayName = fullName || root.accountName
        }
      }
    }
  }
  readonly property int fieldWidth: Math.min(Style.space(340), Math.max(0, root.width - Style.space(48)))
  readonly property int fieldHeight: Style.space(54)
  readonly property int outlineThickness: Math.max(1, Style.space(1))
  readonly property int fieldFontSize: Style.space(16)
  readonly property int passwordDotFontSize: Style.space(18)
  readonly property int passwordDotLetterSpacing: Math.round(Style.font.heading * 0.19)
  // Space to keep clear on each side of the field for the fingerprint icon
  // (icon width plus a gap) so the centered dots never run under it.
  readonly property real fingerprintReserve: fingerprintConfigured ? Math.round(fingerprintIcon.implicitWidth + 12) : 0
  // Shrink the dots to fit once the password outgrows the field, so every
  // keystroke stays visible — otherwise long passwords clip with no feedback.
  readonly property real passwordDotScale: dotMetrics.advanceWidth > 0
    ? Math.min(1, (passwordInput.width - 4) / dotMetrics.advanceWidth)
    : 1
  readonly property bool showPasswordCursor: inputEnabled && !authenticatingPassword && failureMessage.length === 0
  readonly property bool errorState: failureMessage.length > 0
  readonly property var inputBorderSpec: errorState
    ? Border.flat("#F38BA8", root.outlineThickness)
    : Border.flat("#99B4A1F5", root.outlineThickness)

  signal submitPassword(string password)
  signal passwordTextEdited(string password)
  signal clearFailureRequested()
  signal wakeRequested()

  // Cache-busts the lock background by appending `?v=`. Adding a query
  // string keeps Image's loader happy while forcing it to reload when the
  // user picks a new background mid-session.
  function fileUrl(path) {
    if (!path) return ""
    var encoded = String(path).split("/").map(encodeURIComponent).join("/")
    return "file://" + encoded + "?v=" + backgroundVersion
  }

  function forcePasswordFocus() {
    passwordInput.forceActiveFocus()
  }

  function clearPassword() {
    passwordTextEdited("")
  }

  function syncPasswordText() {
    if (passwordInput.text === passwordText) return
    syncingPasswordText = true
    passwordInput.text = passwordText
    syncingPasswordText = false
  }

  onPasswordTextChanged: syncPasswordText()
  onInputEnabledChanged: {
    if (inputEnabled) Qt.callLater(forcePasswordFocus)
  }
  Component.onCompleted: {
    syncPasswordText()
    if (inputEnabled) Qt.callLater(forcePasswordFocus)
  }

  // Measures the masked password at full size; passwordDotScale compares this
  // against the field width to decide how far the dots must shrink to fit.
  TextMetrics {
    id: dotMetrics
    font.family: root.uiFont
    font.pixelSize: root.passwordDotFontSize
    font.letterSpacing: root.passwordDotLetterSpacing
    text: "●".repeat(passwordInput.text.length)
  }

  Rectangle {
    anchors.fill: parent
    color: Color.background

    Image {
      id: wallpaper
      anchors.fill: parent
      source: root.loadBackground ? root.fileUrl(root.backgroundPath) : ""
      fillMode: Image.PreserveAspectCrop
      asynchronous: true
      cache: false
      sourceSize.width: width
      sourceSize.height: height
    }

    MultiEffect {
      anchors.fill: wallpaper
      source: wallpaper
      autoPaddingEnabled: false
      blurEnabled: root.loadBackground && wallpaper.status === Image.Ready
      blur: 1.0
      blurMax: 128
      blurMultiplier: 1.25
      contrast: -0.08
    }

    MouseArea {
      anchors.fill: parent
      hoverEnabled: true
      onClicked: { root.wakeRequested(); root.forcePasswordFocus() }
      onPositionChanged: root.wakeRequested()
    }

    Column {
      anchors.horizontalCenter: parent.horizontalCenter
      anchors.bottom: userLabel.top
      anchors.bottomMargin: Style.space(40)
      width: Math.max(0, parent.width - Style.space(48))
      spacing: Style.space(8)
      Text {
        width: parent.width
        text: Qt.formatTime(clock.date, "HH:mm")
        color: "#F2EFFA"
        font.family: root.uiFont
        font.pixelSize: Style.space(80)
        font.weight: Font.Light
        horizontalAlignment: Text.AlignHCenter
      }
      Text {
        width: parent.width
        text: clock.date.toLocaleDateString(Qt.locale("es_ES"), "dddd, d 'de' MMMM")
        color: "#E1DCEB"
        font.family: root.uiFont
        font.pixelSize: Style.space(18)
        horizontalAlignment: Text.AlignHCenter
        elide: Text.ElideRight
      }
    }

    Text {
      id: userLabel
      anchors.horizontalCenter: parent.horizontalCenter
      anchors.bottom: inputField.top
      anchors.bottomMargin: Style.space(18)
      width: root.fieldWidth
      text: root.displayName
      textFormat: Text.PlainText
      color: "#F2EFFA"
      font.family: root.uiFont
      font.pixelSize: Style.space(18)
      font.weight: Font.DemiBold
      horizontalAlignment: Text.AlignHCenter
      elide: Text.ElideRight
    }

    BorderSurface {
      id: inputField
      width: root.fieldWidth
      height: root.fieldHeight
      anchors.centerIn: parent
      anchors.verticalCenterOffset: Math.min(Style.space(100), parent.height * 0.12)
      color: "#E6211E2C"
      borderSpec: root.inputBorderSpec
      radius: Style.space(12)
      clip: true

      TextInput {
        id: passwordInput
        anchors.fill: parent
        anchors.topMargin: inputField.borderTop
        // Reserve the fingerprint icon's width on both sides so the centered
        // dots stay symmetric and never slide under the icon as they grow.
        anchors.rightMargin: inputField.borderRight + 18 + root.fingerprintReserve
        anchors.bottomMargin: inputField.borderBottom
        anchors.leftMargin: inputField.borderLeft + 18 + root.fingerprintReserve
        verticalAlignment: TextInput.AlignVCenter
        horizontalAlignment: TextInput.AlignHCenter
        activeFocusOnPress: true
        clip: true
        enabled: root.inputEnabled && !root.authenticatingPassword
        readOnly: root.authenticatingPassword
        echoMode: TextInput.Password
        passwordCharacter: "\u25CF"
        passwordMaskDelay: 0
        color: "#F2EFFA"
        selectionColor: "#665B4689"
        selectedTextColor: "#F2EFFA"
        font.family: root.uiFont
        font.pixelSize: text.length > 0 ? Math.max(1, Math.floor(root.passwordDotFontSize * root.passwordDotScale)) : root.fieldFontSize
        font.letterSpacing: text.length > 0 ? root.passwordDotLetterSpacing * root.passwordDotScale : 0
        cursorVisible: activeFocus && root.showPasswordCursor && text.length > 0
        cursorDelegate: Rectangle {
          width: 2
          color: "#F2EFFA"
          visible: passwordInput.cursorVisible
        }

        onTextChanged: {
          if (!root.syncingPasswordText) root.passwordTextEdited(text)
          if (text.length > 0) {
            root.wakeRequested()
          }
          if (text.length > 0 && root.failureMessage.length > 0) root.clearFailureRequested()
        }

        onAccepted: {
          var submitted = root.passwordText
          root.passwordTextEdited("")
          if (submitted.length > 0) root.submitPassword(submitted)
        }

        Keys.onPressed: function(event) {
          root.wakeRequested()
          if (event.key === Qt.Key_Escape || (event.modifiers & Qt.ControlModifier && event.key === Qt.Key_U)) {
            root.passwordTextEdited("")
            event.accepted = true
          }
        }
      }

      Text {
        textFormat: Text.PlainText
        anchors.fill: passwordInput
        text: root.authenticatingPassword ? "Comprobando…" : (root.failureMessage.length > 0 ? "No se pudo autenticar" : root.placeholderText)
        visible: passwordInput.text.length === 0
        color: root.authenticatingPassword ? "#F2EFFA" : (root.failureMessage.length > 0 ? "#F38BA8" : "#C1B6D4")
        font.family: root.uiFont
        font.pixelSize: root.fieldFontSize
        font.italic: !root.authenticatingPassword && root.failureMessage.length > 0
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
      }

      // Fingerprint hint pinned inside the field's right edge when a sensor is
      // enrolled, so the user knows they can touch to unlock instead of typing.
      // Matches hyprlock, which draws its fingerprint icon in the same spot.
      Text {
        id: fingerprintIcon
        objectName: "fingerprintIndicator"
        anchors.right: parent.right
        anchors.rightMargin: inputField.borderRight + 18
        anchors.verticalCenter: parent.verticalCenter
        visible: root.fingerprintConfigured
        text: "󰈷"
        color: "#B4A1F5"
        font.family: "JetBrainsMono Nerd Font"
        font.pixelSize: Math.round(root.fieldFontSize * 1.1)
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
      }
    }
  }
}
