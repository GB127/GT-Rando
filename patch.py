
from ctypes import *
from enum import IntEnum

#------------------------------------------------------------------------------

class e_rom_screen_flag(IntEnum):
  ROM_SCREEN_FLAG_ICE_PHYSICS = (1<<0)
  ROM_SCREEN_FLAG_DARKNESS    = (1<<1)

class e_rom_ctile(IntEnum):
  ROM_CTILE_EMPTY         = 0x01 # $00
  ROM_CTILE_SPIKES        = 0x02 # $10
  ROM_CTILE_HOLE          = 0x03 # $30
  ROM_CTILE_SAND_NW       = 0x04 # $40
  ROM_CTILE_SAND_NE       = 0x05 # $42
  ROM_CTILE_SAND_SW       = 0x06 # $44
  ROM_CTILE_SAND_SE       = 0x07 # $46
  ROM_CTILE_STAIRS_HI     = 0x08 # $70
  ROM_CTILE_STAIRS_LO     = 0x09 # $71
  ROM_CTILE_BLOCK_1       = 0x0A # $80 (block player, block hookshot with sound)
  ROM_CTILE_BLOCK_2       = 0x0B # $C0 (block player, block hookshot without sound)
  ROM_CTILE_BLOCK_3       = 0x0C # $E0 (short wall)
  ROM_CTILE_BLOCK_4       = 0x0D # $F0 (block player, do not block hookshot)

# * means it is nowhere to be found in the original game
class e_rom_itile(IntEnum):
  ROM_ITILE_BARREL        = 0x00,
  ROM_ITILE_POT           = 0x02,
  ROM_ITILE_EGG           = 0x04,
  ROM_ITILE_SIGN          = 0x06, # *
  ROM_ITILE_POTTED_FLOWER = 0x08,
  ROM_ITILE_CHERRY_BOMB   = 0x0A, # *
  ROM_ITILE_LOG           = 0x0C, # *
  ROM_ITILE_SOMETHING     = 0x0E, # *
  ROM_ITILE_RED_BOX       = 0x10, # *
  ROM_ITILE_SHELL         = 0x12, # *
  ROM_ITILE_PLATES        = 0x14, # *
  ROM_ITILE_ROCK          = 0x16, # *
  ROM_ITILE_COCONUT       = 0x18,
  ROM_ITILE_STARRED_BLOCK = 0x1A,
  ROM_ITILE_GREEN_BLOCK   = 0x1C,
  ROM_ITILE_YELLOW_BLOCK  = 0x1E,
  ROM_ITILE_RED_BLOCK     = 0x20, # *

#------------------------------------------------------------------------------

class s_rom_level(Structure):
  _fields_ = [
    ("screen_index", c_uint),       # Do not change this
    ("num_screens", c_uint),        # Do not change this
    ("boss_screen_index", c_uint),
    ("boss_music_index", c_uint),
    ("music_index", c_uint),
    ("player1_start", c_ubyte * 2),
    ("player2_start", c_ubyte * 2)]

class s_rom_class_1_sprite(Structure):
  _fields_ = [
    ("type", c_ubyte),
    ("data_0", c_ubyte),
    ("data_1", c_ubyte),
    ("x", c_ubyte),
    ("y", c_ubyte)]

class s_rom_class_2_sprite(Structure):
  _fields_ = [
    ("type", c_ubyte),
    ("id", c_ubyte),
    ("x", c_ubyte),
    ("y", c_ubyte)]

class s_rom_exit(Structure):
  _fields_ = [
    ("type", c_ubyte),
    ("dst_screen", c_ubyte),
    ("dst_x", c_ubyte),
    ("dst_y", c_ubyte),
    ("tile_index", c_ushort)]

class s_rom_itile(Structure):
  _fields_ = [
    ("type", c_ubyte),
    ("tile_index", c_ushort)]

class s_rom_screen(Structure):
  _fields_ = [
    ("flags", c_uint),
    ("bot_gtiles", c_ushort * 1024),
    ("bot_ctiles", c_ubyte * 1024),
    ("top_gtiles", c_ushort * 1024),
    ("top_ctiles", c_ubyte * 1024),
    ("num_class_1_sprites", c_uint),
    ("num_class_2_sprites", c_uint),
    ("num_exits", c_uint),
    ("num_itiles", c_uint),
    ("class_1_sprites", s_rom_class_1_sprite * 32),
    ("class_2_sprites", s_rom_class_2_sprite * 32),
    ("exits", s_rom_exit * 16),
    ("itiles", s_rom_itile * 32)]

class s_rom_game(Structure):
  _fields_ = [
    ("num_levels", c_uint),              # Do not change this
    ("num_screens", c_uint),             # Do not change this
    ("levels", POINTER(s_rom_level)),
    ("screens", POINTER(s_rom_screen))]

class s_rom_data(Structure):
  _fields_ = [
    ("game", s_rom_game)]

#------------------------------------------------------------------------------

class s_rom_hole(Structure):
  _fields_ = [
    ("loca", c_uint),
    ("size", c_uint)]

class s_result(Structure):
  _fields_ = [
    ("num_banks", c_uint),
    ("num_bytes", c_uint)]

#------------------------------------------------------------------------------

lib = cdll.LoadLibrary('./patch.dll')

lib.commence.restype = POINTER(s_rom_data)
lib.conclude.restype = c_uint

# The DLL expects a buffer exactly 2 MiB in size (maximum size of a LoROM)
rom_data = bytearray(2<<20)

#------------------------------------------------------------------------------
"""
#------------------------------------------------------------------------------
# Conclude

result = s_result()

# Returns 1 on success, 0 on error
rv = lib.conclude(pointer(result))

#------------------------------------------------------------------------------
# Save result to disk

f = open("goof_troop_mod.smc", "wb")
f.write(rom_data[0:result.num_banks*32768])
f.close()
"""