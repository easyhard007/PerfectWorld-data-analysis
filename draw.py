from pyecharts.charts import Scatter
import pyecharts.options as opts
import pandas as pd
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker

def drawGodScoreChart(playerNames,scores,adrs,godScores,count10s,title='',method='score'):
    yaxis_name = '完美天梯分'
    formatter_score = JsCode(
                        "function (params) {return '【'+params.value[3] +'】<br>天梯分: '+  params.value[1] +  '<br>十黑场数: ' + params.value[4] + '<br>十黑场均ADR: ' + params.value[0] + '<br> 内战幻神指数: '+ params.value[2]}"
                    )

    if(method=='ranking'):
        yaxis_name = '天梯场均ADR'
        formatter_score = JsCode(
                        "function (params) {return '【'+params.value[3] +'】<br>天梯场均ADR: '+  params.value[1] +  '<br>十黑场数: ' + params.value[4] + '<br>十黑场均ADR: ' + params.value[0] + '<br> 内战幻神指数: '+ params.value[2]}"
                    )
    c = (
        Scatter(init_opts=opts.InitOpts(width="1000px", height="800px"))
        .add_xaxis(adrs)
        .add_yaxis(
            '',
            [list(z) for z in zip(scores,godScores,playerNames,count10s)],
            label_opts=opts.LabelOpts(
                formatter=JsCode(
                    "function(params){return params.value[3];}"
                )
            ),)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                name='十黑场均ADR',
                type_="value", 
                min_= min(adrs)*0.9 ,
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name=yaxis_name,
                type_="value",
                min_= min(scores)*0.9,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(
                formatter=formatter_score
            ),
            title_opts=opts.TitleOpts(
                title=title,
                pos_left='center'
                ),
            visualmap_opts=opts.VisualMapOpts(
                type_="color", max_=max(godScores), min_=min(godScores), dimension=2 , orient="horizontal", pos_left="center", range_text=["内战幻神", "内战演员"],item_height=500,item_width=20
            ),
            datazoom_opts=opts.DataZoomOpts(type_="inside",range_start=0,range_end=100)
        )
        .render(title+".html")
    )


