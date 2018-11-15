import pygame
import os 
import sys 
import time 
import random

# the Pygame docs say size(text) -> (width, height)

# PYGAME
MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

# SPELL ERROR
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

# GAME
WINDOW_TITLE = "RPG"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_TICK = 60
TOOLTIP_MARGIN = 8
INVENTORY_SPELL_HEIGHT = 50
INVENTORY_SPELL_ITEM_MAX_ROW_COUNT = 12
INVENTORY_SPELL_ITEM_COUNT = 36
ERROR_REMAINING_TICK = 60 * 5

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
LEVEL_DIFFICULTY_NORMAL = (255, 255, 255)
LEVEL_DIFFICULTY_MEDIUM = (224, 114, 57)
LEVEL_DIFFICULTY_HARD = (255, 26, 26)


pygame.init()

FONT = pygame.font.Font(None,30)
FONT_WOW_TINY = pygame.font.Font("assets/fonts/frizquad.ttf",15)
FONT_WOW = pygame.font.Font("assets/fonts/frizquad.ttf",20)
FONT_WOW_VERY_TINY = pygame.font.Font("assets/fonts/frizquad.ttf",10)
FONT_ARIALN = pygame.font.Font("assets/fonts/arialn.ttf",22)
FONT_ARIALN_TINY = pygame.font.Font("assets/fonts/arialn.ttf",15)

# CACHE
ASSETS_CACHE = {}

class Assets:
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

RESIZE_SPELL = (50, 50)
RESIZE_EFFECT = (30, 30)

