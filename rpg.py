import os
import random
import sys
import time

import pygame
from numpy import isin

# the Pygame docs say size(text) -> (width, height)
# PYGAME
MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

# ACTION RESPONSE
ACTION_REPLAY = -2
ACTION_SUCCESS = -1
SPELL_ERROR_REASON_NOT_ENOUGHT_MANA = 0
SPELL_ERROR_REASON_NOT_ENOUGHT_PLACE = 1
SPELL_ERROR_REASON_NOT_ENOUGHT_SKILLPOINT = 2
SPELL_ERROR_REASON_NOT_ENOUGHT_MONEY = 3
SPELL_ERROR_REASON_ENEMY_NOT_ENOUGHT_MANA = 4

SPELL_ERROR_TRADUCTION = {
    SPELL_ERROR_REASON_NOT_ENOUGHT_MANA: "Not enought mana.",
    SPELL_ERROR_REASON_NOT_ENOUGHT_PLACE: "Not enought place.",
    SPELL_ERROR_REASON_NOT_ENOUGHT_SKILLPOINT: "Not enought skillpoint.",
    SPELL_ERROR_REASON_NOT_ENOUGHT_MONEY: "Not enought money.",
    SPELL_ERROR_REASON_ENEMY_NOT_ENOUGHT_MANA: "Enemy has not enought money.",
}

# MODULAR
UI_MODULAR_BAR_INFO_TYPE_HEALTH = 0
UI_MODULAR_BAR_INFO_TYPE_MANA = 1
UI_MODULAR_BAR_INFO_TYPE_EXPERIENCE = 2

# COST
COST_HEALTH = 0
COST_MANA = 1
COST_RAGE = 2

# GAME
WINDOW_TITLE = "RPG"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_TICK = 60
TOOLTIP_MARGIN = 15
INVENTORY_SPELL_HEIGHT = 50
INVENTORY_SPELL_ITEM_MAX_ROW_COUNT = 12
INVENTORY_SPELL_ITEM_COUNT = 36
ERROR_REMAINING_TICK = 60 * 5
FRAME_EFFECT_MAX_LINE_COUNT = 5

# GAME PLAY
SPELL_TEST_COST = 5

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (245, 245, 245)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE_BACK = (0, 0, 10)
YELLOW_TEXT = (255, 213, 23)
YELLOW_FRAME_TEXT = (240, 197, 0)
BLUE_XP = (0, 66, 150)
Q_POOR = (157, 157, 157)
Q_COMMON = (255, 255, 255)
Q_UNCOMMON = (30, 255, 0)
Q_RARE = (0, 112, 221)
Q_EPIC = (163, 53, 238)
Q_LEGENDARY = (255, 128, 0)
LEVEL_DIFFICULTY_TRASH = (121, 121, 121)
LEVEL_DIFFICULTY_EASY = (47, 131, 46)
LEVEL_DIFFICULTY_NORMAL = (201, 201, 8)
LEVEL_DIFFICULTY_MEDIUM = (224, 114, 57)
LEVEL_DIFFICULTY_HARD = (255, 26, 26)
LEVEL_DIFFICULTY_DEAD_SKULL = 0x0

pygame.init()

# CACHE
ASSETS_CACHE = {}


class Assets:

    @staticmethod
    def loadFont(path, size):
        font = None

        try:
            font = pygame.font.Font(path, size)
            print("Loaded font: " + str(path))
        except Exception as exception:
            print("Failed to load font \"" + str(path) + "\" with size: " + str(size) + ", error: " + str(exception))
            font = Assets.loadFont("assets/fonts/frizquad.ttf", 20)

        return font

    @staticmethod
    def loadResizedImage(path, size):
        return pygame.transform.scale(Assets.loadImage(path), size)

    @staticmethod
    def loadImage(path):
        image = None

        if path in ASSETS_CACHE:
            image = ASSETS_CACHE[path]
        else:
            try:
                image = pygame.image.load(path)
                ASSETS_CACHE.update({path: image})
                print("Loaded image: " + str(path))
            except Exception as exception:
                print("Failed to load image \"" + str(path) + "\", error: " + str(exception))
                image = TEXTURE_TEST

        return image


# # Loading Fonts
print("Loading fonts...")
# FONT = Assets.loadFont(None, 30)
FONT_WOW = Assets.loadFont("assets/fonts/frizquad.ttf", 20)
FONT_TOOLTIP_TITLE = Assets.loadFont("assets/fonts/frizquad.ttf", 20)
FONT_TOOLTIP_DESCRIPTION = Assets.loadFont("assets/fonts/frizquad.ttf", 16)
FONT_WOW_TINY = Assets.loadFont("assets/fonts/frizquad.ttf", 15)
FONT_WOW_VERY_TINY = Assets.loadFont("assets/fonts/frizquad.ttf", 10)
FONT_ARIALN = Assets.loadFont("assets/fonts/arialn.ttf", 22)
FONT_ARIALN_TINY = Assets.loadFont("assets/fonts/arialn.ttf", 15)

# # Loading Textures
print("Loading textues...")
RESIZE_SPELL = (50, 50)
RESIZE_EFFECT = (35, 35)
RESIZE_PORTRAIT = (94, 94)

TEXTURE_TEST = Assets.loadImage("assets/test.png")
TEXTURE_TEST_ICON = Assets.loadResizedImage("assets/test.png", RESIZE_SPELL)
TEXTURE_TEST_PORTRAIT = Assets.loadResizedImage("assets/targetframes/portraits/test.png", RESIZE_PORTRAIT)
TEXTURE_HIGHLIGHT = Assets.loadImage("assets/inventory/spellbar/ButtonHilight.png")
TEXTURE_HIGHLIGHTRESIZE = Assets.loadResizedImage("assets/inventory/spellbar/ButtonHilight.png", (52, 52))
TEXTURE_HIGHLIGHTRESIZE_TRANSPARENCY = Assets.loadResizedImage("assets/inventory/spellbar/ButtonHilightTransparency.png", (52, 52))
TEXTURE_UI_GRYPHON = Assets.loadImage("assets/inventory/spellbar/gryphonspelldecoration.png")
TEXTURE_PLAYER = Assets.loadImage("assets/player/human_male.png")

TEXTURE_BACKGROUND_TEST = Assets.loadImage("assets/background/test.png")

TEXTURE_INVENTORY_SPELL_HOLDER = Assets.loadImage("assets/inventory/spellbar/holder.png")
TEXTURE_INVENTORY_SPELL_HOLDER_BORDER = Assets.loadResizedImage("assets/inventory/spellbar/holder_border.png", (48, 50))
TEXTURE_INVENTORY_SPELL_HOLDCLICK = Assets.loadResizedImage("assets/inventory/spellbar/Hold_click.png", (45, 45))

