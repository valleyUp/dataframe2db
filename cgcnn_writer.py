import pandas as pd 
import pymysql
import json
import numpy as np
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

CGCNN_DATA = '~/id_prop_46740.json.gz'

data = pd.read_json(CGCNN_DATA)
toWrite = data[['mp-id', 'structure', 'composition']]
toWrite = toWrite.to_numpy().tolist()
cursor = conn.cursor()
cursor.execute(sql_create_table)
cursor.close()
conn.commit()

cursor = conn.cursor()
cursor.executemany(sql_insert, toWrite)
cursor.close()
conn.commit()

sql_create_idx = """
CREATE TABLE IF NOT EXISTS `cgcnn_index` (
    uni_idx INT NOT NULL,
    isin_3402 TINYINT(1),
    isin_27430 TINYINT(1),
    isin_46740 TINYINT(1)
)
"""
sql_insert_idx = "INSERT INTO `cgcnn_index` (uni_idx, isin_3402, isin_27430, isin_46740) VALUES (%s, %s, %s, %s)"
idx_3402 = pd.read_csv('/home/gll/refRepo/cgcnn/data/material-data/mp-ids-3402.csv', header=None)[0]
idx_27430 = pd.read_csv('/home/gll/refRepo/cgcnn/data/material-data/mp-ids-27430.csv', header=None)[0]
idx_46744 = pd.read_csv('/home/gll/refRepo/cgcnn/data/material-data/mp-ids-46744.csv', header=None)[0]

idx = data['mp-id']
idx2Write = {
    'uni_idx': (np.arange(46740) + 1).tolist(), 
    '3402': idx.isin(idx_3402), 
    '27430': idx.isin(idx_27430), 
    '46744': idx.isin(idx_46744)
}
idx2Write = pd.DataFrame(idx2Write).astype(int)
cursor = conn.cursor()
cursor.execute(sql_create_idx)
cursor.close()
conn.commit()
cursor = conn.cursor()
cursor.execute(sql_create_idx)
cursor.executemany(sql_insert_idx, idx2Write.to_numpy().tolist())
cursor.close()
conn.commit()

sql_create_labels = """
CREATE TABLE IF NOT EXISTS `material_labels` (
    uni_idx INT NOT NULL,
    
    
)
"""