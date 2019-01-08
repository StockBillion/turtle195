#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, sys, numpy, datetime as dt, time
from matplotlib.pylab import date2num, num2date
from ttindex import TurTleIndex
from stock_utils import StockDataSource, StockDisp, StockAccount


hs300 = '000300.sh'
hs300_stocks = [
    ('sh', '603156', '养元饮品'), ('sh', '601138', '工业富联'), ('sz', '002001', '新和成'), ('sz', '000661', '长春高新'), ('sh', '600998', '九州通'), ('sz', '002179', '中航光电'), ('sh', '600004', '白云机场'), ('sz', '300296', '利亚德'), ('sh', '603986', '兆易创新'), ('sz', '002120', '韵达股份'), ('sz', '002311', '海大集团'), ('sz', '002422', '科伦药业'), ('sz', '002773', '康弘药业'), ('sh', '603259', '药明康德'), ('sh', '600027', '华电国际'), ('sz', '000408', '藏格控股'), 
    ('sz', '002271', '东方雨虹'), ('sh', '600566', '济川药业'), ('sz', '000703', '恒逸石化'), ('sz', '002032', '苏泊尔'), ('sz', '300142', '沃森生物'), ('sh', '601066', '中信建投'), ('sh', '600760', '中航沈飞'), ('sz', '300408', '三环集团'), ('sz', '000786', '北新建材'), ('sh', '601808', '中海油服'), ('sh', '600176', '中国巨石'), ('sh', '600438', '通威股份'), ('sz', '002493', '荣盛石化'), ('sz', '001965', '招商公路'), ('sz', '002625', '光启技术'), ('sz', '300433', '蓝思科技'), ('sz', '002925', '盈趣科技'), 
    ('sz', '002050', '三花智控'), ('sz', '002085', '万丰奥威'), ('sh', '600867', '通化东宝'), ('sh', '600809', '山西汾酒'), ('sh', '601838', '成都银行'), ('sh', '600339', '中油工程'), ('sh', '601108', '财通证券'), ('sh', '601360', '三六零'), ('sh', '600516', '方大炭素'), ('sh', '601238', '广汽集团'), ('sh', '600398', '海澜之家'), ('sh', '603288', '海天味业'), ('sh', '601828', '美凯龙'), ('sh', '600025', '华能水电'), ('sh', '600346', '恒力股份'), ('sh', '600487', '亨通光电'), ('sh', '603260', '合盛硅业'), ('sh', '603833', '欧派家居'), ('sh', '600011', '华能国际'), ('sh', '603799', '华友钴业'), ('sz', '002624', '完美世界'), ('sz', '002572', '索菲亚'), ('sz', '300003', '乐普医疗'), ('sz', '002468', '申通快递'), ('sz', '002601', '龙蟒佰利'), ('sh', '601012', '隆基股份'), ('sh', '600390', '五矿资本'), ('sz', '002294', '信立泰'), ('sz', '300136', '信维通信'), ('sz', '300015', '爱尔眼科'), ('sz', '000898', '鞍钢股份'), ('sh', '601212', '白银有色'), ('sh', '600219', '南山铝业'), 
    ('sh', '601898', '中煤能源'), ('sh', '601991', '大唐发电'), ('sz', '300122', '智飞生物'), ('sh', '601878', '浙商证券'), ('sz', '002460', '赣锋锂业'), ('sh', '601228', '广州港'), ('sz', '002555', '三七互娱'), ('sz', '002558', '世纪游轮'), ('sz', '002602', '世纪华通'), ('sh', '600233', '圆通速递'), ('sz', '002508', '老板电器'), ('sz', '002411', '必康股份'), ('sz', '002352', '顺丰控股'), ('sz', '002044', '美年健康'), ('sz', '000959', '首钢股份'), ('sz', '000961', '中南建设'), ('sh', '600436', '片仔癀'), ('sh', '600522', '中天科技'), ('sh', '600909', '华安证券'), ('sh', '603160', '汇顶科技'), ('sh', '603858', '步长制药'), ('sh', '601997', '贵阳银行'), ('sh', '601992', '金隅股份'), ('sh', '601881', '中国银河'), ('sh', '601229', '上海银行'), ('sh', '601117', '中国化学'), ('sh', '600977', '中国电影'), ('sh', '600926', '杭州银行'), ('sh', '600919', '江苏银行'), ('sh', '600549', '厦门钨业'), ('sh', '601155', '新城控股'), ('sz', '300033', '同花顺'), ('sz', '002466', '天齐锂业'), 
    ('sz', '000627', '天茂集团'), ('sz', '002714', '牧原股份'), ('sz', '300072', '三聚环保'), ('sh', '600482', '中国动力'), ('sz', '000983', '西山煤电'), ('sz', '000671', '阳光城'), ('sz', '000938', '紫光股份'), ('sh', '601611', '中国核建'), ('sz', '002797', '第一创业'), ('sz', '002310', '东方园林'), ('sh', '601877', '正泰电器'), ('sh', '600498', '烽火通信'), ('sh', '600297', '广汇汽车'), ('sz', '000839', '中信国安'), ('sz', '002027', '分众传媒'), ('sh', '600061', '国投安信'), ('sh', '600606', '绿地控股'), ('sh', '600704', '物产中大'), ('sh', '600816', '安信信托'), ('sz', '001979', '招商蛇口'), ('sz', '000415', '渤海租赁'), ('sz', '300144', '宋城演艺'), ('sh', '601198', '东兴证券'), ('sh', '601211', '国泰君安'), ('sh', '601985', '中国核电'), ('sz', '002736', '国信证券'), ('sz', '300059', '东方财富'), ('sh', '600958', '东方证券'), ('sh', '601021', '春秋航空'), ('sh', '601788', '光大证券'), ('sh', '601919', '中国远洋'), ('sz', '000166', '申万宏源'), 
    ('sh', '601727', '上海电气'), ('sh', '600570', '恒生电子'), ('sh', '600038', '哈飞股份'), ('sz', '300251', '光线传媒'), ('sz', '300124', '汇川技术'), ('sz', '300070', '碧水源'), ('sz', '300024', '机器人'), ('sz', '300017', '网宿科技'), ('sz', '002153', '石基信息'), ('sz', '000413', '东旭光电'), ('sh', '601216', '内蒙君正'), ('sh', '601225', '陕西煤业'), ('sh', '600023', '浙能电力'), ('sz', '002252', '上海莱士'), ('sz', '000503', '海虹控股'), ('sz', '002475', '立讯精密'), ('sz', '002008', '大族激光'), ('sz', '002456', '欧菲光'), ('sz', '002230', '科大讯飞'), ('sz', '002065', '东华软件'), ('sz', '000826', '桑德环境'), ('sh', '600018', '上港集团'), ('sh', '600688', '上海石化'), ('sh', '600705', '中航投资'), ('sz', '000333', '美的集团'), ('sz', '000963', '华东医药'), ('sz', '002450', '康得新'), ('sh', '600332', '广州药业'), ('sh', '603993', '洛阳钼业'), ('sz', '002236', '大华股份'), ('sz', '002673', '西部证券'), ('sh', '600157', '永泰能源'), ('sh', '600340', '华夏幸福'), 
    ('sh', '600637', '百视通'), ('sh', '600886', '国投电力'), ('sh', '601800', '中国交建'), ('sz', '002081', '金螳螂'), ('sz', '002241', '歌尔声学'), ('sh', '601336', '新华保险'), ('sh', '601555', '东吴证券'), ('sh', '601633', '长城汽车'), ('sh', '601669', '中国水电'), ('sh', '601901', '方正证券'), ('sh', '600372', '中航电子'), ('sz', '002594', '比亚迪'), ('sh', '601018', '宁波港'), ('sh', '601377', '兴业证券'), ('sh', '601933', '永辉超市'), ('sz', '000776', '广发证券'), ('sz', '002146', '荣盛发展'), ('sz', '002415', '海康威视'), ('sh', '600115', '东方航空'), ('sh', '600406', '国电南瑞'), ('sh', '600276', '恒瑞医药'), ('sh', '600535', '天士力'), ('sh', '600703', '三安光电'), ('sh', '600887', '伊利股份'), ('sh', '600893', '航空动力'), ('sh', '601818', '光大银行'), ('sh', '601288', '农业银行'), ('sz', '002304', '洋河股份'), ('sh', '600999', '招商证券'), ('sh', '601607', '上海医药'), ('sh', '601688', '华泰证券'), ('sh', '601888', '中国国旅'), ('sh', '601989', '中国重工'), 
    ('sz', '002007', '华兰生物'), ('sh', '600369', '西南证券'), ('sh', '601618', '中国中冶'), ('sh', '601668', '中国建筑'), ('sh', '600518', '康美药业'), ('sh', '601766', '中国南车'), ('sh', '600352', '浙江龙盛'), ('sh', '600588', '用友软件'), ('sh', '600674', '川投能源'), ('sh', '601186', '中国铁建'), ('sh', '601899', '紫金矿业'), ('sz', '000728', '国元证券'), ('sz', '000783', '长江证券'), ('sz', '002202', '金风科技'), ('sh', '601390', '中国中铁'), ('sh', '601601', '中国太保'), ('sh', '601939', '建设银行'), ('sh', '601169', '北京银行'), ('sh', '601009', '南京银行'), ('sh', '600111', '包钢稀土'), ('sh', '600089', '特变电工'), ('sz', '002142', '宁波银行'), ('sz', '000895', '双汇发展'), ('sz', '000423', '东阿阿胶'), ('sz', '000338', '潍柴动力'), ('sh', '600109', '国金证券'), ('sh', '601857', '中国石油'), ('sh', '601088', '中国神华'), ('sh', '601333', '广深铁路'), ('sz', '000876', '新希望'), ('sh', '600837', '海通证券'), ('sh', '600208', '新湖中宝'), ('sh', '601328', '交通银行'), 
    ('sh', '601998', '中信银行'), ('sh', '601600', '中国铝业'), ('sh', '601318', '中国平安'), ('sh', '601166', '兴业银行'), ('sh', '601628', '中国人寿'), ('sh', '600066', '宇通客车'), ('sh', '600118', '中国卫星'), ('sh', '600489', '中金黄金'), ('sh', '600048', '保利地产'), ('sh', '600068', '葛洲坝'), ('sh', '601111', '中国国航'), ('sh', '600547', '山东黄金'), ('sh', '601398', '工商银行'), ('sh', '601006', '大秦铁路'), ('sh', '601988', '中国银行'), ('sh', '600415', '小商品城'), ('sh', '600271', '航天信息'), ('sh', '600383', '金地集团'), ('sz', '000768', '西飞国际'), ('sz', '002024', '苏宁电器'), ('sz', '000538', '云南白药'), ('sz', '000157', '中联重科'), ('sz', '000425', '徐工科技'), ('sz', '000568', '泸州老窖'), ('sh', '600019', '宝钢股份'), ('sz', '000630', '铜陵有色'), ('sz', '000651', '格力电器'), ('sz', '000625', '长安汽车'), ('sz', '000709', '唐钢股份'), ('sz', '000792', '盐湖钾肥'), ('sz', '000063', '中兴通讯'), ('sz', '000402', '金融街'), ('sh', '600050', '中国联通'), 
    ('sh', '600036', '招商银行'), ('sh', '600031', '三一重工'), ('sh', '600030', '中信证券'), ('sh', '600029', '南方航空'), ('sh', '600015', '华夏银行'), ('sh', '600028', '中国石化'), ('sh', '600016', '民生银行'), ('sh', '600010', '包钢股份'), ('sh', '600009', '上海机场'), ('sh', '600900', '长江电力'), ('sh', '600795', '国电电力'), ('sh', '600739', '辽宁成大'), ('sh', '600741', '巴士股份'), ('sh', '600690', '青岛海尔'), ('sh', '600221', '海南航空'), ('sh', '600583', '海油工程'), ('sh', '600585', '海螺水泥'), ('sh', '600519', '贵州茅台'), ('sz', '000858', '五粮液'), ('sh', '600309', '烟台万华'), ('sh', '600196', '复星医药'), ('sh', '600000', '浦发银行'), ('sh', '600660', '福耀玻璃'), ('sh', '600085', '同仁堂'), ('sh', '600100', '同方股份'), ('sh', '600104', '上海汽车'), ('sh', '600153', '建发股份'), ('sh', '600188', '兖州煤业'), ('sh', '600177', '雅戈尔'), ('sh', '600170', '上海建工'), ('sh', '600362', '江西铜业')
]