TEXTURE_ICON_SPELL_NOTHING = Assets.loadResizedImage("assets/icons/spells/spell_nothing.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_BASEATTACK = Assets.loadResizedImage("assets/icons/spells/spell_baseattack.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_LIFEDRAIN = Assets.loadResizedImage("assets/icons/spells/spell_lifedrain.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_FIREBALL = Assets.loadResizedImage("assets/icons/spells/spell_fireball.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_CORRUPTION = Assets.loadResizedImage("assets/icons/spells/spell_corruption.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_MANADRAIN = Assets.loadResizedImage("assets/icons/spells/spell_manadrain.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_LIFETAP = Assets.loadResizedImage("assets/icons/spells/spell_lifetap.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_RENEW = Assets.loadResizedImage("assets/icons/spells/spell_renew.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_IMMOLATION = Assets.loadResizedImage("assets/icons/spells/spell_immolation.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_CURSEOFAGONY = Assets.loadResizedImage("assets/icons/spells/spell_curseofagony.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_FLASHHEAL = Assets.loadResizedImage("assets/icons/spells/spell_flashheal.png", RESIZE_SPELL)

TEXTURE_ICON_SPELL_ITEM_MASK = Assets.loadResizedImage("assets/icons/spells/item_mask.png", RESIZE_SPELL)

TEXTURE_ICON_EFFECT_DEBUFF_BURNING = Assets.loadResizedImage("assets/icons/effects/Debuff_Burning.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_CORRUPTION = Assets.loadResizedImage("assets/icons/effects/Debuff_Corruption.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_BLEEDING = Assets.loadResizedImage("assets/icons/effects/Debuff_Bleeding.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_IMMOLATION = Assets.loadResizedImage("assets/icons/effects/Debuff_Immolation.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_CURSEOFAGONY = Assets.loadResizedImage("assets/icons/effects/Debuff_CurseOfAgony.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_BUFF_RENEW = Assets.loadResizedImage("assets/icons/effects/Buff_Renew.png", RESIZE_EFFECT)

TEXTURE_XPBAR_UI = Assets.loadImage("assets/inventory/xpbar/xpbar.png")
TEXTURE_FRAMESTATUES_HP = Assets.loadImage("assets/framestatues/hpbar.png")
TEXTURE_FRAMESTATUES_MANA = Assets.loadImage("assets/framestatues/manabar.png")
TEXTURE_FRAMESTATUES_RAGE = Assets.loadImage("assets/framestatues/ragebar.png")
TEXTURE_FRAMESTATUES_XP = Assets.loadImage("assets/framestatues/xpbar.png")
TEXTURE_FRAME_PLAYER = Assets.loadImage("assets/targetframes/playerframe/player_frame.png")
TEXTURE_FRAME_ENEMY_NORMAL = Assets.loadImage("assets/targetframes/enemyframe/enemy_frame_normal.png")
TEXTURE_FRAME_ENEMY_RARE = Assets.loadImage("assets/targetframes/enemyframe/enemy_frame_rare.png")
TEXTURE_FRAME_ENEMY_RARE_ELITE = Assets.loadImage("assets/targetframes/enemyframe/enemy_frame_rareelite.png")
TEXTURE_FRAME_ENEMY_ELITE = Assets.loadImage("assets/targetframes/enemyframe/enemy_frame_elite.png")
TEXTURE_LEVEL_SKULL = Assets.loadResizedImage("assets/targetframes/high_difficulty_level.png", (24, 24))

TEXTURE_FRAME_PORTRAIT_ANIMAL_WOLF_WHITE = Assets.loadResizedImage("assets/targetframes/portraits/animals/wolf1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_BEAR_BROWN_1 = Assets.loadResizedImage("assets/targetframes/portraits/animals/bear1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_BEAR_BROWN_2 = Assets.loadResizedImage("assets/targetframes/portraits/animals/bear2.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_BEAR_BROWN_3 = Assets.loadResizedImage("assets/targetframes/portraits/animals/bear3.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_BEAR_GREY_1 = Assets.loadResizedImage("assets/targetframes/portraits/animals/bear4.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_BEAR_ZOMBIE_1 = Assets.loadResizedImage("assets/targetframes/portraits/animals/bear5.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_RAPTOR_BLUE = Assets.loadResizedImage("assets/targetframes/portraits/animals/raptor1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_RAT_1 = Assets.loadResizedImage("assets/targetframes/portraits/animals/rat1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_CERBERUS_WHITE = Assets.loadResizedImage("assets/targetframes/portraits/animals/cerberus1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_ANIMAL_SPIDER_BLACK_1 = Assets.loadResizedImage("assets/targetframes/portraits/animals/spider1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_HUMAN_MALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/humanmale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_HUMAN_FEMALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/humanfemale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_NIGHTELF_MALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/nightelfmale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_WORGEN_MALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/worgenmale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_SINDOREI_FEMALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/sindoreifemale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_GNOME_MALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/gnomemale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEFIAS_UNDEAD_MALE_1 = Assets.loadResizedImage("assets/targetframes/portraits/defias/undeadmale1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_SUCCUBUS_1 = Assets.loadResizedImage("assets/targetframes/portraits/demons/succubus1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_SUCCUBUS_2 = Assets.loadResizedImage("assets/targetframes/portraits/demons/succubus2.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_IMP_1 = Assets.loadResizedImage("assets/targetframes/portraits/demons/imp1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_IMP_2 = Assets.loadResizedImage("assets/targetframes/portraits/demons/imp2.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_IMP_3 = Assets.loadResizedImage("assets/targetframes/portraits/demons/imp3.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_IMP_4 = Assets.loadResizedImage("assets/targetframes/portraits/demons/imp4.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_PITLORD_1 = Assets.loadResizedImage("assets/targetframes/portraits/demons/pitlord1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_PITLORD_2 = Assets.loadResizedImage("assets/targetframes/portraits/demons/pitlord2.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_IMPMOTHER_1 = Assets.loadResizedImage("assets/targetframes/portraits/demons/impmother1.png", RESIZE_PORTRAIT)
TEXTURE_FRAME_PORTRAIT_DEMON_INFERNAL_1 = Assets.loadResizedImage("assets/targetframes/portraits/demons/infernal1.png", RESIZE_PORTRAIT)


class Maths:

    @staticmethod
    def between(number, min_value, max_value):
        return number >= min_value and number <= max_value


class Drawable:

    def draw(self, screen):
        pass


class Tickable:

    def tick(self):
        pass


class GameObject(Drawable, Tickable):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVelocity = 0
        self.yVelocity = 0

    def applyVelocity(self, x, y):
        self.xVelocity = x
        self.yVelocity = y

    def resetVelocity(self):
        self.applyVelocity(0, 0)

    def tick(self):
        self.x += self.xVelocity * 0.72
        self.y += self.yVelocity * 0.72


class Item(Drawable):

    def __init__(self, name, texture):
        self.name = name
        self.texture = texture
        self.tooltip = ItemTooltip(self)
        self.tooltip.tooltip_items.append(TooltipData().text(str(name)).color(Q_UNCOMMON))

    def attachTooltip(self, newTooltip):
        self.tooltip = newTooltip
        return self


class SpellItem(Item):

    def __init__(self, spellClass):
        self.spell = globals()[spellClass]()
        Item.__init__(self, str(spellClass), self.spell.icon)
        self.tooltip = SpellTooltip(self)
        self.roundplay = 0

    def triggerUse(self):
        if player.canPlay:
            spellResult = self.spell.use(player, enemy)
            if spellResult == ACTION_SUCCESS:
                self.roundplay = 0
                player.hasPlay = True
            elif spellResult == ACTION_REPLAY:
                self.roundplay += 1
                if self.roundplay < 2:
                    player.hasPlay = False
                else:
                    self.roundplay = 0
                    player.hasPlay = True

            else:
                uiManager.notifyError(SPELL_ERROR_TRADUCTION[spellResult])


class UIComponent(GameObject):

    def __init__(self, x, y, width, height):
        GameObject.__init__(self, x, y)
        self.width = width
        self.height = height
        self.selected = False
        self.shouldDrawBorder = False
        self.shouldDrawOutline = False
        self.outlineColor = RED
        self.outlineDrawOffset = (0, 0, 0, 0)

    def drawBorder(self, enabled):
        self.shouldDrawBorder = enabled
        return self

    def drawOutline(self, color, enabled):
        if color != None:
            self.outlineColor = color
        self.shouldDrawOutline = enabled
        return self

    def outlineOffset(self, x1, y1, x2, y2):
        self.outlineDrawOffset = (x1, y1, x2, y2)
        return self

    def collide(self, x, y):
        self.selected = (self.x <= x and x <= self.x + self.width) and (self.y <= y and y <= self.y + self.height)
        return self.selected

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        pass

    def onClick(self, button, pressed):
        pass

    def drawBorderOn(self, screen):
        pygame.draw.rect(screen, self.outlineColor, (self.x + self.outlineDrawOffset[0], self.y + self.outlineDrawOffset[1], self.width - self.outlineDrawOffset[0] + self.outlineDrawOffset[2], self.height - self.outlineDrawOffset[1] + self.outlineDrawOffset[3]), 1)

    def draw(self, screen):
        if self.shouldDrawBorder or self.shouldDrawOutline:
            self.drawBorderOn(screen)


class UIContainerComponent(UIComponent):

    def __init__(self, x, y, width, height):
        UIComponent.__init__(self, x, y, width, height)
        self.childs = []

    def collide(self, x, y):
        for child in self.childs:
            if child.collide(x, y):
                self.onChildCollided(x, y, child)
        return super().collide(x, y)

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        for child in self.childs:
            child.onScreenResize(newScreenWidth, newScreenHeight)

    def dispatchClickEvent(self, button, pressed):
        for child in self.childs:
            if child.selected:
                self.onChildClick(button, pressed, child)
                child.onClick(button, pressed)

    def onChildClick(self, button, pressed, child):
        pass

    def onChildCollided(self, x, y, child):
        pass

    def tick(self):
        super().tick()
        for child in self.childs:
            child.tick()

    def draw(self, screen):
        super().draw(screen)
        for child in self.childs:
            child.draw(screen)


class Background(UIComponent):

    def __init__(self, x, y, width, height, texture):
        UIComponent.__init__(self, x, y, width, height)
        self.texture = pygame.transform.scale(texture, (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y))


class WindowBackground(UIComponent):

    def __init__(self, texture):
        UIComponent.__init__(self, 0, 0, 0, 0)
        self.originalTexture = texture
        self.texture = None
        self.onScreenResize(-1, -1)

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.texture = pygame.transform.scale(self.originalTexture, (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y))


class Inventory(UIContainerComponent):

    def __init__(self, x, y, width, height, backgroundTexture):
        UIContainerComponent.__init__(self, x, y, width, height)
        self.backgroundTexture = backgroundTexture


class SpellInventory(Inventory):

    def __init__(self, player):
        Inventory.__init__(self, 0, WINDOW_HEIGHT - INVENTORY_SPELL_HEIGHT, WINDOW_WIDTH, INVENTORY_SPELL_HEIGHT, None)
        self.player = player

        for i in range(0, INVENTORY_SPELL_ITEM_COUNT):
            self.childs.append(ItemHolder(0, 0, 48, 46).text(str(i)).texture(TEXTURE_INVENTORY_SPELL_HOLDER))

        self.childs[24].item = SpellItem("BaseAttack")
        self.childs[33].item = SpellItem("EnemyLevelUpDebugAttack")
        self.childs[34].item = SpellItem("LevelUpDebugAttack")
        self.childs[35].item = SpellItem("NothingAttack")

        spells = [
            "FireBallSpell",
            "ImmolationSpell",
            "CorruptionSpell",
            "CurseOfAgonySpell",
            "HealDrainSpell",
            "ManaDrainSpell",
            "LifeTapSpell",
            "RenewHealingSpell",
            "FlashHealHealingSpell"
        ]
        offset = 0

        for i in range(0, min(INVENTORY_SPELL_ITEM_MAX_ROW_COUNT, len(spells))):
            self.childs[offset + 12 + i].item = SpellItem(spells[i])

        self.updateButtons()

    def updateButtons(self):
        offset = (WINDOW_WIDTH - ((INVENTORY_SPELL_ITEM_COUNT / 3) * 49)) / 2
        k = 0
        for i in range(0, int(INVENTORY_SPELL_ITEM_COUNT / INVENTORY_SPELL_ITEM_MAX_ROW_COUNT)):
            for j in range(1, INVENTORY_SPELL_ITEM_MAX_ROW_COUNT + 1):
                holder = self.childs[k]
                holder.x = self.x + ((j - 1) * 49) + offset
                holder.y = self.y - (50 * i) - 20
                k += 1

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        super().onScreenResize(newScreenWidth, newScreenHeight)
        self.y = WINDOW_HEIGHT - INVENTORY_SPELL_HEIGHT
        self.width = WINDOW_WIDTH
        self.updateButtons()

    def draw(self, screen):
        if self.backgroundTexture != None:
            screen.blit(self.backgroundTexture, (self.x, self.y))
        super().draw(screen)


class Text(UIComponent):

    def __init__(self, x, y, text, color):
        UIComponent.__init__(self, x, y, 0, 0)
        self.renderedText = None
        self.textValue = text
        self.textColor = color
        self.textFont = FONT_WOW_TINY
        self.textOffsetY = 0

    def create(self):
        self.text(self.textValue, self.textColor)
        return self

    def color(self, newColor):
        self.textColor = newColor
        return self

    def font(self, newFont):
        self.textFont = newFont
        return self

    def text(self, value, color):
        self.value = value
        self.textColor = color

        self.renderedText = self.textFont.render(value, True, color)
        self.width, self.height = self.textFont.size(value)

        return self

    def draw(self, screen):
        super().draw(screen)
        if self.renderedText != None:
            screen.blit(self.renderedText, (self.x, self.y + self.textOffsetY))


class Button(UIComponent):

    def __init__(self, x, y, width, height):
        UIComponent.__init__(self, x, y, width, height)

    def text(self, buttonText):
        self.buttonText = buttonText
        return self

    def textColor(self, buttonTextColor):
        self.buttonTextColor = buttonTextColor
        return self

    def texture(self, buttonTexture):
        self.buttonTexture = buttonTexture
        return self

    def draw(self, screen):
        super().draw(screen)
        if hasattr(self, 'buttonTexture'):
            screen.blit(self.buttonTexture, (self.x, self.y))
        if hasattr(self, 'buttonText'):
            color = WHITE
            if hasattr(self, 'buttonTextColor'):
                color = self.buttonTextColor
            size = FONT_WOW_TINY.size(str(self.buttonText))
            screen.blit(FONT_WOW_TINY.render(str(self.buttonText), 1, color), (self.x + self.width - size[1], self.y))
        if self.selected:
            screen.blit(TEXTURE_HIGHLIGHTRESIZE_TRANSPARENCY, (self.x - 2, self.y - 2))
            # pygame.draw.rect(screen, (40, 95, 220), (self.x, self.y, self.width, self.height), 2)


class ItemHolder(Button):

    def __init__(self, x, y, width, height):
        Button.__init__(self, x, y, width, height)
        self.item = None
        self.savedTooltip = None
        self.texture(TEXTURE_INVENTORY_SPELL_HOLDER)
        self.maintained = False

    def onClick(self, button, pressed):
        if button == MOUSE_LEFT or button == MOUSE_RIGHT:
            self.maintained = pressed
            if pressed and isinstance(self.item, SpellItem):
                self.item.triggerUse()

        elif button == MOUSE_MIDDLE and pressed:
            self.item = None

    def tick(self):
        if not self.selected and self.maintained:
            self.maintained = False

        if self.item != None and self.item.tooltip != None:
            if self.savedTooltip != self.item.tooltip:
                self.savedTooltip = self.item.tooltip

            if self.item.tooltip in uiManager.tooltips:
                uiManager.tooltips.remove(self.item.tooltip)
            self.item.tooltip.updatePosition(uiManager.mouseX, uiManager.mouseY)
            if self.selected:
                uiManager.tooltips.append(self.item.tooltip)

        if self.savedTooltip != None and self.item == None and self.savedTooltip in uiManager.tooltips:
            uiManager.tooltips.remove(self.savedTooltip)
            self.savedTooltip = None

        if self.item != None:
            self.item.spell.tick()

    def draw(self, screen):
        super().draw(screen)
        if self.item != None:            
            screen.blit(self.item.texture, (self.x, self.y))
            screen.blit(TEXTURE_INVENTORY_SPELL_HOLDER_BORDER, (self.x, self.y))
            if isinstance(self.item, SpellItem) and not self.item.spell.hasEnought(player):
                screen.blit(TEXTURE_ICON_SPELL_ITEM_MASK, (self.x, self.y))
            if self.selected:
                screen.blit(TEXTURE_HIGHLIGHTRESIZE_TRANSPARENCY, (self.x - 2, self.y - 2))
            if self.maintained:
                screen.blit(TEXTURE_INVENTORY_SPELL_HOLDCLICK, (self.x + 2, self.y + 3))
            # x = (w - ww) / 2;
            # y = (h - hh) / 2;


class Tooltip(UIComponent):

    def __init__(self, x, y, width, height):
        UIComponent.__init__(self, x, y, width, height)
        self.tooltip_items = []
        self.displayed = False

    def updatePosition(self, x, y):
        pass


class SpellTooltip(Tooltip):

    def __init__(self, spell_item):
        Tooltip.__init__(self, 0, 0, 0, 0)
        self.spell_item = spell_item

    def render_tooltip(self, screen):
        tooltip_items = self.spell_item.spell.getTooltipData()

        total_height = 0
        max_width = 0

        texts = []
        texts_positions = []

        """
        52 char ~= 485 px [contained] ->> - MARGIN * 2 = 445
        -> 1 char ~= 9.32 px
        
        available spaces:
            - for default window size: 0.25% = 327 px [contained] ->> - MARGIN * 2 = 287
            - for maximized window size: 0.33% = 646 px [contained] ->> - MARGIN * 2 = 606
        """
        line_max_pixel_count = WINDOW_WIDTH * 0.25 - (TOOLTIP_MARGIN * 2)

        for item in tooltip_items:
            remaining_text = item.textValue

            while True:
                cut = remaining_text.split()
                phrase = cut[0] + " "
                index = 0
                max_index = len(cut) - 1

                while item.textFont.size(phrase + cut[index])[0] < line_max_pixel_count and index < max_index:
                    # print("----------")
                    # print("size: " + str(item.textFont.size(phrase + cut[index])[0]))
                    # print("index: " + str(index))
                    # print("cut length: " + str(len(cut)))
                    # print("cut[index]: " + cut[index])
                    # print("index < len(cut): " + str(index < len(cut)))

                    index += 1
                    phrase += cut[index] + " "
                    # print("now phrase:" + str(phrase))
                phrase = phrase[:-1]

                remaining_text = None
                if index < max_index:
                    remaining_text = ""
                    for i in range(index + 1, len(cut)):
                        remaining_text += cut[i] + " "

                    remaining_text = remaining_text[:-1]
                    # print("remaining_text" + remaining_text)

                text = item.textFont.render(phrase, True, item.textColor)
                size = item.textFont.size(phrase)

                texts.append(text)
                texts_positions.append(total_height)
                total_height += size[1]
                if size[0] > max_width:
                    max_width = size[0]

                if remaining_text == None:
                    break

        self.x = WINDOW_WIDTH - 25 - max_width
        self.y = WINDOW_HEIGHT * 0.95 - total_height

        rectangle = (self.x + 8 - TOOLTIP_MARGIN, self.y - 25 - TOOLTIP_MARGIN, max_width + 8 + TOOLTIP_MARGIN, total_height + 8 + TOOLTIP_MARGIN)
        pygame.draw.rect(screen, DARK_BLUE_BACK, rectangle)
        pygame.draw.rect(screen, WHITE, rectangle, 1)

        for i in range(0, len(texts)):
            screen.blit(texts[i], (self.x + 4, self.y - 29 + texts_positions[i]))

    def draw(self, screen):
        self.render_tooltip(screen)


class ItemTooltip(Tooltip):

    def __init__(self, item):
        Tooltip.__init__(self, 0, 0, 32, 32)
        self.item = item

    def updatePosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        totalHeight = 0
        maxWidth = 0

        texts = []
        textsPositions = []

        for tooltipData in self.tooltip_items:
            text = tooltipData.textFont.render(tooltipData.dataText, True, tooltipData.dataColor)
            size = tooltipData.textFont.size(tooltipData.dataText)
            texts.append(text)
            textsPositions.append(totalHeight)
            totalHeight += size[1]
            if size[0] > maxWidth:
                maxWidth = size[0]

        rectangle = (self.x + 8 - TOOLTIP_MARGIN, self.y - 25 - TOOLTIP_MARGIN, maxWidth + TOOLTIP_MARGIN, totalHeight + TOOLTIP_MARGIN)
        # rect = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        # rect.fill((0, 0, 10, 5))
        # screen.blit(rect, (rectangle))
        pygame.draw.rect(screen, DARK_BLUE_BACK, rectangle)
        pygame.draw.rect(screen, WHITE, rectangle, 1)

        for i in range(0, len(texts)):
            screen.blit(texts[i], (self.x + 4, self.y - 29 + textsPositions[i]))


class TooltipData:

    def __init__(self):
        self.textValue = None
        self.textColor = WHITE
        self.textFont = FONT_WOW

    def text(self, textValue):
        self.textValue = textValue
        return self

    def font(self, textFont):
        self.textFont = textFont
        return self

    def color(self, textColor):
        self.textColor = textColor
        return self


class EmptyLineTooltipData(TooltipData):

    def __init__(self):
        TooltipData.__init__(self)
        self.textValue = ""


class TitleTooltipData(TooltipData):

    def __init__(self):
        TooltipData.__init__(self)
        self.textFont = FONT_TOOLTIP_TITLE


class DescriptionTooltipData(TooltipData):

    def __init__(self):
        TooltipData.__init__(self)
        self.textFont = FONT_TOOLTIP_DESCRIPTION


class Bar(UIComponent):

    def __init__(self, x, y, width, height):
        UIComponent.__init__(self, x, y, width, height)


class ModularBar(Bar):

    def __init__(self, x, y, width, height, informationType):
        Bar.__init__(self, x, y, width, height)
        self.informationType = informationType
        self.barColor = RED
        self.barColor2 = GREEN

    def color(self, barColor):
        self.barColor = barColor
        return self

    def color2(self, barColor2):
        self.barColor2 = barColor2
        return self


class LivingEntityModularBar(ModularBar):

    def __init__(self, x, y, width, height, informationType, livingEntity):
        ModularBar.__init__(self, x, y, width, height, informationType)
        self.livingEntity = livingEntity
        self.invalidateCache()

    def isCacheValid(self):
        return self.scaledTextureCache != None and self.scaledTextureContainer != None and self.cachedValue != -1 and self.cachedMaxValue != -1

    def invalidateCache(self):
        self.scaledTextureCache = None
        self.scaledTextureContainer = None
        self.cachedValue = -1
        self.cachedMaxValue = -1

    def draw(self, screen):
        value = 0
        maxValue = 1
        targetTexture = None

        if self.informationType == UI_MODULAR_BAR_INFO_TYPE_HEALTH:
            value = self.livingEntity.health
            maxValue = self.livingEntity.maxHealth
            targetTexture = TEXTURE_FRAMESTATUES_HP
        elif self.informationType == UI_MODULAR_BAR_INFO_TYPE_MANA:
            value = self.livingEntity.mana
            maxValue = self.livingEntity.maxMana
            targetTexture = TEXTURE_FRAMESTATUES_MANA
        elif self.informationType == UI_MODULAR_BAR_INFO_TYPE_EXPERIENCE:
            value = self.livingEntity.experience
            maxValue = self.livingEntity.maxExperience
            targetTexture = TEXTURE_FRAMESTATUES_XP

        if value <= 0:
            value = 0
        if maxValue == 0:
            maxValue = 1

        if self.cachedValue != value or self.cachedMaxValue != maxValue:
            self.invalidateCache()
            self.cachedValue = value
            self.cachedMaxValue = maxValue

        if not self.isCacheValid():
            self.scaledTextureCache = pygame.transform.scale(targetTexture, (int(self.width * (value / maxValue)), self.height - 6))
            self.scaledTextureContainer = pygame.transform.scale(TEXTURE_XPBAR_UI, (self.width, self.height))

        screen.blit(self.scaledTextureCache, (self.x, self.y + 3))

        if self.informationType == UI_MODULAR_BAR_INFO_TYPE_EXPERIENCE:
            screen.blit(self.scaledTextureContainer, (self.x, self.y))

        if self.selected:
            text = Text(0, self.y + 1, str(value) + "/" + str(maxValue), LIGHT_GREY).font(FONT_ARIALN_TINY).create()
            text.x = self.x + ((self.width - text.width) / 2)
            text.textOffsetY = 2
            text.draw(screen)


class BottomLivingEntityExperienceBar(LivingEntityModularBar):

    def __init__(self, livingEntity):
        LivingEntityModularBar.__init__(self, 0, 0, 0, 20, UI_MODULAR_BAR_INFO_TYPE_EXPERIENCE, livingEntity)
        self.onScreenResize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        super().onScreenResize(newScreenWidth, newScreenHeight)
        self.x = int(WINDOW_WIDTH * 0.20)
        self.y = WINDOW_HEIGHT - self.height
        self.width = int(WINDOW_WIDTH * 0.60)
        self.invalidateCache()


class LivingEntityStatusFrame(UIContainerComponent):

    def __init__(self, x, y, frameTexture, livingEntity):
        UIContainerComponent.__init__(self, x, y, 0, 0)
        self.frameTexture = frameTexture
        self.livingEntity = livingEntity

        self.textColor = YELLOW_FRAME_TEXT
        self.portraitOffsetY = 0
        self.iconsEffectOffset = (0, 0)

        self.nameText = Text(0, 0, livingEntity.name, self.textColor).font(FONT_WOW_TINY).create()
        self.healthBar = LivingEntityModularBar(0, 0, 20, 20, UI_MODULAR_BAR_INFO_TYPE_HEALTH, livingEntity)
        self.manaBar = LivingEntityModularBar(0, 0, 20, 20, UI_MODULAR_BAR_INFO_TYPE_MANA, livingEntity)
        self.levelText = Text(0, 0, "", self.textColor).font(FONT_WOW_TINY).create()

        self.childs.append(self.healthBar)
        self.childs.append(self.manaBar)

        self.width, self.height = self.frameTexture.get_rect().size

    def tick(self):
        super().tick()

        if self.textColor != LEVEL_DIFFICULTY_DEAD_SKULL:
            self.levelText.text(str(self.livingEntity.level), self.textColor)

    def draw(self, screen):
        super().draw(screen)
        if self.livingEntity.texture != None:
            textureWidth, textureHeight = self.livingEntity.texture.get_rect().size
            screen.blit(self.livingEntity.texture, (self.x + self.portraitOffsetY + ((94 - textureWidth) / 2), self.y + 28 + ((94 - textureHeight) / 2)))
        screen.blit(self.frameTexture, (self.x, self.y))
        self.nameText.draw(screen)

        if self.textColor == LEVEL_DIFFICULTY_DEAD_SKULL:
            screen.blit(TEXTURE_LEVEL_SKULL, (self.levelText.x + 1, self.levelText.y - 2))
        else:
            self.levelText.draw(screen)

        xOffset = 0
        yOffset = 0
        lineCount = 0
        for effect in self.livingEntity.effects:
            Button(self.x + self.iconsEffectOffset[0] + xOffset, self.y + self.iconsEffectOffset[1] + yOffset, RESIZE_EFFECT[0], RESIZE_EFFECT[1]).texture(effect.texture).draw(screen)

            xOffset += RESIZE_EFFECT[0] * 1.15
            lineCount += 1
            if lineCount % FRAME_EFFECT_MAX_LINE_COUNT == 0:
                lineCount = 0
                xOffset = 0
                yOffset += RESIZE_EFFECT[1] * 1.15


class PlayerEntityStatusFrame(LivingEntityStatusFrame):

    def __init__(self, player):
        LivingEntityStatusFrame.__init__(self, 0, 0, TEXTURE_FRAME_PLAYER, player)
        self.onScreenResize(-1, -1)
        self.healthBar.width = 197
        self.healthBar.height = 22
        self.manaBar.width = 197
        self.manaBar.height = 22
        self.portraitOffsetY = 78
        self.iconsEffectOffset = (182, 113)

    def tick(self):
        super().tick()
        self.updateSize()

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        self.x = int(WINDOW_WIDTH * 0.01)
        self.y = int(WINDOW_HEIGHT * 0.04)
        self.nameText.x = self.x + 180 + ((199 - self.nameText.width) / 2)
        self.nameText.y = self.y + 39 + ((29 - self.nameText.height) / 2)
        self.healthBar.x = self.x + 182
        self.healthBar.y = self.y + 67
        self.manaBar.x = self.x + 182
        self.manaBar.y = self.y + 86
        self.updateSize()

    def updateSize(self):
        self.levelText.x = self.x + 67 + ((43 - self.levelText.width) / 2)
        self.levelText.y = self.y + 89 + ((45 - self.levelText.height) / 2)


class EnemyEntityStatusFrame(LivingEntityStatusFrame):

    def __init__(self, enemy):
        LivingEntityStatusFrame.__init__(self, 0, 0, TEXTURE_FRAME_ENEMY_NORMAL, enemy)
        self.onScreenResize(-1, -1)
        self.healthBar.width = 197
        self.healthBar.height = 22
        self.manaBar.width = 197
        self.manaBar.height = 22
        self.portraitOffsetY = 258
        self.iconsEffectOffset = (51, 113)

    def tick(self):
        super().tick()
        self.updateSize()
        self.updateColorFromLevel()

    def updateColorFromLevel(self):
        if player.level - 6 >= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_TRASH
        elif player.level - 5 <= self.livingEntity.level and player.level - 3 >= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_EASY
        elif player.level - 2 <= self.livingEntity.level and player.level + 2 >= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_NORMAL
        elif player.level + 3 <= self.livingEntity.level and player.level + 4 >= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_MEDIUM
        elif player.level + 5 <= self.livingEntity.level and player.level + 9 >= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_HARD
        elif player.level + 10 <= self.livingEntity.level:
            self.textColor = LEVEL_DIFFICULTY_DEAD_SKULL

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        self.x = int(WINDOW_WIDTH * 0.99) - self.width
        self.y = int(WINDOW_HEIGHT * 0.04)
        self.nameText.x = self.x + 49 + ((199 - self.nameText.width) / 2)
        self.nameText.y = self.y + 39 + ((29 - self.nameText.height) / 2)
        self.healthBar.x = self.x + 51
        self.healthBar.y = self.y + 67
        self.manaBar.x = self.x + 51
        self.manaBar.y = self.y + 86
        self.updateSize()

    def updateSize(self):
        self.levelText.x = self.x + 319 + ((43 - self.levelText.width) / 2)
        self.levelText.y = self.y + 89 + ((45 - self.levelText.height) / 2)


class UIManager(Drawable, Tickable):

    def __init__(self):
        self.components = []
        self.objects = []
        self.tooltips = []
        self.mouseX = -1
        self.mouseY = -1
        self.errorText = None
        self.errorTextComponent = None
        self.errorRemainingTick = 0

    def notifyError(self, error):
        self.errorText = error
        self.errorTextComponent = Text(0, 0, error, RED).create()
        self.errorRemainingTick = ERROR_REMAINING_TICK

    def updateMousePosition(self, x, y):
        self.mouseX = x
        self.mouseY = y
        for tooltip in self.tooltips:
            tooltip.updatePosition(x, y)

    def updateScreenSize(self, newScreenWidth, newScreenHeight):
        for component in self.components:
            component.onScreenResize(newScreenWidth, newScreenHeight)

    def fireMouseButtonEvent(self, event, pressed):
        for component in self.components:
            if component.selected:
                component.onClick(event.button, pressed)
            if isinstance(component, UIContainerComponent):
                component.dispatchClickEvent(event.button, pressed)

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
        for tooltip in self.tooltips:
            tooltip.draw(screen)

        if self.errorTextComponent != None:
            self.errorTextComponent.x = (WINDOW_WIDTH - self.errorTextComponent.width) / 2
            self.errorTextComponent.y = WINDOW_HEIGHT * 0.13
            self.errorTextComponent.draw(screen)

        Text(20, 20, "FPS: " + str(clock.get_fps()), RED).create().draw(screen)

    def tick(self):
        self.errorRemainingTick -= 1
        if self.errorRemainingTick <= 0:
            self.errorTextComponent = None

        for gameObject in self.objects:
            gameObject.tick()
        for component in self.components:
            if self.mouseX != -1 and self.mouseY != -1:
                component.collide(self.mouseX, self.mouseY)
            component.tick()

    def mousePosition(self):
        return (self.mouseX, self.mouseY)


class Entity(GameObject):

    def __init__(self, x, y, health):
        GameObject.__init__(self, x, y)
        self.health = health
        self.maxHealth = health
        self.baseHealth = health

    def offsetHealth(self, offset):
        newHealth = self.health + offset
        if newHealth > self.maxHealth:
            newHealth = self.maxHealth

        self.health = newHealth

    def isDead(self):
        return self.health <= 0


class LivingEntity(Entity):

    def __init__(self, x, y, health, mana, name, level, experience):
        Entity.__init__(self, x, y, health)
        self.mana = mana
        self.maxMana = mana
        self.baseMana = mana
        self.experience = experience
        self.maxExperience = experience
        self.baseExperience = experience
        self.rage = 0
        self.maxRage = 0
        self.baseRage = 0
        self.name = name
        self.level = level
        self.effects = []

    def levelUp(self):
        self.level += 1

    def offsetMana(self, offset):
        newMana = self.mana + offset
        if newMana > self.maxMana:
            newMana = self.maxMana

        self.mana = newMana

    def giveEffect(self, givenEffect):
        correspondingEffect = None
        for effect in self.effects:
            if isinstance(effect, givenEffect.__class__):
                correspondingEffect = effect
                break

        if correspondingEffect != None:
            givenEffect.attachPreviousEffect(correspondingEffect)
            self.effects.remove(correspondingEffect)

        self.effects.append(givenEffect)


class Player(LivingEntity):

    def __init__(self, x, y, health, mana, level, name):
        LivingEntity.__init__(self, x, y, health, mana, name, level, 0)
        self.texture = TEXTURE_TEST_PORTRAIT
        self.canPlay = False
        self.hasPlay = False

    def tick(self):
        if self.experience >= (self.level + 1) * 50:
            self.levelUp()


class Enemy(LivingEntity):

    def __init__(self, x, y, health, level, attack):
        LivingEntity.__init__(self, x, y, health, 0, "Enemy", level, 0)
        self.attackValue = attack
        self.texture = TEXTURE_FRAME_PORTRAIT_DEMON_IMP_1

    def attack(self, player):
        player.health -= self.attackValue * self.level

    # def draw(self, screen):
    #    screen.blit(self.texture, (self.x, self.y));
    #    screen.blit(FONT.render(str("self.name"), 1, (255,255,255)), (self.x, self.y - 10))


class Action(Tickable):

    def __init__(self, icon):
        self.icon = icon
        self.tooltipData = None
        self.cacheTooltip = True
        self.cost = 0
        self.costType = COST_MANA
        self.damage = 0
        self.minDamage = 0
        self.maxDamage = 0
        self.heal = 0
        self.minHealing = 0
        self.maxHealing = 0
        self.debuffMinDamage = 0
        self.debuffMaxDamage = 0
        self.buffMinHealing = 0
        self.buffMaxHealing = 0
        self.amount = 0

    def use(self, player, target):
        return ACTION_SUCCESS

    def hasEnought(self, livingEntity):
        value = 0
        if self.costType == COST_HEALTH:
            value = livingEntity.health
        elif self.costType == COST_MANA:
            value = livingEntity.mana
        elif self.costType == COST_RAGE:
            value = livingEntity.rage
        else:
            raise ValueError("Invalid cost type with id: " + self.costType)

        return self.cost <= value

    def getTooltipData(self):
        if self.tooltipData == None or not self.cacheTooltip:
            self.tooltipData = self.createTooltipData()

        return self.tooltipData

    def createTooltipData(self):
        return [
            TitleTooltipData().text(str(self.__class__.__name__)),
            DescriptionTooltipData().text("This action don't have any custom tooltip tooltip_items attached.").color(RED),
        ]


class Attack(Action):
    pass


class LevelUpDebugAttack(Attack):

    def __init__(self):
        Action.__init__(self, TEXTURE_TEST_ICON)

    def use(self, player, target):
        player.levelUp()
        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("[Debug] Player level up"),
            DescriptionTooltipData().text("Level up the player").color(YELLOW_TEXT),
        ]


class EnemyLevelUpDebugAttack(Attack):

    def __init__(self):
        Action.__init__(self, TEXTURE_TEST_ICON)
        self.cacheTooltip = True

    def use(self, player, target):
        target.levelUp()
        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("[Debug] Enemy level up"),
            DescriptionTooltipData().text("Level up the enemy").color(YELLOW_TEXT)
        ]


class BaseAttack(Attack):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_BASEATTACK)

    def use(self, player, target):
        target.health -= random.randint(3, 5)

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Attack"),
        ]


class NothingAttack(Attack):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_NOTHING)

    def createTooltipData(self):
        return [
            TitleTooltipData().text("[Debug] Do nothing :/"),
            DescriptionTooltipData().text("You have basically do nothing").color(YELLOW_TEXT),
            DescriptionTooltipData().text("Yeah... Noob.").color(YELLOW_TEXT),
        ]


class Spell(Action):
    pass


class LifeTapSpell(Spell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_LIFETAP)
        self.cacheTooltip = False

    def tick(self):
        self.amount = 20  # TODO: Fonction liee au lvl du joueur

    def use(self, player, target):
        player.health -= self.amount
        player.offsetMana(self.amount)

        return ACTION_REPLAY

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Life Tap"),
            DescriptionTooltipData().text("Instant"),
            DescriptionTooltipData().text("Converts " + str(self.amount) + " health into " + str(self.amount) + " mana.").color(YELLOW_TEXT),
        ]


class AttackSpell(Spell):
    pass


class HealingSpell(Spell):
    pass


class RenewHealingSpell(HealingSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_RENEW)
        self.cacheTooltip = False

    def tick(self):
        self.cost = 30  # TODO: Fonction mathematiques a ajouter
        self.amount = 3  # TODO: Fonction mathematiques a ajouter
        self.buffMaxHealing = self.amount * 15  # TODO: Fonction mathematiques a ajouter

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost

        player.giveEffect(RenewRegenBuffEffect(self))

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Renew"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Heals you of " + str(self.buffMaxHealing) + " damage over 15sec.").color(YELLOW_TEXT)
        ]


class FlashHealHealingSpell(HealingSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_FLASHHEAL)
        self.cacheTooltip = False

    def tick(self):
        self.cost = 35  # TODO: Ajouter la vraie fonction plus tard
        self.minHealing = 54  # TODO: Ajouter la vraie fonction plus tard
        self.maxHealing = 67  # TODO: Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost
        rand = random.randint(self.minHealing, self.maxHealing)
        player.offsetHealth(rand)

        return ACTION_REPLAY

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Flash Heal"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Instant"),
            DescriptionTooltipData().text("Heals you for " + str(self.minHealing) + " to " + str(self.maxHealing) + ".").color(YELLOW_TEXT)
        ]


class HealDrainSpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_LIFEDRAIN)
        self.cacheTooltip = False

    def tick(self):
        self.cost = 17  # TODO: Ajouter la vraie fonction plus tard
        self.minDamage = 3  # TODO: Ajouter la vraie fonction plus tard
        self.maxDamage = int(self.minDamage * 5)  # TODO: Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost
        rand = random.randint(1, 6)
        if rand > 5:
            rand = 5
        damage = int(self.minDamage * rand)
        target.health -= damage
        player.offsetHealth(damage)

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Heal Drain"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Transfers between " + str(self.minDamage) + " and " + str(self.maxDamage) + " health from the target to the caster.").color(YELLOW_TEXT),
        ]


class ManaDrainSpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_MANADRAIN)
        self.cacheTooltip = False

    def tick(self):
        self.cost = 19  # TODO: Ajouter la vraie fonction plus tard
        self.minHealing = 8  # TODO: Ajouter la vraie fonction plus tard
        self.maxHealing = int(self.minHealing * 5)  # TODO: Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost
        rand = random.randint(1, 6)
        if rand > 5:
            rand = 5
        amount = int(self.minHealing * rand)
        drain = target.mana
        if drain >= amount:
            drain = amount

        player.offsetMana(drain)
        target.mana -= drain

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Mana Drain"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Drain between 6 and 30 mana point from your target.").color(YELLOW_TEXT)
        ]


class FireBallSpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_FIREBALL)
        self.cacheToolTip = False

    def tick(self):
        self.cost = 30  # TODO : Ajouter la vraie fonction plus tard
        self.minDamage = 14  # TODO : Ajouter la vraie fonction plus tard
        self.MaxDamage = 23  # TODO : Ajouter la vraie fonction plus tard
        self.debuffMaxDamage = 2  # TODO : Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost
        rand = random.randint(self.minDamage, self.MaxDamage)
        target.health -= rand

        target.giveEffect(BurningDebuffEffect(self))

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Fireball"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Hurls a fiery ball that causes " + str(self.minDamage) + " to " + str(self.MaxDamage) + " Fire damage and an").color(YELLOW_TEXT),
            DescriptionTooltipData().text("additional " + str(self.debuffMaxDamage) + " Fire damage over 4sec.").color(YELLOW_TEXT),
        ]


class CorruptionSpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_CORRUPTION)
        self.cacheToolTip = False

    def tick(self):
        self.cost = 35  # TODO : Ajouter la vraie fonction plus tard
        self.amount = 10  # TODO : Ajouter la vraie fonction plus tard
        self.debuffMaxDamage = self.amount * 4  # TODO : Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost

        target.giveEffect(CorruptionDebuffEffect(self))

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Corruption"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Corrupts the target, causing " + str(self.debuffMaxDamage) + " Shadow damage over 12sec.").color(YELLOW_TEXT)
        ]


class ImmolationSpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_IMMOLATION)
        self.cacheToolTip = False

    def tick(self):
        self.cost = 25  # TODO : Ajouter la vraie fonction plus tard
        self.damage = 8  # TODO : Ajouter la vraie fonction plus tard
        self.amount = 4  # TODO : Ajouter la vraie fonction plus tard
        self.debuffMaxDamage = self.amount * 5  # TODO : Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost

        target.health -= self.damage

        target.giveEffect(ImmolationDebuffEffect(self))

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Immolation"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Burns the enemy for " + str(self.damage) + " Fire damage and then an additional " + str(self.debuffMaxDamage) + " Fire").color(YELLOW_TEXT),
             DescriptionTooltipData().text("damage over 15sec.").color(YELLOW_TEXT)
        ]


