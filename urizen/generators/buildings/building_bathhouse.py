#!/usr/bin/python3

import random
from copy import deepcopy
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_bathhouse(w=12, h=8, wall_material=None, floor_material=None):
    """
    Construct bathhouse with sweating room and dressing room.

    Constraints:

        - Map width and map height must be >= 8
        - Map width and map height must be <= 15
        - Wall material must be 'block', 'plank', 'brick' or 'stone'.
        - Floor material must be 'dirt', 'parquet' or 'cobblestone'.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height

    wall_material : str
        Wall's material.

    floor_material : str
        Floor's material.
    """
    # Initial checks. Don't accept too small/big bathhouse
    if w < 8 or h < 8:
        raise ValueError('Building is too small: w or h < 8')
    elif w > 15 or h > 15:
        raise ValueError('Building is too big: w or h > 15')
    # Choose materials
    if not wall_material:
        wall_material = random.choice([C.wall_block, C.wall_plank, C.wall_brick, C.wall_stone])
    elif wall_material not in (['block', 'plank', 'brick', 'stone']):
        raise ValueError('Wall material should be "block", "plank", "brick" or "stone"')
    if wall_material == 'block':
        wall_material = C.wall_block
    elif wall_material == 'plank':
        wall_material = C.wall_plank
    elif wall_material == 'brick':
        wall_material = C.wall_brick
    elif wall_material == 'stone':
        wall_material = C.wall_stone

    if not floor_material:
        floor_material = random.choice([C.floor_dirt, C.floor_parquet, C.floor_cobblestone])
    elif floor_material not in (['dirt', 'parquet', 'cobblestone']):
        raise ValueError('Floor material should be "dirt", "parquet" or "cobblestone"')
    if floor_material == 'dirt':
        floor_material = C.floor_dirt
    elif floor_material == 'parquet':
        floor_material = C.floor_parquet
    elif floor_material == 'cobblestone':
        floor_material = C.floor_cobblestone

    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)

    is_horizontal = random.choice([True, False])
    if w < 12 and h < 12:
        bathhouse = _room_sweating_square(w, h, wall_material, floor_material)
        M.meld(bathhouse, 0, 0)
    elif (w > h) or (w == h and w >= 12 and is_horizontal):
        sweating_room_w = w // 3 * 2
        sweating_room = _room_sweating_horizontal(sweating_room_w, h, wall_material, floor_material)
        M.meld(sweating_room, 0, 0)
        dressing_room = _room_dressing_horizontal(w-sweating_room_w+1, h, wall_material, floor_material)
        M.meld(dressing_room, sweating_room_w-1, 0)
    elif (w < h) or (w == h and w >= 12 and not is_horizontal):
        sweating_room_h = h // 3 * 2
        sweating_room = _room_sweating_vertical(w, sweating_room_h, wall_material, floor_material)
        M.meld(sweating_room, 0, 0)
        dressing_room = _room_dressing_vertical(w, h-sweating_room_h+1, wall_material, floor_material)
        M.meld(dressing_room, 0, sweating_room_h-1)

    if random.random() > 0.5:
        M.hmirror()
    else:
        M.vmirror()

    return M


def _room_sweating_horizontal(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in (w-3, w-2):
        M[x, 1].put(T.furniture_chimney())
    for x in range(1, 4):
        for y in (1, 3, h-2):
            M[x, y].put(T.furniture_longtable())
    for x in range(w-3, w-1):
        for y in (h-4, h-2):
            M[x, y].put(T.furniture_longtable())
    M[4, 1].put(T.furniture_box_filled())
    for x in (1, w-2):
        M[x, h-3].put(T.washtub())
    M[1, h-4].put(T.washtub())

    return M


def _room_dressing_horizontal(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for y in (1, h-2):
        M[1, y].put(T.furniture_bed_single())
    M[2, h-2].put(T.furniture_cabinet())
    M[w-2, 1].put(T.light_lantern())
    for x in(1, w-2):
        M[x, h-4].put(T.furniture_box_filled())
    for x in range(1, w-2):
        M[x, 2].put(T.furniture_longtable())
    M[0, h//2-1] = C.door_closed_window()
    M[w-1, h//2-1] = C.door_closed_window()

    return M


def _room_sweating_vertical(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in (w//2-1, w//2):
        M[x, h//2].put(T.furniture_chimney())
    for y in range(h-4, h-1):
        M[w-2, y].put(T.washtub())
    M[1, h//2-1].put(T.bucket())
    M[1, h-2].put(T.tool_broom())
    for x in range(1, w-1):
        M[x, 1].put(T.furniture_longtable())
    for x in range(w//2, w-1):
        M[x, 3].put(T.furniture_longtable())

    return M


def _room_dressing_vertical(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[w//2-1, 0] = C.door_closed_window()
    M[w//2-1, h-1] = C.door_closed()
    for x in range(w//2+1, w-1):
        M[x, h-2].put(T.furniture_longtable())
    for x in range(1, w//2-2):
        for y in range(1, h-1):
            M[x, y].put(T.furniture_barrel())
    M[w//2, 1].put(T.furniture_stool())
    M[w-2, 1].put(T.light_lantern())

    return M


def _room_sweating_square(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in (w//2-1, w//2):
        M[x, h//2-1].put(T.furniture_chimney())
    for x in range(1, w//2):
        M[x, 1].put(T.furniture_longtable())
    for x in range(w//2, w-1):
        M[x, 2].put(T.furniture_longtable())
    M[w-2, h//2-1].put(T.bucket())
    M[w//2-2, h-2].put(T.tool_broom())
    M[w//2-1, h-1] = C.door_closed()
    for y in range(h//2+1, h-1):
        M[1, y].put(T.furniture_barrel())
    M[w-2, h-2].put(T.furniture_bed_single())
    for y in range(h//2+1, h-1):
        M[w//2, y] = wall_material()
    M[w//2+1, h//2+1] = wall_material()
    M[w-3, h-2].put(T.furniture_cabinet())
    M[w-2, 1].put(T.washtub())
    M[1, 3].put(T.washtub())

    return M
