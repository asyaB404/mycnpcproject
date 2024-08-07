import math
import random
import time
import net.minecraft.util.EntityDamageSourceIndirect as EDSI

r_angle = 0
rotate_speed = 0
rotate_angle = 0
rotate_direction = True


def interact(e):
    def atk():
        p = e.player
        r1 = random.choice([-1, 0, 1])
        r = random.random()
        for x in range(120):
            e.API.executeCommand(e.player.world, "/particleex normal endRod "
                                 + str(p.x + math.sin(math.radians(p.getRotation() + 120 + x)) * 3) + " "
                                 + str(p.y + 1.5 + math.sin(math.radians((x - 60) * r1)) * 5 * r) + " "
                                 + str(
                p.z + math.cos(math.radians(p.getRotation() - 60 + x)) * 3) +
                                 " 1 0.5 0.5 1 180"
                                 + " " + str(
                math.sin(math.radians(p.getRotation() + 180)) * math.cos(math.radians(-p.getPitch())) * 1 / 1.5) + " "
                                 + str(math.sin(math.radians(-p.getPitch())) * 0.75 / 1.5 * 0) + " "
                                 + str(
                math.cos(math.radians(p.getRotation())) * math.cos(math.radians(-p.getPitch())) * 1 / 1.5) + ""
                                 + " 0 0 0 1 5")
        target = p.world.getNearbyEntities(e.API.getIPos(
            p.x + math.sin(math.radians(p.getRotation() + 180)) * 3,
            p.y + 1,
            p.z + math.cos(math.radians(p.getRotation())) * 3), 3, 5)
        p.message(str(e.API.getIPos(
            p.x + math.sin(math.radians(p.getRotation() + 180)) * math.cos(
                math.radians(-p.getPitch())) * 2,
            p.y + 1 + math.sin(math.radians(-p.getPitch())) * 1.5,
            p.z + math.cos(math.radians(p.getRotation())) * math.cos(
                math.radians(-p.getPitch())) * 2)))
        for ent in target:
            damage(ent, p, 10, "近战")

    # for x in range(2):
    #     atk()


def damaged(e):
    if e.player.tempdata.get("dodge_time") > 0:
        e.damage = 0
        e.setCanceled(True)


def timer(e):
    if e.id == 0 and e.player.tempdata.get("dodge_time") is not None:
        if e.player.tempdata.get("dodge_time") > 0:
            e.player.world.spawnParticle("cloud", e.player.x, e.player.y + 0.5, e.player.z, 0.2, 0.2, 0.2, 0, 30)
            e.player.tempdata.put("dodge_time", e.player.tempdata.get("dodge_time") - 0.1)
        else:
            e.player.timers.stop(0)
    elif e.id == 1:
        global rotate_speed, rotate_angle, rotate_direction, r_angle
        r_angle += rotate_speed
        if rotate_direction:
            e.API.executeCommand(e.player.world, "/tp " + str(e.player.name) + " ~ ~ ~ ~" + str(rotate_speed) + " ~")
        else:
            e.API.executeCommand(e.player.world, "/tp " + str(e.player.name) + " ~ ~ ~ ~" + str(-rotate_speed) + " ~")
        if r_angle >= rotate_angle:
            e.player.timers.stop(1)
            r_angle = 0
            rotate_speed = 0
            rotate_angle = 0
            rotate_direction = True
    elif e.id == 2:
        e.player.tempdata.put("c17", 0)
        e.player.tempdata.put("c30", 0)
        e.player.tempdata.put("c31", 0)
        e.player.tempdata.put("c32", 0)
        e.player.timers.stop(2)


def keyPressed(e):
    if time.time() > e.player.tempdata.get("dodge_cooling_time"):
        if e.key == 17:
            if if_pressed_count(e, 17):
                dodge(e, 0, 1.5)
        elif e.key == 30:
            if if_pressed_count(e, 30):
                dodge(e, 1, 1.5)
                rotate(e, True, 7.5, 30)
        elif e.key == 31:
            if if_pressed_count(e, 31):
                dodge(e, 2, 1.5)
        elif e.key == 32:
            if if_pressed_count(e, 32):
                dodge(e, 3, 1.5)
                rotate(e, False, 7.5, 30)


def rotate(e, direction, speed, angle):
    global rotate_speed, rotate_angle, rotate_direction
    e.player.timers.forceStart(1, 0, True)
    rotate_speed = speed
    rotate_angle = angle
    if direction:
        rotate_direction = True
    else:
        rotate_direction = False


def dodge(e, direction, speed=1.0):
    e.player.timers.forceStart(00, 0, True)
    e.player.tempdata.put("dodge_time", 0.5)
    e.player.tempdata.put("dodge_cooling_time", time.time() + 0.75)
    e.player.setMotionY(0.2)
    e.player.world.playSoundAt(e.player.pos, "minecraft:item.armor.equip_leather", 1, 0.8)
    if direction == 0:
        e.player.setMotionX(math.sin(math.radians(e.player.getRotation() + 180)) * speed)
        e.player.setMotionZ(math.cos(math.radians(e.player.getRotation())) * 1)
    elif direction == 1:
        e.player.setMotionX(math.sin(math.radians(e.player.getRotation() + 120)) * speed)
        e.player.setMotionZ(math.cos(math.radians(e.player.getRotation() - 60)) * speed)
    elif direction == 2:
        e.player.setMotionX(math.sin(math.radians(e.player.getRotation() + 180)) * -speed)
        e.player.setMotionZ(math.cos(math.radians(e.player.getRotation())) * -speed)
    elif direction == 3:
        e.player.setMotionX(math.sin(math.radians(e.player.getRotation() + 240)) * speed)
        e.player.setMotionZ(math.cos(math.radians(e.player.getRotation() + 60)) * speed)


def prevent_npe(target, name, count=0):
    if target.tempdata.get(name):
        return False
    target.tempdata.put(name, count)
    return True


def if_pressed_count(e, key, count=2):
    prevent_npe(e.player, "c{}".format(key))
    e.player.timers.forceStart(2, 5, True)
    e.player.tempdata.put("c{}".format(key), e.player.tempdata.get("c{}".format(key)) + 1)
    if e.player.tempdata.get("c{}".format(key)) >= count:
        e.player.tempdata.put("c{}".format(key), 0)
        return True
    return False


def getItemLore(item, line):
    arr = item.getLore()
    if line < len(arr):
        if arr[line] is not None:
            return arr[line]
    return "0"


def damage(entity1, entity0, count, type, parameters=None):
    # DamageSource = Java.type("net.minecraft.util.DamageSource")
    if parameters is None:
        parameters = []
    if entity1:
        mc_entity1 = entity1.getMCEntity()
    else:
        mc_entity1 = None
    mc_entity0 = entity0.getMCEntity()
    source = EDSI(type, mc_entity0, mc_entity1)
    if parameters.count("远程") != 0:
        source.func_76349_b()
    if parameters.count("爆炸") != 0:
        source.func_94539_a()
    if parameters.count("破甲") != 0:
        source.func_76348_h()
    if parameters.count("伤害创造") != 0:
        source.func_76359_i()
    if parameters.count("绝对") != 0:
        source.func_151518_m()
    if parameters.count("火焰") != 0:
        source.func_76361_j()
    if parameters.count("魔法") != 0:
        source.func_82726_p()
    mc_entity0.func_70097_a(source, count)
