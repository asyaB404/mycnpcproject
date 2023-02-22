import time

can_buy_count = [12, 7, 6, 5]  # 必填
cooling_time = 300
text = "1"


def init(e):
    e.npc.tempdata.put("cooling_time", time.time())
    for id in range(len(can_buy_count)):
        e.npc.storeddata.put("slot" + str(id) + "count", can_buy_count[id])


def tick(e):
    if time.time() >= e.npc.tempdata.get("cooling_time"):
        for id in range(len(can_buy_count)):
            e.npc.storeddata.put("slot" + str(id) + "count", can_buy_count[id])
        e.npc.tempdata.put("cooling_time", time.time() + cooling_time)


def interact(e):
    p = e.player
    p.tempdata.put("npc_shop", e.npc)
    global text
    text = "1"
    if p.tempdata.get("wallet") is not None and e.player.getInventory().count(
            e.player.world.createItem("customnpcs:scripted_item", 0, 1), True, True) == 1:
        for item in e.player.getInventory().getItems():
            if u"钱币袋" in item.getDisplayName():
                open_shop_buy_gui(e)
                break
    else:
        p.message(u"需要背包里有个钱袋才能交易")


def customGuiButton(e):
    p = e.player
    g = e.gui
    if e.buttonId == 102:
        if g.getID() == 4:
            open_shop_buy_gui(e)
        elif g.getID() == 3:
            open_shop_sell_gui(e)

    if 100 <= e.buttonId <= 101:
        text = g.getComponent(210).getText()
        count = 1
        if text is not None:
            if text.isdigit() and int(text) > 0:
                count = int(text)
            else:
                g.getComponent(210).setText("1")
                p.message(u"请输入合法数字")
            if e.buttonId == 100:
                if count > 1:
                    g.getComponent(210).setText(str(count - 1))
            elif e.buttonId == 101:
                g.getComponent(210).setText(str(count + 1))
        p.showCustomGui(g)
        g.updateComponent(g.getComponent(210))
    g.update(p)


def customGuiSlot(e):
    p = e.player
    g = e.gui
    npc = p.tempdata.get("npc_shop")
    s = npc.storeddata
    id = e.slotId
    item = e.stack
    if g.getID() == 3:
        if 60 <= id <= 95:
            for id in range(36):
                if 0 <= id <= 8:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60].getStack())
                elif 9 <= id <= 17:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60 + 18].getStack())
                elif 18 <= id <= 26:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60].getStack())
                elif 27 <= id <= 35:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60 - 18].getStack())
        if p.getGamemode() == 1:
            if "new" in item.getDisplayName():
                item.setCustomName(item.getDisplayName()[3:])
                g.getSlots()[id].setStack(item)
                s.put("slot" + str(id), e.stack.getItemNbt().toJsonString())
                p.message(u"创建成功")
            elif "remove" in item.getDisplayName():
                s.remove("slot" + str(id))
                p.message(u"删除成功")
            # else:
            #     p.dropItem(e.stack.copy())
            #     e.stack.setStackSize(0)


