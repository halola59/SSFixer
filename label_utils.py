### 📄 label_utils.py
import xml.etree.ElementTree as ET

def load_labels(label_xml_path):
    labels = {}
    tree = ET.parse(label_xml_path)
    root = tree.getroot()

    ns = {
        "link": "http://www.xbrl.org/2003/linkbase",
        "xlink": "http://www.w3.org/1999/xlink",
        "label": "http://xbrl.org/2008/label"
    }

    locators = {}

    for loc in root.findall(".//link:loc", ns):
        href = loc.attrib.get("{http://www.w3.org/1999/xlink}href", "")
        label = loc.attrib.get("{http://www.w3.org/1999/xlink}label", "")
        if "#" in href:
            fragment = href.split("#")[-1]
            locators[label] = fragment

    for label_elem in root.findall(".//label:label", ns):
        label_id = label_elem.attrib.get("{http://www.w3.org/1999/xlink}label", "")
        text = label_elem.text.strip() if label_elem.text else ""
        concept_id = locators.get(label_id.replace("label_", "loc_"))
        if concept_id:
            labels[concept_id] = text

    return labels
