from database.DBTable import DBTable
from commands.wrappers import aesthetic_discord


class ItemIndex:
    def __init__(self):
        self._item_index = DBTable("items")
        self.items = self._item_index.getTable()
        return


class Inventory:
    _iIndex = ItemIndex()
    page_len = 10

    def __init__(self, player_id):
        self._inventoryTable = DBTable('inventory')
        self.inv_items = self._inventoryTable.getEntries(playerID=player_id)

    @aesthetic_discord.box
    def getItem(self, item_number) -> str:
        item = self._iIndex.items[self.inv_items[item_number - 1].itemID - 1]

        return f"{item.iName} ({item.iRarity}): \n{item.iDesc} "

    @aesthetic_discord.box
    def getInvPage(self, page_number) -> str:
        retstr = ""

        at_position = page_number * self.page_len
        for itemindex in range(at_position, at_position + self.page_len):
            if itemindex >= len(self.inv_items):
                break

            itemrow = self.inv_items[itemindex]
            item = self._iIndex.items[itemrow.itemID - 1]

            retstr = retstr + str(itemindex + 1) + ". " + \
                     item.iName + " (" + item.iRarity + ")x" + str(itemrow.quantity) + "\n"

        if len(self.inv_items) == 0:
            retstr = "Non hai oggetti nell'inventario. è ora di grindare!"

        return retstr

    def addItem(self, item_id):
        self._inventoryTable.addEntry(["playerID", "itemID"], [self.userdata.playerID, item_id])
        self.inv_items = self._inventoryTable.getEntries(playerID=self.userdata.playerID)