TEXTURE_TEST = Assets.loadImage("assets/test.png")
TEXTURE_TEST_PORTRAIT = Assets.loadResizedImage("assets/targetframes/portraits/test.png", (94, 94))
TEXTURE_HIGHLIGHT = Assets.loadImage("assets/inventory/spellbar/ButtonHilight.png")
TEXTURE_HIGHLIGHTRESIZE = Assets.loadResizedImage("assets/inventory/spellbar/ButtonHilight.png", (52, 52))
TEXTURE_HIGHLIGHTRESIZE_TRANSPARENCY = Assets.loadResizedImage("assets/inventory/spellbar/ButtonHilightTransparency.png", (52, 52))
TEXTURE_UI_GRYPHON = Assets.loadImage("assets/inventory/spellbar/gryphonspelldecoration.png")
TEXTURE_PLAYER = Assets.loadImage("assets/player/human_male.png")
TEXTURE_ICON_SPELL_NOTHING = Assets.loadResizedImage("assets/icons/spells/spell_nothing.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_BASEATTACK = Assets.loadResizedImage("assets/icons/spells/spell_baseattack.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_LIFEDRAIN = Assets.loadResizedImage("assets/icons/spells/spell_lifedrain.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_FIREBALL = Assets.loadResizedImage("assets/icons/spells/spell_fireball.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_CORRUPTION = Assets.loadResizedImage("assets/icons/spells/spell_corruption.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_MANADRAIN = Assets.loadResizedImage("assets/icons/spells/spell_manadrain.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_LIFETAP = Assets.loadResizedImage("assets/icons/spells/spell_lifetap.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_HOLYHANDS = Assets.loadResizedImage("assets/icons/spells/spell_holyhands.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_IMMOLATION = Assets.loadResizedImage("assets/icons/spells/spell_immolation.png", RESIZE_SPELL)
TEXTURE_ICON_SPELL_CURSEOFAGONY = Assets.loadResizedImage("assets/icons/spells/spell_curseofagony.png", RESIZE_SPELL)
TEXTURE_INVENTORY_SPELL_HOLDER = Assets.loadImage("assets/inventory/spellbar/holder.png")
TEXTURE_INVENTORY_SPELL_HOLDER_BORDER = Assets.loadResizedImage("assets/inventory/spellbar/holder_border.png", (48, 50))
TEXTURE_INVENTORY_SPELL_HOLDCLICK = Assets.loadResizedImage("assets/inventory/spellbar/Hold_click.png", (45, 45))
TEXTURE_ICON_EFFECT_DEBUFF_BURNING = Assets.loadResizedImage("assets/icons/effects/Debuff_Burning.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_CORRUPTION = Assets.loadResizedImage("assets/icons/effects/Debuff_Corruption.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_BLEEDING = Assets.loadResizedImage("assets/icons/effects/Debuff_Bleeding.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_IMMOLATION = Assets.loadResizedImage("assets/icons/effects/Debuff_Immolation.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_DEBUFF_CURSEOFAGONY = Assets.loadResizedImage("assets/icons/effects/Debuff_CurseOfAgony.png", RESIZE_EFFECT)
TEXTURE_ICON_EFFECT_BUFF_REGEN = Assets.loadResizedImage("assets/icons/effects/Buff_Regen.png", RESIZE_EFFECT)
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
        self.tooltip.data.append(TooltipData().text(str(name)).color(Q_UNCOMMON))

    def attachTooltip(self, newTooltip):
        self.tooltip = newTooltip
        return self

class SpellItem(Item):
    def __init__(self, spellClass):
        self.spell = globals()[spellClass]()
        Item.__init__(self, str(spellClass), self.spell.icon)
    
    def triggerUse(self):
        if player.canPlay:
            spellResult = self.spell.use(player, enemy)
            if spellResult == ACTION_SUCCESS:                
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

    def drawBorder(self, enabled):
        self.shouldDrawBorder = enabled
        return self

    def collide(self, x, y):
        self.selected = (self.x <= x and x <= self.x + self.width) and (self.y <= y and y <= self.y + self.height)
        return self.selected

    def onScreenResize(self, newScreenWidth, newScreenHeight):
        pass

    def onClick(self, button, pressed):
        pass

    def draw(self, screen):
        if self.shouldDrawBorder:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height), 1)

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
        self.childs[34].item = SpellItem("LevelUpAttack")
        self.childs[35].item = SpellItem("NothingAttack")
        
        spells = [
            "FireBallSpell",
            "ImmolationSpell",
            "CorruptionSpell",
            "CurseOfAgonySpell",
            "HealDrainSpell",
            "ManaDrainSpell",
            "LifeTapSpell",
            "HolyHandsHealingSpell"
        ]
        offset = 0

        for i in range(0, min(INVENTORY_SPELL_ITEM_MAX_ROW_COUNT, len(spells))):
            self.childs[offset + 12 + i].item = SpellItem(spells[i])

        self.updateButtons()

    def updateButtons(self):
        offset = (WINDOW_WIDTH - ((INVENTORY_SPELL_ITEM_COUNT/3) * 49)) / 2
        k = 0                                                                    
        for i in range(0, int(INVENTORY_SPELL_ITEM_COUNT / INVENTORY_SPELL_ITEM_MAX_ROW_COUNT)):
            for j in range(1, INVENTORY_SPELL_ITEM_MAX_ROW_COUNT + 1):
                holder = self.childs[k]
                holder.x = self.x + ((j - 1) * 49) + offset
                holder.y = self.y - (50 * i) - 20
                k+= 1
    
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
            #pygame.draw.rect(screen, (40, 95, 220), (self.x, self.y, self.width, self.height), 2)

class ItemHolder(Button):
    def __init__(self, x, y, width, height):
        Button.__init__(self, x, y, width, height)
        self.item = None
        self.texture(TEXTURE_INVENTORY_SPELL_HOLDER)
        self.maintained = False
    
    def onClick(self, button, pressed):
        if button == MOUSE_LEFT or button == MOUSE_RIGHT:
            self.maintained = pressed
            if pressed and isinstance(self.item, SpellItem):
                self.item.triggerUse()
                
        elif button == MOUSE_MIDDLE and pressed:
            if self.item == None:
                rand = random.randint(0,3)
                print(str(rand))
                if rand == 0:
                    self.item = SpellItem("FireBallSpell")
                elif rand == 1:
                    self.item = SpellItem("HealDrainSpell")
                elif rand == 2:
                    self.item = SpellItem("NothingAttack")   
                elif rand == 3:
                    self.item = SpellItem("BaseAttack")  
                 
                #self.item = Item("Epée magique", TEXTURE_ICON_SPELL_LIFEDRAIN)
            else:
                self.item = None

    def tick(self):
        if not self.selected and self.maintained:
            self.maintained = False

    def draw(self, screen):
        super().draw(screen)
        if self.item != None:
            screen.blit(self.item.texture, (self.x, self.y))
            screen.blit(TEXTURE_INVENTORY_SPELL_HOLDER_BORDER, (self.x, self.y))
            if self.selected:
                screen.blit(TEXTURE_HIGHLIGHTRESIZE_TRANSPARENCY, (self.x - 2, self.y - 2))
            if self.maintained:
                screen.blit(TEXTURE_INVENTORY_SPELL_HOLDCLICK, (self.x + 2, self.y + 3))
            if self.item.tooltip != None:
                if self.selected:
                    uiManager.tooltips.append(self.item.tooltip)
                else:
                    if self.item.tooltip in uiManager.tooltips:
                        uiManager.tooltips.remove(self.item.tooltip)
            #x = (w - ww) / 2;
            #y = (h - hh) / 2;

class Tooltip(UIComponent):
    def __init__(self, x, y, width, height):
        UIComponent.__init__(self, x, y, width, height)
        self.data = []
        self.displayed = False

class SpellTooltip(Tooltip):
    def __init__(self):
        Tooltip.__init__(self, 0, 0, 200, 300)
    def draw(self, screen):
        self.x = WINDOW_WIDTH * 0.8
        self.y = WINDOW_HEIGHT * 0.8

        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        screen.blit(FONT_WOW.render("Ceci est un test", 1, YELLOW_TEXT), (self.x, self.y))

class ItemTooltip(Tooltip):
    def __init__(self, item):
        Tooltip.__init__(self, 0, 0, 32, 32)
        self.item = item
    
    def draw(self, screen):
        totalHeight = 0
        maxWidth = 0

        texts = []
        textsPositions = []

        for tooltipData in self.data:                                                
            text = FONT_WOW.render(tooltipData.dataText, True, tooltipData.dataColor)
            size = FONT_WOW.size(tooltipData.dataText)
            texts.append(text)
            textsPositions.append(totalHeight)
            totalHeight += size[1]
            if size[0] > maxWidth:
                maxWidth = size[0]                                    

        rectangle = (self.x + 8 - TOOLTIP_MARGIN, self.y - 25 - TOOLTIP_MARGIN, maxWidth + TOOLTIP_MARGIN, totalHeight + TOOLTIP_MARGIN)
        #rect = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        #rect.fill((0, 0, 10, 5))
        #screen.blit(rect, (rectangle))
        pygame.draw.rect(screen, DARK_BLUE_BACK, rectangle)
        pygame.draw.rect(screen, WHITE, rectangle, 1)
        
        for i in range(0, len(texts)):
            screen.blit(texts[i], (self.x + 4, self.y - 29 + textsPositions[i]))

class TooltipData:
    def __init__(self):
        self.dataText = None
        self.dataColor = None

    def text(self, dataText):
        self.dataText = dataText
        return self

    def color(self, dataColor):
        self.dataColor = dataColor   
        return self

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

        self.nameText = Text(0, 0, livingEntity.name, self.textColor).font(FONT_WOW_TINY).create()
        self.healthBar = LivingEntityModularBar(0, 0, 20, 20, UI_MODULAR_BAR_INFO_TYPE_HEALTH, livingEntity)
        self.manaBar = LivingEntityModularBar(0, 0, 20, 20, UI_MODULAR_BAR_INFO_TYPE_MANA, livingEntity)
        self.levelText = Text(0, 0, "", self.textColor).font(FONT_WOW_TINY).create()
        
        self.childs.append(self.healthBar)
        self.childs.append(self.manaBar)

        self.width, self.height = self.frameTexture.get_rect().size

    def tick(self):
        super().tick()
        self.levelText.text(str(self.livingEntity.level), self.textColor)

    def draw(self, screen):
        super().draw(screen)
        if self.livingEntity.texture != None:
            textureWidth, textureHeight = self.livingEntity.texture.get_rect().size
            screen.blit(self.livingEntity.texture, (self.x + 78 + ((94 - textureWidth) / 2), self.y + 28 + ((94 - textureHeight) / 2)))
        screen.blit(self.frameTexture, (self.x, self.y))
        self.nameText.draw(screen)
        self.levelText.draw(screen)
        
class PlayerEntityStatusFrame(LivingEntityStatusFrame):
    def __init__(self, player):
        LivingEntityStatusFrame.__init__(self, 0, 0, TEXTURE_FRAME_PLAYER, player)
        self.onScreenResize(-1, -1)
        self.healthBar.width = 197
        self.healthBar.height = 22
        self.manaBar.width = 197
        self.manaBar.height = 22
    
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
            tooltip.x = x
            tooltip.y = y

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
        if self.errorTextComponent != None:
            self.errorTextComponent.x = (WINDOW_WIDTH - self.errorTextComponent.width) / 2
            self.errorTextComponent.y = WINDOW_HEIGHT * 0.13
            self.errorTextComponent.draw(screen)

        for component in self.components:
            component.draw(screen)
        for tooltip in self.tooltips:
            tooltip.draw(screen)

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
    def __init__(self, x, y, health, mana, level, experience):
        Entity.__init__(self, x, y, health)
        self.mana = mana
        self.maxMana = mana
        self.baseMana = mana
        self.experience = experience
        self.maxExperience = experience
        self.baseExperience = experience
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
        LivingEntity.__init__(self, x, y, health, mana, level, 0)
        self.name = name
        self.texture = TEXTURE_TEST_PORTRAIT
        self.canPlay = False
        self.hasPlay = False

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y));
        screen.blit(FONT.render(str(self.name), 1, (255,255,255)), (self.x, self.y - 10))

    def tick(self):
        if self.experience >= (self.level + 1) * 50:
            levelUp()

class Enemy(LivingEntity):
    def __init__(self, x, y, health, level, attack):
        LivingEntity.__init__(self, x, y, health, 0, level, 0)
        self.attackValue = attack
        self.texture = TEXTURE_PLAYER

    def attack(self, player):
        player.health -= self.attackValue * self.level

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y));
        screen.blit(FONT.render(str("self.name"), 1, (255,255,255)), (self.x, self.y - 10))