def customGuiSlotClicked(e):
    p = e.player
    g = e.gui
    npc = p.tempdata.get("npc_shop")
    wallet = p.tempdata.get("wallet")
    s = npc.storeddata
    id = e.slotId
    if g.getID() == 3:
        if 0 <= id <= 59:
            item = e.stack
            all_lore = item.getLore()
            if all_lore:
                for i, lore in enumerate(all_lore):
                    if u"§5价格" in lore:
                        global text
                        text = g.getComponent(210).getText()
                        if g.getComponent(210).getText() is not None:
                            if text.isdigit() and int(text) > 0:
                                count = int(text)
                                if count > s.get("slot" + str(id) + "count") or e.clickType == "QUICK_MOVE":
                                    count = s.get("slot" + str(id) + "count")
                                price = description_to_coins(lore) * count
                                if wallet.storeddata.get("coins") >= price:
                                    p.world.playSoundAt(p.pos, "minecraft:entity.arrow.hit_player", 2, 1.25)
                                    wallet.storeddata.put("coins", wallet.storeddata.get("coins") - price)
                                    s.put("slot" + str(id) + "count", s.get("slot" + str(id) + "count") - count)
                                    item0 = item.copy()
                                    p.message(u"你购买了:" + str(count) + u"个{}".format(item.getDisplayName()))
                                    item0.setStackSize(int(count))
                                    p.message(u"该物品剩余库存数:" + str(s.get("slot" + str(id) + "count")))
                                    setItemLore(item0, i,
                                                coins_to_description(description_to_coins(lore) / 4))
                                    item.setStackSize(int(s.get("slot" + str(id) + "count")))
                                    p.dropItem(item0).setPickupDelay(1)
                                else:
                                    p.message(u"钱币不足")
            # p.updatePlayerInventory()
            g.update(p)
            if p.getMainhandItem().getName() != "customnpcs:npcscripter":
                e.setCanceled(True)
                open_shop_buy_gui(e)
        elif 60 <= id <= 95:
            for id in range(36):
                if 0 <= id <= 8:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60].getStack())
                elif 9 <= id <= 17:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60 + 18].getStack())
                elif 18 <= id <= 26:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60].getStack())
                elif 27 <= id <= 35:
                    p.getInventory().setSlot(id, g.getSlots()[id + 60 - 18].getStack())
    if g.getID() == 4:
        item = e.stack
        all_lore = item.getLore()
        if all_lore:
            for lore in all_lore:
                if u"§5价格" in lore:
                    count = 1
                    if e.clickType == "QUICK_MOVE":
                        count = item.getStackSize()
                    price = description_to_coins(lore) * count
                    p.world.playSoundAt(p.pos, "minecraft:entity.arrow.hit_player", 2, 1.25)
                    wallet.storeddata.put("coins", wallet.storeddata.get("coins") + price)
                    p.message(
                        u"你出售了:" + str(count) + u"个{}".format(item.getDisplayName()) + u",得到了{}".format(
                            coins_to_description(price, 1)))
                    item.setStackSize(int(item.getStackSize() - count))
                    p.getInventoryHeldItem().setStackSize(int(p.getInventoryHeldItem().getStackSize() - count))
        if p.getMainhandItem().getName() != "customnpcs:npcscripter":
            open_shop_sell_gui(e)
            e.setCanceled(True)


