from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import json
from pathlib import Path

def prettify_xml(elem) -> str:
    rough = tostring(elem, encoding='utf-8')
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

def make_cell(root, _id, parent, value="", style="", vertex=False, edge=False,
              x=None, y=None, w=None, h=None, source=None, target=None):
    cell = SubElement(root, "mxCell", id=str(_id))
    if value is not None:
        cell.set("value", value)
    if style:
        cell.set("style", style)
    cell.set("parent", str(parent))
    if vertex:
        cell.set("vertex", "1")
    if edge:
        cell.set("edge", "1")
    geo = SubElement(cell, "mxGeometry", attrib={"as": "geometry"})
    if edge:
        geo.set("relative", "1")
    else:
        geo.set("x", str(x or 0))
        geo.set("y", str(y or 0))
        geo.set("width", str(w or 120))
        geo.set("height", str(h or 60))
    if source:
        cell.set("source", str(source))
    if target:
        cell.set("target", str(target))
    return cell

def generate_drawio(schema: dict):
    mxfile = Element("mxfile", host="app.diagrams.net")
    diagram = SubElement(mxfile, "diagram", name="Chen ER")
    model = SubElement(diagram, "mxGraphModel", dx="1600", dy="1200", grid="1", gridSize="10",
                       guides="1", tooltips="1", connect="1", arrows="1", fold="1",
                       page="1", pageScale="1", pageWidth="1920", pageHeight="1080",
                       math="0", shadow="0")
    root = SubElement(model, "root")
    SubElement(root, "mxCell", id="0")
    SubElement(root, "mxCell", id="1", parent="0")

    # 布局参数
    ENT_W, ENT_H, ATTR_W, ATTR_H, REL_W, REL_H = 140, 60, 120, 40, 110, 70
    X_LEFT, X_RIGHT, X_MID = 140, 760, 470
    Y_START, Y_STEP = 80, 140

    ent_pos, ent_cell_id = {}, {}

    # 生成实体
    for i, e in enumerate(schema.get("entities", [])):
        eid = e.get("id", f"E{i}")
        name = e.get("name", eid)
        col = i % 2
        x = X_LEFT if col == 0 else X_RIGHT
        y = Y_START + (i // 2) * Y_STEP
        style = "shape=rectangle;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;"
        make_cell(root, eid, "1", f"实体：{name}", style, True, False, x, y, ENT_W, ENT_H)
        ent_pos[eid] = (x + ENT_W/2, y + ENT_H/2)
        ent_cell_id[eid] = eid

        for ai, a in enumerate(e.get("attributes", [])[:7]):
            aname = a.get("name") if isinstance(a, dict) else a
            is_key = a.get("isKey") if isinstance(a, dict) else False
            a_id = f"{eid}_A{ai}"
            a_label = f"{'PK: ' if is_key or str(aname).lower()=='id' else ''}{aname}"
            a_style = "shape=ellipse;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;"
            if is_key or str(aname).lower() == "id":
                a_style += "strokeWidth=3;"
            ax = x - 180 + (ai % 2) * 360
            ay = y - 60 + (ai // 2) * 40
            make_cell(root, a_id, "1", a_label, a_style, True, False, ax, ay, ATTR_W, ATTR_H)
            make_cell(root, f"{a_id}_E", "1", "", "endArrow=none;strokeColor=#000000;",
                      False, True, source=a_id, target=eid)

    # 生成关系
    for ri, r in enumerate(schema.get("relationships", [])):
        rid, rname = r.get("id", f"R{ri}"), r.get("name", f"R{ri}")
        parts = r.get("between", [])
        if len(parts) >= 2:
            e1, e2 = parts[0]["entityId"], parts[1]["entityId"]
            x1, y1 = ent_pos.get(e1, (X_MID, Y_START))
            x2, y2 = ent_pos.get(e2, (X_MID, Y_START + 100))
            rx, ry = (x1 + x2)/2 - REL_W/2, (y1 + y2)/2 - REL_H/2
        else:
            rx, ry = X_MID - REL_W/2, Y_START + ri * Y_STEP
        r_style = "shape=rhombus;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;"
        make_cell(root, rid, "1", rname, r_style, True, False, rx, ry, REL_W, REL_H)
        for pi, p in enumerate(parts):
            eid, card = p["entityId"], p.get("cardinality", "")
            make_cell(root, f"{rid}_E{pi}", "1", card,
                      "endArrow=none;strokeColor=#000000;labelBackgroundColor=#ffffff;",
                      False, True, source=eid, target=rid)

    return prettify_xml(mxfile)

# 示例用法
with open("chen_er_schema (1).json", "r", encoding="utf-8") as f:
    schema = json.load(f)
xml_text = generate_drawio(schema)
Path("output_er.drawio").write_text(xml_text, encoding="utf-8")
print("✅ 生成完成：output_er.drawio")
