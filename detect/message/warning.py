from const import const
from datetime import datetime


class warningMessage(object):
    def __init__(self):
        key_list = const.ROI_name
        value_list = []
        for i in range(len(const.ROI_name)):
            value_list.append([])
        self.message = dict(zip(key_list, value_list))
        self.lasttime = datetime.now()

    def update(self, cls, num, mes):
        if num >= len(self.message[const.ROI_name[cls]]):
            while num - len(self.message[const.ROI_name[cls]]) > 0:
                self.message[const.ROI_name[cls]].append(None)
            self.message[const.ROI_name[cls]].append(mes)
            return True
        if self.message[const.ROI_name[cls]][num] is None:
            self.message[const.ROI_name[cls]][num] = mes
            return True
        if "Car not matched with armor" in self.message[const.ROI_name[cls]][num]:
            if "detected enermy" in mes:
                self.message[const.ROI_name[cls]][num] = mes
                return True
        return False

    def refresh(self):
        if (datetime.now()-self.lasttime).total_seconds() > 5:
            self.clear()
            self.lasttime = datetime.now()

    def clear(self):
        for key in self.message.keys():
            self.message[key] = []

    def show(self):
        print(self.message)


if __name__ == "__main__":
    a = warningMessage()
    a.show()
    a.update(0, 5, "Car not matched with armor")
    a.show()
    a.update(0, 5, "detected enermy")
    a.show()
    import time
    time.sleep(15)
    a.update(0, 5, "Car not matched with armor")
    a.show()
