

# 链接数据库
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['lianjia']
mydb = db['BOOK']
if __name__ == "__main__":
    price ='2100-2300'
    index = price.index('-')
    min = price[:index]
    max = price[index+1:]
    print(min)
    print(max)