cmdline = {
    'start_date': date2num(dt.datetime.strptime('20080101', '%Y%m%d')),
    'end_date': date2num(dt.datetime.strptime('20190201', '%Y%m%d')),
    'loss_unit': 0.01,
    "append": 1,
    'stop_loss': 3,
    'long_cycle': 55,
    'short_cycle': 20,
    'strong_cycle': 20,
    'data_path': './data-qfq-13',
    'stock_count': 20,
    'record_file': 'hs300'
}


def InputArgs():
    parser = argparse.ArgumentParser(description="show example")

    # parser.add_argument('hs300_stocks', default=['000300.sh'], nargs='*')
    parser.add_argument("-a", "--append", default=1, help="append")
    parser.add_argument("-c", "--count", default=20, help="stock count")
    parser.add_argument("-e", "--end_date", default='', help="end date")
    parser.add_argument("-f", "--record_file", default='hs300', help="record file")
    parser.add_argument("-l", "--stop_loss", default=3, help="stop loss")
    parser.add_argument("-p", "--data_path", default='./data-qfq-13', help="stock data path")
    parser.add_argument("-s", "--start_date", default='20070101', help="start date")
    parser.add_argument("-S", "--strong_cycle", default=20, help="strong cycle")
    parser.add_argument("-u", "--loss_unit", default=0.01, help="loss unit")

    ARGS = parser.parse_args()
    global cmdline

    if ARGS.start_date:
        _date = dt.datetime.strptime(str(ARGS.start_date), '%Y%m%d')
        cmdline['start_date'] = date2num(_date)
    if ARGS.end_date:
        _date = dt.datetime.strptime(str(ARGS.end_date), '%Y%m%d')
        cmdline['end_date'] = date2num(_date)

    if ARGS.data_path:
        cmdline['data_path'] = ARGS.data_path
    if ARGS.record_file:
        cmdline['record_file'] = ARGS.record_file
    if ARGS.count:
        cmdline['stock_count'] = int(ARGS.count)

    if ARGS.loss_unit:
        cmdline['loss_unit'] = float(ARGS.loss_unit)
    if ARGS.append:
        cmdline['append'] = int(ARGS.append)
    if ARGS.stop_loss:
        cmdline['stop_loss'] = int(ARGS.stop_loss)
    if ARGS.strong_cycle:
        cmdline['strong_cycle'] = int(ARGS.strong_cycle)
    # print( cmdline )


