"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 11:23
@Site    : 
@File    : altair_plot_test.py
@Software: PyCharm
@Remark  : 
"""

import unittest

import altair as alt
from vega_datasets import data
import altair_viewer

import warnings

from app_test.test_utils.wrapper_utils import Tester

alt.renderers.enable("altair_viewer")
warnings.filterwarnings("ignore")


class AltairPlotCase(unittest.TestCase):
    """
    使用单元的DataFrame
    Altair 用到了协程相关
    """

    @Tester(
        exec_time=True,
    )
    def test_base_plot(self):
        """
        基本的plot
        :return:
        """
        cars = data.cars()
        chart = alt.Chart(cars).mark_point().encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color="Origin"
        )
        chart.show()

    @Tester(
        # args=["test_base_plot"],
        exec_time=True,
    )
    def test_base_2_plot(self):
        """
        稍微复杂一点
        :return:
        """
        source = data.cars()
        brush = alt.selection(type='interval')

        points = alt.Chart(source).mark_point().encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color=alt.condition(brush, 'Origin', alt.value('lightgray'))
        ).add_selection(
            brush
        )

        bars = alt.Chart(source).mark_bar().encode(
            y='Origin',
            color='Origin',
            x='count(Origin)'
        ).transform_filter(
            brush
        )
        altair_viewer.show(points | bars)

    @Tester()
    def test_add_line(self):
        source = data.stocks()
        lines = (
            alt.Chart(source)
            .mark_line()
            .encode(x="date", y="price", color="symbol")
        )
        xrule = (
            alt.Chart()
            .mark_rule(color="cyan", strokeWidth=2)
            .encode(x=alt.datum(alt.DateTime(year=2006, month="November")))
        )
        yrule = (
            alt.Chart().mark_rule(strokeDash=[12, 6], size=2).encode(y=alt.datum(350))
        )
        altair_viewer.show(lines + yrule + xrule)

    @Tester()
    def test_comp_plot(self):
        source = data.seattle_weather()
        scale = alt.Scale(domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
                          range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd'])
        color = alt.Color('weather:N', scale=scale)
        # We create two selections:
        # - a brush that is active on the top panel
        # - a multi-click that is active on the bottom panel
        brush = alt.selection_interval(encodings=['x'])
        click = alt.selection_multi(encodings=['color'])

        # Top panel is scatter plot of temperature vs time
        points = alt.Chart().mark_point().encode(
            alt.X('monthdate(date):T', title='Date'),
            alt.Y('temp_max:Q',
                  title='Maximum Daily Temperature (C)',
                  scale=alt.Scale(domain=[-5, 40])
                  ),
            color=alt.condition(brush, color, alt.value('lightgray')),
            size=alt.Size('precipitation:Q', scale=alt.Scale(range=[5, 200]))
        ).properties(
            width=550,
            height=300
        ).add_selection(
            brush
        ).transform_filter(
            click
        )

        # Bottom panel is a bar chart of weather type
        bars = alt.Chart().mark_bar().encode(
            x='count()',
            y='weather:N',
            color=alt.condition(click, color, alt.value('lightgray')),
        ).transform_filter(
            brush
        ).properties(
            width=550,
        ).add_selection(
            click
        )

        plot = alt.vconcat(
            points,
            bars,
            data=source,
            title="Seattle Weather: 2012-2015"
        )

        altair_viewer.show(plot)

    def test_scatter_plot(self):
        pass

    def test_bin_mapping_plot(self):
        pass

    def test_visual_mapping_plot(self):
        pass

    def test_trans_bar_plot(self):
        pass

    def test_pareto_plot(self):
        pass

    def test_multi_plot(self):
        pass
