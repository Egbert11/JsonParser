#-*-coding:utf-8-*-
__author__ = 'Administrator'

#无效字符，应跳过
STRIP_TAB = [u' ', u'\t', u'\r', u'\n']

#Json->Python 转义字符的转换
ESCAPE_DICT = {
    u'"': u'"',
    u'\\': u'\\',
    u'/': u'/',
    u'b': u'\b',
    u'f': u'\f',
    u'n': u'\n',
    u'r': u'\r',
    u't': u'\t',
    u'u': None,
}

#Python->Json转义字符的转换
RE_ESCAPE_DICT = {
        u'"': u'\\"',
        u'\\': u'\\\\',
        u'/': u'\\/',
        u'\b': u'\\b',
        u'\f': u'\\f',
        u'\n': u'\\n',
        u'\r': u'\\r',
        u'\t': u'\\t',
}

###########################################################
'''
深度复制
'''

def deepcopy(data):
    '''
    选择对应深度复制的函数
    '''
    if isinstance(data, list):
        return deepcopy_list(data)
    elif isinstance(data, tuple):
        return deepcopy_tuple(data)
    elif isinstance(data, dict):
        return deepcopy_dict(data)
    elif isinstance(data, (int, long, float, str, unicode, bool, type(None))):
        return data
    else:
        raise JsonInvalidTypeException(type(data))

def deepcopy_dict(data):
    '''
    字典深度复制
    '''
    assert type(data) == type({})

    result = {}
    for k, v in data.iteritems():
        result[deepcopy(k)] = deepcopy(v)
    return result


def deepcopy_list(data):
    '''
    列表深度复制
    '''
    assert isinstance(data, list)

    result = []
    for item in data:
        result.append(deepcopy(item))
    return result

def deepcopy_tuple(data):
    '''
    元组深度复制
    '''
    assert isinstance(data, tuple)

    result = ()
    for item in data:
        result.append(deepcopy(item))
    return result

###########################################################
'''
打印函数  Python->Json
'''

def dump_json(buffer, data):
    if isinstance(data, dict):
        dump_object(buffer, data)
    elif isinstance(data, (list, tuple)):
        dump_array(buffer, data)
    elif isinstance(data, (bool)):
        dump_bool(buffer, data)
    elif isinstance(data, (str, unicode)):
        dump_string(buffer, data)
    elif isinstance(data, (int, float)):
        dump_num(buffer, data)
    elif type(data) == type(None):
        dump_null(buffer, data)
    else:
        raise JsonInvalidTypeException(type(data))

def dump_object(buffer, data):
    '''
    将dict转化为object
    '''
    #count 用于计算dict的项数
    count = 0
    buffer.append(u'{')
    for k, v in data.iteritems():
        count += 1
        dump_json(buffer, k)
        buffer.append(u':')
        dump_json(buffer, v)
        if count < len(data):
            buffer.append(u', ')
    buffer.append(u'}')

def dump_array(buffer, data):
    '''
    将list,tuple转化为array
    '''
    #count 用于计算list或tuple的项数
    count = 0
    buffer.append(u'[')
    for v in data:
        count += 1
        dump_json(buffer, v)
        if count < len(data):
            buffer.append(u', ')
    buffer.append(u']')

def dump_string(buffer, data):
    '''
    将string转化为Json格式的字符串
    '''
    s = []
    for c in data:
        if c in RE_ESCAPE_DICT.keys(): #转义字符的转化
            s.append(RE_ESCAPE_DICT[c])
        elif c >= 32 and c <= 126:  #可打印的字符
            s.append(c)
        elif c >= u'\u4e00'and c <= u'\u9fa5':#汉字
            s.append(u'\\u%x' % ord(c))
        else:#其他
            s.append(c)
    buffer.append(u'"%s"' % ''.join(s))


def dump_num(buffer, data):
    '''
    将int,float转为Json格式的字符串
    '''
    buffer.append(u'%s' % data)


def dump_bool(buffer, data):
    if data:
        buffer.append(u'true')
    else:
        buffer.append(u'false')

def dump_null(buffer, data):
    buffer.append(u'null')
###########################################################
'''
解析函数  Json->Python
'''

def parse_object(s, pos):
    '''
    object -> dict
    '''
    pos = skip_blank(s, pos, u'an object')
    assert s[pos] == u'{'
    pos += 1
    d = {}

    try:
        while True:
            pos = skip_blank(s, pos, u'a string or a }')
            c = s[pos]
            if c == u'}':
                break
            #寻找字典的key
            key, pos = parse_scan(s, pos)
            pos = skip_blank(s, pos, u'a :')
            c = s[pos]
            if c != u':':
                raise JsonUnexpectedCharException(u':', c)
            #跳过':'
            pos += 1
            #寻找字典的值
            pos = skip_blank(s, pos, u'a value')
            val, pos = parse_scan(s, pos)
            d[key] = val
            #继续寻找键值对
            pos = skip_blank(s, pos, u'a , of a }')
            c = s[pos]
            #如果出现',',说明还有键值对
            if c == u',':
                pos += 1
            #如果出现'}'，说明字典结束
            c = s[pos]
            if c == u'}':
                break
    except IndexError:
        raise JsonInvalidEndException(u'a , or a }')
    return d, pos + 1