class CurseOfAgonySpell(AttackSpell):

    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_CURSEOFAGONY)
        self.cacheToolTip = False

    def tick(self):
        self.cost = 25  # TODO : Ajouter la vraie fonction plus tard
        self.debuffMinDamage = 7  # TODO : Ajouter la vraie fonction plus tard
        self.debuffMaxDamage = self.debuffMinDamage * 12  # TODO : Ajouter la vraie fonction plus tard

    def use(self, player, target):
        if not self.hasEnought(player):
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= self.cost

        target.giveEffect(CurseOfAgonyDebuffEffect(self))

        return ACTION_SUCCESS

    def createTooltipData(self):
        return [
            TitleTooltipData().text("Curse of Agony"),
            DescriptionTooltipData().text("Mana : " + str(self.cost)),
            DescriptionTooltipData().text("Curses the target with agony, causing " + str(self.debuffMaxDamage) + " Shadow damage over 24sec. This damage is dealt slowly at first, and builds up as the Curse reaches its full duration. Only one Curse can be active on any one target.").color(YELLOW_TEXT)
        ]


class GameLogic(Drawable, Tickable):

    def __init__(self, player):
        self.player = player
        self.gameObjects = []
        self.isPlayerRound = True
        self.hasPreviousRoundEnd = True
        self.remainingEnemyRound = []
        self.disabledEntitiesForRound = []

    def handle(self):
        if self.hasPreviousRoundEnd:
            self.hasPreviousRoundEnd = False

            for livingEntity in self.gameObjects:
                if isinstance(livingEntity, LivingEntity):
                    self.handleEffects(livingEntity)

        if self.isPlayerRound:
            if self.player not in self.disabledEntitiesForRound:
                self.handlePlayerRound(self.player)

            self.remainingEnemyRound = []
            for enemy in self.gameObjects:
                if isinstance(enemy, Enemy) and enemy not in self.disabledEntitiesForRound:
                    self.remainingEnemyRound.append(enemy)

        else:
            if self.player.hasPlay and len(self.remainingEnemyRound) > 0:
                self.handleEnemyRound(self.remainingEnemyRound[0])
                if len(self.remainingEnemyRound) == 0:
                    self.isPlayerRound = True
                    self.hasPreviousRoundEnd = True

        self.removeDeadEntities()

    def handlePlayerRound(self, player):
        player.canPlay = True
        player.hasPlay = False
        self.isPlayerRound = False

    def handleEnemyRound(self, target):
        self.remainingEnemyRound.remove(target)
        target.attack(self.player)

    def handleEffects(self, livingEntity):
        for effect in livingEntity.effects:
            canEntityMove = effect.execute(livingEntity)

            if not canEntityMove:
                self.disabledEntitiesForRound.append(livingEntity)

            if effect.hasEnded:
                livingEntity.effects.remove(effect)

    def removeDeadEntities(self):
        for entity in self.gameObjects:
            if isinstance(entity, Entity) and entity.isDead():
                self.gameObjects.remove(entity)
        for entity in self.remainingEnemyRound:
            if entity.isDead():
                self.remainingEnemyRound.remove(entity)

    def draw(self, screen):
        for gameObject in self.gameObjects:
            gameObject.draw(screen)


