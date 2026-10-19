-- Personal shortcuts: Super is the Windows key.
hl.unbind("SUPER + SHIFT + W")
o.bind("SUPER + SHIFT + W", "WhatsApp", { webapp = "https://web.whatsapp.com/", focus = true })
-- Super+C replaces Omarchy universal copy; standard Ctrl+C is unchanged.
hl.unbind("SUPER + C")
o.bind("SUPER + C", "Visual Studio Code", { launch = "code" })
hl.unbind("SUPER + SHIFT + C")
o.bind("SUPER + SHIFT + C", "Color picker", "pkill hyprpicker || hyprpicker -a")
hl.unbind("SUPER + SHIFT + N")
o.bind("SUPER + SHIFT + N", "Omawrite", { launch = "omawrite" })
hl.unbind("SUPER + SHIFT + S")
o.bind("SUPER + SHIFT + S", "Screenshot", "omarchy-capture-screenshot")
