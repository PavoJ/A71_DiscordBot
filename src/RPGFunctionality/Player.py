from RPGFunctionality.Inventory import Inventory
from database.DBTable import DBTable
from commands.wrappers import aesthetic_discord


class Player:

    def __init__(self, player_id):
        self.inventory = Inventory(player_id)

        self._userTable = DBTable('userdata')
        self.userdata = self._userTable.getEntry(userID=player_id)

        if self.userdata is None:
            self._userTable.addEntry(["userID"], [player_id])
            self.userdata = self._userTable.getEntry(userID=player_id)

    def add_xp(self, qnt):
        self._userTable.changeEntry("userID", self.userdata.playerID, "xp", self.userdata.xp + qnt)
        self.userdata = self._userTable.getEntry(playerID=self.userdata.playerID)