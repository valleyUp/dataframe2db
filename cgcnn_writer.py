import pandas as pd 
import pymysql
import json
from monty.json import MontyDecoder, MontyEncoder

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1',
    database='matDatabase'
)

sql_create_table = f"""
CREATE TABLE IF NOT EXISTS `material_feature` (
    uni_idx INT NOT NULL AUTO_INCREMENT,
    material_id VARCHAR(200) COMMENT 'material id from materials project',
    structure LONGTEXT COMMENT 'structure obj serialized as json',
    composition LONGTEXT COMMENT 'composition obj serialized as json',
    UNIQUE KEY (uni_idx)
)
"""

sql_insert = "INSERT INTO `material_feature` (material_id, structure, composition) VALUES (%s, %s, %s)"

CGCNN_DATA = '~/Downloads/id_prop_46744.json.gz'
MP_DATA = '~/Downloads/mp_2019_13w.json.gz'

data = pd.read_json(CGCNN_DATA)
# data2 = pd.read_json(MP_DATA)
data.structure = data.structure.apply(json.loads, cls=MontyDecoder)
cursor = conn.cursor()
cursor.execute(sql_create_table)
cursor.close()
conn.commit()
for i, mpp_id in enumerate(data['mp-id']):
    print(f"Inserting {mpp_id} into database...")
    structure = data['structure'].iloc[i]
    composition = structure.composition
    cursor = conn.cursor()
    cursor.execute(sql_insert, (mpp_id, json.dumps(structure, cls=MontyEncoder), json.dumps(composition, cls=MontyEncoder)))
    cursor.close()
    conn.commit()