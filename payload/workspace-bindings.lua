-- Optional: replaces the stock move-to-group bindings on these two keys.
hl.unbind("SUPER + CTRL + LEFT")
hl.unbind("SUPER + CTRL + RIGHT")
o.bind("SUPER + CTRL + LEFT", "Previous workspace", hl.dsp.focus({ workspace = "e-1" }))
o.bind("SUPER + CTRL + RIGHT", "Next workspace", hl.dsp.focus({ workspace = "e+1" }))
