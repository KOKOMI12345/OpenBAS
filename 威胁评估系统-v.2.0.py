from Log4p.core import *
from plugins.work import *
import traceback

# BOSS威胁评估系统
class BossAssessmentSystem:
    def __init__(self):
        self.log = LogManager().GetLogger("BossAssessmentSystem")

    def create_advice(self, information: str):
        with open("advice.txt", "w", encoding="utf-8") as f:
            f.write("coded by:芙宁娜-荒性\n")
            f.write("评估结果如下\n")
            f.write("----======================分界线=======================----")
            f.write("\n")
            f.write(information)
            f.write("----======================分界线=======================----")

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
        
        information += "---===============================---\n"
        information += f"小队平均等级:{int(sum([player.level for player in players_team]) / len(players_team))}\n"
        information += f"小队平均攻击力:{int(sum([player.attack for player in players_team]) / len(players_team))}\n"
        information += f"小队平均防御力:{int(sum([player.defense for player in players_team]) / len(players_team))}\n"
        information += f"小队平均生命值:{int(sum([player.hp for player in players_team]) / len(players_team))}\n"
        information += f"敌方平均等级:{int(sum([boss.level for boss in boss_teams]) / len(boss_teams))}\n"
        information += f"敌方平均攻击力:{int(sum([boss.attack for boss in boss_teams]) / len(boss_teams))}\n"
        information += f"敌方平均生命值:{int(sum([boss.hp for boss in boss_teams]) / len(boss_teams))}\n"
        information += "---===============================---\n"


        information += "威胁评估情况如下:\n"
        for i, threat in enumerate(boss_threats):
            information += f"敌人{i + 1}|{boss.name}|: 威胁指数: {int(threat)}% , 弱点: {boss_teams[i].weak_element}\n"
        information += "建议: \n"
        information += "根据评估结果，建议采取以下策略:\n"
        #这里根据每个角色的属性,技能来,首先,获取每个敌对成员的弱点,威胁指数
        for i, boss in enumerate(boss_teams):
            if int(boss_threats[i]) < 50:
                information += f"敌人{i + 1}|{boss.name}|: 威胁较低, 可以延后打,如果只有他一个人,那随便啦! :)\n"
            elif int(boss_threats[i]) < 80:
                information += f"敌人{i + 1}|{boss.name}|: 威胁中等, 需要使用范围攻击\n"
            else:
                if int(boss_threats[i]) > 90:
                   information += f"敌人{i + 1}|{boss.name}|: 威胁非常高,对团队的威胁较大,小心尝试\n"
                else:
                   information += f"敌人{i + 1}|{boss.name}|: 威胁较高, 需要优先打\n"
            match boss.weak_element:
                case "火":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为火, 可以针对使用火系技能\n"
                case "物理":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为物理, 可以针对使用物理攻击技能\n"
                case "冰":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为冰, 可以针对使用冰系技能\n"
                case "雷":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为雷, 可以针对使用雷系技能\n"
                case "风":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为风, 可以针对使用风系技能\n"
                case "量子":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为量子, 可以针对使用量子系技能\n"
                case "虚数":
                    information += f"敌人{i + 1}|{boss.name}|: 弱点属性为虚数, 可以针对使用虚数系技能\n"
        for a,player in enumerate(players_team):
            match player.element:
                case _:
                    for s,boss in enumerate(boss_teams):
                        if boss.weak_element == player.element:
                            information += f"队友{a + 1}|{player.name}|: 属性为{player.element}, 可以针对敌人{boss.name}的弱点元素:{boss.weak_element}攻击\n"
                        else:
                            information += f"队友{a + 1}|{player.name}|: 属性为{player.element}, 不适合对付敌人{boss.name},但仍可造成伤害\n"
        information += f"角色死亡风险评估:\n"
        for i,player in enumerate(players_team):
            match player.level:
                case _:
                    for m,boss in enumerate(boss_teams):
                        if player.level < boss.level:
                            information += f"队友{i + 1}|{player.name}|: 等级低于敌人{boss.name}, 存在死亡风险\n"
                        else:
                            information += f"队友{i + 1}|{player.name}|: 等级高于或等于敌人{boss.name}, 死亡风险较低\n"
        information += f"角色保护优先级建议:\n"
        avallabie_constellations = ["巡猎","丰饶", "存护","智识","同协","虚无","毁灭"]
        for i,player in enumerate(players_team):
            match player.constellation:
                case "巡猎":
                    information += f"队友{i + 1}|{player.name}|: 输出位, 建议优先保护\n"
                case "丰饶":
                    information += f"队友{i + 1}|{player.name}|: 治疗位, 第二保护对象\n"
                case "存护":
                    information += f"队友{i + 1}|{player.name}|: 防护位, 第三保护对象,如果此角色血量危机,则先保护自身\n"
                case "智识":
                    information += f"队友{i + 1}|{player.name}|: 群体输出位, 优先级如同第一\n"
                case "同协":
                    information += f"对友{i + 1}{player.name}|: 辅助位, 第二保护对象\n"
                case "虚无":
                    information += f"队友{i + 1}|{player.name}|: 辅助位, 第三保护对象\n"
                case "毁灭":
                    information += f"队友{i + 1}|{player.name}|: 小队的攻击性全能手, 第一保护对象\n"
                case _:
                    self.log.warning(f"角色{player.name}的命座{player.constellation},请检查")
                    self.log.info(f"合法命座为: {avallabie_constellations}")

        self.create_advice(information)
        self.log.info("评估完成，结果已保存至文件")
        input("按Enter退出")
    
    def run(self):
        try:
            self.log.info("coded by:芙宁娜-荒性")
            self.log.info("欢迎您使用BOSS威胁-建议评估系统")
            self.log.info("请输入以下参数")
            mode = str(input("评估模式?[1.单个BOSS,2.多敌对人员或boss]"))
            team_man = int(input("小队人员?(上限为4人)"))
            boss_man = int(input("敌对人员人数?(如果是单个BOSS模式,则填入0)"))
            players_team = []
            boss_teams = []
            
            if mode == "1":
                if team_man > 4:
                    self.log.error("小队人员过多，请重新输入")
                    raise SystemExit 
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
                raise SystemExit
        
        except Exception as e:
            self.log.error(f"评估失败,发生异常: {e}")
            self.log.error("请联系开发人员")
            raise SystemExit
        
        except KeyboardInterrupt:
            self.log.info("评估终止,用户手动退出")
            raise SystemExit

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
        constellation = input("命途: ")
        return Character(name,level, hp, attack, defense, attack_speed, crit_rate, crit_damage, element,constellation)

    def get_boss_info(self):
        boss_name = input("敌人名称: ")
        boss_level = int(input("等级: "))
        boss_hp = int(input("生命值: "))
        boss_attack = int(input("攻击力: "))
        boss_weak_element = input("弱点属性(用空格分隔): ").split(" ")
        return Boss(boss_name,boss_level, boss_hp, boss_attack, boss_weak_element)

try:
   unit_test = BossAssessmentSystem()
   unit_test.run()
except Exception as e:
    error_message = traceback.format_exc()
    unit_test.log.critical(error_message)