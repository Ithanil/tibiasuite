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
        print("Regen report for " +  self.__label)
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
        self.set_list(item_list)

    def set_resting_area(self, resting_area):
        if (resting_area == True):
            self.__rafac = 2.0
        else:
            self.__rafac = 1.0
    
    def set_list(self, item_list):
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

    def get_item_list(self):
        return self.__item_list

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
                "Health Potion" : [100, 0]
              }

    if (resting_area == True):
        for key in potsmap:
            potsmap[key][0] *= 0.5 # atm we apply resting area boni to all regen_item, but ingame pots are not affected
            potsmap[key][1] *= 0.5

    return regen_item(label = type, hps = potsmap[type][0] / cd, mps = potsmap[type][1] / cd, cost = cost, duration = cd)

mushrooms = create_foodregen(1000/(7*60+20)*20, "Sorcerer", True)
mushrooms.report()
print()

softboots = create_softboots()
softboots.report()
print()

lifering = create_lifering(300)
lifering.report()
print()

manapots = create_potion("Mana Potion", 45, 1, False)
manapots.report()
print()
manapots = create_potion("Mana Potion", 45, 1, True)

item_list = regen_item_list([mushrooms, softboots, lifering], True)
#item_list = regen_item_list([mushrooms, softboots, lifering, manapots], True)
#item_list = regen_item_list([mushrooms], True)

gfb_mp = 530
gfb_sp = 3
gfb_out = 4
gfb_price = 44

gfb_ps = item_list.get_mps() / gfb_mp
gfb_sp_ps = gfb_sp * gfb_ps
gfb_out_ps = gfb_out * gfb_ps
gfb_gold_ps = gfb_price * gfb_out_ps - item_list.get_costps() 

print("GFB casts per second: " + str(gfb_ps))
print("GFB soul points per second: " + str(gfb_sp_ps))
print("GFB runes per second: " + str(gfb_out_ps))
print("GFB gold per second: " + str(gfb_gold_ps))
print("Mana used per second: " + str(item_list.get_mps()))
print()
print("GFB casts per minute: " + str(gfb_ps*60))
print("GFB soul points per minute: " + str(gfb_sp_ps*60))
print("GFB runes per minute: " + str(gfb_out_ps*60))
print("GFB gold per minte: " + str(gfb_gold_ps*60))
print("Mana used per minute: " + str(item_list.get_mps()*60))
print()
print("GFB casts per hour: " + str(gfb_ps*3600))
print("GFB soul points per hour: " + str(gfb_sp_ps*3600))
print("GFB runes per hour: " + str(gfb_out_ps*3600))
print("GFB gold per hour: " + str(gfb_gold_ps*3600))
print("Mana used per hour: " + str(item_list.get_mps()*3600))
