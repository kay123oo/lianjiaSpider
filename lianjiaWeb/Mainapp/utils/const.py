class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


const = _const()
const.PRICE_00 = 0
const.PRICE_01 = 1
const.PRICE_02 = 2
const.PRICE_03 = 3
const.PRICE_04 = 4
const.PRICE_05 = 5
const.PRICE_06 = 6
const.PRICE_07 = 7
const.RENT_TYPE_00 = 0
const.RENT_TYPE_01 = 1
const.RENT_TYPE_02 = 2
const.ORIENTATION_00 = 0
const.ORIENTATION_01 = 1
const.ORIENTATION_02 = 2
const.ORIENTATION_03 = 3
const.ORIENTATION_04 = 4
const.HOUSE_TYPE_00 = 0
const.HOUSE_TYPE_01 = 1
const.HOUSE_TYPE_02 = 2
const.HOUSE_TYPE_03 = 3
const.FLOOR_LOW = 0
const.FLOOR_MID = 1
const.FLOOR_HIGH = 2
const.ELEVATOR = 0
const.NO_ELEVATOR = 1


