class Character:
    def __init__(self,name, level, hp, attack, defense, attack_speed, crit_rate, crit_damage, element):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.attack_speed = attack_speed
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.element = element

class Boss:
    def __init__(self,name, level, hp, attack, weak_element):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.weak_element = weak_element

def assess_threat(player_team, boss):
    player_power = sum([character.hp + character.attack + character.defense for character in player_team])
    boss_power = boss.hp + boss.attack

    for character in player_team:
        if boss.weak_element == character.element:
            player_power *= 1.2

    threat_level = boss_power / player_power
    return threat_level

