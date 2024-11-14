import spacy
import os

# 加载中文模型（需要先安装模型：python -m spacy download zh_core_web_trf）
nlp = spacy.load('zh_core_web_trf')

# 输入文本
text = "大家好，我们集体观影活动定于11月16日周六上午9：00—12：00，地点是王克桢楼1206"

# 处理文本
doc = nlp(text)

# 初始化列表
times = []
locations = []
events = []

# 提取实体
for ent in doc.ents:
    if ent.label_ == 'DATE':
        times.append(ent.text)
    elif ent.label_ in ('GPE', 'LOC'):
        locations.append(ent.text)
    elif ent.label_ == 'EVENT':
        events.append(ent.text)

# 输出结果
print("时间:", times)
print("地点:", locations)
print("事件:", events)