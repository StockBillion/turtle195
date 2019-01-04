#!/usr/bin/env python
#-*- coding: utf8 -*-
import re, pandas as pf


stock_list_str =  ''' 
     <tr>
        <td><div align="center">603156</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603156/nc.shtml" target="_blank">养元饮品</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601138</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601138/nc.shtml" target="_blank">工业富联</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">002001</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002001/nc.shtml" target="_blank">新和成</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000661</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000661/nc.shtml" target="_blank">长春高新</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">000553</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000553/nc.shtml" target="_blank">沙隆达A</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600998</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600998/nc.shtml" target="_blank">九州通</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">002179</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002179/nc.shtml" target="_blank">中航光电</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600004</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600004/nc.shtml" target="_blank">白云机场</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">300296</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300296/nc.shtml" target="_blank">利亚德</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">603986</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603986/nc.shtml" target="_blank">兆易创新</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">002120</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002120/nc.shtml" target="_blank">韵达股份</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002311</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002311/nc.shtml" target="_blank">海大集团</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">002422</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002422/nc.shtml" target="_blank">科伦药业</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002773</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002773/nc.shtml" target="_blank">康弘药业</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">603259</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603259/nc.shtml" target="_blank">药明康德</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600027</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600027/nc.shtml" target="_blank">华电国际</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">000408</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000408/nc.shtml" target="_blank">藏格控股</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002271</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002271/nc.shtml" target="_blank">东方雨虹</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">600566</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600566/nc.shtml" target="_blank">济川药业</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000703</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000703/nc.shtml" target="_blank">恒逸石化</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">002032</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002032/nc.shtml" target="_blank">苏泊尔</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300142</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300142/nc.shtml" target="_blank">沃森生物</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">601066</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601066/nc.shtml" target="_blank">中信建投</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600760</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600760/nc.shtml" target="_blank">中航沈飞</a></div></td>
        <td><div align="center">2018-12-17</div></td>
      </tr>
		  <tr>
        <td><div align="center">300408</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300408/nc.shtml" target="_blank">三环集团</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000786</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000786/nc.shtml" target="_blank">北新建材</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601808</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601808/nc.shtml" target="_blank">中海油服</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600176</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600176/nc.shtml" target="_blank">中国巨石</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600438</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600438/nc.shtml" target="_blank">通威股份</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002493</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002493/nc.shtml" target="_blank">荣盛石化</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">001965</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz001965/nc.shtml" target="_blank">招商公路</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002625</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002625/nc.shtml" target="_blank">光启技术</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">300433</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300433/nc.shtml" target="_blank">蓝思科技</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002925</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002925/nc.shtml" target="_blank">盈趣科技</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">002050</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002050/nc.shtml" target="_blank">三花智控</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002085</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002085/nc.shtml" target="_blank">万丰奥威</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600867</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600867/nc.shtml" target="_blank">通化东宝</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600809</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600809/nc.shtml" target="_blank">山西汾酒</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601838</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601838/nc.shtml" target="_blank">成都银行</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600339</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600339/nc.shtml" target="_blank">中油工程</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr> 
      <tr>
        <td><div align="center">601108</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601108/nc.shtml" target="_blank">财通证券</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601360</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601360/nc.shtml" target="_blank">三六零</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600516</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600516/nc.shtml" target="_blank">方大炭素</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601238</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601238/nc.shtml" target="_blank">广汽集团</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600398</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600398/nc.shtml" target="_blank">海澜之家</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">603288</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603288/nc.shtml" target="_blank">海天味业</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601828</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601828/nc.shtml" target="_blank">美凯龙</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600025</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600025/nc.shtml" target="_blank">华能水电</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600346</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600346/nc.shtml" target="_blank">恒力股份</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600487</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600487/nc.shtml" target="_blank">亨通光电</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">603260</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603260/nc.shtml" target="_blank">合盛硅业</a></div></td>
        <td><div align="center">2018-06-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">603833</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603833/nc.shtml" target="_blank">欧派家居</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600011</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600011/nc.shtml" target="_blank">华能国际</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">603799</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603799/nc.shtml" target="_blank">华友钴业</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">002624</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002624/nc.shtml" target="_blank">完美世界</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002572</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002572/nc.shtml" target="_blank">索菲亚</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">300003</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300003/nc.shtml" target="_blank">乐普医疗</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002468</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002468/nc.shtml" target="_blank">申通快递</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">002601</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002601/nc.shtml" target="_blank">龙蟒佰利</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601012</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601012/nc.shtml" target="_blank">隆基股份</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600390</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600390/nc.shtml" target="_blank">五矿资本</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002294</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002294/nc.shtml" target="_blank">信立泰</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">300136</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300136/nc.shtml" target="_blank">信维通信</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300015</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300015/nc.shtml" target="_blank">爱尔眼科</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">000898</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000898/nc.shtml" target="_blank">鞍钢股份</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601212</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601212/nc.shtml" target="_blank">白银有色</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">600219</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600219/nc.shtml" target="_blank">南山铝业</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601898</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601898/nc.shtml" target="_blank">中煤能源</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601991</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601991/nc.shtml" target="_blank">大唐发电</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300122</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300122/nc.shtml" target="_blank">智飞生物</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601878</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601878/nc.shtml" target="_blank">浙商证券</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002460</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002460/nc.shtml" target="_blank">赣锋锂业</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr>
        <td><div align="center">601228</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601228/nc.shtml" target="_blank">广州港</a></div></td>
        <td><div align="center">2017-12-11</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002555</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002555/nc.shtml" target="_blank">三七互娱</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">002558</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002558/nc.shtml" target="_blank">世纪游轮</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002602</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002602/nc.shtml" target="_blank">世纪华通</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">600233</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600233/nc.shtml" target="_blank">圆通速递</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002508</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002508/nc.shtml" target="_blank">老板电器</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">002411</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002411/nc.shtml" target="_blank">必康股份</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002352</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002352/nc.shtml" target="_blank">顺丰控股</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">002044</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002044/nc.shtml" target="_blank">美年健康</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000959</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000959/nc.shtml" target="_blank">首钢股份</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">000961</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000961/nc.shtml" target="_blank">中南建设</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600436</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600436/nc.shtml" target="_blank">片仔癀</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">600522</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600522/nc.shtml" target="_blank">中天科技</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600909</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600909/nc.shtml" target="_blank">华安证券</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">603160</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603160/nc.shtml" target="_blank">汇顶科技</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">603858</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603858/nc.shtml" target="_blank">步长制药</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">601997</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601997/nc.shtml" target="_blank">贵阳银行</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601992</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601992/nc.shtml" target="_blank">金隅股份</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">601881</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601881/nc.shtml" target="_blank">中国银河</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601229</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601229/nc.shtml" target="_blank">上海银行</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">601117</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601117/nc.shtml" target="_blank">中国化学</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600977</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600977/nc.shtml" target="_blank">中国电影</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">600926</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600926/nc.shtml" target="_blank">杭州银行</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600919</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600919/nc.shtml" target="_blank">江苏银行</a></div></td>
        <td><div align="center">2017-06-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">600549</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600549/nc.shtml" target="_blank">厦门钨业</a></div></td>
        <td><div align="center">2017-02-14</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601155</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601155/nc.shtml" target="_blank">新城控股</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">300033</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300033/nc.shtml" target="_blank">同花顺</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002466</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002466/nc.shtml" target="_blank">天齐锂业</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">000627</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000627/nc.shtml" target="_blank">天茂集团</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002714</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002714/nc.shtml" target="_blank">牧原股份</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">300072</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300072/nc.shtml" target="_blank">三聚环保</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600482</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600482/nc.shtml" target="_blank">中国动力</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">000983</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000983/nc.shtml" target="_blank">西山煤电</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000671</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000671/nc.shtml" target="_blank">阳光城</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">000938</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000938/nc.shtml" target="_blank">紫光股份</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601611</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601611/nc.shtml" target="_blank">中国核建</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">002797</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002797/nc.shtml" target="_blank">第一创业</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002310</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002310/nc.shtml" target="_blank">东方园林</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">601877</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601877/nc.shtml" target="_blank">正泰电器</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600498</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600498/nc.shtml" target="_blank">烽火通信</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr>
        <td><div align="center">600297</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600297/nc.shtml" target="_blank">广汇汽车</a></div></td>
        <td><div align="center">2016-12-12</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000839</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000839/nc.shtml" target="_blank">中信国安</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr>
        <td><div align="center">002027</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002027/nc.shtml" target="_blank">分众传媒</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600061</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600061/nc.shtml" target="_blank">国投安信</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr>
        <td><div align="center">600606</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600606/nc.shtml" target="_blank">绿地控股</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600704</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600704/nc.shtml" target="_blank">物产中大</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr>
        <td><div align="center">600816</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600816/nc.shtml" target="_blank">安信信托</a></div></td>
        <td><div align="center">2016-06-13</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">001979</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz001979/nc.shtml" target="_blank">招商蛇口</a></div></td>
        <td><div align="center">2015-12-30</div></td>
      </tr>
		  <tr>
        <td><div align="center">000415</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000415/nc.shtml" target="_blank">渤海租赁</a></div></td>
        <td><div align="center">2015-12-14</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300144</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300144/nc.shtml" target="_blank">宋城演艺</a></div></td>
        <td><div align="center">2015-12-14</div></td>
      </tr>
		  <tr>
        <td><div align="center">601198</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601198/nc.shtml" target="_blank">东兴证券</a></div></td>
        <td><div align="center">2015-12-14</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601211</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601211/nc.shtml" target="_blank">国泰君安</a></div></td>
        <td><div align="center">2015-12-14</div></td>
      </tr>
		  <tr>
        <td><div align="center">601985</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601985/nc.shtml" target="_blank">中国核电</a></div></td>
        <td><div align="center">2015-12-14</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002736</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002736/nc.shtml" target="_blank">国信证券</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">300059</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300059/nc.shtml" target="_blank">东方财富</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600958</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600958/nc.shtml" target="_blank">东方证券</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">601021</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601021/nc.shtml" target="_blank">春秋航空</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601788</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601788/nc.shtml" target="_blank">光大证券</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">601919</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601919/nc.shtml" target="_blank">中国远洋</a></div></td>
        <td><div align="center">2015-06-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000166</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000166/nc.shtml" target="_blank">申万宏源</a></div></td>
        <td><div align="center">2015-01-26</div></td>
      </tr>
		  <tr>
        <td><div align="center">601727</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601727/nc.shtml" target="_blank">上海电气</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600570</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600570/nc.shtml" target="_blank">恒生电子</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">600038</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600038/nc.shtml" target="_blank">哈飞股份</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300251</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300251/nc.shtml" target="_blank">光线传媒</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">300124</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300124/nc.shtml" target="_blank">汇川技术</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300070</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300070/nc.shtml" target="_blank">碧水源</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">300024</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300024/nc.shtml" target="_blank">机器人</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">300017</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz300017/nc.shtml" target="_blank">网宿科技</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">002153</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002153/nc.shtml" target="_blank">石基信息</a></div></td>
        <td><div align="center">2014-12-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000413</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000413/nc.shtml" target="_blank">东旭光电</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">601216</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601216/nc.shtml" target="_blank">内蒙君正</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601225</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601225/nc.shtml" target="_blank">陕西煤业</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">600023</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600023/nc.shtml" target="_blank">浙能电力</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002252</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002252/nc.shtml" target="_blank">上海莱士</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">000503</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000503/nc.shtml" target="_blank">海虹控股</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002475</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002475/nc.shtml" target="_blank">立讯精密</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">002008</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002008/nc.shtml" target="_blank">大族激光</a></div></td>
        <td><div align="center">2014-06-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002456</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002456/nc.shtml" target="_blank">欧菲光</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">002230</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002230/nc.shtml" target="_blank">科大讯飞</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002065</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002065/nc.shtml" target="_blank">东华软件</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">000826</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000826/nc.shtml" target="_blank">桑德环境</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600018</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600018/nc.shtml" target="_blank">上港集团</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">600688</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600688/nc.shtml" target="_blank">上海石化</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600705</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600705/nc.shtml" target="_blank">中航投资</a></div></td>
        <td><div align="center">2013-12-16</div></td>
      </tr>
		  <tr>
        <td><div align="center">000333</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000333/nc.shtml" target="_blank">美的集团</a></div></td>
        <td><div align="center">2013-09-18</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000963</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000963/nc.shtml" target="_blank">华东医药</a></div></td>
        <td><div align="center">2013-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">002450</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002450/nc.shtml" target="_blank">康得新</a></div></td>
        <td><div align="center">2013-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600332</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600332/nc.shtml" target="_blank">广州药业</a></div></td>
        <td><div align="center">2013-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">603993</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh603993/nc.shtml" target="_blank">洛阳钼业</a></div></td>
        <td><div align="center">2013-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002236</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002236/nc.shtml" target="_blank">大华股份</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">002673</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002673/nc.shtml" target="_blank">西部证券</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600157</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600157/nc.shtml" target="_blank">永泰能源</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600340</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600340/nc.shtml" target="_blank">华夏幸福</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600637</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600637/nc.shtml" target="_blank">百视通</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600886</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600886/nc.shtml" target="_blank">国投电力</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601800</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601800/nc.shtml" target="_blank">中国交建</a></div></td>
        <td><div align="center">2013-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">000725</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000725/nc.shtml" target="_blank">京东方A</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002081</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002081/nc.shtml" target="_blank">金螳螂</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">002241</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002241/nc.shtml" target="_blank">歌尔声学</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601336</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601336/nc.shtml" target="_blank">新华保险</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">601555</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601555/nc.shtml" target="_blank">东吴证券</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601633</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601633/nc.shtml" target="_blank">长城汽车</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">601669</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601669/nc.shtml" target="_blank">中国水电</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601901</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601901/nc.shtml" target="_blank">方正证券</a></div></td>
        <td><div align="center">2012-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">600372</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600372/nc.shtml" target="_blank">中航电子</a></div></td>
        <td><div align="center">2012-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002594</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002594/nc.shtml" target="_blank">比亚迪</a></div></td>
        <td><div align="center">2012-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">601018</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601018/nc.shtml" target="_blank">宁波港</a></div></td>
        <td><div align="center">2011-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601377</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601377/nc.shtml" target="_blank">兴业证券</a></div></td>
        <td><div align="center">2011-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601933</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601933/nc.shtml" target="_blank">永辉超市</a></div></td>
        <td><div align="center">2011-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000776</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000776/nc.shtml" target="_blank">广发证券</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">002146</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002146/nc.shtml" target="_blank">荣盛发展</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002415</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002415/nc.shtml" target="_blank">海康威视</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600115</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600115/nc.shtml" target="_blank">东方航空</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600406</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600406/nc.shtml" target="_blank">国电南瑞</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600276</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600276/nc.shtml" target="_blank">恒瑞医药</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600535</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600535/nc.shtml" target="_blank">天士力</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600703</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600703/nc.shtml" target="_blank">三安光电</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600887</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600887/nc.shtml" target="_blank">伊利股份</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600893</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600893/nc.shtml" target="_blank">航空动力</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601818</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601818/nc.shtml" target="_blank">光大银行</a></div></td>
        <td><div align="center">2011-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">601288</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601288/nc.shtml" target="_blank">农业银行</a></div></td>
        <td><div align="center">2010-07-29</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002304</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002304/nc.shtml" target="_blank">洋河股份</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">600999</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600999/nc.shtml" target="_blank">招商证券</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601607</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601607/nc.shtml" target="_blank">上海医药</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601688</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601688/nc.shtml" target="_blank">华泰证券</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601888</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601888/nc.shtml" target="_blank">中国国旅</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601989</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601989/nc.shtml" target="_blank">中国重工</a></div></td>
        <td><div align="center">2010-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002007</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002007/nc.shtml" target="_blank">华兰生物</a></div></td>
        <td><div align="center">2010-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600369</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600369/nc.shtml" target="_blank">西南证券</a></div></td>
        <td><div align="center">2010-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601618</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601618/nc.shtml" target="_blank">中国中冶</a></div></td>
        <td><div align="center">2010-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">601668</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601668/nc.shtml" target="_blank">中国建筑</a></div></td>
        <td><div align="center">2010-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600518</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600518/nc.shtml" target="_blank">康美药业</a></div></td>
        <td><div align="center">2009-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601766</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601766/nc.shtml" target="_blank">中国南车</a></div></td>
        <td><div align="center">2009-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600352</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600352/nc.shtml" target="_blank">浙江龙盛</a></div></td>
        <td><div align="center">2009-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">000100</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000100/nc.shtml" target="_blank">TCL集团</a></div></td>
        <td><div align="center">2009-01-05</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600588</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600588/nc.shtml" target="_blank">用友软件</a></div></td>
        <td><div align="center">2009-01-05</div></td>
      </tr>
		  <tr>
        <td><div align="center">600674</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600674/nc.shtml" target="_blank">川投能源</a></div></td>
        <td><div align="center">2009-01-05</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601186</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601186/nc.shtml" target="_blank">中国铁建</a></div></td>
        <td><div align="center">2009-01-05</div></td>
      </tr>
		  <tr>
        <td><div align="center">601899</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601899/nc.shtml" target="_blank">紫金矿业</a></div></td>
        <td><div align="center">2009-01-05</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000728</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000728/nc.shtml" target="_blank">国元证券</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">000783</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000783/nc.shtml" target="_blank">长江证券</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002202</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002202/nc.shtml" target="_blank">金风科技</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601390</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601390/nc.shtml" target="_blank">中国中铁</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601601</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601601/nc.shtml" target="_blank">中国太保</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">601939</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601939/nc.shtml" target="_blank">建设银行</a></div></td>
        <td><div align="center">2008-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601169</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601169/nc.shtml" target="_blank">北京银行</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">601009</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601009/nc.shtml" target="_blank">南京银行</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600111</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600111/nc.shtml" target="_blank">包钢稀土</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">600089</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600089/nc.shtml" target="_blank">特变电工</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">002142</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002142/nc.shtml" target="_blank">宁波银行</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">000895</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000895/nc.shtml" target="_blank">双汇发展</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000423</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000423/nc.shtml" target="_blank">东阿阿胶</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">000338</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000338/nc.shtml" target="_blank">潍柴动力</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600109</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600109/nc.shtml" target="_blank">国金证券</a></div></td>
        <td><div align="center">2008-01-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">601857</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601857/nc.shtml" target="_blank">中国石油</a></div></td>
        <td><div align="center">2007-11-19</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601088</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601088/nc.shtml" target="_blank">中国神华</a></div></td>
        <td><div align="center">2007-10-23</div></td>
      </tr>
		  <tr>
        <td><div align="center">601333</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601333/nc.shtml" target="_blank">广深铁路</a></div></td>
        <td><div align="center">2007-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000876</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000876/nc.shtml" target="_blank">新希望</a></div></td>
        <td><div align="center">2007-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">600837</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600837/nc.shtml" target="_blank">海通证券</a></div></td>
        <td><div align="center">2007-07-02</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600208</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600208/nc.shtml" target="_blank">新湖中宝</a></div></td>
        <td><div align="center">2007-07-02</div></td>
      </tr>
		  <tr>
        <td><div align="center">601328</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601328/nc.shtml" target="_blank">交通银行</a></div></td>
        <td><div align="center">2007-05-29</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601998</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601998/nc.shtml" target="_blank">中信银行</a></div></td>
        <td><div align="center">2007-05-18</div></td>
      </tr>
		  <tr>
        <td><div align="center">601600</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601600/nc.shtml" target="_blank">中国铝业</a></div></td>
        <td><div align="center">2007-04-30</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601318</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601318/nc.shtml" target="_blank">中国平安</a></div></td>
        <td><div align="center">2007-03-15</div></td>
      </tr>
		  <tr>
        <td><div align="center">601166</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601166/nc.shtml" target="_blank">兴业银行</a></div></td>
        <td><div align="center">2007-02-26</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601628</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601628/nc.shtml" target="_blank">中国人寿</a></div></td>
        <td><div align="center">2007-01-23</div></td>
      </tr>
		  <tr>
        <td><div align="center">600066</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600066/nc.shtml" target="_blank">宇通客车</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600118</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600118/nc.shtml" target="_blank">中国卫星</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600489</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600489/nc.shtml" target="_blank">中金黄金</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600048</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600048/nc.shtml" target="_blank">保利地产</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600068</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600068/nc.shtml" target="_blank">葛洲坝</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601111</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601111/nc.shtml" target="_blank">中国国航</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">600547</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600547/nc.shtml" target="_blank">山东黄金</a></div></td>
        <td><div align="center">2007-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601398</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601398/nc.shtml" target="_blank">工商银行</a></div></td>
        <td><div align="center">2006-11-10</div></td>
      </tr>
		  <tr>
        <td><div align="center">601006</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601006/nc.shtml" target="_blank">大秦铁路</a></div></td>
        <td><div align="center">2006-08-15</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">601988</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh601988/nc.shtml" target="_blank">中国银行</a></div></td>
        <td><div align="center">2006-07-19</div></td>
      </tr>
		  <tr>
        <td><div align="center">600415</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600415/nc.shtml" target="_blank">小商品城</a></div></td>
        <td><div align="center">2006-07-03</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600271</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600271/nc.shtml" target="_blank">航天信息</a></div></td>
        <td><div align="center">2006-04-21</div></td>
      </tr>
		  <tr>
        <td><div align="center">600383</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600383/nc.shtml" target="_blank">金地集团</a></div></td>
        <td><div align="center">2006-01-04</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000768</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000768/nc.shtml" target="_blank">西飞国际</a></div></td>
        <td><div align="center">2006-01-04</div></td>
      </tr>
		  <tr>
        <td><div align="center">002024</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz002024/nc.shtml" target="_blank">苏宁电器</a></div></td>
        <td><div align="center">2005-07-01</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000538</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000538/nc.shtml" target="_blank">云南白药</a></div></td>
        <td><div align="center">2005-07-01</div></td>
      </tr>
		  <tr>
        <td><div align="center">000157</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000157/nc.shtml" target="_blank">中联重科</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000425</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000425/nc.shtml" target="_blank">徐工科技</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000568</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000568/nc.shtml" target="_blank">泸州老窖</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600019</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600019/nc.shtml" target="_blank">宝钢股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000630</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000630/nc.shtml" target="_blank">铜陵有色</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000651</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000651/nc.shtml" target="_blank">格力电器</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000625</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000625/nc.shtml" target="_blank">长安汽车</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000709</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000709/nc.shtml" target="_blank">唐钢股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000792</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000792/nc.shtml" target="_blank">盐湖钾肥</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000069</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000069/nc.shtml" target="_blank">华侨城A</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000063</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000063/nc.shtml" target="_blank">中兴通讯</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000402</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000402/nc.shtml" target="_blank">金融街</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">000002</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000002/nc.shtml" target="_blank">万科A</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000001</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000001/nc.shtml" target="_blank">深发展A</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600050</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600050/nc.shtml" target="_blank">中国联通</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600036</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600036/nc.shtml" target="_blank">招商银行</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600031</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600031/nc.shtml" target="_blank">三一重工</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600030</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600030/nc.shtml" target="_blank">中信证券</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600029</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600029/nc.shtml" target="_blank">南方航空</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600015</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600015/nc.shtml" target="_blank">华夏银行</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600028</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600028/nc.shtml" target="_blank">中国石化</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600016</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600016/nc.shtml" target="_blank">民生银行</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600010</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600010/nc.shtml" target="_blank">包钢股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600009</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600009/nc.shtml" target="_blank">上海机场</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600900</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600900/nc.shtml" target="_blank">长江电力</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600795</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600795/nc.shtml" target="_blank">国电电力</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600739</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600739/nc.shtml" target="_blank">辽宁成大</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600741</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600741/nc.shtml" target="_blank">巴士股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600690</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600690/nc.shtml" target="_blank">青岛海尔</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600221</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600221/nc.shtml" target="_blank">海南航空</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600583</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600583/nc.shtml" target="_blank">海油工程</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600585</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600585/nc.shtml" target="_blank">海螺水泥</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600519</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml" target="_blank">贵州茅台</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">000858</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sz000858/nc.shtml" target="_blank">五粮液</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600309</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600309/nc.shtml" target="_blank">烟台万华</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600196</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600196/nc.shtml" target="_blank">复星医药</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600000</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600000/nc.shtml" target="_blank">浦发银行</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600660</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600660/nc.shtml" target="_blank">福耀玻璃</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600085</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600085/nc.shtml" target="_blank">同仁堂</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600100</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600100/nc.shtml" target="_blank">同方股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600104</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600104/nc.shtml" target="_blank">上海汽车</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600153</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600153/nc.shtml" target="_blank">建发股份</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600188</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600188/nc.shtml" target="_blank">兖州煤业</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600177</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600177/nc.shtml" target="_blank">雅戈尔</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr>
        <td><div align="center">600170</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600170/nc.shtml" target="_blank">上海建工</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
		  <tr class="tr_2">
        <td><div align="center">600362</div></td>
        <td><div align="center"><a href="http://finance.sina.com.cn/realstock/company/sh600362/nc.shtml" target="_blank">江西铜业</a></div></td>
        <td><div align="center">2005-04-08</div></td>
      </tr>
	''' 
