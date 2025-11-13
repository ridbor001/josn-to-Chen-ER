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

todo:
1.生成的er图紧凑,很多线都重叠了,需要自己手动排版,不方便,下一步会自动处理排版
2. ...
