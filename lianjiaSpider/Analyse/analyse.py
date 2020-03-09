from pyecharts.charts import Bar, Line
import pymongo
import pandas as pd
import numpy as np
from pymongo import MongoClient

conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('lianjia')  # 连接到Lianjia数据库

zufang = db.get_collection('zufang_sh') # 连接到集合zufang
mon_data = zufang.find()  # 查询这个集合下的所有记录
lianjia_df=pd.DataFrame(list(mon_data))

zone_price=pd.merge(data.groupby(['所在区'])['单价(元/平米)'].mean().round(0).sort_values(ascending=False).to_frame().reset_index(),data.groupby(['所在区'])['总价(万元)'].mean().round(0).to_frame().reset_index(),on=['所在区'])
bar = Bar("北京各区二手房价格")
bar.add("单价(元/平米)", zone_price['所在区'], zone_price['单价(元/平米)'],is_label_show=True,label_pos='inside',label_text_color ='#000',is_toolbox_show=False,)
line = Line()
line.add("总价(万元)", zone_price['所在区'], zone_price['总价(万元)'],is_label_show=True,is_toolbox_show=False,)

overlap = Overlap(height=400,width=900)
overlap.add(bar)
overlap.add(line,yaxis_index=1, is_add_yaxis=True,)
overlap

