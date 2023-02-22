import time,math


def target(e):
    e.npc.tempdata.put("target", e.entity)
    e.npc.timers.forceStart(200, 0, True)


def targetLost(e):
    e.npc.timers.stop(200)


def timer(e):
    if e.id == 0:
        gesture_attack_1(e)
        e.npc.timers.stop(0)
    if e.id == 1:
        gesture_init(e)
        e.npc.timers.stop(1)
    if e.id == 200:
        if e.npc.tempdata.get("target"):
            # if e.npc.pos.distanceTo(e.npc.tempdata.get("target").pos) <= 1.2:
            #     # e.npc.getAi().setTacticalType(6)
            #     e.npc.getAi().setRetaliateType(3)
            # else:
            #     e.npc.getAi().setTacticalType(2)
            #     e.npc.getAi().setRetaliateType(0)
            if time.time() >= e.npc.tempdata.get("cooling"):
                if 1 <= e.npc.pos.distanceTo(e.npc.tempdata.get("target").pos) <= 2.5:
                    gesture_attack_0(e)
                    e.npc.tempdata.put("cooling", time.time() + 1.75)


def gesture_init(e):
    e.npc.job.setAnimationSpeed(2)
    e.npc.job.getPart(1).setRotation(90, 180, 180)
    e.npc.job.getPart(2).setRotation(90, 180, 180)
    e.npc.job.getPart(1 + 6).setRotation(90, 170, 180)
    e.npc.job.getPart(2 + 6).setRotation(90, 190, 180)
    e.npc.getStats().getRanged().setMeleeRange(1)
    e.npc.updateClient()


def gesture_attack_0(e):
    e.npc.job.setAnimationSpeed(4)
    e.npc.job.getPart(1).setRotation(90, 180, 180)
    e.npc.job.getPart(2).setRotation(90, 180, 180)
    e.npc.job.getPart(1 + 6).setRotation(35, 150, 180)
    e.npc.job.getPart(2 + 6).setRotation(35, 210, 180)
    e.npc.getStats().getRanged().setMeleeRange(3)
    e.npc.updateClient()
    e.npc.timers.forceStart(0, 10, True)


def gesture_attack_1(e):
    e.npc.job.setAnimationSpeed(6)
    e.npc.job.getPart(1).setRotation(35, 160, 180)
    e.npc.job.getPart(2).setRotation(35, 200, 180)
    e.npc.job.getPart(1 + 6).setRotation(120, 190, 180)
    e.npc.job.getPart(2 + 6).setRotation(120, 170, 180)
    speed = 0.35
    e.npc.setMotionX(
        math.sin(math.radians(e.npc.getRotation() + 180)) * math.cos(
            math.radians(-e.npc.getPitch())) * speed)
    e.npc.setMotionZ(
        math.cos(math.radians(e.npc.getRotation())) * math.cos(math.radians(-e.npc.getPitch())) * speed)
    e.npc.setMotionY(math.sin(math.radians(-e.npc.getPitch())) * 0.55 * speed+0.1)
    e.npc.updateClient()
    e.npc.timers.forceStart(1, 9, True)
