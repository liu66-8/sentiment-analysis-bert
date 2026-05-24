const RadarChart = {
    template: `<div ref="chartRef" style="width:100%;height:400px;"></div>`,
    props: { predictions: Object },
    setup(props) {
        const chartRef = Vue.ref(null);
        let myChart = null;

        const initChart = () => {
            if (!chartRef.value || !props.predictions) return;
            if (!myChart) myChart = echarts.init(chartRef.value);

            const categoryScores = {};
            const categoryCounts = {};
            for (const [, val] of Object.entries(props.predictions)) {
                const cat = val.category || '其他';
                if (!categoryScores[cat]) { categoryScores[cat] = 0; categoryCounts[cat] = 0; }
                let score = 0;
                if (val.sentiment === '正面') score = 3;
                else if (val.sentiment === '中性') score = 2;
                else if (val.sentiment === '负面') score = 1;
                categoryScores[cat] += score;
                categoryCounts[cat] += 1;
            }

            const categories = ['位置', '服务', '价格', '环境', '菜品', '整体'];
            const data = categories.map(c => {
                const avg = categoryCounts[c] ? (categoryScores[c] / categoryCounts[c]) * 100 / 3 : 0;
                return Math.round(avg);
            });

            myChart.setOption({
                title: { text: '维度情感雷达图', left: 'center', textStyle: { fontSize: 14 } },
                radar: {
                    indicator: categories.map(c => ({ name: c, max: 100 })),
                    center: ['50%', '55%'],
                    radius: '65%',
                },
                series: [{
                    type: 'radar',
                    data: [{ value: data, name: '情感得分', areaStyle: { color: 'rgba(102,126,234,0.3)' } }],
                    symbol: 'circle', symbolSize: 6,
                    lineStyle: { color: '#667eea', width: 2 },
                    itemStyle: { color: '#667eea' },
                }],
            });
        };

        Vue.watch(() => props.predictions, () => { Vue.nextTick(initChart); });
        Vue.onMounted(() => { Vue.nextTick(initChart); });
        Vue.onUnmounted(() => { if (myChart) myChart.dispose(); });

        return { chartRef };
    },
};