class StockSetData:
    
    @staticmethod
    def loaddata(start_index, end_index):
        datasrc = StockDataSource(cmdline['data_path'])
        datasrc.load(hs300, cmdline['start_date'], cmdline['end_date'], 'index', 'daily')
        print("load", hs300)

        for i in range(start_index, end_index):
            stock = hs300_stocks[i]
            datasrc.load(stock[1] + '.' + stock[0], cmdline['start_date'], 
                cmdline['end_date'], 'stock', 'daily')
            print("load", str(i), "stocks.")
            
    @staticmethod
    def MergeData(data_file = './hs300_all.daily.csv'):
        datasrc = StockDataSource(cmdline['data_path'])
        all_count = min(len(hs300_stocks), cmdline['stock_count'])
        _start_time = time.time()

        code = hs300_stocks[0][1] + '.' + hs300_stocks[0][0]
        stocks = datasrc._read(code, 'daily')

        for i in range(1, all_count):
            code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
            _stocks = datasrc._read(code, 'daily')
            stocks = stocks.append(_stocks, ignore_index=True)

            if i % 20 == 19:
                print('read', i+1, 'stocks data, run', time.time() - _start_time, 'seconds.')
        print('read', all_count, 'stocks data, run', time.time() - _start_time, 'seconds.')

        stocks.to_csv(data_file)
        print('write csv file', len(stocks), 'rows,', 'use time:', time.time()-_start_time, 'seconds')

    @staticmethod
    def parse_data(data_file):
        data_lists = {}

        _count = min(len(hs300_stocks), cmdline['stock_count'])
        for i in range(0, _count):
            code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
            data_lists[code.upper()] = []

        stock_data = StockDataSource.read_data_file(data_file)
        stock_data = stock_data.sort_index(ascending=False)
        rows = stock_data.values.tolist()
        print('stock_data length = ', len(stock_data))

        _last = len(rows) - 1
        for i in range(0, _last):
            tscode, trade_date, _open, high, low, close = rows[i][0:6]
            timenum = StockDataSource.float_date(trade_date)
            data_lists[tscode].append( (timenum, float(_open), float(high), float(low), float(close)) )

        return data_lists


