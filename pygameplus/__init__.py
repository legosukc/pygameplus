'''
An extension to the 'pygame' library.\n
Implements useful functions, mostly.
'''
from numba import njit
import math
import pygame

clock = pygame.time.Clock()

@njit
def LookAtPos(x1=int or float, y1=int or float, x2=int or float, y2=int or float, skipChecks=True) -> float or int:
    '''
    "Looks At" the second position given from the first position.\n
    Returns the angle.\n
    The 'skipChecks' parameter determines if the given values should be verified.\n
    Leave it alone if unsure, otherwise if you think the values might be invalid, set it to False.
    '''
    if not skipChecks:
        if not (isinstance(x1, (int, float)) and isinstance(y1, (int, float)) and isinstance(x2, (int, float)) and isinstance(y2, (int, float))):
            print("One of the values are invalid!")
            raise TypeError
    
    angle = math.degrees(math.atan2(-(y1-y2), x1-x2))
    if angle <= -90:
        angle += 360
    return angle+90

def GetDeltaTime(TargetFPS=60) -> float or int:
    try: delta = TargetFPS / clock.get_fps()
    except ZeroDivisionError: delta = 1
    return delta

def Raycast(collide=pygame.sprite.Group, dir=1 or -1, pos=tuple, stepLength=16, size=(1,1), ScrX=480) -> tuple[bool, tuple]:
    class Raycast(pygame.sprite.DirtySprite):
        def __init__(ray):
            super().__init__()
            ray.image = pygame.surface.Surface(size)
            ray.rect = ray.image.get_rect()
            ray.rect.center = pos
            ray.dirty = 1
    ray = Raycast()
    def Touching(): return pygame.sprite.spritecollideany(ray, collide)
    while not Touching():
        ray.rect.x += dir * stepLength
        if ray.rect.x <= 0 or ray.rect.x >= ScrX:
            return False, ray.rect.center
    while Touching():
        ray.rect.x -= dir
    return True, ray.rect.center

def Average(values=list, rnd=False, skipChecks=True) -> float or int:
    '''
    Gets the average of the given values in a list.\n
    List (values) must only containe integers or floats.\n
    'rnd' (Bool) determines if the returned value should be rounded. (Integer)\n
    The 'skipChecks' parameter determines if the given values should be verified.\n
    Leave it alone if unsure, otherwise if you think the values might be invalid, set it to False.
    '''
    if not skipChecks:
        if not (isinstance(values, list) and isinstance(rnd, bool)):
            print("One of the values were invalid!")
            raise TypeError
    avg = 0
    for i in range(len(values)):
        avg += values[i]
    if rnd: return avg // len(values)
    return avg / len(values)

@njit
def WithinRange(value=int or float, min=int or float, max=int or float, CanEqualTo=True, skipChecks=True) -> bool:
    '''
    Returns true if 'value' is inbetween the 'min' and 'max' values, otherwise, returns false.\n
    The 'CanEqualTo' parameter determines if 'value' can equal the 'min' and 'max' values.\n
    The 'skipChecks' parameter determines if the given values should be verified.\n
    Leave it alone if unsure, otherwise if you think the values might be invalid, set it to False.
    '''
    if not skipChecks:
        if not (isinstance(value, (int, float)) and isinstance(min, (int, float)) and isinstance(max, (int, float)) and isinstance(CanEqualTo, bool)):
            print("One of the values are invalid!")
            raise TypeError
    if CanEqualTo: return value >= min and value <= max
    else: return value > min and value < max
#end

def GetClosetSprites(sprite=pygame.sprite.Sprite, sprites=pygame.sprite.Group, range=90) -> pygame.sprite.Group:
    '''
    "Range" is in increments of a pixel.
    '''
    sprites = sprites.sprites()
    closest = pygame.sprite.Group()
    for i, compSprite in enumerate(sprites):
        rect = compSprite.rect
        if (abs(sprite.rect.centerx) - abs(rect.centerx)) + (abs(sprite.rect.centery) - abs(rect.centery)) < range:
            closest.add(compSprite)
    return closest