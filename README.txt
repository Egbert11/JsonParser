˵���ĵ���
test.jsonΪ�����ĵ�����test.json��JsonParser.py����ͬһ��Ŀ¼�£�Ȼ������JsonParser.py���ɡ�result.jsonΪ��������������ļ���

JsonParser.py�ڵ���ͺ���˵����
JsonParser�ࣺ
1��load(self, s),��ȡjson��ʽ����,����sΪһ��json�ַ���,�޷���ֵ��Ϊ��㿼��,json�������ٶ�ֻΪobject
2��dump(self),�����������ݷ���json�ַ���

3��loadJson(self, f),���ļ��ж���json��ʽ����,fΪ�ļ�·��,�쳣����ͬ1,�ļ�����ʧ���׳��쳣

4��dumpJson(self, f),�����е�������json��ʽ�����ļ�,�ļ��������򸲸�,�ļ�����ʧ���׳��쳣

5��loadDict(self, d),��ȡdict�е�����,��������,�����������ַ�����key�����
6��dumpDict(self),����һ���ֵ�,������������

7��__getitem__(self, key),�÷����Ų���������json����
8��__setitem__(self, key, value),�÷����Ų���������json����
9��__delitem__(self, key),�÷����Ų�����ɾ��json����
10��__getslice__(self, i, j),�÷����Ų������Լ���Ƭ������json����
11��update(self, d),����json����

��ȸ��ƣ�
1��deepcopy(data��,ѡ���Ӧ��ȸ��Ƶĺ���
2��deepcopy_dict(data),�ֵ���ȸ���
3��deepcopy_list(data),�б���ȸ���
4��deepcopy_tuple(data),Ԫ����ȸ���


��ӡ����  Python->Json:
1��def dump_json(buffer, data),ѡ���Ӧ��ת������
2��dump_object(buffer, data),��dictת��Ϊobject
3��dump_array(buffer, data),��list,tupleת��Ϊarray
4��dump_string(buffer, data),��stringת��ΪJson��ʽ���ַ���
5��dump_num(buffer, data),��int,floatתΪJson��ʽ���ַ���
6��dump_bool(buffer, data),��bool����תΪJson��ʽ���ַ���
7��dump_null(buffer, data),��NoneתΪnull
   

��������  Json->Python:
1��parse_object(s, pos),object -> dict
2��parse_string(s, pos),string -> unicode
3��parse_array(s, pos),array -> list
4��parse_num(s, pos),number -> int, long, float
5��parse_scan(s, pos),Json -> Pythonɨ��ƥ����
6��skip_blank(s, pos, s_expect),�����ո�
7��is_hex_str(s),�����ж��Ƿ�����ʮ�����Ʊ�����ַ�


�����쳣��:
1��JsonInvalidException(Exception),Json��ʽ����
2��JsonInvalidEndException(JsonInvalidException),�Ƿ���β
3��JsonUnexpectedCharException(JsonInvalidException),��������ȷ���ַ�
4��JsonInvalidEscapeException(JsonInvalidException),��������ȷ��ת���ַ�
5��JsonInvalidTypeException(JsonInvalidException),δ֪����������

