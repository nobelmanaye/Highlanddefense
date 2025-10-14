

from Cinematics.Explosion import *
def Handle_explosion(character, ExplostionLst):
    cannon_exp_size = 0.8
    rifle_exp_size = 0.2

    if type(character) ==Rifleman:
        if character.angle == 0:
            munition_effect = Explosion(character.position.x-10,character.position.y+10+30,character.angle, rifle_exp_size) 
            ExplostionLst.append(munition_effect)
            return munition_effect
        else: 
            munition_effect = Explosion(character.position.x-10,character.position.y+10+30,character.angle, rifle_exp_size) 
            ExplostionLst.append(munition_effect)
            return munition_effect
    if type(character) == cannon:
        if character.angle ==90:
            munition_effect = Explosion(character.position.x+135,character.position.y+31,character.angle,cannon_exp_size)



        if character.angle ==180:
            munition_effect = Explosion(character.position.x+86,character.position.y+89,character.angle,cannon_exp_size)

        if character.angle ==0:
             munition_effect = Explosion(character.position.x-10 + 0.33*character.getWidth(),character.position.y-character.getWidth(),character.angle,cannon_exp_size)
        if character.angle == 270:
        
            munition_effect = Explosion(character.position.x-10,character.position.y+10,character.angle,cannon_exp_size)



