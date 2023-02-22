def customGuiSlotClicked(e):
    if 0 <= e.slotId <= 6:
        if e.clickType == "THROW" or e.dragType == 1 or e.clickType == "QUICK_CRAFT":
            e.setCanceled(True)

    if e.clickType == "PICKUP_ALL":
        e.setCanceled(True)


def customGuiSlot(e):
    p = e.player
    si = e.slotId
    s = p.storeddata

    def try_put(id):
        l = []
        for x in range(0, 7):
            if s.get("slot" + str(x)) != "0" and "minecraft:air" not in s.get("slot" + str(x)):
                l.append(p.world.createItemFromNbt(e.API.stringToNbt(s.get("slot" + str(x)))).getDisplayName())
            else:
                l.append("0")
        if si == id:
            if (u"饰品" in getItemLore(e.stack,
                                       0) or e.stack.getName() == "minecraft:air") and e.stack.getDisplayName() not in l and \
                    e.stack.getStackSize() < 2:
                s.put("slot" + str(id), e.stack.getItemNbt().toJsonString())
            else:
                p.message(u"该物品不是饰品或已装备同名饰品")
                p.dropItem(e.stack.copy()).setPickupDelay(1)
                e.stack.setStackSize(0)

    for i in range(0, 7):
        try_put(i)


def keyPressed(e):
    if e.key == 15 and e.isShiftPressed == True:
        def open_gui():
            p = e.player
            s = p.storeddata
            g = e.API.createCustomGui(1, 480, 250, False)
            g.addTexturedRect(0, "minecraft:textures/gui/container/inventory.png", 576 // 4, 664 // 4, 256, 86, 0, 80)
            g.addTexturedRect(1, "minecraft:textures/gui/container/inventory.png", 600 // 4, 576 // 4, 128, 19, 6, 82)
            if p.tempdata.get("wallet"):
                g.addLabel(400, generate_coins_description(p.tempdata.get("wallet"), 1), 10, 20, 80, 20)
            g.showPlayerInventory(0, 128)
            for x in range(0, 7):
                prevent_npe(p, "slot" + str(x), "0")
                if "minecraft:air" in s.get("slot" + str(x)) or s.get("slot" + str(x)) == "0":
                    g.addItemSlot(x * 18, 104)
                else:
                    g.addItemSlot(x * 18, 104, p.world.createItemFromNbt(e.API.stringToNbt(s.get("slot" + str(x)))))
            p.showCustomGui(g)

        open_gui()


def prevent_npe(target, name, count=0):
    if target.storeddata.get(name) is None:
        target.storeddata.put(name, count)


def getItemLore(item, line):
    arr = item.getLore()
    if line < len(arr):
        if arr[line] is not None:
            return arr[line]
    return "0"


def generate_coins_description(item, arg=0):
    varcoins = item.storeddata.get("coins")
    s0 = u"§q白铁币:0枚"
    s1 = u"§6青铜币:0枚"
    s2 = u"§7黑石币:0枚"
    s3 = u"§4红木币:0枚"
    if varcoins >= 64 ** 3:
        coin3 = int(varcoins // 64 ** 3)
        s0 = u"§q白铁币:{}枚".format(coin3)
        varcoins %= 64 ** 3
    if varcoins >= 64 ** 2:
        coin2 = int(varcoins // 64 ** 2)
        s1 = u"§6青铜币:{}枚".format(coin2)
        varcoins %= 64 ** 2
    if varcoins >= 64:
        coin1 = int(varcoins // 64)
        s2 = u"§7黑石币:{}枚".format(coin1)
        varcoins %= 64
    if varcoins > 0:
        coin0 = int(varcoins)
        s3 = u"§4红木币:{}枚".format(coin0)
    if arg == 0:
        return u"§7其内含有:" + s0 + " " + s1 + " " + s2 + " " + s3
    return s0 + "\n" + s1 + "\n" + s2 + "\n" + s3
