import math
import random
import time
import net.minecraft.util.EntityDamageSourceIndirect as EDSI


def target(e):
    e.npc.tempdata.put("target", e.entity)
    e.npc.timers.forceStart(200, 1, True)


def targetLost(e):
    e.npc.timers.stop(200)


def timer(e):
    if e.npc.health > 0:
        if e.id == 100:
            gesture_attack_0_1(e)
            e.npc.updateClient()
            e.npc.timers.stop(100)
        if e.id == 101:
            gesture_init(e)
            e.npc.updateClient()
            e.npc.timers.stop(101)
        if e.id == 102:
            gesture_attack_1_1(e)
            e.npc.updateClient()
            e.npc.timers.stop(102)
        if e.id == 103:
            gesture_init(e)
            e.npc.updateClient()
            e.npc.timers.stop(103)
        if e.id == 104:
            gesture_attack_2_1(e)
            e.npc.updateClient()
            e.npc.timers.stop(104)
        if e.id == 105:
            gesture_init(e)
            e.npc.updateClient()
            e.npc.timers.stop(105)
        if e.id == 106:
            gesture_attack_3_1(e)
            e.npc.updateClient()
            e.npc.timers.stop(106)
        if e.id == 200:
            if e.npc.tempdata.get("target"):
                if time.time() >= e.npc.tempdata.get("cooling"):
                    if e.npc.pos.distanceTo(e.npc.tempdata.get("target").pos) <= 10:
                        g = random.randint(0, 3)
                    elif e.npc.pos.distanceTo(e.npc.tempdata.get("target").pos) <= 15:
                        g = 3
                    else:
                        g = 4
                    if g == 0 or g == 2:
                        gesture_attack_0_0(e)
                    if g == 1 or g == 2:
                        gesture_attack_1_0(e)
                    if g == 3:
                        gesture_attack_3(e)
                    if g == 4:
                        gesture_attack_2_0(e)
                    e.npc.tempdata.put("cooling", time.time() + 2.5)
    else:
        e.npc.timers.clear()


def collide(e):
    knockback(e.npc, e.entity, 0.15)
    e.npc.setPosition(e.npc.getHomeX(), e.npc.getHomeY(), e.npc.getHomeZ())


def knockback(self, ent, bouns=0.25):
    ent.setMotionX((ent.x - self.x) * bouns)
    ent.setMotionY((ent.y - self.y) * bouns)
    ent.setMotionZ((ent.z - self.z) * bouns)


def gesture_attack_0_0(e):
    e.npc.getInventory().setRightHand(e.npc.getInventory().getProjectile())
    e.npc.job.getPart(9).setRotation(190, 180, 180)
    e.npc.job.setAnimationSpeed(2)
    e.npc.job.getPart(8).setRotation(90, 250, 250)
    e.npc.updateClient()
    e.npc.timers.forceStart(100, 20, True)


def gesture_attack_0_1(e):
    e.npc.job.setAnimationSpeed(5)
    e.npc.job.getPart(2).setRotation(90, 250, 250)
    e.npc.updateClient()
    e.npc.job.getPart(8).setRotation(160, 175, 85)
    e.npc.updateClient()
    p = e.npc
    p.world.playSoundAt(p.pos, "customnpcs:misc.old_explode", 4, 0.85)
    for x in range(120):
        p.world.spawnParticle("cloud", p.x + math.sin(math.radians(p.getRotation() + 285 - x)) * math.cos(
            math.radians(-p.getPitch())) * 7.5,
                              p.y + 5.5 + math.sin(math.radians(-p.getPitch() - x / 1.5)) * 0.75 * 7.5,
                              p.z + math.cos(math.radians(p.getRotation() + 105 - x)) * math.cos(
                                  math.radians(-p.getPitch())) * 7.5,
                              0.2, 0.2, 0.2, 0, 10)
        for ent in p.world.getNearbyEntities(e.API.getIPos(
                p.x + math.sin(math.radians(p.getRotation() + 285 - x)) * math.cos(
                    math.radians(-p.getPitch())) * 5.5,
                p.y + 5.5 + math.sin(math.radians(-p.getPitch() - x / 1.5)) * 0.75 * 6.5,
                p.z + math.cos(math.radians(p.getRotation() + 105 - x)) * math.cos(
                    math.radians(-p.getPitch())) * 5.5,

        ), 2, 5):
            if ent != e.npc:
                damage(ent, e.npc, 10, "近战", [])
                knockback(e, e.npc, ent, 0.6)
                ent.setMotionY(1)

    e.npc.timers.forceStart(101, 10, True)


