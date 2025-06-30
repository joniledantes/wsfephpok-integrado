import xml.etree.ElementTree as ET

# Archivos de entrada y salida
input_file = "C:\\Users\\Viaweb\\Desktop\\wordpress_export.xml"
output_file = "C:\\Users\\Viaweb\\Desktop\\wordpress_export_sin_duplicados.xml"

# Cargar el XML
tree = ET.parse(input_file)
root = tree.getroot()
channel = root.find("channel")

# Diccionario para almacenar contenido único
contenido_unico = {}
items_a_eliminar = []

# Recorrer cada <item> (página)
for item in channel.findall("item"):
    content = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")

    if content is not None and content.text:
        contenido_texto = content.text.strip()

        # Si el contenido ya existe en el diccionario, marcarlo para eliminar
        if contenido_texto in contenido_unico:
            items_a_eliminar.append(item)
        else:
            contenido_unico[contenido_texto] = item

# Eliminar los elementos duplicados
for item in items_a_eliminar:
    channel.remove(item)

# Guardar el XML limpio
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"✅ Archivo limpio generado: {output_file}")