# print( stock_list_str )

p = re.compile(u"(s[h,z])(\d{6})/nc.shtml\" target=\"_blank\">([\u4e00-\u9fa5]+)</a></div>")
# p = re.compile(u"/(s[h,z])(\d{4})/nc.shtml\" target=\"_blank\">([\u4e00-\u9fa5]+)</a></div>")
m = re.findall(p, stock_list_str)
print( m )
# print( len(m) )
# pf.DataFrame( m ).to_csv('./data/hs300.csv')



# psh = re.compile(u"<td><div align=\"center\">(60\d{4})</div></td>")
# psz = re.compile(u"<td><div align=\"center\">(00\d{4})</div></td>")

# # psz = re.compile(u"(00\d{4}),([\u4e00-\u9fa5]+),")

# # m1 = re.search(psh, stock_list_str)
# # m2 = re.search(psz, stock_list_str)

# m1 = re.findall(psh, stock_list_str)
# m2 = re.findall(psz, stock_list_str)
# print( m1 )
# print( m2 )
# print( len(m1) )
# print( len(m2) )


# a = {'pages': 6, 
# 'data': ["603993,洛阳钼业,有色金属,洛阳市,0.19,1.91,10.42,215.99240583,215.99240583,3.74,660.6998946042,14.65,0.282918,000300,2019-01-03,3.74,0.81,551982,205053788","603986,兆易创新,电子设备,北京市,1.31,6.71,20.03,2.84644488,2.07397179,59.2,122.779129968,34.4,0.091848,000300,2019-01-03,59.20,-1.00,37396,224237190","603858,步长制药,医药生物,菏泽市,1.37,14.96,9.21,8.8634,4.26185646,24.85,105.907133031,13.59,0.119421,000300,2019-01-03,24.85,-0.48,24378,60978544","603833,欧派家居,,广州市,2.85,17.1,17.9,4.20283454,0.92108143,75.88,69.8916589084,19.93,0.105194,000300,2019-01-03,75.88,-1.85,2813,21575430","603799,华友钴业,有色金属,嘉兴市,2.3,9.69,27.18,8.29747285,8.19881192,29.39,240.9630823288,9.57,0.157527,000300,2019-01-03,29.39,0.24,172257,506880400","603288,海天味业,食品饮料,佛山市,1.16,4.67,25.71,27.0036934,27.0036934,65,1755.240071,42.04,0.588905,000300,2019-01-03,65.00,-3.47,32544,210606074","603260,合盛硅业,,嘉兴市,3.35,11,35.14,6.7,2.60841805,42.1,109.814399905,9.42,0.034328,000300,2019-01-03,42.10,-2.46,17098,72893895","603259,药明康德,,无锡市,1.94,10.14,22.8,11.64741086,2.20672756,71.62,74.6270058072,32.44,0.081383,000300,2019-01-03,71.62,-0.44,18278,131323627","603160,汇顶科技,电子设备,深圳市,0.7,8.06,8.89,4.56651659,2.31595583,72.42,167.7215212086,77.82,0.071901,000300,2019-01-03,72.42,-0.73,10620,76464278","603156,养元饮品,,衡水市,2.34,14.54,19.04,7.5327,0.6027,41.77,25.174779,13.56,0.027138,000300,2019-01-03,41.77,0.10,7184,29857847","601998,中信银行,金融,北京市,0.72,7.95,8.93,489.34796573,467.87327034,5.34,1703.7357606438,5.33,0.176284,000300,2019-01-03,5.34,0.19,134374,71681120","601997,贵阳银行,金融,贵阳市,1.62,12.22,14.14,22.985919,12.38965095,10.61,131.4541965795,4.9,0.157319,000300,2019-01-03,10.61,0.38,49369,52443181","601992,金隅集团,建材,北京市,0.29,4.01,5.78,106.77771134,106.72923134,3.28,273.3603910592,8.46,0.12095,000300,2019-01-03,3.28,-2.38,711933,234218357","601991,大唐发电,公用事业,北京市,0.1,2.56,3.96,185.06710504,133.10037578,3.13,312.823468,24.66,0.083744,000300,2019-01-03,3.13,0.00,74826,23556652","601989,中国重工,交运设备,北京市,0.06,3.71,1.91,228.79793243,183.61665066,4.35,798.732430371,52.75,0.420741,000300,2019-01-03,4.35,2.11,928211,402425808","601988,中国银行,金融,北京市,0.5,5.02,9.97,2943.87791241,2943.87791241,3.55,7482.175777033,5.11,0.805186,000300,2019-01-03,3.55,0.28,970304,343657152","601985,中国核电,公用事业,北京市,0.25,2.93,8.53,155.6543,155.6543,5.28,821.854704,16.22,0.265575,000300,2019-01-03,5.28,0.19,108637,57353217","601939,建设银行,金融,北京市,0.86,7.44,11.57,2500.10977486,2500.10977486,6.26,600.5629661356,5.48,0.452956,000300,2019-01-03,6.26,0.16,375585,235052101","601933,永辉超市,商贸零售,福州市,0.11,1.96,5.26,95.70462108,79.68291316,7.9,629.495013964,55.71,0.326372,000300,2019-01-03,7.90,0.00,243275,192061272","601919,中远海控,交通运输,天津市,0.08,2.19,4.01,102.16274357,102.16274357,4.2,320.698322994,37.31,0.168101,000300,2019-01-03,4.20,2.94,220037,91620017","601901,方正证券,金融,长沙市,0.06,4.61,1.21,82.32101395,82.32101395,5.83,479.9315113285,79.19,0.235424,000300,2019-01-03,5.83,10.00,943011,545368432","601899,紫金矿业,有色金属,龙岩市,0.15,1.53,9.47,230.31218891,226.12665837,3.05,514.7096380285,15.72,0.393242,000300,2019-01-03,3.05,1.33,2236570,671474352","601898,中煤能源,能源,北京市,0.31,6.96,4.55,132.586634,132.586634,4.67,427.39841868,11.26,0.091458,000300,2019-01-03,4.67,0.86,72982,34070535","601888,中国国旅,餐饮旅游,北京市,1.39,8.12,18.1,19.52475544,19.52475544,56.98,1112.5205649712,30.84,0.630014,000300,2019-01-03,56.98,-4.72,112043,646870464","601881,中国银河,,北京市,0.18,6.46,2.88,101.37258757,49.19515517,6.93,85.1371902612,28.18,0.09475,000300,2019-01-03,6.93,1.76,178995,125009120","601878,浙商证券,金融,杭州市,0.17,4.08,4.14,33.333334,12.08508241,7.3,88.221101593,32.48,0.103169,000300,2019-01-03,7.30,1.81,318880,235343384","601877,正泰电器,电气设备,温州市,1.3,9.69,13.66,21.51428516,17.371839,22.51,391.04009589,13.02,0.218709,000300,2019-01-03,22.51,-4.42,64583,147431380","601857,中国石油,能源,北京市,0.26,6.65,3.99,1830.20977818,1830.20977818,7.21,11674.5818106778,20.57,0.625579,000300,2019-01-03,7.21,0.70,247369,177485219","601838,成都银行,金融,成都市,0.95,8.28,12.38,36.12251334,3.61225134,7.97,28.7896431798,6.36,0.034005,000300,2019-01-03,7.97,0.50,64766,51888328","601828,美凯龙,轻工制造,上海市,1.09,11.63,10.18,35.5,9.88896031,10.51,33.1065,6.73,0.036771,000300,2019-01-03,10.51,-2.41,43787,46668645","601818,光大银行,金融,北京市,0.5,5.42,8.97,524.89265354,466.79265354,3.75,1492.894869525,5.32,0.627255,000300,2019-01-03,3.75,2.74,688409,256292723","601808,中海油服,能源,天津市,-0.06,7.16,-0.81,47.71592,47.71592,8.26,244.5346568,-106.81,0.053482,000300,2019-01-03,8.26,-1.31,42318,35137893","601800,中国交建,建筑,北京市,0.74,10.46,6.95,161.74735425,161.74735425,11.06,1299.244238005,10.43,0.281438,000300,2019-01-03,11.06,-0.36,126334,140104225","601788,光大证券,金融,上海市,0.26,10.58,2.42,46.10787639,46.10787639,8.93,348.8682063227,26.24,0.184451,000300,2019-01-03,8.93,2.06,301563,270525952","601766,中国中车,交运设备,北京市,0.26,4.34,6.12,286.98864088,272.88758333,9.04,2071.7593832872,25.83,0.928343,000300,2019-01-03,9.04,2.26,528228,472865408","601727,上海电气,电气设备,上海市,0.15,3.86,3.86,147.25187459,129.63033574,5,499.5060787,25.46,0.18834,000300,2019-01-03,5.00,1.01,74249,36765153","601688,华泰证券,金融,南京市,0.61,12.88,4.63,82.515,71.627688,16.56,901.480548672,22.88,0.57173,000300,2019-01-03,16.56,2.10,590724,982742848","601669,中国电建,建筑,北京市,0.38,5.08,7.45,152.99035024,111.4440154,4.9,546.07567546,9.29,0.324925,000300,2019-01-03,4.90,-0.41,160660,78692797","601668,中国建筑,建筑,北京市,0.62,5.11,12.07,419.85174455,416.24384644,5.6,2330.965540064,6.46,1.268666,000300,2019-01-03,5.60,0.00,601047,335024112","601633,长城汽车,交运设备,保定市,0.43,5.62,7.82,91.27269,91.27269,5.58,336.3472782,9.73,0.072986,000300,2019-01-03,5.58,-0.53,102360,57137006","601628,中国人寿,金融,北京市,0.69,11.41,6.1,282.64705,282.64705,20.16,4198.023648,21.51,0.358658,000300,2019-01-03,20.16,1.05,46153,92670930","601618,中国中冶,建筑,北京市,0.18,3.17,4.54,207.2361917,207.2361917,3.07,548.075408519,12.67,0.236589,000300,2019-01-03,3.07,0.00,207350,63437535","601611,中国核建,建筑,上海市,0.22,3.23,6.05,26.25,9.618,6.58,63.28644,22.44,0.055665,000300,2019-01-03,6.58,0.46,32944,21729110","601607,上海医药,医药生物,上海市,1.19,13.56,9.29,28.42089322,28.42007722,16.54,318.0534519772,10.46,0.204083,000300,2019-01-03,16.54,0.92,67462,110492416","601601,中国太保,金融,上海市,1.4,15.78,9.07,90.62,90.62,27.93,1755.87531,14.93,0.929473,000300,2019-01-03,27.93,1.93,199312,555746016","601600,中国铝业,有色金属,北京市,0.08,3.32,3.29,149.03798236,149.03798236,3.52,385.7860958336,26.29,0.24838,000300,2019-01-03,3.52,0.57,267150,93840739","601555,东吴证券,金融,苏州市,0.06,6.81,0.93,30,28.91,6.9,199.479,80.86,0.174827,000300,2019-01-03,6.90,2.22,202954,140881527","601398,工商银行,金融,北京市,0.67,6.12,10.91,3564.06257089,3564.06257089,5.2,14019.835052028,5.8,1.210393,000300,2019-01-03,5.20,0.00,943284,489960752","601390,中国中铁,建筑,北京市,0.56,6.87,8.05,228.44301543,228.44301543,6.92,1289.6742787756,9.09,0.552693,000300,2019-01-03,6.92,0.73,325934,224714583","601377,兴业证券,金融,福州市,0.11,4.96,2.18,66.96671674,66.96671674,4.62,309.3862313388,31.92,0.227142,000300,2019-01-03,4.62,2.90,518175,239995542"]
# }

