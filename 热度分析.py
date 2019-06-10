import pymongo
from matplotlib import pyplot as plt
import matplotlib

def main():
    client = pymongo.MongoClient(host="localhost",port=27017)
    db = client["jd_phone"]
    collection = db["JdPhoneItem"]
    results = collection.find()#由数据库中调出数据
    store = []
    for result in results:
        shop = {}
        if result["sale"]=='销量较少':
            result['sale']=0
        shop['store']=result['store']
        shop['heat']=result['sale']
        store.append(shop)
    heat = {}
    for each in store:
        if each["store"] not in heat.keys():
            heat.setdefault(each['store'],0)
            heat[each['store']]+=each['heat']
        else:
            heat[each['store']] += each['heat']

    heats = sorted(heat.items(),key=lambda y:y[1],reverse=True)#正向排序
    data = heats[0:10]
    names = list(map(lambda x:x[0],data))
    namess = []
    for name in names:
        name = name[0:len(name)//2]+"\n"+name[len(name)//2:]
        namess.append(name)#店名
    hts = list(map(lambda x:x[1],data))#热度
    matplotlib.rc('font',family='FangSong_GB2312',
                  weight='bold',
                  size=23
                  )

    plt.figure(figsize=(40,20),dpi=100)
    plt.bar(range(len(namess)),hts,width=0.3)
    plt.xticks(range(len(namess)),namess,rotation=45)
    plt.xlabel("商店名")
    plt.ylabel("热度系数 单位(问题数)")
    plt.title("京东手机销售热度排行",fontsize=45)
    plt.grid(alpha=0.5)#透明度0.5
    plt.savefig("./redu.png")
    plt.show()

if __name__ == '__main__':
    main()