class BaseEffect(Drawable):

    def __init__(self, texture):
        self.texture = texture
        self.hasEnded = False
        self.previousEffect = None

    def attachPreviousEffect(self, effect):
        self.previousEffect = effect
        self.onPreviousEffectAttached(effect)
        return self

    def onPreviousEffectAttached(self, effect):
        pass

    def execute(self, livingEntity):
        return True

    def endEffect(self):
        self.hasEnded = True


class TimedEffect(BaseEffect):

    def __init__(self, texture, remaingTime):
        BaseEffect.__init__(self, texture)
        self.remaingTime = remaingTime
        self.minDamage = 0
        self.maxDamage = 0
        self.minHealing = 0
        self.maxHealing = 0
        self.amount = 0

    def finishExecute(self):
        self.remaingTime -= 1
        if self.remaingTime <= 0:
            self.endEffect()


class BuffEffect(TimedEffect):
    pass


class RenewRegenBuffEffect(BuffEffect):

    def __init__(self, renewHealingSpell):
        BuffEffect.__init__(self, TEXTURE_ICON_EFFECT_BUFF_RENEW, 15)
        self.amount = renewHealingSpell.amount

    def execute(self, livingEntity):
        livingEntity.offsetHealth(self.amount)

        self.finishExecute()
        return True


