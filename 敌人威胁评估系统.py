from Log4p.core import *
from plugins.work import *

# BOSS威胁评估系统
class BossAssessmentSystem:
    def __init__(self):
        self.log = LogManager().GetLogger("BossAssessmentSystem")

    def create_advice(self, information: str):
        with open("advice.txt", "w", encoding="utf-8") as f:
            f.write("coded by:芙宁娜-荒性\n")
            f.write("评估结果如下\n")
            f.write("\n")
            f.write(information)

    def create_text(self, boss_teams, players_team):
        self.log.info("参数输入完成，开始评估")
        boss_threats = []
        for boss in boss_teams:
            boss_threat = assess_threat(players_team, boss)
            boss_threats.append(boss_threat)

        information = "小队成员信息:\n"
        for i, player in enumerate(players_team):
            information += f"成员{i + 1}|{player.name}|: 等级 {player.level}, 生命值 {player.hp}, 攻击力 {player.attack}, 防御力 {player.defense}, 属性 {player.element}\n"

        information += "敌对成员信息:\n"
        for i, boss in enumerate(boss_teams):
            information += f"敌人{i + 1}|{boss.name}|: 等级 {boss.level}, 生命值 {boss.hp}, 攻击力 {boss.attack}, 弱点属性 {boss.weak_element}\n"

        information += "威胁评估情况如下:\n"
        for i, threat in enumerate(boss_threats):
            information += f"敌人{i + 1}|{boss.name}|: 威胁指数: {int(threat*10)}% , 弱点: {boss_teams[i].weak_element}\n"
        information += "建议: \n"
        information += "根据评估结果，建议采取以下策略:\n"
        #这里根据每个角色的属性,技能来,首先,获取每个敌对成员的弱点,威胁指数
        for i, boss in enumerate(boss_teams):
            if int(boss_threats[i]*10) < 50:
                information += f"敌人{i + 1}|{boss.name}|: 威胁较低, 可以延后打,如果只有他一个人,那随便啦! :)\n"
            elif int(boss_threats[i]*10) < 80:
                information += f"敌人{i + 1}|{boss.name}|: 威胁中等, 需要使用范围攻击\n"
            else:
                information += f"敌人{i + 1}|{boss.name}|: 威胁较高, 需要优先打\n"
        for a,player in enumerate(players_team):
            match player.element:
                case "存护" | "防御":
                    information += f"成员{a + 1}|{player.name}|: 团队的护盾, 可以使用防御技能,对于威胁较高的,血量低的可以优先防御\n"
                case "回血" | "治疗" | "丰饶":
                    information += f"成员{a + 1}|{player.name}|: 团队的奶妈, 可以使用治疗技能,对于血量低的,优先治疗,重点保护对象\n"
                case "巡猎" | "攻击":
                    information += f"成员{a + 1}|{player.name}|: 团队的输出,是第二保护对象\n"
                case "同协" | "辅助":
                    information += f"成员{a + 1}|{player.name}|: 团队的辅助, 可以使用辅助技能,为队伍带来整体加成\n"
                case _:
                    information += f"成员{a + 1}|{player.name}|: 没有特殊属性, 需要根据实际情况选择技能\n"
                    information += f"开发者提醒: 我也才刚刚玩呀, 可能会有错误, 请多包涵QAQ\n"

        self.create_advice(information)
        self.log.info("评估完成，结果已保存至文件")
        input("按Enter退出")
    
    def run(self):
        try:
            self.log.info("coded by:芙宁娜-荒性")
            self.log.info("欢迎您使用BOSS威胁-建议评估系统")
            self.log.info("请输入以下参数")
            mode = input("评估模式?[1.单个BOSS,2.多敌对人员或boss]")
            team_man = int(input("小队人员?(上限为4人)"))
            boss_man = input("敌对人员人数?(如果是单个BOSS模式,则不用管)")
            players_team = []
            boss_teams = []
            
            if mode == "1":
                if team_man > 4:
                    self.log.error("小队人员过多，请重新输入")
                    exit()
                for i in range(team_man):
                    print(f"请输入第{i + 1}位小队成员的信息：")
                    player = self.get_player_info()
                    players_team.append(player)

                print("请输入敌对人员信息：")
                boss = self.get_boss_info()
                boss_teams.append(boss)
                self.create_text(boss_teams=boss_teams, players_team=players_team)
            
            elif mode == "2":
                if team_man > 4:
                    self.log.error("小队人员过多，请重新输入")
                    exit()
                for i in range(team_man):
                    print(f"请输入第{i + 1}位小队成员的信息：")
                    player = self.get_player_info()
                    players_team.append(player)
                
                for a in range(boss_man):
                    print(f"请输入第{a + 1}位BOSS的信息:")
                    boss = self.get_boss_info()
                    boss_teams.append(boss)
                
                self.create_text(boss_teams=boss_teams, players_team=players_team)
            
            else:
                self.log.error("未知模式")
                exit()
        
        except Exception as e:
            self.log.error(f"评估失败,发生异常: {e}")
            self.log.error("请联系开发人员")
            exit()
        
        except KeyboardInterrupt:
            self.log.info("评估终止,用户手动退出")
            exit()

    def get_player_info(self):
        name = input("姓名: ")
        level = int(input("等级: "))
        hp = int(input("生命值: "))
        attack = int(input("攻击力: "))
        defense = int(input("防御力: "))
        attack_speed = float(input("攻速: "))
        crit_rate = float(input("暴击率: "))
        crit_damage = float(input("暴击伤害: "))
        element = input("属性: ")
        return Character(name,level, hp, attack, defense, attack_speed, crit_rate, crit_damage, element)

    def get_boss_info(self):
        boss_name = input("敌人名称: ")
        boss_level = int(input("等级: "))
        boss_hp = int(input("生命值: "))
        boss_attack = int(input("攻击力: "))
        boss_weak_element = input("弱点属性: ")
        return Boss(boss_name,boss_level, boss_hp, boss_attack, boss_weak_element)

try:
   unit_test = BossAssessmentSystem()
   unit_test.run()
except Exception as e:
    unit_test.log.critical(f"失败,发生异常: {e}")