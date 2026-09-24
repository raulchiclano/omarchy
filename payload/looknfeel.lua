-- Window borders coordinated with the purple wallpaper.
hl.config({
  general = {
    border_size = 2,
    col = {
      active_border = "rgba(b4a1f5ff)",
      inactive_border = "rgba(393449ff)",
    },
  },
  decoration = {
    rounding = 8,
    shadow = {
      enabled = true,
      range = 18,
      render_power = 3,
      color = "rgba(100b2066)",
      color_inactive = "rgba(100b2033)",
    },
  },
})

-- BEGIN SOFT DESKTOP MOTION
-- Short transitions without overshoot; speed units are 100 ms.
hl.config({ animations = { enabled = true } })
hl.curve("softDesktopOut", { type = "bezier", points = { { 0.22, 1 }, { 0.36, 1 } } })
hl.animation({ leaf = "windows", enabled = true, speed = 2, bezier = "softDesktopOut" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 1.8, bezier = "softDesktopOut", style = "popin 96%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.5, bezier = "almostLinear", style = "popin 97%" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.8, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.5, bezier = "almostLinear" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 2, bezier = "easeInOutCubic", style = "slide" })
-- END SOFT DESKTOP MOTION
