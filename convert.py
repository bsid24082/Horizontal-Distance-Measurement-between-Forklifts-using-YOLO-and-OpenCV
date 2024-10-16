import os
import xml.etree.ElementTree as ET

# Function to convert Pascal VOC XML to YOLO format
def convert_voc_to_yolo(xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            image_width = int(root.find("size/width").text)
            image_height = int(root.find("size/height").text)
            
            output_file = os.path.join(output_folder, xml_file.replace(".xml", ".txt"))
            
            with open(output_file, "w") as f:
                for obj in root.findall("object"):
                    class_name = obj.find("name").text
                    bbox = obj.find("bndbox")
                    
                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)
                    
                    # Convert to YOLO format
                    x_center = (xmin + xmax) / 2 / image_width
                    y_center = (ymin + ymax) / 2 / image_height
                    width = (xmax - xmin) / image_width
                    height = (ymax - ymin) / image_height
                    
                    # Write class index and YOLO bounding box
                    f.write(f"0 {x_center} {y_center} {width} {height}\n")
                    
    print("XML to YOLO conversion complete.")

# Path to your XML annotations and output folder
xml_folder = "/Users/bsid24082/Documents/IIQ/forklict/collision1_frames"
output_folder = "/Users/bsid24082/Documents/IIQ/forklict/yolo_labels"

convert_voc_to_yolo(xml_folder, output_folder)