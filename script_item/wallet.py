def tick(e):
    if e.player.getInventory().count(e.player.world.createItem("customnpcs:scripted_item", 0, 1), True, True) > 1:
        c = 0
        for item in e.player.getInventory().getItems():
            if u"钱币袋" in item.getDisplayName():
                c += 1
                if c > 1:
                    e.player.dropItem(item.copy()).setPickupDelay(200)
                    item.setStackSize(0)
                    c -= 1

    def put(name, multiple):
        if e.player.getInventory().count(e.player.world.createItem(name, 0, 1), True, True) > 0:
            e.item.storeddata.put("coins", e.item.storeddata.get("coins") + e.player.getInventory().count(
                e.player.world.createItem(name, 0, 1), True, True) * multiple)
            for item in e.player.getInventory().getItems():
                if item.getName() == name:
                    item.setStackSize(0)

    if e.player.storeddata.get("auto_collet_coins") == 1:
        put("variedcommodities:coin_wood", 1)
        put("variedcommodities:coin_stone", 64)
        put("variedcommodities:coin_bronze", 64 * 64)
        put("variedcommodities:coin_iron", 64 ** 3)
    setItemLore(e.item, 0, generate_coins_description(e.item))
    e.player.tempdata.put("wallet", e.item)


def interact(e):
    # e.player.message(str(e.item.storeddata.get("coins")))

    def open_wgui():
        g = e.API.createCustomGui(2, 480, 250, False)
        g.addTexturedRect(0, "minecraft:textures/gui/container/inventory.png", 576 // 4, 664 // 4, 256, 86, 0, 80)
        g.showPlayerInventory(0, 128)
        g.addButton(100, u"设置是否自动将背包里的钱币装入袋子", 576 // 4, 570 // 4, 155, 20)
        g.addButton(101, u"§q白铁币", 60 // 4, 300 // 4, 25, 10)
        g.addButton(102, u"§6青铜币", 60 // 4, 348 // 4, 25, 10)
        g.addButton(103, u"§7黑石币", 60 // 4, 396 // 4, 25, 10)
        g.addButton(104, u"§4红木币", 60 // 4, 444 // 4, 25, 10)
        g.addButton(105, u"§q白铁币", 60 // 4 + 60, 300 // 4, 25, 10)
        g.addButton(106, u"§6青铜币", 60 // 4 + 60, 348 // 4, 25, 10)
        g.addButton(107, u"§7黑石币", 60 // 4 + 60, 396 // 4, 25, 10)
        g.addButton(108, u"§4红木币", 60 // 4 + 60, 444 // 4, 25, 10)
        g.addButton(109, u"§q取出全部", 240 // 4, 80 // 4, 38, 20)
        g.addButton(110, u"§q存入全部", 400 // 4, 80 // 4, 38, 20)
        g.addButton(111, u"堆叠钱币", 1280 // 4, 900 // 4, 38, 20)
        g.addTextField(200, 28, 65, 16, 8).setText("1")
        g.addTextField(201, 88, 65, 16, 8).setText("1")
        g.addLabel(400, generate_coins_description(e.player.tempdata.get("wallet"), 1), 10, 20, 80, 20)
        g.addLabel(401, u"§q取出     枚", 10, 60, 60, 20)
        g.addLabel(402, u"§q存入     枚", 70, 60, 60, 20)
        e.player.showCustomGui(g)

    open_wgui()


def customGuiButton(e):
    p = e.player
    wallet = p.tempdata.get("wallet")
    g = p.getCustomGui()
    if g.getID() == 2:
        def single_put(name, amount, multiple=1, message=u"钱币不足!"):
            if e.player.getInventory().count(e.player.world.createItem(name, 0, 1), True, True) >= multiple:
                wallet.storeddata.put("coins", wallet.storeddata.get("coins") + amount * multiple)
                for item in p.getInventory().getItems():
                    if item.getName() == name:
                        item.setStackSize(int(item.getStackSize() - multiple))
                        break
            else:
                p.message(message)

        def extract(name, amount, multiple=1, message=u"钱币不足!"):
            if wallet.storeddata.get("coins") >= amount * multiple:
                is_give = p.giveItem(name, 0, multiple)
                wallet.storeddata.put("coins", wallet.storeddata.get("coins") - amount * multiple)
                if not is_give:
                    p.dropItem(p.world.createItem(name, 0, multiple))
            else:
                if message != "":
                    p.message(message)

        def try_stack_all():
            def try_stack(name, name1):
                if item.getName() == name:
                    is_give = p.giveItem(name1, 0, 1)
                    item.setStackSize(0)
                    if not is_give:
                        p.dropItem(p.world.createItem(name1, 0, 1))

            for item in p.getInventory().getItems():
                if "coin" in item.getName():
                    if item.getStackSize() >= 64:
                        try_stack("variedcommodities:coin_wood", "variedcommodities:coin_stone")
                        try_stack("variedcommodities:coin_stone", "variedcommodities:coin_bronze")
                        try_stack("variedcommodities:coin_bronze", "variedcommodities:coin_iron")

        if e.buttonId == 100:
            if p.storeddata.get("auto_collet_coins") == 0 or p.storeddata.get("auto_collet_coins") is None:
                p.storeddata.put("auto_collet_coins", 1)
                p.message(u"已开启自动将背包里的钱币装入袋子")
            else:
                p.storeddata.put("auto_collet_coins", 0)
                p.message(u"已关闭自动将背包里的钱币装入袋子")
        elif 101 <= e.buttonId <= 104 or e.buttonId == 109:
            if p.storeddata.get("auto_collet_coins") == 1:
                p.message(u"已关闭自动将背包里的钱币装入袋子")
                p.storeddata.put("auto_collet_coins", 0)
            if g.getComponent(200).getText() is not None:
                if g.getComponent(200).getText().isdigit():
                    count = int(g.getComponent(200).getText())
                    if count > 64:
                        g.getComponent(200).setText("64")
                        count = 64
                    if e.buttonId == 101:
                        extract("variedcommodities:coin_iron", 64 ** 3, count)
                    elif e.buttonId == 102:
                        extract("variedcommodities:coin_bronze", 64 ** 2, count)
                    elif e.buttonId == 103:
                        extract("variedcommodities:coin_stone", 64, count)
                    elif e.buttonId == 104:
                        extract("variedcommodities:coin_wood", 1, count)
                    elif e.buttonId == 109:
                        while wallet.storeddata.get("coins") > 0:
                            extract("variedcommodities:coin_iron", 64 ** 3, 1, "")
                            extract("variedcommodities:coin_bronze", 64 ** 2, 1, "")
                            extract("variedcommodities:coin_stone", 64, 1, "")
                            extract("variedcommodities:coin_wood", 1, 1, "")
                            try_stack_all()
                else:
                    g.getComponent(200).setText("1")
                    p.message(u"请输入数字(1~64)")
        elif 105 <= e.buttonId <= 108:
            if g.getComponent(201).getText() is not None:
                if g.getComponent(201).getText().isdigit():
                    count = int(g.getComponent(201).getText())
                    if count > 64:
                        g.getComponent(201).setText("64")
                        count = 64
                    if e.buttonId == 105:
                        single_put("variedcommodities:coin_iron", 64 ** 3, count)
                    elif e.buttonId == 106:
                        single_put("variedcommodities:coin_bronze", 64 ** 2, count)
                    elif e.buttonId == 107:
                        single_put("variedcommodities:coin_stone", 64, count)
                    elif e.buttonId == 108:
                        single_put("variedcommodities:coin_wood", 1, count)
                else:
                    g.getComponent(201).setText("1")
                    p.message(u"请输入数字(1~64)")
        elif e.buttonId == 111:
            try_stack_all()
        elif e.buttonId == 110:
            def put(name, multiple):
                if e.player.getInventory().count(e.player.world.createItem(name, 0, 1), True, True) > 0:
                    wallet.storeddata.put("coins", wallet.storeddata.get("coins") + e.player.getInventory().count(
                        e.player.world.createItem(name, 0, 1), True, True) * multiple)
                    for item in e.player.getInventory().getItems():
                        if item.getName() == name:
                            item.setStackSize(0)

            put("variedcommodities:coin_wood", 1)
            put("variedcommodities:coin_stone", 64)
            put("variedcommodities:coin_bronze", 64 * 64)
            put("variedcommodities:coin_iron", 64 ** 3)
        g.addLabel(400, generate_coins_description(e.player.tempdata.get("wallet"), 1), 10, 20, 80, 20)
    g.update(p)


def init(e):
    e.item.setMaxStackSize(1)
    e.item.setDurabilityShow(False)
    e.item.setTexture(1, "variedcommodities:satchel")
    if e.item.storeddata.has("coins") is False:
        e.item.storeddata.put("coins", 0)


def setItemLore(item, line, str):
    arr = item.getLore()
    if line < len(arr):
        arr[line] = str
        item.setLore(arr)


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
        return u"§5其内含有:" + s0 + " " + s1 + " " + s2 + " " + s3
    else:
        return s0 + "\n" + s1 + "\n" + s2 + "\n" + s3
