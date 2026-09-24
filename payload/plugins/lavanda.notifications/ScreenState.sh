#!/usr/bin/env bash
# Only report a clear screen after all public state checks succeed.
set -uo pipefail
hidden() { printf '%s\n' hidden; exit 0; }
lock_state=$(timeout 1s omarchy-shell lock isLocked 2>/dev/null) || hidden
[[ $lock_state == false ]] || hidden
timeout 1s omarchy-hyprland-session-locked >/dev/null 2>&1
[[ $? == 1 ]] || hidden
idle_state=$(timeout 1s omarchy-shell idle status 2>/dev/null) || hidden
jq -e '
  type == "object" and
  .screensaverWindows == 0 and
  .timers.screensaverLaunchGrace == false and
  .processes.screensaver == false
' <<<"$idle_state" >/dev/null 2>&1 || hidden
printf '%s\n' clear