def gesture_attack_1_0(e):
    e.npc.getInventory().setLeftHand(e.npc.getInventory().getProjectile())
    e.npc.job.getPart(9).setRotation(190, 180, 180)
    e.npc.job.setAnimationSpeed(2)
    e.npc.job.getPart(7).setRotation(90, 110, 110)
    e.npc.updateClient()
    e.npc.timers.forceStart(102, 20, True)


def gesture_attack_1_1(e):
    e.npc.job.setAnimationSpeed(5)
    e.npc.job.getPart(1).setRotation(90, 110, 110)
    e.npc.updateClient()
    e.npc.job.getPart(7).setRotation(160, 185, 275)
    e.npc.updateClient()
    p = e.npc
    p.world.playSoundAt(p.pos, "customnpcs:misc.old_explode", 4, 0.85)
    for x in range(120):
        p.world.spawnParticle("cloud", p.x + math.sin(math.radians(p.getRotation() + 75 + x)) * math.cos(
            math.radians(-p.getPitch())) * 7.5,
                              p.y + 5.5 + math.sin(math.radians(-p.getPitch() - x / 1.5)) * 0.75 * 7.5,
                              p.z + math.cos(math.radians(p.getRotation() - 105 + x)) * math.cos(
                                  math.radians(-p.getPitch())) * 7.5,
                              0.2, 0.2, 0.2, 0, 10)
        for ent in p.world.getNearbyEntities(e.API.getIPos(
                p.x + math.sin(math.radians(p.getRotation() + 75 + x)) * math.cos(
                    math.radians(-p.getPitch())) * 5.5,
                p.y + 5.5 + math.sin(math.radians(-p.getPitch() - x / 1.5)) * 0.75 * 6.5,
                p.z + math.cos(math.radians(p.getRotation() - 105 + x)) * math.cos(
                    math.radians(-p.getPitch())) * 5.5,
        ), 2, 5):
            if ent != e.npc:
                damage(ent, e.npc, 10, "近战", [])
                knockback(e, e.npc, ent, 0.6)
                ent.setMotionY(1)

    e.npc.timers.forceStart(101, 10, True)


def gesture_attack_2_0(e):
    e.npc.updateClient
    e.npc.job.getPart(9).setRotation(190, 180, 180)
    e.npc.job.setAnimationSpeed(2)
    e.npc.job.getPart(8).setRotation(55, 250, 250)
    e.npc.job.getPart(7).setRotation(55, 110, 110)
    e.npc.job.getPart(6).setRotation(160, 180, 180)
    e.npc.timers.forceStart(104, 30, True)


def gesture_attack_2_1(e):
    e.npc.job.setAnimationSpeed(4)
    e.npc.job.getPart(2).setRotation(55, 250, 250)
    e.npc.job.getPart(1).setRotation(55, 110, 110)
    e.npc.job.getPart(0).setRotation(160, 180, 180)
    e.npc.job.getPart(6).setRotation(215, 180, 180)
    e.npc.job.getPart(7).setRotation(128, 150, 165)
    e.npc.job.getPart(8).setRotation(128, 210, 195)
    e.npc.job.getPart(9).setRotation(195, 180, 180)
    for x in range(20):
        if e.npc.tempdata.get("target"):
            e.npc.shootItem(e.npc.tempdata.get("target"),
                            e.npc.world.createItem("minecraft:stone", random.randint(0, 6), 1), 70)
        e.npc.timers.forceStart(105, 15, True)


