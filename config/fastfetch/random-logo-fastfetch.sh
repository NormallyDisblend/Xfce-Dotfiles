#!/bin/sh
LOGO_DIR="$HOME/.config/fastfetch"
RANDOM_LOGO=$(find "$LOGO_DIR" -type f -name "*.png" | shuf -n 1)
TARGET="$HOME/.config/fastfetch/png/current-logo.png"

if [ "$RANDOM_LOGO" != "$TARGET" ]; then
  cp "$RANDOM_LOGO" "$TARGET"
fi

fastfetch
