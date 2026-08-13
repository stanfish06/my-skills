#!/usr/bin/env bash

# UI/UX Pro Max is a generated seven-skill bundle with its own installer.
# Install it into the vault's canonical global skill store, then let the
# normal skills CLI propagate that store to each supported agent.
UI_UX_PRO_MAX_DEFAULT_CLI_VERSION="2.14.1"
UI_UX_PRO_MAX_BUNDLE_SKILLS="ui-ux-pro-max banner-design brand design-system design slides ui-styling"

cleanup_ui_ux_pro_max_first_install() {
  local skills_dir="$1"
  local name

  for name in $UI_UX_PRO_MAX_BUNDLE_SKILLS; do
    rm -rf -- "${skills_dir:?}/$name"
  done
  rm -f -- "$skills_dir/.ui-ux-pro-max-managed"
}

install_ui_ux_pro_max() {
  local cli_version="${UI_UX_PRO_MAX_CLI_VERSION:-$UI_UX_PRO_MAX_DEFAULT_CLI_VERSION}"
  local skills_dir="$HOME/.agents/skills"
  local marker="$skills_dir/.ui-ux-pro-max-managed"
  local managed=0
  local install_status name marker_tmp

  if [ "${UI_UX_PRO_MAX_SKIP:-0}" = "1" ]; then
    echo "ui-ux-pro-max: skipped (UI_UX_PRO_MAX_SKIP=1)"
    return 0
  fi

  if [ -f "$marker" ]; then
    managed=1
  else
    for name in $UI_UX_PRO_MAX_BUNDLE_SKILLS; do
      if [ -e "$skills_dir/$name" ] || [ -L "$skills_dir/$name" ]; then
        echo "ERROR: refusing to overwrite unmanaged skill at $skills_dir/$name." >&2
        echo "Remove or relocate it before enabling the ui-ux extra." >&2
        return 1
      fi
    done
  fi

  echo "ui-ux-pro-max: installing bundle with CLI $cli_version..."
  if npx -y "ui-ux-pro-max-cli@$cli_version" init \
      --ai universal --global --force; then
    install_status=0
  else
    install_status=$?
  fi

  if [ "$install_status" -ne 0 ]; then
    if [ "$managed" -eq 0 ]; then
      cleanup_ui_ux_pro_max_first_install "$skills_dir"
    fi
    echo "ERROR: ui-ux-pro-max installer failed." >&2
    return "$install_status"
  fi

  for name in $UI_UX_PRO_MAX_BUNDLE_SKILLS; do
    if [ ! -f "$skills_dir/$name/SKILL.md" ]; then
      if [ "$managed" -eq 0 ]; then
        cleanup_ui_ux_pro_max_first_install "$skills_dir"
      fi
      echo "ERROR: ui-ux-pro-max did not install the complete bundle; missing $name/SKILL.md." >&2
      return 1
    fi
  done

  marker_tmp="$marker.tmp.$$"
  printf '%s\n' "$cli_version" >"$marker_tmp"
  mv "$marker_tmp" "$marker"
  echo "ui-ux-pro-max: installed seven-skill bundle at $skills_dir"
}
