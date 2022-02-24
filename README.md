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



## Feeder Python with Extracted Text
> **PATH : ./Lib/Feed_Text/Gather_Text.py** 

```sh
/ES/Python-3.5.1/python /ES/ES_Feeder_Python/Lib/Feed_Text/Gather_Text.py
```
**Extract Text Log**  
```sh
[INFO] 2022-02-24 09:17:29,847 > @@@@@@@ not jpype.isJVMStarted() .. Retry.. @@@@@@
[INFO] 2022-02-24 09:17:29,908 > START...
[INFO] 2022-02-24 09:17:29,908 > doc >> /ES/ADSP_Summary.pdf [593890]
INFO  INSIDE ~ Text Extract Library
INFO  FILE SIZE ====>593890
INFO] 2022-02-24 09:17:31,259 > Call_Jar_Text ... 
he ADSp cover all Freight Forwarding Contracts undertak- 
en by the Freight Forwarder as contractor for all activities, regardless of whether they ar...
[INFO] 2022-02-24 09:17:31,268 > Finished...
```

## Feeder Python with Extracted Text through Socket Client
> **PATH : ./Lib/Feed_Text/Socket/Socket_Client.py** 

**Extract Text Log using Socket Client**  
```sh
INFO] 2022-02-24 10:37:54,745 > Connecting to Port => '127.0.0.1' 
[INFO] 2022-02-24 10:37:54,746 > Send => 'ECM;0900bf4b9816277d\n'
[INFO] 2022-02-24 10:37:56,146 > Received => 'S;tmp_ECM_0900bf4b9816277d_0900bf4b9816277d_1645667246307.pdf\n'
[INFO] 2022-02-24 10:37:56,498 > @@@@@@@ not jpype.isJVMStarted() .. Retry.. @@@@@@
[INFO] 2022-02-24 10:37:56,604 > START...
[INFO] 2022-02-24 10:37:56,604 > doc >> /ES/download_test/tmp_ECM_0900bf4b9816277d_0900bf4b9816277d_1645667246307.pdf [267960]
INFO  INSIDE ~ Text Extract Library
INFO  FILE SIZE ====>267960
WARN  Using fallback font WenQuanYiZenHei for CID-keyed TrueType font Gulim
WARN  Using fallback font WenQuanYiZenHei for CID-keyed TrueType font GulimChe
WARN  No Unicode mapping for CID+122 (122) in font OGCFMA+Wingdings-Regular
he ADSp cover all Freight Forwarding Contracts undertak- 
en by the Freight Forwarder as contractor for all activities, regardless of whether they ar...
[INFO] 2022-02-24 10:37:57,896 > Finished...
[INFO] 2022-02-24 10:37:57,896 > Socket Closed..
```
