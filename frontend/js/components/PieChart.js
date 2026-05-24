const PieChart = {
    template: `<div ref="chartRef" style="width:100%;height:320px;"></div>`,
    props: { summary: Object },
    setup(props) {
        const chartRef = Vue.ref(null);
        let myChart = null;

        const initChart = () => {
            if (!chartRef.value || !props.summary) return;
            if (!myChart) myChart = echarts.init(chartRef.value);

            const data = [
                { value: props.summary['正面'] || 0, name: '正面', itemStyle: { color: '#67c23a' } },
                { value: props.summary['中性'] || 0, name: '中性', itemStyle: { color: '#e6a23c' } },
                { value: props.summary['负面'] || 0, name: '负面', itemStyle: { color: '#f56c6c' } },
                { value: props.summary['未提及'] || 0, name: '未提及', itemStyle: { color: '#c0c4cc' } },
            ].filter(d => d.value > 0);

            myChart.setOption({
                title: { text: '情感分布', left: 'center', textStyle: { fontSize: 14 } },
                tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
                legend: { bottom: 0 },
                series: [{
                    type: 'pie', radius: ['45%', '70%'], center: ['50%', '50%'],
                    label: { show: true, formatter: '{b}\n{c}' },
                    emphasis: { label: { fontSize: 18, fontWeight: 'bold' } },
                    data,
                }],
            });
        };

        Vue.watch(() => props.summary, () => { Vue.nextTick(initChart); });
        Vue.onMounted(() => { Vue.nextTick(initChart); });
        Vue.onUnmounted(() => { if (myChart) myChart.dispose(); });

        return { chartRef };
    },
};