class Action:
    def __init__(self, icon):
        self.icon = icon

    def use(self, player, target):
        return ACTION_SUCCESS

class Attack(Action):
    pass

class BaseAttack(Attack):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_BASEATTACK)

    def use(self, player, target):
        target.health -= random.randint(3,5)

        return ACTION_SUCCESS

class NothingAttack(Attack):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_NOTHING)

    def use(self, player, target):

        damage = 0
        target.health -= damage

        return ACTION_SUCCESS  

class LevelUpAttack(Attack):
    def __init__(self):
        Action.__init__(self, TEXTURE_TEST)

    def use(self, player, target):
        player.levelUp()
        return ACTION_SUCCESS  
     
class Spell(Action):
    pass

class LifeTapSpell(Spell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_LIFETAP)

    def use(self, player, target):

        player.health -= 20
        player.offsetMana(20)

        return ACTION_SUCCESS  

class AttackSpell(Spell):
    pass

class HealingSpell(Spell):
    pass
                                  
class HolyHandsHealingSpell(HealingSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_HOLYHANDS)

    def use(self, player, target):
        if player.mana < 18:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 18
        player.giveEffect(HolyHandsRegenBuffEffect())                        
        return ACTION_SUCCESS

class HealDrainSpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_LIFEDRAIN)

    def use(self, player, target):
        if player.mana < 17:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.offsetMana(-17) #Multiplié par 1.15^(playerlever-1) --- 1.15 = pourcentage à ajuster
        damage = random.randint(12,18)
        target.health -= damage
        player.offsetHealth(damage)

        return ACTION_SUCCESS

class ManaDrainSpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_MANADRAIN)

    def use(self, player, target):
        if player.mana < 12:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 12
        manaamount = random.randint(1,5)
        if manaamount == 1:
            manadrainamount = 6
        if manaamount == 2:
            manadrainamount = 12
        if manaamount == 3:
            manadrainamount = 18
        if manaamount == 4:
            manadrainamount = 24
        if manaamount == 5:
            manadrainamount = 30

        drain = target.mana
        if drain >= manadrainamount:
            drain = manadrainamount

        player.offsetMana(drain)
        target.mana -= drain

        return ACTION_SUCCESS

class FireBallSpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_FIREBALL)

    def use(self, player, target):
        if player.mana < 24:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 24 #same as lifedrain
        damage = random.randint(22, 26)
        target.health -= damage

        if random.randint(1,3) == random.randint(1,3):
            target.giveEffect(BurningDebuffEffect())
        return ACTION_SUCCESS

class CorruptionSpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_CORRUPTION)

    def use(self, player, target):
        if player.mana < 15:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 15 #same as lifedrain
        target.giveEffect(CorruptionDebuffEffect())

        return ACTION_SUCCESS

class ImmolationSpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_IMMOLATION)

    def use(self, player, target):
        if player.mana < 15:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 15 #same as lifedrain
        target.health -= random.randint(6,8)
        target.giveEffect(ImmolationDebuffEffect())

        return ACTION_SUCCESS

