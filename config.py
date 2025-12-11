import pygame

# --- Screen Settings ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FONT_SIZE = 20

# --- Visualization Settings ---
# Set to 10,000 as requested to be used by all algorithms
NUM_BARS = 10_000
# Update frequency can be tuned here for all visualizers
UPDATE_FREQUENCY = 5_000 

# --- Colors ---
BG_COLOR = (20, 20, 20)
BAR_COLOR = (200, 200, 200)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (40, 40, 40)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_TEXT_COLOR = (255, 255, 255)
TAB_ACTIVE_COLOR = (0, 122, 204)
TAB_INACTIVE_COLOR = (50, 50, 50)

# Accent colors for each algorithm's highlights
CASCADE_COLOR = (227, 11, 92) # Pink/Red
PIGEONHOLE_COLOR = (0, 255, 100) # Green
BALANCE_BEAM_SWAP_COLOR = (137, 207, 240) # Baby Blue
BALANCE_BEAM_SCAN_COLOR = (255, 255, 102) # Yellow

# --- Data Generation Settings ---
# Settings for general-purpose algorithms (Cascade, Balance Beam)
GENERAL_NUM_ELEMENTS = 100_000
GENERAL_MIN_VAL = 1.0
GENERAL_MAX_VAL = 1_000_000.0

# Settings for Pigeonhole Sort (requires a permutation)
PIGEONHOLE_NUM_ELEMENTS = 10_000 # Must match NUM_BARS for 1-to-1 mapping
PIGEONHOLE_MAX_VAL = 100_000