class DebuffEffect(TimedEffect):
    pass


class BurningDebuffEffect(DebuffEffect):

    def __init__(self, fireBallSpell):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_BURNING, 4)
        self.damageDelay = 0
        self.maxDebuffDamage = fireBallSpell.debuffMaxDamage / 2

    def execute(self, livingEntity):
        self.damageDelay += 1
        if self.damageDelay == 2:
            livingEntity.health -= self.maxDebuffDamage  # TODO: Fonction maths...
        elif self.damageDelay == 4:
            livingEntity.health -= self.maxDebuffDamage  # TODO: Fonction maths...
            self.damageDelay = 0

        self.finishExecute()
        return True


class ImmolationDebuffEffect(DebuffEffect):

    def __init__(self, immolationSpell):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_IMMOLATION, 15)
        self.damageDelay = 0
        self.amount = immolationSpell.amount

    def execute(self, livingEntity):
        self.damageDelay += 1
        if self.damageDelay == 3:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 6:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 9:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 12:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 15:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
            self.damageDelay = 0

        self.finishExecute()
        return True


class CorruptionDebuffEffect(DebuffEffect):

    def __init__(self, corruptionDebuffEffect):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_CORRUPTION, 12)
        self.damageDelay = 0
        self.amount = corruptionDebuffEffect.amount

    def execute(self, livingEntity):
        self.damageDelay += 1
        if self.damageDelay == 3:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 6:
            livingEntity.health -= self.amount  # TODO: Fonction maths...
        elif self.damageDelay == 9:
            livingEntity.health -= self.amount
        elif self.damageDelay == 12:
            livingEntity.health -= self.amount
            self.damageDelay = 0

        self.finishExecute()
        return True