class CurseOfAgonySpell(AttackSpell):
    def __init__(self):
        Action.__init__(self, TEXTURE_ICON_SPELL_CURSEOFAGONY)
    
    def use(self, player, target):
        if player.mana < 12:
            return SPELL_ERROR_REASON_NOT_ENOUGHT_MANA

        player.mana -= 12 #same as lifedrain
        target.giveEffect(CurseOfAgonyDebuffEffect())

        return ACTION_SUCCESS

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

    def finishExecute(self):
        self.remaingTime -= 1
        if self.remaingTime <= 0:
            self.endEffect()

class BuffEffect(TimedEffect):
    pass

class HolyHandsRegenBuffEffect(BuffEffect):
    def __init__(self):
        BuffEffect.__init__(self, TEXTURE_ICON_EFFECT_BUFF_REGEN, 10)

    def execute(self, livingEntity):
        livingEntity.offsetHealth(4)

        self.finishExecute()
        return True

class DebuffEffect(TimedEffect):
    pass

class BurningDebuffEffect(DebuffEffect):
    def __init__(self):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_BURNING, random.randint(3,5))

    def execute(self, livingEntity):
        livingEntity.health -= random.randint(2,3) # multiplié par le level ou un truc du genre

        self.finishExecute()
        return True        

class ImmolationDebuffEffect(DebuffEffect):
    def __init__(self):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_IMMOLATION, 6)

    def execute(self, livingEntity):
        livingEntity.health -= 2 # multiplié par le level ou un truc du genre

        self.finishExecute()
        return True      

class CorruptionDebuffEffect(DebuffEffect):
    def __init__(self):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_CORRUPTION, 15)

    def execute(self, livingEntity):
        livingEntity.health -= 3 # multiplié par le level ou un truc du genre

        self.finishExecute()
        return True

class CurseOfAgonyDebuffEffect(DebuffEffect):
    def __init__(self):
        DebuffEffect.__init__(self, TEXTURE_ICON_EFFECT_DEBUFF_CURSEOFAGONY, 6)
        self.curseDamage = 0

    def onPreviousEffectAttached(self, effect):
        add = 2
        if self.curseDamage >= 12:
            add = 0
        
        self.curseDamage = effect.curseDamage + add

    def execute(self, livingEntity):
        if self.curseDamage < 12:
            self.curseDamage += 2
        
        livingEntity.health -= self.curseDamage

        self.finishExecute()
        return True
        

uiManager = UIManager()
player = Player(75, 600, 100 , 100, 1, "Hero")
gameLogic = GameLogic(player)
enemy = Enemy(50, 50, 100, 1, 5)

gameLogic.gameObjects.append(player)
gameLogic.gameObjects.append(enemy)

#uiManager.components.append(Button(50, 50, 60, 60).text("warp").texture(TEXTURE_TEST))
#uiManager.components.append(Text(100, 300, "J'aime la glace'o'chocolat", RED).create())
uiManager.components.append(SpellInventory(player))
uiManager.components.append(BottomLivingEntityExperienceBar(player))
uiManager.components.append(PlayerEntityStatusFrame(player))

uiManager.notifyError("C'est une erreur")

def loop():
    uiManager.tick()

    if not enemy.isDead():
        Text(50, 350, "Enemy: " + str(enemy.health) + "/"+ str(enemy.maxHealth), RED).create().draw(screen)
        Text(200, 350, "mana: " + str(enemy.mana) + "/"+ str(enemy.maxMana), WHITE).create().draw(screen)
    else:
        Text(50, 350, "Enemy is dead (actual: " + str(enemy.health) + ")", RED).create().draw(screen)
        
    if not player.isDead():
        Text(50, 400, "Player: " + str(player.health) + "/"+ str(player.maxHealth), RED).create().draw(screen)     
        Text(200, 400, "mana: " + str(player.mana) + "/"+ str(player.maxMana), WHITE).create().draw(screen)    
    else:
        Text(50, 400, "Player is dead (actual: " + str(player.health) + ")", RED).create().draw(screen)
    
    gameLogic.handle()
    
    gameLogic.draw(screen)
    uiManager.draw(screen)

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
    pygame.display.flip()
    clock.tick(GAME_TICK)
 
pygame.quit()