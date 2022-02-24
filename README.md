# Elastic_Feeder_Python
Feeed DB Datas with Attached File to Elastic Cluster


## Feeder Python with Sample DB to Elasticsearch Cluster
> installpath]  /TOM/ES/ES_Feeder_Python/Lib/Memory
> ['/TOM/ES/ES_Feeder_Python/Lib/DB/ojdbc6.jar', '/TOM/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/', '/TOM/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/*.jar', > '/TOM/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/DocumentsTextExtract-import-1.0_lib/*']

```sh
[INFO] 2022-02-24 08:57:41,100 > [Set_DB_Connect] Set DB Connection Environment
idx_list_dic  {'30': 'posco_purchase_item_idx'}
```

```sh
Initialze_delete_all_idx  PURCHASE_ITEM_NO {'30': 'posco_purchase_item_idx'}
```

```sh
No Date Options..

[INFO] 2022-02-24 08:57:41,484 > self.index_name >> purchase_item_idx
[INFO] 2022-02-24 08:57:41,484 > self.doctype >> _doc
[INFO] 2022-02-24 08:57:41,485 > self.elasticsearch_ip >> ['10.132.57.65:9201']

idx : purchase_item_idx
new_params : ['999', None, None]
```

**Indexing StringBuffer**  