class CurseOfAgonyDebuffEffect(DebuffEffect):

    def __init__(self, curseOfAgonySpell):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_CURSEOFAGONY, 24)
        self.curseStackDamage = curseOfAgonySpell.debuffMinDamage
        self.curseMaxDamage = curseOfAgonySpell.debuffMaxDamage
        self.damageDelay = 0  # TODO: Faire que si Curse of Agony est relancer par dessus son debuff encore actif, qu'il ne reprenne pas damageDelay = 0 mais garde sa précédente valeur

    def onPreviousEffectAttached(self, effect):
        self.damageDelay += 2

    def execute(self, livingEntity):
        self.damageDelay += 1
        if self.damageDelay == 2:
            livingEntity.health -= self.curseStackDamage - 2
        if self.damageDelay == 4:
            livingEntity.health -= self.curseStackDamage - 2
        if self.damageDelay == 6:
            livingEntity.health -= self.curseStackDamage - 1
        if self.damageDelay == 8:
            livingEntity.health -= self.curseStackDamage - 1
        if self.damageDelay == 10:
            livingEntity.health -= self.curseStackDamage
        if self.damageDelay == 12:
            livingEntity.health -= self.curseStackDamage
        if self.damageDelay == 14:
            livingEntity.health -= self.curseStackDamage
        if self.damageDelay == 16:
            livingEntity.health -= self.curseStackDamage
        if self.damageDelay == 18:
            livingEntity.health -= self.curseStackDamage + 1
        if self.damageDelay == 20:
            livingEntity.health -= self.curseStackDamage + 1
        if self.damageDelay == 22:
            livingEntity.health -= self.curseStackDamage + 2
        if self.damageDelay >= 24:
            livingEntity.health -= self.curseStackDamage + 2

        self.finishExecute()
        return True