# data = (
#     ["603993,洛阳钼业,有色金属,洛阳市,0.19,1.91,10.42,215.99240583,215.99240583,3.74,660.6998946042,14.65,0.282918,000300,2019-01-03,3.74,0.81,551982,205053788","603986,兆易创新,电子设备,北京市,1.31,6.71,20.03,2.84644488,2.07397179,59.2,122.779129968,34.4,0.091848,000300,2019-01-03,59.20,-1.00,37396,224237190","603858,步长制药,医药生物,菏泽市,1.37,14.96,9.21,8.8634,4.26185646,24.85,105.907133031,13.59,0.119421,000300,2019-01-03,24.85,-0.48,24378,60978544","603833,欧派家居,,广州市,2.85,17.1,17.9,4.20283454,0.92108143,75.88,69.8916589084,19.93,0.105194,000300,2019-01-03,75.88,-1.85,2813,21575430","603799,华友钴业,有色金属,嘉兴市,2.3,9.69,27.18,8.29747285,8.19881192,29.39,240.9630823288,9.57,0.157527,000300,2019-01-03,29.39,0.24,172257,506880400","603288,海天味业,食品饮料,佛山市,1.16,4.67,25.71,27.0036934,27.0036934,65,1755.240071,42.04,0.588905,000300,2019-01-03,65.00,-3.47,32544,210606074","603260,合盛硅业,,嘉兴市,3.35,11,35.14,6.7,2.60841805,42.1,109.814399905,9.42,0.034328,000300,2019-01-03,42.10,-2.46,17098,72893895","603259,药明康德,,无锡市,1.94,10.14,22.8,11.64741086,2.20672756,71.62,74.6270058072,32.44,0.081383,000300,2019-01-03,71.62,-0.44,18278,131323627","603160,汇顶科技,电子设备,深圳市,0.7,8.06,8.89,4.56651659,2.31595583,72.42,167.7215212086,77.82,0.071901,000300,2019-01-03,72.42,-0.73,10620,76464278","603156,养元饮品,,衡水市,2.34,14.54,19.04,7.5327,0.6027,41.77,25.174779,13.56,0.027138,000300,2019-01-03,41.77,0.10,7184,29857847","601998,中信银行,金融,北京市,0.72,7.95,8.93,489.34796573,467.87327034,5.34,1703.7357606438,5.33,0.176284,000300,2019-01-03,5.34,0.19,134374,71681120","601997,贵阳银行,金融,贵阳市,1.62,12.22,14.14,22.985919,12.38965095,10.61,131.4541965795,4.9,0.157319,000300,2019-01-03,10.61,0.38,49369,52443181","601992,金隅集团,建材,北京市,0.29,4.01,5.78,106.77771134,106.72923134,3.28,273.3603910592,8.46,0.12095,000300,2019-01-03,3.28,-2.38,711933,234218357","601991,大唐发电,公用事业,北京市,0.1,2.56,3.96,185.06710504,133.10037578,3.13,312.823468,24.66,0.083744,000300,2019-01-03,3.13,0.00,74826,23556652","601989,中国重工,交运设备,北京市,0.06,3.71,1.91,228.79793243,183.61665066,4.35,798.732430371,52.75,0.420741,000300,2019-01-03,4.35,2.11,928211,402425808","601988,中国银行,金融,北京市,0.5,5.02,9.97,2943.87791241,2943.87791241,3.55,7482.175777033,5.11,0.805186,000300,2019-01-03,3.55,0.28,970304,343657152","601985,中国核电,公用事业,北京市,0.25,2.93,8.53,155.6543,155.6543,5.28,821.854704,16.22,0.265575,000300,2019-01-03,5.28,0.19,108637,57353217","601939,建设银行,金融,北京市,0.86,7.44,11.57,2500.10977486,2500.10977486,6.26,600.5629661356,5.48,0.452956,000300,2019-01-03,6.26,0.16,375585,235052101","601933,永辉超市,商贸零售,福州市,0.11,1.96,5.26,95.70462108,79.68291316,7.9,629.495013964,55.71,0.326372,000300,2019-01-03,7.90,0.00,243275,192061272","601919,中远海控,交通运输,天津市,0.08,2.19,4.01,102.16274357,102.16274357,4.2,320.698322994,37.31,0.168101,000300,2019-01-03,4.20,2.94,220037,91620017","601901,方正证券,金融,长沙市,0.06,4.61,1.21,82.32101395,82.32101395,5.83,479.9315113285,79.19,0.235424,000300,2019-01-03,5.83,10.00,943011,545368432","601899,紫金矿业,有色金属,龙岩市,0.15,1.53,9.47,230.31218891,226.12665837,3.05,514.7096380285,15.72,0.393242,000300,2019-01-03,3.05,1.33,2236570,671474352","601898,中煤能源,能源,北京市,0.31,6.96,4.55,132.586634,132.586634,4.67,427.39841868,11.26,0.091458,000300,2019-01-03,4.67,0.86,72982,34070535","601888,中国国旅,餐饮旅游,北京市,1.39,8.12,18.1,19.52475544,19.52475544,56.98,1112.5205649712,30.84,0.630014,000300,2019-01-03,56.98,-4.72,112043,646870464","601881,中国银河,,北京市,0.18,6.46,2.88,101.37258757,49.19515517,6.93,85.1371902612,28.18,0.09475,000300,2019-01-03,6.93,1.76,178995,125009120","601878,浙商证券,金融,杭州市,0.17,4.08,4.14,33.333334,12.08508241,7.3,88.221101593,32.48,0.103169,000300,2019-01-03,7.30,1.81,318880,235343384","601877,正泰电器,电气设备,温州市,1.3,9.69,13.66,21.51428516,17.371839,22.51,391.04009589,13.02,0.218709,000300,2019-01-03,22.51,-4.42,64583,147431380","601857,中国石油,能源,北京市,0.26,6.65,3.99,1830.20977818,1830.20977818,7.21,11674.5818106778,20.57,0.625579,000300,2019-01-03,7.21,0.70,247369,177485219","601838,成都银行,金融,成都市,0.95,8.28,12.38,36.12251334,3.61225134,7.97,28.7896431798,6.36,0.034005,000300,2019-01-03,7.97,0.50,64766,51888328","601828,美凯龙,轻工制造,上海市,1.09,11.63,10.18,35.5,9.88896031,10.51,33.1065,6.73,0.036771,000300,2019-01-03,10.51,-2.41,43787,46668645","601818,光大银行,金融,北京市,0.5,5.42,8.97,524.89265354,466.79265354,3.75,1492.894869525,5.32,0.627255,000300,2019-01-03,3.75,2.74,688409,256292723","601808,中海油服,能源,天津市,-0.06,7.16,-0.81,47.71592,47.71592,8.26,244.5346568,-106.81,0.053482,000300,2019-01-03,8.26,-1.31,42318,35137893","601800,中国交建,建筑,北京市,0.74,10.46,6.95,161.74735425,161.74735425,11.06,1299.244238005,10.43,0.281438,000300,2019-01-03,11.06,-0.36,126334,140104225","601788,光大证券,金融,上海市,0.26,10.58,2.42,46.10787639,46.10787639,8.93,348.8682063227,26.24,0.184451,000300,2019-01-03,8.93,2.06,301563,270525952","601766,中国中车,交运设备,北京市,0.26,4.34,6.12,286.98864088,272.88758333,9.04,2071.7593832872,25.83,0.928343,000300,2019-01-03,9.04,2.26,528228,472865408","601727,上海电气,电气设备,上海市,0.15,3.86,3.86,147.25187459,129.63033574,5,499.5060787,25.46,0.18834,000300,2019-01-03,5.00,1.01,74249,36765153","601688,华泰证券,金融,南京市,0.61,12.88,4.63,82.515,71.627688,16.56,901.480548672,22.88,0.57173,000300,2019-01-03,16.56,2.10,590724,982742848","601669,中国电建,建筑,北京市,0.38,5.08,7.45,152.99035024,111.4440154,4.9,546.07567546,9.29,0.324925,000300,2019-01-03,4.90,-0.41,160660,78692797","601668,中国建筑,建筑,北京市,0.62,5.11,12.07,419.85174455,416.24384644,5.6,2330.965540064,6.46,1.268666,000300,2019-01-03,5.60,0.00,601047,335024112","601633,长城汽车,交运设备,保定市,0.43,5.62,7.82,91.27269,91.27269,5.58,336.3472782,9.73,0.072986,000300,2019-01-03,5.58,-0.53,102360,57137006","601628,中国人寿,金融,北京市,0.69,11.41,6.1,282.64705,282.64705,20.16,4198.023648,21.51,0.358658,000300,2019-01-03,20.16,1.05,46153,92670930","601618,中国中冶,建筑,北京市,0.18,3.17,4.54,207.2361917,207.2361917,3.07,548.075408519,12.67,0.236589,000300,2019-01-03,3.07,0.00,207350,63437535","601611,中国核建,建筑,上海市,0.22,3.23,6.05,26.25,9.618,6.58,63.28644,22.44,0.055665,000300,2019-01-03,6.58,0.46,32944,21729110","601607,上海医药,医药生物,上海市,1.19,13.56,9.29,28.42089322,28.42007722,16.54,318.0534519772,10.46,0.204083,000300,2019-01-03,16.54,0.92,67462,110492416","601601,中国太保,金融,上海市,1.4,15.78,9.07,90.62,90.62,27.93,1755.87531,14.93,0.929473,000300,2019-01-03,27.93,1.93,199312,555746016","601600,中国铝业,有色金属,北京市,0.08,3.32,3.29,149.03798236,149.03798236,3.52,385.7860958336,26.29,0.24838,000300,2019-01-03,3.52,0.57,267150,93840739","601555,东吴证券,金融,苏州市,0.06,6.81,0.93,30,28.91,6.9,199.479,80.86,0.174827,000300,2019-01-03,6.90,2.22,202954,140881527","601398,工商银行,金融,北京市,0.67,6.12,10.91,3564.06257089,3564.06257089,5.2,14019.835052028,5.8,1.210393,000300,2019-01-03,5.20,0.00,943284,489960752","601390,中国中铁,建筑,北京市,0.56,6.87,8.05,228.44301543,228.44301543,6.92,1289.6742787756,9.09,0.552693,000300,2019-01-03,6.92,0.73,325934,224714583","601377,兴业证券,金融,福州市,0.11,4.96,2.18,66.96671674,66.96671674,4.62,309.3862313388,31.92,0.227142,000300,2019-01-03,4.62,2.90,518175,239995542"],
# )

# data = a['data']
stock_codes = []
stock_names = []

# psh = r"60\d{4},[\u4e00-\u9fa5]+,"
# psz = r"00\d{4},[\u4e00-\u9fa5]+,"

# psh = re.compile(u"(60\d{4}),([\u4e00-\u9fa5]+),")
# psz = re.compile(u"(00\d{4}),([\u4e00-\u9fa5]+),")

# m1 = re.search(psh, data[0])
# m2 = re.search(psz, data[0])
# print( m1 )
# print( m1.group(1), m1.group(2) )
# print( m2 )

# for i in range(0, len(data)):
#     m1 = re.search(psh, data[i])
#     m2 = re.search(psz, data[i])
#     if m1:
#         stock_codes.append( m1.group(1) + '.sh' )
#         stock_names.append( m1.group(2) )
#     elif m2:
#         stock_codes.append( m1.group(1) + '.sz' )
#         stock_names.append( m1.group(2) )

# print( stock_codes )
# print( stock_names )

    # stock_codes.append(data[i])

# print (a['data'][0])
# print (a['data'][2])
# print (a['data'][9])