class TurtleStrongTest:
    '海龟强势股测试'

    def __init__(self, max_sidx, max_count):
        self.max_sidx = max_sidx
        self.max_count = max_count
        self.scale = 1.0/max_count

        self.dataset = StockDataSource(cmdline['data_path'])
        self.all_count = min(len(hs300_stocks), cmdline['stock_count'])

        self.year = 0
        self.start = time.time()
        
        self.turtles = {}
        self.codes = []
        self.data_indexs = {}

        self.date_vecs = {}
        self.long_indexs = {}

        self.closes = {}
        self.opens = {}
        self.highs = {}
        self.lows = {}

        self.curr_closes = {}
        self.curr_holds = {}
        self.curr_prices = {}

        self.dataset.read(hs300, 'daily')
        self.hs300_list = self.dataset.parse_price('index')
        self.index_dates = numpy.transpose( self.hs300_list )[0]
        
        for i in range(0, self.all_count):
            code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
            self.codes.append(code)
            
            self.dataset.read(code, 'daily')
            _list = self.dataset.parse_price('stock')
            self._read_stock(code, _list)

            if i % 100 == 99:
                print('read', i+1, 'stocks data, run', time.time() - self.start, 'seconds.')
        print('read', len(self.codes), 'stocks data, run', time.time() - self.start, 'seconds.')

    def _read_stock(self, code, data_list):
        self.turtles[code] = TurTleIndex(data_list)
        self.long_indexs[code] = self.turtles[code].long_index( cmdline['strong_cycle'] )
        self.date_vecs[code] = self.turtles[code].data['date']

        self.closes[code] = self.turtles[code].data['close']
        self.opens[code] = self.turtles[code].data['open']
        self.highs[code] = self.turtles[code].data['high']
        self.lows[code] = self.turtles[code].data['low']


    def _index_turtle(self):
        self.turtles[hs300] = TurTleIndex(self.hs300_list)
        self.turtles[hs300].price_wave(cmdline['long_cycle'], cmdline['short_cycle'])
        # self.index_dates = self.turtles[hs300].data['date']

        self.turtles[hs300].long_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
            cmdline['append'], cmdline['stop_loss'])
        self.index_long_state = self.turtles[hs300].data['state']

        self.turtles[hs300].short_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
            cmdline['append'], cmdline['stop_loss'])
        self.index_short_state = self.turtles[hs300].data['state']

    def _stock_turtle(self):
        self.states = {}
        self.key_prices = {}
        self.long_waves = {}

        for code in self.codes:
            self.turtles[code].price_wave(cmdline['long_cycle'], cmdline['short_cycle'])
            self.turtles[code].long_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
                cmdline['append'], cmdline['stop_loss'])

            self.states[code] = self.turtles[code].data['state']
            self.key_prices[code] = self.turtles[code].data['key_prices']
            self.long_waves[code] = self.turtles[code].data['long_wave' ]
            # self.turtles[code].save_data(code)
        print('calculate', len(self.codes), 'stocks turtle index, run', time.time() - self.start, 'seconds.')


    def _update_index(self, _date):
        self.curr_closes = {}

        for code in self.codes:
            dates = self.date_vecs[code]
            _len = len(dates)

            while self.data_indexs[code] < _len and dates[self.data_indexs[code]] < _date:
                self.data_indexs[code] += 1
            _idx = self.data_indexs[code]
            if _idx >= _len or dates[_idx] > _date: 
                continue
            self.curr_closes[code] = self.closes[code][_idx]

    def _sort_strong_stocks(self, _date):
        _curr_stocks = []
        for code in self.curr_closes:
            _curr_stocks.append({ 'code': code, 'close': self.curr_closes[code], 
                'strong': self.long_indexs[code][self.data_indexs[code]] })
        return sorted(_curr_stocks, key = lambda stock: stock['strong'], reverse = True)

    def _order(self, code, volume, trade_price, _date):
        _idx = self.data_indexs[code]
        _volume = 0
        if self.highs[code][_idx] - self.lows[code][_idx] > 0.01:
            _volume = self.account._Order(code, trade_price, volume, _date)
        return _volume

    def _clear(self, _date):
        for code in self.account.stocks.index:
            volume = self.account.Volume(code)
            if volume < 10 and volume > -10:
                continue
            self._order(code, -volume, self.opens[code][ self.data_indexs[code] ], _date)


    def _update_long_hold(self, _date):
        # self.sorted_stocks = self._sort_strong_stocks(_date)
        self.stock_sidxs = {}
        _sorted_count = min(len(self.sorted_stocks), self.all_count)

        for i in range(0, _sorted_count):
            code = self.sorted_stocks[i]['code']
            self.stock_sidxs[code] = i
            volume = self.account.Volume(code)
            if i < self.max_sidx and len(self.account.stocks) < self.max_count and volume < 100:
                kp = self.opens[code][self.data_indexs[code]]
                volume = self.account.market_value * self.scale / kp
                self._order(code, volume, kp, _date)
                
        for code in self.account.stocks.index:
            volume = self.account.Volume(code)
            if volume > 0 and code in self.stock_sidxs and self.stock_sidxs[code] >= self.max_sidx:
                self._order(code, -volume, self.opens[code][ self.data_indexs[code] ], _date)


    def _open_turtle(self, code, _date, _cash_unit):
        _idx = self.data_indexs[code]
        _Nl = self.long_waves[code][_idx]
        _kp = self.key_prices[code][_idx]
        _trade_unit = _cash_unit / _Nl

        if self._order(code, _trade_unit, _kp, _date):
            self.curr_holds[code] = { 'trade_unit': _trade_unit, 'count': 1, 'last_price': _kp, 'Nl': _Nl }

    def _update_turtle(self, _date):
        if len(self.account.stocks) < self.max_count:
            self.sorted_stocks = self._sort_strong_stocks(_date)
            _sorted_count = min(len(self.sorted_stocks), self.all_count)
            _cash_unit = self.account.market_value * self.scale * cmdline['loss_unit']

            for i in range(0, _sorted_count):
                code = self.sorted_stocks[i]['code']
                volume = self.account.Volume(code)

                if volume < 10 and self.states[code][self.data_indexs[code]]:
                    self._open_turtle(code, _date, _cash_unit)
                if len(self.account.stocks) >= self.max_count:
                    break

        for code in self.account.stocks.index:
            _idx = self.data_indexs[code]
            _kp = self.key_prices[code][_idx]
            volume = self.account.Volume(code)

            if volume > 0 and not self.states[code][_idx]:
                if self._order(code, -volume, _kp, _date):
                    del self.curr_holds[code]

            if code in self.curr_holds and self.curr_holds[code]['count'] < self.states[code][_idx]:
                _kp = self.curr_holds[code]['last_price'] + self.curr_holds[code]['Nl'] * cmdline['append']
                if _kp > self.highs[code][_idx] or _kp < self.lows[code][_idx]:
                    continue

                if self.opens[code][_idx] > _kp:
                    _kp = self.opens[code][_idx]
                if self._order(code, self.curr_holds[code]['trade_unit'], _kp, _date):
                    self.curr_holds[code]['count'] += 1
                    self.curr_holds[code]['last_price'] = _kp


    def print_progress(self, _date):
        _year = StockDataSource.datetime(_date).year
        if self.year != _year:
            self.year = _year
            print( "process to", self.year, ', market_value', self.account.market_value, ', run', time.time() - self.start, 'seconds.' )

    def _start_static(self):
        funcName = sys._getframe().f_back.f_code.co_name #获取调用函数名
        lineNumber = sys._getframe().f_back.f_lineno     #获取行号
        coname = sys._getframe().f_code.co_name          #获取当前函数名
        print( coname, funcName, lineNumber ) 

        self.account = StockAccount(10000, 0)
        self.market_values = []
        self.market_values.append(self.account.market_value)
        for code in self.codes:
            self.data_indexs[code] = 0


    def long_hold(self):
        '''长期持有强势股'''

        # self.index_dates = numpy.transpose( self.hs300_list )[0]
        self._start_static()

        for _idx in range(1, len(self.index_dates)):
            _date = self.index_dates[_idx]
            # self.print_progress(_date)

            if _date < cmdline['start_date'] or _date > cmdline['end_date']:
                # self.account.ProfitDaily()
                self.market_values.append(self.account.market_value)
                continue

            self.account.ProfitDaily()
            self._update_index(_date)

            self.sorted_stocks = self._sort_strong_stocks(_date)
            self._update_long_hold(_date)

            self.account.UpdateValue(self.curr_closes)
            self.market_values.append(self.account.market_value)


    def hold_turtle(self):
        '''长期持股,根据海龟法则交易个股'''

        # self.index_dates = numpy.transpose( self.hs300_list )[0]
        self._start_static()
        self._stock_turtle()

        for _idx in range(1, len(self.index_dates)):
            _date = self.index_dates[_idx]
            # self.print_progress(_date)

            if _date < cmdline['start_date'] or _date > cmdline['end_date']:
                # self.account.ProfitDaily()
                self.market_values.append(self.account.market_value)
                continue

            self.account.ProfitDaily()
            self._update_index(_date)
            self._update_turtle(_date)

            self.account.UpdateValue(self.curr_closes)
            self.market_values.append(self.account.market_value)


    def turtle_turtle(self):
        '''根据海龟法则分析指数判断牛熊市，然后根据海龟法则交易个股'''

        long_days = 0
        self._start_static()
        self._index_turtle()
        self._stock_turtle()

        for _idx in range(1, len(self.index_dates)):
            _date = self.index_dates[_idx]
            # self.print_progress(_date)

            if _date < cmdline['start_date'] or _date > cmdline['end_date']:
                # self.account.ProfitDaily()
                self.market_values.append(self.account.market_value)
                continue

            self.account.ProfitDaily()
            self._update_index(_date)

            if self.index_long_state[_idx]:
                self._update_turtle(_date)
            elif len(self.account.stocks): #and self.index_short_state[_idx]:
                self._clear(_date)
                
            self.account.UpdateValue(self.curr_closes)
            self.market_values.append(self.account.market_value)
            if len(self.account.stocks):
                long_days += 1
        print('all day %d, long day %d.' % (len(self.index_dates), long_days))


    def turtle_hold(self):
        '''根据海龟法则分析指数数据,判断牛熊市,决定是否持股'''

        self._start_static()
        self._index_turtle()

        for _idx in range(1, len(self.index_dates)):
            _date = self.index_dates[_idx]
            # self.print_progress(_date)

            if _date < cmdline['start_date'] or _date > cmdline['end_date']:
                # self.account.ProfitDaily()
                self.market_values.append(self.account.market_value)
                continue

            self.account.ProfitDaily()
            self._update_index(_date)

            if self.index_long_state[_idx]:
                self.sorted_stocks = self._sort_strong_stocks(_date)
                self._update_long_hold(_date)
            elif len(self.account.stocks):
                self._clear(_date)
                
            self.account.UpdateValue(self.curr_closes)
            self.market_values.append(self.account.market_value)


    def show(self):
        # print( self.account.stocks )
        # print( self.account.get_records() )
        self.account.status_info()

    def plot(self, cmd, photo_file):
        plot = StockDisp(cmd + '-' + hs300)
        plot.LogKDisp(plot.ax1, self.hs300_list)
        plot.LogPlot(plot.ax1, self.index_dates, self.market_values, 'r', 6)
        # plot.show()
        plot.save( photo_file )