def open_shop_sell_gui(e):
    p = e.player
    g = e.API.createCustomGui(4, 480, 250, False)
    id = 0
    for y in range(4):
        for x in range(9):
            g.addTexturedRect(id, "minecraft:textures/gui/container/inventory.png", (x * 18) - 40 + 600 // 4,
                              (-y * 18) + 140 + 160 // 4, 19, 19, 6, 82)
            g.addItemSlot((x * 18) - 40, (-y * 18) + 140)
            id += 1
    for id in range(36):
        if 0 <= id <= 8:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id))
        elif 9 <= id <= 17:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id + 18))
        elif 18 <= id <= 26:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id))
        elif 27 <= id <= 35:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id - 18))
    g.addButton(102, u"§q§l出售物品", 320 // 4, 400 // 4, 45, 20)
    g.addLabel(400, generate_coins_description(p.tempdata.get("wallet"), 1), 10, 20, 80, 20)
    g.addLabel(401, u"§q点击背包里的物品来出售", 125, 100, 160, 20)
    g.addLabel(402, u"§q同时按住shift来出售一组", 125, 110, 160, 20)
    g.update(p)
    p.showCustomGui(g)


def open_shop_buy_gui(e):
    p = e.player
    npc = p.tempdata.get("npc_shop")
    s = npc.storeddata
    g = e.API.createCustomGui(3, 480, 250, False)
    id = 0
    for y in range(6):
        for x in range(10):
            g.addTexturedRect(id, "minecraft:textures/gui/container/inventory.png", (x * 18) + 140 + 600 // 4,
                              (y * 18) + 60 + 160 // 4, 19, 19, 6, 82)
            g.addItemSlot((x * 18) + 140, (y * 18) + 60)
            id += 1
    for y in range(4):
        for x in range(9):
            g.addTexturedRect(id, "minecraft:textures/gui/container/inventory.png", (x * 18) - 40 + 600 // 4,
                              (-y * 18) + 140 + 160 // 4, 19, 19, 6, 82)
            g.addItemSlot((x * 18) - 40, (-y * 18) + 140)
            id += 1
    for id in range(60, 96):
        if 60 <= id <= 68:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id - 60))
        elif 69 <= id <= 77:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id + 18 - 60))
        elif 78 <= id <= 86:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id - 60))
        elif 87 <= id <= 95:
            g.getSlots()[id].setStack(p.getInventory().getSlot(id - 18 - 60))
    g.addButton(100, u"§q§l-", 792 // 4, 452 // 4, 25, 12)
    g.addButton(101, u"§q§l+", 892 // 4, 452 // 4, 25, 12)
    g.addButton(102, u"§q§l购买物品", 320 // 4, 400 // 4, 45, 20)
    global text
    g.addTextField(210, 218, 105, 16, 8).setText(text)
    g.addLabel(400, generate_coins_description(p.tempdata.get("wallet"), 1), 10, 20, 80, 20)
    g.addLabel(401, u"§q购买     个", 200, 100, 60, 20)
    g.addLabel(402, u"§q按住shift点击商品来购买一组", 290, 210, 140, 20)
    for id in range(60):
        if s.get("slot" + str(id)) is not None and "minecraft:air" not in s.get("slot" + str(id)):
            item = p.world.createItemFromNbt(e.API.stringToNbt(s.get("slot" + str(id))))
            if s.get("slot" + str(id) + "count") > item.getMaxStackSize():
                item.setStackSize(item.getMaxStackSize())
            else:
                item.setStackSize(int(s.get("slot" + str(id) + "count")))
            g.getSlots()[id].setStack(item)
    g.update(p)
    p.showCustomGui(g)


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


def description_to_coins(str):
    coins = 0
    for i in [u"§f", u"§6", u"§7", u"§4"]:
        i0 = str.index(i)
        i0 += 1
        c0 = ""
        while str[i0 + 1] != u"●":
            c0 += str[i0 + 1]
            i0 += 1
        if c0.isdigit():
            if i == u"§f":
                coins += int(c0) * 64 ** 3
            elif i == u"§6":
                coins += int(c0) * 64 ** 2
            elif i == u"§7":
                coins += int(c0) * 64
            elif i == u"§4":
                coins += int(c0)
    return coins


def coins_to_description(coins, args=0):
    varcoins = coins
    coin0 = 0
    coin1 = 0
    coin2 = 0
    coin3 = 0
    if varcoins >= 64 ** 3:
        coin3 = int(varcoins // 64 ** 3)
        varcoins %= 64 ** 3
    if varcoins >= 64 ** 2:
        coin2 = int(varcoins // 64 ** 2)
        varcoins %= 64 ** 2
    if varcoins >= 64:
        coin1 = int(varcoins // 64)
        varcoins %= 64
    if varcoins > 0:
        coin0 = int(varcoins)
    s = u"§5价格：§f{}●§6{}●§7{}●§4{}●".format(coin3, coin2, coin1, coin0)
    if args == 1:
        s = u"§f{}●§6{}●§7{}●§4{}●".format(coin3, coin2, coin1, coin0)
    return s


def getItemLore(item, line):
    arr = item.getLore()
    if line >= 0:
        if line < len(arr):
            if arr[line] is not None:
                return arr[line]


def setItemLore(item, line, str):
    arr = item.getLore()
    if line < len(arr):
        arr[line] = str
        item.setLore(arr)