def parse_string(s, pos):
    '''
    string -> unicode
    '''
    pos = skip_blank(s, pos, u'a string')
    assert s[pos] == u'"'
    pos += 1
    chars = []
    try:
        while True:
            c = s[pos]
            pos += 1
            #字符串结束，返回当前字符串及'"'后一位置pos
            if c == u'"':
                break
            #遇上转义字符
            if c == u'\\':
                c = s[pos]
                #查表，以检查转义字符合法性
                if c not in ESCAPE_DICT.keys():
                    raise JsonInvalidEscapeException(c)
                c = ESCAPE_DICT[c]
                pos += 1
                #考虑u'uxxxx'的情况，其中x为16进制表示数
                if not c:
                    pos_next = pos + 4
                    digits = s[pos:pos_next]
                    pos = pos_next
                    if not is_hex_str(digits):
                        raise JsonInvalidEscapeException(u'u'+digits)
                    #如果合法，将u'uxxxx'转化为Unicode编码的字符
                    c = unichr(int(digits,16))
            chars.append(c)
    except IndexError:
        raise JsonInvalidEndException(u'next string character')
    return ''.join(chars), pos


def parse_array(s, pos):
    '''
    array -> list
    '''
    pos = skip_blank(s, pos, u'an array')
    assert s[pos] == u'['
    pos += 1
    array = []
    try:
        while True:
            pos = skip_blank(s, pos, u'a value or a ]')
            #如果是u']',则结束
            if s[pos] == u']':
                break
            val, pos = parse_scan(s, pos)
            array.append(val)
            #print s[pos]
            #继续查找value
            pos = skip_blank(s, pos, u'a , or a ]')
            #如果c为','，说明还有其他value
            if s[pos] == u',':
                pos += 1
            if s[pos] == u']':
                break
    except IndexError:
        raise JsonInvalidEndException(u'a , or a ]')
    return array, pos + 1


def parse_num(s, pos):
    '''
    number -> int, long, float
    '''
    pos = skip_blank(s, pos, u'a number')
    c = s[pos]
    pos += 1
    try:
        #判断底数是正数还是负数
        c, pos, negative = isNegative(c, s, pos)
        #result为求得的底数部分
        result, c, pos = getNumber(s, c, pos)
        #检查是否包含指数
        if c.lower() in u'e':
            result = float(result)
            c = s[pos]
            pos += 1
            exp_val = 0
            #检查指数是正数还是负数
            c, pos, exp_neg = isNegative(c, s, pos)
            while c.isdigit():
                exp_val *= 10
                exp_val +=strToInt(c)
                c = s[pos]
                pos += 1
            if exp_neg:
                exp_val = -exp_val
            #计算result
            result = result * (10 ** exp_val)
        #根据result的正负号计算最终的result
        if negative:
            result = -result
    except IndexError:
        raise JsonInvalidEndException(u'rest part of number %s' % repr(c))
    return result, pos - 1

def parse_scan(s, pos):
    '''
    Json -> Python扫描匹配项
    '''
    if s[pos] == u'"':
        return parse_string(s, pos)
    elif s[pos] == u'[':
        return parse_array(s, pos)
    elif s[pos] == u'{':
        return parse_object(s, pos)
    elif s[pos] == u'f' and s.startswith('false', pos, pos+5):
        return False, pos + 5
    elif s[pos] == u't' and s.startswith('true', pos, pos+4):
        return True, pos + 4
    elif s[pos] == u'n' and s.startswith('null', pos, pos+4):
        return None, pos + 4
    else:
        pass

    if s[pos].isdigit() or s[pos] in [u'+', u'-']:
        return parse_num(s, pos)
    raise JsonUnexpectedCharException(u'(", [, {, false, true, null, number)', u'(%s)' % s[pos])


def skip_blank(s, pos, s_expect):
    '''
    跳过空格
    '''
    try:
        while s[pos] in STRIP_TAB:
            pos += 1
    except IndexError:
            raise JsonInvalidEndException(s_expect)
    return pos

def is_hex_str(s):
    '''
    用于判断是否属于十六进制编码的字符
    '''
    if len(s) == 4:
        for c in s:
            if c.lower() not in u'0123456789abcdef':
                return False
        return True

#判断是否为负数
def isNegative(c, s, pos):
    negative = False
    if c == u'-':
        negative = True
        c = s[pos]
        pos += 1
    if c == u'+':
        negative = False
        c = s[pos]
        pos += 1
    return c, pos, negative

#将单个字符转变为对应的数字
def strToInt(c):
    if c == u'1':
        result = 1
    elif c == u'2':
        result = 2
    elif c == u'3':
        result = 3
    elif c == u'4':
        result = 4
    elif c == u'5':
        result = 5
    elif c == u'6':
        result = 6
    elif c == u'7':
        result = 7
    elif c == u'8':
        result = 8
    elif c == u'9':
        result = 9
    else:
        result = 0
    return result