if __name__ == "__main__":
    InputArgs()

    # StockSetData.loaddata(200, 300)

    test = TurtleStrongTest(30, 10)
    test.turtle_turtle()

    _cmd = 'turtle_turtle'
    _file = _cmd + '-' + cmdline['record_file']
    print( _cmd, 'use time:', time.time() - test.start, 'seconds')
    test.show()
    test.account.save_records(_file)
    test.plot(_cmd, _file)


    # test.long_hold()
    # cmd = 'long-strong'
    # print( cmd, 'use time:', time.time()-test.start, 'seconds')
    # _file = cmd + '-' + cmdline['record_file']
    # test.show()
    # test.account.save_records(_file)
    # test.plot(cmd, _file)

    # test.turtle_hold()
    # cmd = 'turtle_hold'
    # print( cmd, 'use time:', time.time()-test.start, 'seconds')
    # _file = cmd + '-' + cmdline['record_file']
    # test.show()
    # test.account.save_records(_file)
    # test.plot(cmd, _file)

    # test.hold_turtle()
    # cmd = 'hold_turtle'
    # print( cmd, 'use time:', time.time()-test.start, 'seconds')
    # _file = cmd + '-' + cmdline['record_file']
    # test.show()
    # test.account.save_records(_file)
    # test.plot(cmd, _file)


        # stock_data = csv.reader(open(data_file, 'r'))
        # rows = [stock for stock in stock_data]
        # rows.reverse()

        # for rnum, row in stock_data.iterrows():
        #     tscode, trade_date, open, high, low, close = row[0:6]
        #     timenum = StockDataSource.float_date(trade_date)
        #     data_lists[tscode].append( (timenum, open, high, low, close) )

        # self.index_dates, self.hs300_list, ave_price, volumes = self.dataset.parse_data('index')

        # data_lists = StockSetData.parse_data('./hs300_all.daily.csv')
        # print('parse', len(data_lists), 'stocks data, run', time.time() - self.start, 'seconds.')

        # for i in range(0, self.all_count):
        #     code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
        #     code = code.upper()
        #     if code in data_lists and len(data_lists[code]) > 10:
        #         self.codes.append(code)  
        #         self._read_stock(code, data_lists[code])

        # print('read', len(self.codes), 'stocks data, run', time.time() - self.start, 'seconds.')


    # ss = {'600387': [1, 2, 3], '000225': [4, 5, 6], '300758': [7, 8, 9]}
    # for a in ss.keys():
    #     print( ss[a], a )
    #     print( a )


            # self.date_vecs[code] = _dates
            # self.turtles[code] = TurTleIndex(_list)
            # self.long_indexs[code] = self.turtles[code].long_index( cmdline['strong_cycle'] )
            
            # self.closes[code] = self.turtles[code].data['close']
            # self.opens[code] = self.turtles[code].data['open']
            # self.highs[code] = self.turtles[code].data['high']
            # self.lows[code] = self.turtles[code].data['low']

    # if isinstance(cmdline['cmd'], list):
    #     cmd = cmdline['cmd'][0]
    # else:
    #     cmd = cmdline['cmd']

    # if cmd == 'turtle-turtle':
    #     test.turtle_turtle()
    # elif cmd == 'hold-turtle':
    #     test.hold_turtle()
    # elif cmd == 'turtle-hold':
    #     test.turtle_hold()
    # elif cmd == 'long-hold':
    #     test.long_hold()
    # else:
    #     print( "no process.", cmdline['cmd'] )
    # test.show()

    # _end_time = time.time()
    # print( 'use time:', time.time()-_start_time, 'seconds')

    # _file = cmd + '-' + cmdline['record_file']
    # test.account.save_records(_file)
    # test.plot(_file)



        # if not _volume:
        #     print(StockDataSet.str_date(_date), code, volume, trade_price, self.highs[code][_idx], self.lows[code][_idx])
        #     _volume = self.account._Order(code, trade_price, volume, _date)

        # self.turtles[hs300].save_data(hs300)
        # self.closes[hs300] = self.turtles[hs300].data['close']
        # self.states[hs300] = self.turtles[hs300].data['state']

        # self.curr_prices['trade'] = trade_price
        # self.curr_prices['high'] = self.highs[code][_idx]
        # self.curr_prices['low'] = self.lows[code][_idx]
        # self.account.Order(code, self.curr_prices['trade'], -volume, _date)

            # _idx = self.data_indexs[code]
            # self.curr_prices['trade'] = self.opens[code][_idx]
            # self.curr_prices['high'] = self.highs[code][_idx]
            # self.curr_prices['low'] = self.lows[code][_idx]
            # self.account.Order(code, self.curr_prices['trade'], -volume, _date)
            # self.hold_count -= 1
        # print( self.hold_count, self.account.stocks )

                # self.account.Order(code, kp, volume, _date)
                # self.hold_count += 1

                # self.account.Order(code, self.opens[code][self.data_indexs[code]], -volume, _date)
                # self.hold_count -= 1

        # self.account.Order(code, _kp, _cash_unit / _kp, _date)
        # self.hold_count += 1

        # self.curr_prices['trade'] = trade_price
        # self.curr_prices['high'] = self.highs[code][_idx]
        # self.curr_prices['low'] = self.lows[code][_idx]
        # self.account.Order(code, self.curr_prices['trade'], -volume, _date)

                # if self.states[code][_idx] - self.curr_holds[code]['count'] > 1:
                    # _kp = self.curr_holds[code]['last_price'] + self.curr_holds[code]['Nl'] * cmdline['append']
                # if _kp > self.highs[code][_idx]:
                #     continue
                # self.hold_count -= 1
                # self.account.Order(code, _kp, -volume, _date)
                # volume = self.curr_holds[code]['cash_unit'] / _kp
                # self.account.Order(code, _kp, volume, _date)

            # print( self.hold_count, self.max_count, StockDataSet.str_date( _date) )

            # if len(self.account.stocks) < self.max_count:
            #     self.sorted_stocks = self._sort_strong_stocks(_date)
            #     _sorted_count = min(len(self.sorted_stocks), self.all_count)
            #     _cash_unit = self.account.market_value * self.scale * cmdline['loss_unit']

            #     for i in range(0, _sorted_count):
            #         code = self.sorted_stocks[i]['code']
            #         volume = self.account.Volume(code)

            #         if volume < 10 and self.states[code][self.data_indexs[code]]:
            #             self._open_turtle(code, _date, _cash_unit)
            #         if len(self.account.stocks) >= self.max_count:
            #             break

            # self._update_turtle_hold(_date, self.account.market_value*self.scale)
            
        # self.turtles[hs300] = TurTleIndex(self.hs300_list)
        # self.turtles[hs300].price_wave(cmdline['long_cycle'], cmdline['short_cycle'])
        # self.turtles[hs300].long_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
        #     cmdline['append'], cmdline['stop_loss'])

        # self.closes[hs300] = self.turtles[hs300].data['close']
        # self.hs300_states = self.turtles[hs300].data['state']

    # if type(cmdline['cmd']) is list:
    # print( type(cmdline['cmd']) )
    # print( cmdline['cmd'] )
    # print( cmd )

    # test.long_hold()
    # test.turtle_hold()



        # _curr_stocks = []
        # self.curr_closes = {}

        # for code in self.codes:
        #     dates = self.date_vecs[code]
        #     _len = len(dates)

        #     while self.data_indexs[code] < _len and dates[self.data_indexs[code]] < _date:
        #         self.data_indexs[code] += 1
        #     _idx = self.data_indexs[code]
        #     if _idx >= _len or dates[_idx] > _date: 
        #         continue

        #     self.curr_closes[code] = self.closes[code][_idx]
        #     _curr_stocks.append({'code': code, 'close': self.curr_closes[code], 
        #         'strong': self.long_indexs[code][_idx]})

        # return sorted(_curr_stocks, key = lambda stock: stock['strong'], reverse = True)


    # def _update_turtle_hold(self, _date, _cash_unit):
    #     if self.hold_count < self.max_count:
    #         self.sorted_stocks = self._sort_strong_stocks(_date)
    #         # self.stock_sidxs = {}
    #         self.sorted_count = min(len(self.sorted_stocks), self.all_count)

    #         for i in range(0, self.sorted_count):
    #             code = self.sorted_stocks[i]['code']
    #             # self.stock_sidxs[code] = i
    #             volume = self.account.Volume(code)
    #             if volume < 10 and self.hold_count < self.max_count:
    #                 self._turtle_open(code, _date, _cash_unit)
    #     self._update_turtle()

                    # _idx = self.data_indexs[code]
                    # _Nl = self.long_waves[code][_idx]
                    # _kp = self.key_prices[code][_idx]
                    # _cash_unit = _cash_unit * cmdline['loss_unit'] / _Nl
                    # self.curr_holds[code] = ['cash_unit': _cash_unit, 'count': 1, 
                    #     'last_price': _kp, 'Nl': _Nl]
                    # volume = _cash_unit / _kp
                    # self.account.Order(code, _kp, -volume, _date)


    # loaddata(0, len(hs300_stocks))
    # turtle_hold_stocks(15, 5)
    
    # long_hold_strong_stocks(15, 5)
    # long_hold_strong_stocks(40, 8)


        # turtles[hs300] = TurTleIndex(hs300_list)
        # turtles[hs300].price_wave(cmdline['long_cycle'], cmdline['short_cycle'])
        # turtles[hs300].long_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
        #     cmdline['append'], cmdline['stop_loss'])

        # closes[hs300] = turtles[hs300].data['close']
        # hs300_states = turtles[hs300].data['state']

    # codes = []
    # date_vecs = {}
    # data_indexs = {}

    # closes = {}
    # long_indexs = {}
    # turtles = {}

    # dataset.read(hs300, 'daily')
    # index_dates, hs300_list, ave_price, volumes = dataset.parse_data()

    # turtles[hs300] = TurTleIndex(hs300_list)
    # turtles[hs300].price_wave(long_cycle, short_cycle)
    # turtles[hs300].long_trade(long_cycle, short_cycle, append, stop_loss)

    # closes[hs300] = turtles[hs300].data['close']
    # hs300_states = turtles[hs300].data['state']
    # # keyprice = turtles[hs300].data['key_prices']
    # # Nl = turtles[hs300].data['long_wave']

    # for stock in hs300_stocks:
    #     code = stock[1] + '.' + stock[0]
    #     codes.append(code)
        
    #     dataset.read(code, 'daily')
    #     _dates, _list, ave_price, volumes = dataset.parse_data()
    #     date_vecs[code] = _dates

    #     turtles[code] = TurTleIndex(_list)
    #     long_indexs[code] = turtles[code].long_index(120)
    #     data_indexs[code] = 0
    #     closes[code] = turtles[code].data['close']

    # account = StockAccount(100000, 0)
    # count = 0
    # cash_unit = account.cash

    # market_values = []
    # market_values.append(account.market_value)
    # account.ProfitDaily()

    # for _idx in range(len(index_dates)-10, len(index_dates)):
    #     account.ProfitDaily()
    #     _date = index_dates[_idx]

    #     # curr_closes = {}
    #     # _curr_stocks = []

    #     if _date < start_date or _date > end_date:
    #         market_values.append(account.market_value)
    #         continue

    #     if count < hs300_states[_idx] and count < 4:
    #         count = hs300_states[_idx]
    #         # if count == 1:
    #         #     cash_unit = account.cash * loss_unit * keyprice[i] / Nl[i]
    #         # volume = cash_unit / kp
    #         # if volume >= 100: 
    #         #     account.Order(code, kp, volume, dates[i])

    #     elif count and not hs300_states[_idx]:
    #         count = hs300_states[_idx]
    #         # volume = account.stocks.at[code, 'volume']
    #         # account.Order(code, kp, -volume, dates[i])

    #     _sorted_stocks, curr_closes = sort_strong_stocks(codes, data_indexs, _date, closes, long_indexs)
    #     print( _sorted_stocks )

    #     account.UpdateValue(curr_closes)
    #     market_values.append(account.market_value)

    # plot = StockDisp(hs300)
    # plot.LogKDisp(plot.ax1, hs300_list)
    # plot.LogPlot(plot.ax1, index_dates, market_values, 'r', 4)
    # # plot.LogPlot(plot.ax2, index_dates, Nl, 'r')
    # plot.Plot(plot.ax2, index_dates, long_counts, 'B')
    # plot.show()

    # account.status_info()
    # account.save_records('./data', 'tt-first')
    # print( account.get_records() )


    # print( StockDataSet.float_date('20190104') )
    # print( StockDataSet.datetime('20190104') )
    

    # index_data = dataset.load(hs300, startdate, enddate, 'index', 'daily')
    # for stock in stocks:
        # code = stock[1] + '.' + stock[0]
        # stock_data = dataset.load(code, startdate, enddate, 'stock', 'daily')


    # data_lists = {}
    # dataset.load(hs300, startdate, enddate, 'index', 'daily')
    # data_lists[hs300] = _list
    # turtles[hs300] = TurTleIndex(_list, long_cycle, short_cycle, append, stop_loss)

        # dataset.load(code, startdate, enddate, 'stock', 'daily')
        # data_lists[code] = _list
        # turtles[code] = TurTleIndex(_list, long_cycle, short_cycle, append, stop_loss)

    # print ( closes[hs300] )
    # print ( closes[codes[0]] )


        # for code in codes:
        #     dates = date_vecs[code]
        #     while data_indexs[code] < len(dates) and dates[data_indexs[code]] < _date:
        #         data_indexs[code] += 1
        #     if data_indexs[code] >= len(dates) or dates[data_indexs[code]] > _date: 
        #         continue
        #     curr_closes[code] = closes[code][data_indexs[code]]
        #     _curr_stocks.append({'code': code, 'close': curr_closes[code], 'strong': long_indexs[code][data_indexs[code]]})
        # _sorted_stocks = sorted(_curr_stocks, key = lambda stock: stock['strong'], reverse = True)

    # if ARGS.hs300_stocks:
    #     hs300_stocks = ARGS.hs300_stocks
    # print( type(start_date) )

