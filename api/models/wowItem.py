class Item:
    def __init__(self, id = 1, name = "nome", level = 1, quality_id = 1, quality = 1, class_id = 1, class_name = "Warrior", subclass_id = 1, subclass_name = "Tank", icon_display_id = 1, icon_url = "", inventory_slot_id = 1):
        self.id = id
        self.name = name
        self.level = level
        self.quality = quality
        self.class_name = class_name
        self.subclass_name = subclass_name
        self.inventory_slot_id = inventory_slot_id
        self.icon_url = icon_url
        self.quality_id = quality_id
        self.class_id = class_id
        self.subclass_id = subclass_id
        self.icon_display_id = icon_display_id
