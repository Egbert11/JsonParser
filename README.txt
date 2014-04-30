说明文档：
test.json为测试文档，将test.json与JsonParser.py放在同一个目录下，然后运行JsonParser.py即可。result.json为测试用例的输出文件。

JsonParser.py内的类和函数说明：
JsonParser类：
1、load(self, s),读取json格式数据,输入s为一个json字符串,无返回值。为简便考虑,json的最外层假定只为object
2、dump(self),根据类中数据返回json字符串

3、loadJson(self, f),从文件中读入json格式数据,f为文件路径,异常处理同1,文件操作失败抛出异常

4、dumpJson(self, f),将类中的内容以json格式存入文件,文件若存在则覆盖,文件操作失败抛出异常

5、loadDict(self, d),读取dict中的数据,存入类中,若遇到不是字符串的key则忽略
6、dumpDict(self),返回一个字典,包含类中数据

7、__getitem__(self, key),用方括号操作符访问json数据
8、__setitem__(self, key, value),用方括号操作符设置json数据
9、__delitem__(self, key),用方括号操作符删减json数据
10、__getslice__(self, i, j),用方括号操作符以及切片来访问json数据
11、update(self, d),更新json数据

深度复制：
1、deepcopy(data）,选择对应深度复制的函数
2、deepcopy_dict(data),字典深度复制
3、deepcopy_list(data),列表深度复制
4、deepcopy_tuple(data),元组深度复制


打印函数  Python->Json:
1、def dump_json(buffer, data),选择对应的转换函数
2、dump_object(buffer, data),将dict转化为object
3、dump_array(buffer, data),将list,tuple转化为array
4、dump_string(buffer, data),将string转化为Json格式的字符串
5、dump_num(buffer, data),将int,float转为Json格式的字符串
6、dump_bool(buffer, data),将bool类型转为Json格式的字符串
7、dump_null(buffer, data),将None转为null
   

解析函数  Json->Python:
1、parse_object(s, pos),object -> dict
2、parse_string(s, pos),string -> unicode
3、parse_array(s, pos),array -> list
4、parse_num(s, pos),number -> int, long, float
5、parse_scan(s, pos),Json -> Python扫描匹配项
6、skip_blank(s, pos, s_expect),跳过空格
7、is_hex_str(s),用于判断是否属于十六进制编码的字符


各种异常类:
1、JsonInvalidException(Exception),Json格式错误
2、JsonInvalidEndException(JsonInvalidException),非法结尾
3、JsonUnexpectedCharException(JsonInvalidException),遇到不正确的字符
4、JsonInvalidEscapeException(JsonInvalidException),遇到不正确的转义字符
5、JsonInvalidTypeException(JsonInvalidException),未知的数据类型