# hs300_stocks = [
#     ('sh', '603156', '养元饮品'), ('sh', '601138', '工业富联'), ('sz', '002001', '新和成'), ('sz', '000661', '长春高新'), ('sh', '600998', '九州通'), ('sz', '002179', '中航光电'), ('sh', '600004', '白云机场'), ('sz', '300296', '利亚德'), ('sh', '603986', '兆易创新'), ('sz', '002120', '韵达股份'), ('sz', '002311', '海大集团'), ('sz', '002422', '科伦药业'), ('sz', '002773', '康弘药业'), ('sh', '603259', '药明康德'), ('sh', '600027', '华电国际') 
# ]
# print( 'end_date' in cmdline)

# startdate = '20080101'
# enddate = '20190101'
# start_date = date2num(dt.datetime.strptime(startdate, '%Y%m%d'))
# end_date = date2num(dt.datetime.strptime(enddate, '%Y%m%d'))

# loss_unit = 0.01
# append = 1
# stop_loss = 3
# long_cycle = 55
# short_cycle= 20
# strong_cycle=120

# def _update_long_holds(account, codes, _sorted_stocks, curr_closes, _opens, data_indexs):
#     # _sorted_stocks, curr_closes = sort_strong_stocks(codes, data_indexs, 
#     #             date_vecs, _date, closes, long_indexs)
#     _stock_sidxs = {}
#     _stock_count = min(len(_sorted_stocks), cmdline['stock_count'])