def gesture_attack_3(e):
    e.npc.getInventory().setRightHand(e.npc.world.createItem("variedcommodities:stone_broadsword", 0, 1))
    e.npc.job.getPart(9).setRotation(190, 180, 180)
    e.npc.job.setAnimationSpeed(2)
    e.npc.job.getPart(7).setRotation(0, 180, 160)
    e.npc.job.getPart(8).setRotation(0, 180, 200)
    e.npc.updateClient()
    e.npc.timers.forceStart(106, 20, True)
    # time.sleep(1.05)


def gesture_attack_3_1(e):
    e.npc.job.setAnimationSpeed(6)
    e.npc.job.getPart(1).setRotation(0, 180, 160)
    e.npc.job.getPart(2).setRotation(0, 180, 200)
    e.npc.job.getPart(7).setRotation(150, 230, 160)
    e.npc.job.getPart(8).setRotation(150, 130, 200)
    e.npc.updateClient()
    p = e.npc
    p.world.playSoundAt(p.pos, "customnpcs:misc.old_explode", 4, 1.15)
    for x in range(65):
        p.world.spawnParticle("cloud", p.x + math.sin(math.radians(p.getRotation() + 180)) * math.cos(
            math.radians(-p.getPitch())) * x / 5
                              , p.y + 7 + (math.sin(math.radians(-p.getPitch())) - (x / 10) ** 1.2)
                              , p.z + math.cos(math.radians(p.getRotation())) * math.cos(
                math.radians(-p.getPitch())) * x / 5
                              , 0.2, 0.2, 0.2, 0, 10)
        for ent in p.world.getNearbyEntities(e.API.getIPos(
                p.x + math.sin(math.radians(p.getRotation() + 180)) * math.cos(
                    math.radians(-p.getPitch())) * x / 5,
                p.y + 6.2 + (math.sin(math.radians(-p.getPitch())) - (x / 10) ** 1.2),
                p.z + math.cos(math.radians(p.getRotation())) * math.cos(math.radians(-p.getPitch())) * x / 5,
        ), 1, 5):
            if ent != e.npc:
                damage(ent, e.npc, 15, "近战", [])
                knockback(e, e.npc, ent, 0.3)
                ent.setMotionY(0.5)
    for x in range(30):
        for ent in p.world.getNearbyEntities(e.API.getIPos(
                p.x + math.sin(math.radians(p.getRotation() + 180)) * math.cos(math.radians(-p.getPitch())) * x / 5,
                p.y + 4 + (math.sin(math.radians(-p.getPitch())) - (x / 10) ** 1.2),
                p.z + math.cos(math.radians(p.getRotation())) * math.cos(math.radians(-p.getPitch())) * x / 5,
        ), 2, 5):
            if ent != e.npc:
                damage(ent, e.npc, 15, "近战", [])
                knockback(e, e.npc, ent, 0.3)
                ent.setMotionY(0.5)
    e.npc.timers.forceStart(105, 10, True)


def gesture_init(e):
    e.npc.job.setAnimationSpeed(1)
    e.npc.job.getPart(0).setRotation(215, 180, 180)
    e.npc.job.getPart(1).setRotation(128, 150, 165)
    e.npc.job.getPart(2).setRotation(128, 210, 195)
    e.npc.job.getPart(3).setRotation(190, 180, 180)
    e.npc.job.getPart(6).setRotation(215, 180, 180)
    e.npc.job.getPart(7).setRotation(128, 150, 165)
    e.npc.job.getPart(8).setRotation(128, 210, 195)
    e.npc.job.getPart(9).setRotation(195, 180, 180)
    e.npc.getInventory().setRightHand(e.npc.world.createItem("minecraft:air", 0, 1))
    e.npc.getInventory().setLeftHand(e.npc.world.createItem("minecraft:air", 0, 1))
    e.npc.updateClient()


def damage(entity0, entity1, count, type, parameters):
    if entity1 is not None:
        mcentity1 = entity1.getMCEntity()
    else:
        mcentity1 = None
    mcentity0 = entity0.getMCEntity()
    count = count
    type = type
    source = EDSI(type, mcentity0, mcentity1)
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
    mcentity0.func_70097_a(source, count)
