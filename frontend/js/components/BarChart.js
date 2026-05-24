const BarChart = {
    template: `<div ref="chartRef" style="width:100%;height:300px;"></div>`,
    props: { predictions: Object },
    setup(props) {
        const chartRef = Vue.ref(null);
        let myChart = null;

        const initChart = () => {
            if (!chartRef.value || !props.predictions) return;
            if (!myChart) myChart = echarts.init(chartRef.value);

            const dimensions = [];
            const scores = [];
            const colors = [];
            for (const [, val] of Object.entries(props.predictions)) {
                dimensions.push(val.display_name || '');
                let score = 0;
                if (val.sentiment === '正面') score = 3;
                else if (val.sentiment === '中性') score = 2;
                else if (val.sentiment === '负面') score = 1;
                scores.push(score);
                if (score === 3) colors.push('#67c23a');
                else if (score === 2) colors.push('#e6a23c');
                else if (score === 1) colors.push('#f56c6c');
                else colors.push('#c0c4cc');
            }

            myChart.setOption({
                title: { text: '逐维度情感评分', left: 'center', textStyle: { fontSize: 14 } },
                tooltip: { trigger: 'axis', formatter: p => {
                    const map = {3:'正面',2:'中性',1:'负面',0:'未提及'};
                    return `${p[0].name}: ${map[p[0].value]||''}`;
                }},
                grid: { left: '3%', right: '4%', bottom: '15%', top: 40, containLabel: true },
                xAxis: {
                    type: 'category', data: dimensions,
                    axisLabel: { rotate: 45, fontSize: 10, interval: 0 },
                },
                yAxis: {
                    type: 'value', min: 0, max: 3, interval: 1,
                    axisLabel: { formatter: v => ({0:'未提及',1:'负面',2:'中性',3:'正面'}[v]||'') },
                },
                series: [{
                    type: 'bar', data: scores.map((v, i) => ({ value: v, itemStyle: { color: colors[i] } })),
                    barWidth: '60%', label: { show: true, position: 'top', fontSize: 10,
                        formatter: p => ({0:'',1:'😞',2:'😐',3:'😊'}[p.value]||'') },
                }],
            });
        };

        Vue.watch(() => props.predictions, () => { Vue.nextTick(initChart); });
        Vue.onMounted(() => { Vue.nextTick(initChart); });
        Vue.onUnmounted(() => { if (myChart) myChart.dispose(); });

        return { chartRef };
    },
};