#     for i in range(0, _stock_count):
#         code = _sorted_stocks[i]['code']
#         _stock_sidxs[code] = i
#         volume = account.Volume(code)
#         if i < max_sidx and count < max_count and volume < 100:
#             kp = _opens[code][data_indexs[code]]
#             volume = account.market_value * scale / kp
#             account.Order(code, kp, volume, _date)
#             count += 1

#     for code in account.stocks.index:
#         volume = account.Volume(code)
#         if volume > 0 and code in _stock_sidxs and _stock_sidxs[code] >= max_sidx:
#             account.Order(code, _opens[code][data_indexs[code]], -volume, _date)
#             count -= 1

# def turtle_hold_stocks(max_sidx, max_count):
#     dataset = StockDataSet(cmdline['data_path'])
#     account = StockAccount(1000000, 0)
#     _stock_count = min(len(hs300_stocks), cmdline['stock_count'])

#     codes = []
#     date_vecs = {}
#     data_indexs = {}

#     closes = {}
#     opens = {}
#     long_indexs = {}
#     turtles = {}

#     dataset.read(hs300, 'daily')
#     index_dates, hs300_list, ave_price, volumes = dataset.parse_data()

#     turtles[hs300] = TurTleIndex(hs300_list)
#     turtles[hs300].price_wave(cmdline['long_cycle'], cmdline['short_cycle'])
#     turtles[hs300].long_trade(cmdline['long_cycle'], cmdline['short_cycle'], 
#         cmdline['append'], cmdline['stop_loss'])

#     closes[hs300] = turtles[hs300].data['close']
#     hs300_states = turtles[hs300].data['state']

#     for i in range(0, _stock_count):
#         code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
#         codes.append(code)
        