#取得整数或浮点数
def getNumber(s, c, pos):
    result = 0
    #整数部分
    while True:
        if c.isdigit():
            result *= 10
            result += strToInt(c)
            c = s[pos]
            pos += 1
        else:
            break
    #小数部分
    if c == u'.':
        c = s[pos]
        pos += 1
        result = float(result)
        index = 0.1
        while c.isdigit():
            result += index * strToInt(c)
            index *= 0.1
            c = s[pos]
            pos += 1
    return result, c, pos
##################################################
'''
    各种异常
'''
class JsonInvalidException(Exception):
    '''
    Json格式错误
    '''

class JsonInvalidEndException(JsonInvalidException):
    '''
    非法结尾
    '''
    def __init__(self,s_expect):
        JsonInvalidException.__init__(self,
                u'Expect %s but reach end.' % s_expect)

class JsonUnexpectedCharException(JsonInvalidException):
    '''
    遇到不正确的字符
    '''
    def __init__(self, s_expect, s_meet):
        JsonInvalidException.__init__(self,
                u'Expect %s but meet %s.' % (s_expect, s_meet))

class JsonInvalidEscapeException(JsonInvalidException):
    '''
    遇到不正确的转义字符
    '''
    def __init__(self, c):
        JsonInvalidException.__init__(self,
                u'Invalid escape character %s.' % repr(c))

class JsonInvalidTypeException(JsonInvalidException):
    '''
    未知的数据类型
    '''
    def __init__(self, s_type):
        JsonInvalidException.__init__(self,
                u'Unknown type %s.' % s_type)

#####################################################################


class JsonParser:
    '''
    JsonParser类：能读取json格式的数据，并以Python字典的方式读写数据
    '''
    def __init__(self):
        self.data = None

    def load(self, s):
        '''
        读取json格式数据，输入s为一个json字符串，无返回值。
        若遇到json格式错误的应该抛出异常，json中数字如果超过了python里的浮点数上限的，也可以抛出异常
        为简便考虑，json的最外层假定只为object
        '''
        if type(s) != unicode:
            s = s.decode('utf-8')
        self.data, pos = parse_object(s, 0)

    def dump(self):
        '''
        根据类中数据返回json字符串
        '''
        buffer = []
        dump_json(buffer, self.data)
        return ''.join(buffer)

    def loadJson(self, f):
        '''
        从文件中读入json格式数据，f为文件路径，异常处理同load，文件操作失败抛出异常。
        '''
        try:
            file = open(f, 'r')
            self.load(file.read().decode(u'utf-8'))
        finally:
            file.close()


    def dumpJson(self, f):
        '''
        将类中的内容以json格式存入文件中，文件若存在则覆盖，文件操作失败抛出异常
        '''
        buffer = []
        dump_json(buffer, self.data)

        try:
            file = open(f, 'w')
            file.write(self.dump().encode(u'utf-8'))
        finally:
            file.close()

    def loadDict(self, d):
        '''
        读取dict中的数据，存入类中，若遇到不是字符串的key则忽略
        '''
        data = deepcopy(d)
        if self.data:#self.data不为空
            self.data.udpate(data)
        else:#self.data为空
            self.data = data

    def dumpDict(self):
        '''
        返回一个字典，包含类中数据
        '''
        return deepcopy(self.data)

    def __getitem__(self, key):
        '''
        用方括号操作符访问json数据
        '''
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        '''
        用方括号操作符设置json数据
        '''
        return self.data.__setitem__(key, value)

    def __delitem__(self, key):
        '''
        用方括号操作符删减json数据
        '''
        return self.data.__delitem__(key)


    def __getslice__(self, i, j):
        '''
        用方括号操作符以及切片来访问json数据
        '''
        return self.data.__getslice__(i, j)

    def update(self, d):
        '''
        更新json数据
        '''
        self.data.update(d)

if __name__ == '__main__':
    a1 = JsonParser()
    a2 = JsonParser()
    a3 = JsonParser()

    #基本功能测试用例
    jsonfile = u'test.json'
    test_json_file = open(jsonfile).read()

    a1.load(test_json_file)
    d1 = a1.dumpDict()

    file_path = u'result.json'
    a2.loadDict(d1)

    a2.dumpJson(file_path)
    a3.loadJson(file_path)
    d3 = a3.dumpDict()
    d4 = a2.update({'a':'a'})

    print '基本功能测试：'
    print 'd1:',d1
    print 'd3:',d3
    print 'd1和d3是否相等:',d1 == d3,'\n'  #测试d1和d3是否相等

    #进阶要求测试
    print '进阶要求测试：'
    print '删除a2的string键前：',a2.data
    del a2['string']
    print '删除a2的string键后：',a2.data,'\n'

    print '更改a2的object的值前：',a2.data
    a2['object']=[1,2,3]
    print '更改a2的object的值后：',a2.data,'\n'

    print 'a2对应array的值为：',a2['array']
    print '其中array的前两个值为：',a2['array'][0:2]