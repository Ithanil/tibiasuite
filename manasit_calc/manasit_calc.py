class regen_item:
    def __init__(self, label, hps, mps, cost, duration):
        self.__label = label
        self.__hps = hps
        self.__mps = mps
        self.__cost = cost
        self.__duration = duration
        
        self.__update_costphms()
#        self.set(hps = hps, mps = mps, cost = cost, duration = duration)

    def __update_costph(self):
        if (self.__hps > 0): self.__costph = self.__cost / self.__hps / self.__duration
        else: self.__costph = 0.

    def __update_costpm(self):
        if (self.__mps > 0): self.__costpm = self.__cost / self.__mps / self.__duration
        else: self.__costpm = 0.

    def __update_costps(self):
        self.__costps = self.__cost / self.__duration

    def __update_costphms(self):
        self.__update_costph()
        self.__update_costpm()
        self.__update_costps()

    def set(self, label = None, hps = None, mps = None, cost = None, duration = None):
        if label: self.__label = label
        if hps: self.__hps = hps
        if mps: self.__mps = mps
        if cost: self.__cost = cost
        if duration: self.__duration = duration        

        self.__update_costphms()

    def set_label(self, label):
        self.__label = label

    def set_hps(self, hps):
        self.__hps = hps
        self.__update_costph()

    def set_mps(self, mps):
        self.__mps = mps
        self.__update_costpm()

    def set_cost(self, cost):
        self.__cost = cost
        self.__update_costphms()

    def set_duration(self, duration):
        self.__duration = duration
        self.__update_costphms()

    def get_label(self):
        return self.__label

    def get_hps(self):
        return self.__hps

    def get_mps(self):
        return self.__mps

    def get_cost(self):
        return self.__cost

    def get_duration(self):
        return self.__duration

    def get_costph(self):
        return self.__costph

    def get_costpm(self):
        return self.__costpm

    def get_costps(self):
        return self.__costps

    def get_costphm(self):
        return self.__costph, self.__costpm
    
    def get_costphms(self):
        return self.__costph, self.__costpm, self.__costps

    def calc_hp_gain(self, duration):
        return self.__hps * duration

    def calc_mana_gain(self, duration):
        return self.__mps * duration

    def calc_money_drain(self, duration):
        return self.__cost / self.__duration

    def report(self):
        print("Regen report for " +  self.__label + ":")
        print("hps: " + str(self.__hps))
        print("mps: " + str(self.__mps))
        print("cost: " + str(self.__cost))
        print("duration: " + str(self.__duration))
        print("cost per hp: " + str(self.__costph))
        print("cost per mp: " + str(self.__costpm))
        print("cost per second: " + str(self.__costps))


class regen_item_list:
    def __init__(self, item_list, resting_area = False):
        self.set_resting_area(resting_area)
        self.set_items(item_list)

    def set_resting_area(self, resting_area):
        if (resting_area == True):
            self.__rafac = 2.0
        else:
            self.__rafac = 1.0
    
    def set_items(self, item_list):
        self.__items = []
        self.__hps = 0.
        self.__mps = 0.
        self.__costps = 0.
        
        for item in item_list:
            self.__items.append(item)
            self.__hps += self.__rafac * item.get_hps()
            self.__mps += self.__rafac * item.get_mps()
            self.__costps += item.get_costps()
        
        if (self.__hps > 0): self.__costph = self.__costps / self.__hps
        else: self.__costph = 0.
        
        if (self.__mps > 0): self.__costpm = self.__costps / self.__mps
        else: self.__costpm = 0.

    def get_rafac(self):
        return self.__rafac

    def get_items(self):
        return self.__items

    def get_hps(self):
        return self.__hps

    def get_mps(self):
        return self.__mps

    def get_costps(self):
        return self.__costps

    def get_costph(self):
        return self.__costph

    def get_costpm(self):
        return self.__costpm

    def report(self):
        print("Total hps: " + str(self.__hps))
        print("Total mps: "+ str(self.__mps))
        print("Total cost per hp: " + str(self.__costph))
        print("Total cost per mp: " + str(self.__costpm))
        print("Total cost per second: " + str(self.__costps))
        print()
                    

def create_softboots():
    return regen_item(label = "soft boots", hps = 0.5, mps = 2.0, cost = 10000, duration = 4*60*60)

def create_lifering(cost):
    return regen_item(label = "life ring", hps = 1./3., mps = 4./3. , cost = cost, duration = 20*60)

def create_ringofhealing(cost):
    return regen_item(label = "ring of healing", hps = 1., mps = 4., cost = cost, duration = 450)

def create_foodregen_knight(cost, promoted):
    if (promoted == True): return regen_item(label = "Elite Knight Regen", hps = 0.25, mps = 1./3., cost = cost, duration = 20*60)
    else: return regen_item(label = "Knight Regen", hps = 1./6., mps = 1./3., cost = cost, duration = 20*60) 

def create_foodregen_paladin(cost, promoted):
    if (promoted == True): return regen_item(label = "Royal Paladin Regen", hps = 1./6., mps = 2./3., cost = cost, duration = 20*60)
    else: return regen_item(label = "Paladin Regen", hps = 0.125, mps = 0.5, cost = cost, duration = 20*60)

def create_foodregen_mage(cost, promoted):
    if (promoted == True): return regen_item(label = "Promoted Mage Regen", hps = 1./12., mps = 1., cost = cost, duration = 20*60)
    else: return regen_item(label = "Mage Regen", hps = 1./12., mps = 2./3., cost = cost, duration = 20*60)