#         dataset.read(code, 'daily')
#         _dates, _list, ave_price, volumes = dataset.parse_data()
#         date_vecs[code] = _dates

#         turtles[code] = TurTleIndex(_list)
#         long_indexs[code] = turtles[code].long_index(120)
#         data_indexs[code] = 0
#         closes[code] = turtles[code].data['close']
#         opens[code] = turtles[code].data['open']

#     scale = 1.0/max_count
#     hold_stocks = []
#     count = 0
#     cash_unit = account.cash

#     market_values = []
#     market_values.append(account.market_value*0.001)
#     account.ProfitDaily()

#     for _idx in range(1, len(index_dates)):
#         account.ProfitDaily()
#         _date = index_dates[_idx]
#         curr_closes = {}

#         if _date < cmdline['start_date'] or _date > cmdline['end_date']:
#             market_values.append(account.market_value*0.001)
#             continue

#         # _stock_count = min(len(_sorted_stocks), cmdline['stock_count'])
#         # _stock_count = len(hold_stocks)

#         if hs300_states[_idx]:
#             _sorted_stocks, curr_closes = sort_strong_stocks(codes, data_indexs, 
#                 date_vecs, _date, closes, long_indexs)
#             _stock_sidxs = {}
#             _stock_count = min(len(_sorted_stocks), cmdline['stock_count'])

#             for i in range(0, _stock_count):
#                 code = _sorted_stocks[i]['code']
#                 _stock_sidxs[code] = i
#                 volume = account.Volume(code)
#                 if i < max_sidx and count < max_count and volume < 100:
#                     kp = opens[code][data_indexs[code]]
#                     volume = account.market_value * scale / kp
#                     account.Order(code, kp, volume, _date)
#                     count += 1

#             for code in account.stocks.index:
#                 volume = account.Volume(code)
#                 if volume > 0 and code in _stock_sidxs and _stock_sidxs[code] >= max_sidx:
#                     account.Order(code, opens[code][data_indexs[code]], -volume, _date)
#                     count -= 1
#         else:
#             for code in account.stocks.index:
#                 volume = account.Volume(code)
#                 if volume > 0:
#                     account.Order(code, opens[code][data_indexs[code]], -volume, _date)
#                     count -= 1
            
#         account.UpdateValue(curr_closes)
#         market_values.append(account.market_value*0.001)

#     print( account.stocks )
#     account.status_info()
#     account.save_records('turtle-hold')

#     plot = StockDisp(hs300)
#     plot.LogKDisp(plot.ax1, hs300_list)
#     plot.LogPlot(plot.ax1, index_dates, market_values, 'r', -1)
#     plot.show()


# def sort_strong_stocks(codes, data_indexs, date_vecs, _date, closes, long_indexs):
#     _curr_stocks = []
#     curr_closes = {}

#     for code in codes:
#         dates = date_vecs[code]
#         _len = len(dates)

#         while data_indexs[code] < _len and dates[data_indexs[code]] < _date:
#             data_indexs[code] += 1
#         _idx = data_indexs[code]
#         if _idx >= _len or dates[_idx] > _date: 
#             continue

#         curr_closes[code] = closes[code][_idx]
#         _curr_stocks.append({'code': code, 'close': curr_closes[code], 
#             'strong': long_indexs[code][_idx]})

#     _sorted_data = sorted(_curr_stocks, key = lambda stock: stock['strong'], reverse = True)
#     return _sorted_data, curr_closes


# def long_hold_strong_stocks(max_sidx, max_count):
#     dataset = StockDataSet(cmdline['data_path'])
#     account = StockAccount(1000000, 0)
#     _stock_count = min(len(hs300_stocks), cmdline['stock_count'])

#     codes = []
#     date_vecs = {}
#     data_indexs = {}

#     closes = {}
#     opens = {}
#     long_indexs = {}
#     turtles = {}

#     dataset.read(hs300, 'daily')
#     index_dates, hs300_list, ave_price, volumes = dataset.parse_data()

#     for i in range(0, _stock_count):
#     # for stock in hs300_stocks:
#         code = hs300_stocks[i][1] + '.' + hs300_stocks[i][0]
#         codes.append(code)
        
#         dataset.read(code, 'daily')
#         _dates, _list, ave_price, volumes = dataset.parse_data()
#         date_vecs[code] = _dates

#         turtles[code] = TurTleIndex(_list)
#         long_indexs[code] = turtles[code].long_index(120)
#         data_indexs[code] = 0
#         closes[code] = turtles[code].data['close']
#         opens[code] = turtles[code].data['open']

#     scale = 1.0/max_count
#     count = 0
#     market_values = []
#     market_values.append(account.market_value*0.001)
#     account.ProfitDaily()

#     for _idx in range(1, len(index_dates)):
#         account.ProfitDaily()
#         _date = index_dates[_idx]

#         # print( _date, cmdline['start_date'], cmdline['end_date'])
#         if _date < cmdline['start_date'] or _date > cmdline['end_date']:
#             market_values.append(account.market_value*0.001)
#             continue

#         _sorted_stocks, curr_closes = sort_strong_stocks(codes, data_indexs, 
#             date_vecs, _date, closes, long_indexs)
#         _stock_sidxs = {}
#         _stock_count = min(len(_sorted_stocks), cmdline['stock_count'])

#         for i in range(0, _stock_count):
#             code = _sorted_stocks[i]['code']
#             _stock_sidxs[code] = i
#             volume = account.Volume(code)
#             if i < max_sidx and count < max_count and volume < 100:
#                 kp = opens[code][data_indexs[code]]
#                 volume = account.market_value * scale / kp
#                 account.Order(code, kp, volume, _date)
#                 count += 1

#         for code in account.stocks.index:
#             volume = account.Volume(code)
#             if volume > 0 and code in _stock_sidxs and _stock_sidxs[code] >= max_sidx:
#                 account.Order(code, opens[code][data_indexs[code]], -volume, _date)
#                 count -= 1

#         account.UpdateValue(curr_closes)
#         market_values.append(account.market_value*0.001)

#     # print( market_values )
#     # print( account.get_records() )
#     print( account.stocks )
#     account.status_info()
#     account.save_records('long-hold-strong')

#     plot = StockDisp(hs300)
#     plot.LogKDisp(plot.ax1, hs300_list)
#     plot.LogPlot(plot.ax1, index_dates, market_values, 'r', -1)

#     # plot.Plot(plot.ax1, index_dates, market_values, 'r', -2000)
#     # plot.LogPlot(plot.ax2, index_dates, Nl, 'r')
#     # plot.Plot(plot.ax2, index_dates, long_counts, 'B')

#     plot.show()
