<img width="650" height="565" alt="image" src="https://github.com/user-attachments/assets/419bbc07-85f7-4353-931d-01ceb8447f40" />
可以一键生成陈氏er图,无需手动拖拽,把自己的数据库表给ai,让他根据json格式来生成代码即可,各大ai均可实现此功能
格式:
{
  "direction": "TB",
  "entities": [
   { "id": "SITE", "name": "运营点", "attributes": [
      { "name": "编号", "isKey": true }, { "name": "名称" }, { "name": "城市" },
      { "name": "地址" }, { "name": "电话" }, { "name": "启用" }
    ]},
    { "id": "GUEST_ROOM", "name": "客房", "attributes": [
      { "name": "编号", "isKey": true }, { "name": "运营点编号" }, { "name": "房号" },
      { "name": "房类编号" }, { "name": "楼层" }, { "name": "使用状态" }
    ]}
    ],
     "relationships": [
    { "id": "R1", "name": "订房", "between": [
      { "entityId": "SITE", "cardinality": "1" }, { "entityId": "GUEST_ROOM", "cardinality": "N" }
    ]}
    ]
    }
    
    
运行步骤
1.pip install
2.根据格式修改.json文件
3.运行后将文件内的.drawio文件导入到draw.io里
  此时你会发现排版有点不行,如下图
  <img width="650" height="565" alt="image" src="https://github.com/user-attachments/assets/4324e271-f785-4758-80ae-def8ef1493a1" />
  那么你需要点击调整图形->布局->力导向图,间距输入100即可形成一个不错的图像
  
  操作方式:<img width="779" height="809" alt="image" src="https://github.com/user-attachments/assets/c9087b34-6038-4941-be86-31478139aad3" />

  效果图:<img width="680" height="734" alt="image" src="https://github.com/user-attachments/assets/7c652032-0a8a-4f6a-8f96-0239a220e3df" />

  


todo:
1.生成的er图紧凑,很多线都重叠了,需要自己手动排版,不方便,下一步会自动处理排版
2. ...