uiManager = UIManager()
player = Player(75, 600, 100 , 100, 1, "Hero")
gameLogic = GameLogic(player)
enemy = Enemy(50, 50, 100, 1, 5)

gameLogic.gameObjects.append(player)
gameLogic.gameObjects.append(enemy)

# uiManager.components.append(Button(50, 50, 60, 60).text("warp").texture(TEXTURE_TEST))
# uiManager.components.append(Text(100, 300, "J'aime la glace'o'chocolat", RED).create())
# uiManager.components.append(WindowBackground(TEXTURE_BACKGROUND_TEST))
uiManager.components.append(SpellInventory(player))
uiManager.components.append(BottomLivingEntityExperienceBar(player))
uiManager.components.append(PlayerEntityStatusFrame(player))
uiManager.components.append(EnemyEntityStatusFrame(enemy))

# uiManager.notifyError("Ceci est une erreur")


def loop():
    uiManager.tick()

    gameLogic.handle()

    gameLogic.draw(screen)
    uiManager.draw(screen)


def afterLoop():
    if not enemy.isDead():
        Text(50, 350, "Enemy: " + str(enemy.health) + "/" + str(enemy.maxHealth), RED).create().draw(screen)
        Text(200, 350, "mana: " + str(enemy.mana) + "/" + str(enemy.maxMana), WHITE).create().draw(screen)
    else:
        Text(50, 350, "Enemy is dead (actual: " + str(enemy.health) + ")", RED).create().draw(screen)

    if not player.isDead():
        Text(50, 400, "Player: " + str(player.health) + "/" + str(player.maxHealth), RED).create().draw(screen)
        Text(200, 400, "mana: " + str(player.mana) + "/" + str(player.maxMana), WHITE).create().draw(screen)
    else:
        Text(50, 400, "Player is dead (actual: " + str(player.health) + ")", RED).create().draw(screen)


def handleEvent(event):
    if event.type == pygame.MOUSEMOTION:
        uiManager.updateMousePosition(event.pos[0], event.pos[1])
    elif event.type == pygame.MOUSEBUTTONDOWN:
        uiManager.fireMouseButtonEvent(event, True)
    elif event.type == pygame.MOUSEBUTTONUP:
        uiManager.fireMouseButtonEvent(event, False)
    elif event.type == pygame.VIDEORESIZE:
        uiManager.updateScreenSize(event.w, event.h)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            pass
        elif event.key == pygame.K_LEFT:
            player.applyVelocity(-5, 0)
        elif event.key == pygame.K_RIGHT:
            player.applyVelocity(5, 0)
    elif event.type == pygame.KEYUP:
        player.resetVelocity()


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, 32)
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE, 32)
                WINDOW_WIDTH = event.w
                WINDOW_HEIGHT = event.h
            handleEvent(event)
    screen.fill(BLACK)
    loop()
    afterLoop()
    pygame.display.flip()
    clock.tick(GAME_TICK)

pygame.quit()