def create_foodregen(cost, vocation, promoted):
    vocmap = {
               "Knight" : create_foodregen_knight,
               "Paladin" : create_foodregen_paladin,
               "Sorcerer" : create_foodregen_mage,
               "Druid" : create_foodregen_mage 
             }
    return vocmap[vocation](cost, promoted)

def create_potion(type, cost, cd, resting_area = False):
    potsmap = {
                "Mana Potion" : [0, 100],
                "Strong Mana Potion" : [0, 150],
                "Great Mana Potion" : [0, 200],
                "Ultimate Mana Potion" : [0, 500],
                "Health Potion" : [100, 0]
              }

    if (resting_area == True):
        for key in potsmap:
            potsmap[key][0] *= 0.5 # atm we apply resting area boni to all regen_item, but ingame pots are not affected
            potsmap[key][1] *= 0.5

    return regen_item(label = type, hps = potsmap[type][0] / cd, mps = potsmap[type][1] / cd, cost = cost, duration = cd)


class rune:
    def __init__(self, label, mp, sp, nout, price):
        self.label = label
        self.mp = mp
        self.sp = sp
        self.nout = nout
        self.price = price

    def report(self):
        print("Rune report for " + self.label + ":")
        print("Mana points per cast: " + str(self.mp))
        print("Soul points per cast: " + str(self.sp))
        print("Produced runes per cast: " + str(self.nout))
        print("Market price per rune: " + str(self.price))
        print()


def create_rune_gfb(price):
    return rune("Great Fireball", 530, 3, 4, price)

def create_rune_sd(price):
    return rune("Sudden Death", 985, 5, 3, price)


def analyze_manasit(rune, regen_items, blank_rune_price):

    cast_ps = regen_items.get_mps() / rune.mp
    sp_ps = rune.sp * cast_ps
    nout_ps = rune.nout * cast_ps
    profit_ps = rune.price * nout_ps - blank_rune_price * cast_ps - regen_items.get_costps()

    num_items = len(regen_items.get_items())
    item_string = ""
    for num, item in enumerate(regen_items.get_items()):
        if (num+1 < num_items): item_string += item.get_label() + ", "
        else:
            if (num > 1):
                item_string = item_string[:-1] + " and " + item.get_label()
            else:
                item_string = item.get_label()

    print("Manasit analysis for creating " + rune.label + " runes using...")
    print(item_string + ":")
    print()
    print("Casts per second: " + str(cast_ps))
    print("Soul points per second: " + str(sp_ps))
    print("Runes per second: " + str(nout_ps))
    print("Profit per second: " + str(profit_ps))
    print("Mana used per second: " + str(regen_items.get_mps()))
    print()
    print("Casts per minute: " + str(cast_ps*60))
    print("Soul points per minute: " + str(sp_ps*60))
    print("Runes per minute: " + str(nout_ps*60))
    print("Profit per minute: " + str(profit_ps*60))
    print("Mana used per minute: " + str(regen_items.get_mps()*60))
    print()
    print("Casts per hour: " + str(cast_ps*3600))
    print("Soul points per hour: " + str(sp_ps*3600))
    print("Runes per hour: " + str(nout_ps*3600))
    print("Profit per hour: " + str(profit_ps*3600))
    print("Mana used per hour: " + str(regen_items.get_mps()*3600))
    print()

def calculate_profit_rate(rune, mana_ps, cost_ps, blank_rune_price):
    cast_ps = mana_ps / rune.mp
    nout_ps = rune.nout * cast_ps
    profit_ps = rune.price * nout_ps - blank_rune_price * cast_ps - cost_ps

    return profit_ps


#---------------------------------------------------------------------------#
#                             SCRIPT PART                                   #
#---------------------------------------------------------------------------#

mushrooms = create_foodregen(1000/(7*60+20)*20, "Sorcerer", True)
mushrooms.report()
print()

softboots = create_softboots()
softboots.report()
print()

lifering = create_lifering(350)
lifering.report()
print()

ringofhealing = create_ringofhealing(1200)
ringofhealing.report()
print()

manapots = create_potion("Great Mana Potion", 95, 1, False)
manapots.report()
print()
manapots = create_potion("Great Mana Potion", 95, 1, True)

item_list_softlife = regen_item_list([mushrooms, softboots, lifering], True)
item_list_softroh = regen_item_list([mushrooms, softboots, ringofhealing], True)
item_list_fullpots = regen_item_list([mushrooms, softboots, ringofhealing, manapots], True)
item_list_potsonly = regen_item_list([manapots], True)
item_list_foodonly = regen_item_list([mushrooms], True)

blank_rune_price = 10

gfb_rune = create_rune_gfb(45)
gfb_rune.report()
sd_rune = create_rune_sd(108)
sd_rune.report()

analyze_manasit(gfb_rune, item_list_foodonly, blank_rune_price)
analyze_manasit(gfb_rune, item_list_softlife, blank_rune_price)
analyze_manasit(gfb_rune, item_list_softroh, blank_rune_price)
analyze_manasit(gfb_rune, item_list_potsonly, blank_rune_price)
analyze_manasit(gfb_rune, item_list_fullpots, blank_rune_price)

print()
print()

analyze_manasit(gfb_rune, item_list_softroh, blank_rune_price)
analyze_manasit(sd_rune, item_list_softroh, blank_rune_price)
