const StatsPage = {
    template: `
    <div>
        <div class="page-title">📊 数据统计 Dashboard</div>

        <el-row :gutter="20" style="margin-bottom:20px;">
            <el-col :span="6" v-for="card in overviewCards" :key="card.label">
                <el-card shadow="hover" style="text-align:center;border-radius:12px;">
                    <div style="font-size:36px;font-weight:700;color:{{ card.color }};">{{ card.value }}</div>
                    <div style="color:#909399;font-size:13px;margin-top:4px;">{{ card.label }}</div>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="20" style="margin-bottom:20px;">
            <el-col :span="12">
                <el-card shadow="hover" style="border-radius:12px;">
                    <div ref="distChart" style="width:100%;height:350px;"></div>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover" style="border-radius:12px;">
                    <div ref="avgChart" style="width:100%;height:350px;"></div>
                </el-card>
            </el-col>
        </el-row>

        <el-card shadow="hover" style="border-radius:12px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span style="font-weight:600;font-size:15px;">📈 近期情感趋势</span>
                <el-radio-group v-model="trendDays" size="small" @change="loadTrend">
                    <el-radio-button :value="7">7天</el-radio-button>
                    <el-radio-button :value="14">14天</el-radio-button>
                    <el-radio-button :value="30">30天</el-radio-button>
                </el-radio-group>
            </div>
            <div ref="trendChart" style="width:100%;height:350px;"></div>
        </el-card>
    </div>`,
    setup() {
        const overviewCards = Vue.ref([
            { label: '总分析次数', value: '-', color: '#667eea' },
            { label: '今日分析', value: '-', color: '#67c23a' },
            { label: '平均正面维度', value: '-', color: '#67c23a' },
            { label: '平均负面维度', value: '-', color: '#f56c6c' },
        ]);

        const trendDays = Vue.ref(7);
        const distChart = Vue.ref(null);
        const avgChart = Vue.ref(null);
        const trendChart = Vue.ref(null);
        let distIns = null, avgIns = null, trendIns = null;

        const loadOverview = async () => {
            try {
                const data = await SentimentApi.getStatsOverview();
                overviewCards.value = [
                    { label: '总分析次数', value: data.total_count, color: '#667eea' },
                    { label: '今日分析', value: data.today_count, color: '#67c23a' },
                    { label: '平均正面维度', value: data.avg_positive, color: '#67c23a' },
                    { label: '平均负面维度', value: data.avg_negative, color: '#f56c6c' },
                ];

                if (!avgIns && avgChart.value) avgIns = echarts.init(avgChart.value);
                if (avgIns) {
                    avgIns.setOption({
                        title: { text: '历史平均情感分布', left: 'center', textStyle: { fontSize: 14 } },
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: ['正面', '中性', '负面', '未提及'] },
                        yAxis: { type: 'value' },
                        series: [{
                            type: 'bar',
                            data: [
                                { value: data.avg_positive, itemStyle: { color: '#67c23a' } },
                                { value: data.avg_neutral, itemStyle: { color: '#e6a23c' } },
                                { value: data.avg_negative, itemStyle: { color: '#f56c6c' } },
                                { value: data.avg_not_mentioned, itemStyle: { color: '#c0c4cc' } },
                            ],
                            barWidth: '50%',
                        }],
                    });
                }

                const distData = await SentimentApi.getSentimentDistribution();
                if (!distIns && distChart.value) distIns = echarts.init(distChart.value);
                if (distIns) {
                    distIns.setOption({
                        title: { text: '历史情感总分布', left: 'center', textStyle: { fontSize: 14 } },
                        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
                        legend: { bottom: 0 },
                        series: [{
                            type: 'pie', radius: ['40%', '65%'],
                            label: { formatter: '{b}\n{c}' },
                            data: distData.labels.map((l, i) => {
                                const colors = ['#67c23a', '#e6a23c', '#f56c6c', '#c0c4cc'];
                                return { value: distData.values[i], name: l, itemStyle: { color: colors[i] } };
                            }),
                        }],
                    });
                }
            } catch (e) { /* ignore */ }
        };

        const loadTrend = async () => {
            try {
                const data = await SentimentApi.getTrend(trendDays.value);
                if (!trendIns && trendChart.value) trendIns = echarts.init(trendChart.value);
                if (trendIns && data.trend) {
                    trendIns.setOption({
                        tooltip: { trigger: 'axis' },
                        legend: { data: ['分析数量', '平均正面', '平均负面'] },
                        xAxis: { type: 'category', data: data.trend.map(d => d.date) },
                        yAxis: [
                            { type: 'value', name: '次数' },
                            { type: 'value', name: '平均维度数', min: 0, max: 20 },
                        ],
                        series: [
                            { name: '分析数量', type: 'bar', data: data.trend.map(d => d.count), itemStyle: { color: '#667eea' } },
                            { name: '平均正面', type: 'line', yAxisIndex: 1, data: data.trend.map(d => d.avg_positive), smooth: true, lineStyle: { color: '#67c23a' }, itemStyle: { color: '#67c23a' } },
                            { name: '平均负面', type: 'line', yAxisIndex: 1, data: data.trend.map(d => d.avg_negative), smooth: true, lineStyle: { color: '#f56c6c' }, itemStyle: { color: '#f56c6c' } },
                        ],
                    });
                }
            } catch (e) { /* ignore */ }
        };

        Vue.onMounted(() => {
            loadOverview();
            loadTrend();
        });
        Vue.onUnmounted(() => {
            if (distIns) distIns.dispose();
            if (avgIns) avgIns.dispose();
            if (trendIns) trendIns.dispose();
        });

        return { overviewCards, trendDays, distChart, avgChart, trendChart, loadTrend };
    },
};
