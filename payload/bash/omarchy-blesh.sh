# Fall back to Omarchy defaults if an update changes the integration contract.
# Do this BEFORE loading ble.sh, so fzf is never initialized twice.
_lavanda_compatible=true
[[ $(sha256sum "$OMARCHY_PATH/default/bash/init" 2>/dev/null) == "3ffd0028967c90ee2069ef96ddc06773f107788bfba04edab247967e5a4b3bcc "* ]] || _lavanda_compatible=false
[[ $(sha256sum "$OMARCHY_PATH/default/bash/rc" 2>/dev/null) == "f5abfe8652e3df79de7d247f72a7f3b663a6521a8135609b04b839fc6ac2bfda "* ]] || _lavanda_compatible=false
if [[ $_lavanda_compatible != true ]]; then
  unset _lavanda_compatible
  printf '%s\n' 'Lavanda: Omarchy ha cambiado; se usa Bash estándar hasta revisar la integración.' >&2
  source "$OMARCHY_PATH/default/bash/rc"
  return
fi
unset _lavanda_compatible

# Omarchy defaults, with ble.sh's supported fzf integration.
# Keep packaged files untouched and read the current init on each shell start.
source /usr/share/blesh/ble.sh --attach=none
# ble.sh skips attachment for shells started with -c; use stock init there.
if [[ ! ${BLE_VERSION-} ]]; then
  source "$OMARCHY_PATH/default/bash/rc"
  return
fi
source "$OMARCHY_PATH/default/bash/envs"
source "$OMARCHY_PATH/default/bash/shell"
source "$OMARCHY_PATH/default/bash/aliases"
source "$OMARCHY_PATH/default/bash/functions"
source <(sed \
  -e 's@source /usr/share/fzf/completion.bash@ble-import integration/fzf-completion@' \
  -e 's@source /usr/share/fzf/key-bindings.bash@ble-import integration/fzf-key-bindings@' \
  "$OMARCHY_PATH/default/bash/init")
bind -f "$OMARCHY_PATH/default/bash/inputrc"
