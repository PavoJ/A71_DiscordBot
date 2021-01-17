from database.DBTable import DBTable
from commands.wrappers import aesthetic_discord


class Player:
    def __init__(self, player_id):
        self._inventoryTable = DBTable('inventory')
        self.inventory = self._inventoryTable.getEntries(playerID=player_id)
        self.pagelen = 10

        self._userTable = DBTable('player')
        self.userdata = self._userTable.getEntry(playerID=player_id)

        # todo: load the item index in a static way, so more players access the same index
        self._item_index = DBTable("items")
        self._items = self._item_index.getTable()
        '''
        itemcnt = 0
        for ID, name, desc, rarity, value in self._item_index.getTable():
            self._items.append({"ID": ID, "name": name, "desc": desc, "rarity": rarity, "value": value})
            itemcnt = itemcnt + 1'''

        if self.userdata is None:
            self._userTable.addEntry(["playerID"], [player_id])
            self.userdata = self._userTable.getEntry(playerID=player_id)

    def addXP(self, qnt):
        self._userTable.changeEntry("playerID", self.userdata.playerID, "xp", self.userdata.xp + qnt)
        self.userdata = self._userTable.getEntry(playerID=self.userdata.playerID)

    def addItem(self, item_id):
        self._inventoryTable.addEntry(["playerID", "itemID"], [self.userdata.playerID, item_id])
        self.inventory = self._inventoryTable.getEntries(playerID=self.userdata.playerID)

    @aesthetic_discord.box
    def getItem(self, item_number) -> str:
        item = self._items[self.inventory[item_number - 1].itemID]

        return f"{item.name} ({item.rarity}): \n{item.desc} "

    @aesthetic_discord.box
    def getInvPage(self, page_number) -> str:
        retstr = ""

        at_position = page_number * self.pagelen
        for itemindex in range(at_position, at_position + self.pagelen):
            if itemindex >= len(self.inventory):
                break

            itemrow = self.inventory[itemindex]
            item = self._items[itemrow.itemID-1]

            retstr = retstr + str(itemindex + 1) + ". " + \
                item["name"] + " (" + item["rarity"] + ")" + "\n"

        if len(self.inventory) == 0:
            retstr = "Non hai oggetti nell'inventario. è ora di grindare!"

        return retstr

    '''
    @aesthetic_discord.box
    def getInv(self) -> str:

        retstr = ""
        itemcnt = 1
        
        retstr = getInvPage

        if retstr == "":
            return "non hai oggetti nel tuo inventario. è ora di grindare!"

        return retstr'''
