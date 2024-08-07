import math

LvNeedExp = [10]

for i in range(1, 5 + 1):
    LvNeedExp.append(20)
for i in range(5, 10 + 1):
    LvNeedExp.append(50)


def interact(e):
    if e.player.getMainhandItem().getDisplayName() == "666":
        e.player.storeddata.put("displayExp", 0)
        e.player.storeddata.put("trueExp", 0)
        e.player.storeddata.put("trueLv", 0)


def init(e):
    e.player.timers.forceStart(114514, 1, True)


def timer(e):
    if e.id == 114514:
        prevent_npe(e.player, "displayExp")
        prevent_npe(e.player, "trueExp")
        prevent_npe(e.player, "trueLv")
        if e.player.storeddata.get("displayExp") < getEXP(e.player):
            FAKEgetExpEvent(e.player, getEXP(e.player) - e.player.storeddata.get("displayExp"), e)
            e.player.storeddata.put("displayExp", getEXP(e.player))


def FAKEgetExpEvent(player, vault, e):
    storeddata = player.getStoreddata()
    exp = storeddata.get("trueExp")
    lvl = storeddata.get("trueLv")
    storeddata.put("trueExp", exp + vault)
    if exp >= LvNeedExp[int(lvl)]:
        while exp >= LvNeedExp[int(lvl)]:
            exp -= LvNeedExp[int(lvl)]
            lvl += 1
    player.setExpLevel(-1)
    player.setExpLevel(int(lvl))
    num = exp / (LvNeedExp[int(lvl)])
    player.getMCEntity().func_71023_q(int(math.floor(player.getMCEntity().func_71050_bK() * num)))  # 给予玩家经验
    player.message(str(lvl) + "  " + str(exp))


def getEXP(player):
    return player.getMCEntity().field_71067_cb


def ExptoLevel(exp):
    if exp <= 315:
        return math.floor(math.sqrt((exp + 9)) - 3.0)
    elif 315 < exp <= 1395:
        return math.floor(math.sqrt((40 * exp - 7839)) / 10.0 + 8.1)
    else:
        return math.floor((math.sqrt((72 * exp - 54215)) + 325.0) / 18.0)


def LeveltoExp(level):
    if level <= 16:
        return math.pow(level, 2) + 6 * level
    elif 16 < level <= 31:
        return 2.5 * math.pow(level, 2) + 40.5 * level
    elif level >= 32:
        return 4.5 * math.pow(level, 2) + 162.5 * level


def prevent_npe(target, name, count=0):
    if target.storeddata.get(name) is None:
        target.storeddata.put(name, count)
        return True
    return False
