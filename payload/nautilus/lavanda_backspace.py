"""Backspace navigates history in Nautilus, never inside editable widgets."""
import gi

gi.require_version('Gtk', '4.0')
try:
    gi.require_version('Nautilus', '4.1')
except ValueError:
    gi.require_version('Nautilus', '4.0')
from gi.repository import Gdk, GLib, GObject, Gtk, Nautilus


def editing_or_popup(widget):
    while widget is not None:
        if isinstance(widget, (Gtk.Editable, Gtk.TextView, Gtk.Popover, Gtk.Dialog)):
            return True
        widget = widget.get_parent()
    return False


class LavandaBackspace(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self._application = None
        GLib.idle_add(self._install)

    def _install(self):
        app = Gtk.Application.get_default()
        if app is None:
            return GLib.SOURCE_REMOVE
        self._application = app
        app.connect('window-added', self._attach)
        for window in app.get_windows():
            self._attach(app, window)
        return GLib.SOURCE_REMOVE

    def _attach(self, app, window):
        if window.__gtype__.name != 'NautilusWindow':
            return
        if getattr(window, '_lavanda_backspace', False):
            return
        controller = Gtk.EventControllerKey.new()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        controller.connect('key-pressed', self._pressed, window)
        window.add_controller(controller)
        window._lavanda_backspace = True
        print("Lavanda: Retroceso activado en Nautilus", flush=True)

    def _pressed(self, controller, keyval, keycode, state, window):
        modifiers = state & Gtk.accelerator_get_default_mod_mask()
        if keyval != Gdk.KEY_BackSpace or modifiers:
            return False
        focus = window.get_focus()
        if focus is None or editing_or_popup(focus):
            return False
        # The action lives on the active slot, an ancestor of the focused view.
        # Returning false when unavailable preserves Nautilus' normal behavior.
        return focus.activate_action('slot.back', None)
