import math
import time


def init(e):
    e.npc.tempdata.put("jump_time", time.time() + 3)


def tick(e):
    jt = e.npc.tempdata.get("jump_time")

    if jt <= time.time() and e.npc.health > 0:
        speed = 0.7
        e.npc.world.playSoundAt(e.npc.pos, "minecraft:entity.slime.jump", 1, 0.95)
        e.npc.tempdata.put("jump_time", time.time() + 3)
        e.npc.setMotionX(
            math.sin(math.radians(e.npc.getRotation() + 180)) * math.cos(math.radians(-e.npc.getPitch())) * speed)
        e.npc.setMotionZ(
            math.cos(math.radians(e.npc.getRotation())) * math.cos(math.radians(-e.npc.getPitch())) * speed)
        e.npc.setMotionY(math.sin(math.radians(-e.npc.getPitch())) * 0.55 * speed + 0.5)
