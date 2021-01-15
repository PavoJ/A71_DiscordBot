from DBTable import DBTable
from commands.wrappers import aesthetic_discord


class Player:
    def __init__(self, player_id):
        self._inventoryTable = DBTable('inventory')
        self.inventory = self._inventoryTable.getEntries(playerID=player_id)
        self.pagelen = 10

        self._userTable = DBTable('player')
        self.userdata = self._userTable.getEntry(playerID=player_id)

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
        item_index = DBTable("items")
        item = item_index.getEntry(ID=self.inventory[item_number - 1].itemID)

        return f"{item.name} ({item.rarity}): \n{item.desc} "

    @aesthetic_discord.box
    def getInvPage(self, page_number) -> str:
        items = DBTable("items")
        retstr = ""

        at_position = page_number * self.pagelen
        for itemindex in range(at_position, at_position+self.pagelen):
            if itemindex >= len(self.inventory):
                break

            itemrow = self.inventory[itemindex]
            item = items.getEntry(ID=itemrow.itemID)

            retstr = retstr + str(itemindex + 1) + ". " + \
                    item.name + " (" + item.rarity + ")" + "\n"

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
