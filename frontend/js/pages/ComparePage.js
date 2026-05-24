const ComparePage = {
    template: `
    <div>
        <div class="page-title">🔄 对比分析</div>
        <el-card class="analyze-card" shadow="hover">
            <el-row :gutter="20">
                <el-col :span="12">
                    <div style="font-weight:600;margin-bottom:8px;color:#606266;">📝 评论 A</div>
                    <el-input
                        v-model="textA"
                        type="textarea"
                        :rows="4"
                        placeholder="输入第一条评论..."
                        maxlength="2000"
                        show-word-limit
                        resize="none"
                    />
                </el-col>
                <el-col :span="12">
                    <div style="font-weight:600;margin-bottom:8px;color:#606266;">📝 评论 B</div>
                    <el-input
                        v-model="textB"
                        type="textarea"
                        :rows="4"
                        placeholder="输入第二条评论..."
                        maxlength="2000"
                        show-word-limit
                        resize="none"
                    />
                </el-col>
            </el-row>
            <div style="display:flex;justify-content:center;margin-top:16px;">
                <el-button type="primary" size="large" :loading="loading" :disabled="!textA.trim()||!textB.trim()" @click="doCompare">
                    {{ loading ? '分析中...' : '🔍 开始对比分析' }}
                </el-button>
            </div>
        </el-card>

        <div v-if="loading" class="loading-overlay">
            <div class="el-loading-spinner">
                <svg class="circular" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none"/></svg>
            </div>
            <span style="color:#909399;margin-top:12px;">正在对比分析中...</span>
        </div>

        <div v-if="resultA && resultB && !loading" class="result-section" ref="resultRef">
            <el-row :gutter="20">
                <el-col :span="12">
                    <el-card shadow="hover" style="border-radius:12px;">
                        <div style="font-weight:600;font-size:15px;margin-bottom:12px;color:#409eff;">📝 评论 A</div>
                        <div class="summary-row" style="gap:12px;">
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-positive">{{ resultA.summary['正面'] }}</div>
                                <div class="label">正面</div>
                            </div>
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-negative">{{ resultA.summary['负面'] }}</div>
                                <div class="label">负面</div>
                            </div>
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-neutral">{{ resultA.summary['中性'] }}</div>
                                <div class="label">中性</div>
                            </div>
                        </div>
                        <sentiment-cards :predictions="resultA.predictions"></sentiment-cards>
                    </el-card>
                </el-col>
                <el-col :span="12">
                    <el-card shadow="hover" style="border-radius:12px;">
                        <div style="font-weight:600;font-size:15px;margin-bottom:12px;color:#e6a23c;">📝 评论 B</div>
                        <div class="summary-row" style="gap:12px;">
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-positive">{{ resultB.summary['正面'] }}</div>
                                <div class="label">正面</div>
                            </div>
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-negative">{{ resultB.summary['负面'] }}</div>
                                <div class="label">负面</div>
                            </div>
                            <div class="summary-item" style="min-width:60px;padding:8px;">
                                <div class="count sentiment-neutral">{{ resultB.summary['中性'] }}</div>
                                <div class="label">中性</div>
                            </div>
                        </div>
                        <sentiment-cards :predictions="resultB.predictions"></sentiment-cards>
                    </el-card>
                </el-col>
            </el-row>

            <el-card shadow="hover" style="border-radius:12px;margin-top:20px;">
                <div style="font-weight:600;font-size:15px;margin-bottom:12px;">📊 维度对比图</div>
                <div ref="compareChartRef" style="width:100%;height:380px;"></div>
            </el-card>

            <el-row :gutter="20" style="margin-top:20px;">
                <el-col :span="12">
                    <suggestions-card :suggestions="resultA.suggestions"></suggestions-card>
                </el-col>
                <el-col :span="12">
                    <suggestions-card :suggestions="resultB.suggestions"></suggestions-card>
                </el-col>
            </el-row>
        </div>
    </div>`,
    setup() {
        const textA = Vue.ref('');
        const textB = Vue.ref('');
        const loading = Vue.ref(false);
        const resultA = Vue.ref(null);
        const resultB = Vue.ref(null);
        const resultRef = Vue.ref(null);
        const compareChartRef = Vue.ref(null);
        let compareChart = null;

        Vue.onMounted(() => {
            const cache = JSON.parse(sessionStorage.getItem('compare_cache') || '[]');
            if (cache.length >= 1) {
                textA.value = cache[0].content || '';
                if (cache.length >= 2) {
                    textB.value = cache[1].content || '';
                }
                if (cache.length >= 2) {
                    ElMessage.success('已加载 2 条缓存评论，可直接点击对比分析');
                } else {
                    ElMessage.info('已加载 1 条缓存评论，请输入第二条评论后对比');
                }
            }
        });

        const doCompare = async () => {
            loading.value = true;
            resultA.value = null;
            resultB.value = null;
            try {
                const [dataA, dataB] = await Promise.all([
                    SentimentApi.analyze(textA.value.trim()),
                    SentimentApi.analyze(textB.value.trim()),
                ]);
                resultA.value = dataA;
                resultB.value = dataB;
                Vue.nextTick(() => {
                    if (resultRef.value) resultRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    drawCompareChart(dataA.predictions, dataB.predictions);
                });
            } catch (e) {
                ElMessage.error('分析失败: ' + e.message);
            } finally {
                loading.value = false;
            }
        };

        const drawCompareChart = (predA, predB) => {
            if (!compareChartRef.value) return;
            if (!compareChart) compareChart = echarts.init(compareChartRef.value);

            const dims = [];
            const scoresA = [];
            const scoresB = [];
            for (const [key, val] of Object.entries(predA)) {
                dims.push(val.display_name);
                let s = 0;
                if (val.sentiment === '正面') s = 3; else if (val.sentiment === '中性') s = 2; else if (val.sentiment === '负面') s = 1;
                scoresA.push(s);
                const vb = predB[key];
                let sb = 0;
                if (vb.sentiment === '正面') sb = 3; else if (vb.sentiment === '中性') sb = 2; else if (vb.sentiment === '负面') sb = 1;
                scoresB.push(sb);
            }

            compareChart.setOption({
                tooltip: { trigger: 'axis', formatter: p => {
                    const map = {3:'正面',2:'中性',1:'负面',0:'未提及'};
                    return p.map(d => `${d.seriesName}: ${map[d.value]||''}`).join('<br/>');
                }},
                legend: { data: ['评论A', '评论B'] },
                grid: { left: '3%', right: '4%', bottom: '15%', top: 50 },
                xAxis: { type: 'category', data: dims, axisLabel: { rotate: 45, fontSize: 9, interval: 0 } },
                yAxis: { type: 'value', min: 0, max: 3, interval: 1, axisLabel: { formatter: v => ({0:'',1:'负面',2:'中性',3:'正面'}[v]||'') } },
                series: [
                    { name: '评论A', type: 'bar', data: scoresA, itemStyle: { color: '#409eff' } },
                    { name: '评论B', type: 'bar', data: scoresB, itemStyle: { color: '#e6a23c' } },
                ],
            });
        };

        Vue.onUnmounted(() => { if (compareChart) compareChart.dispose(); });

        return { textA, textB, loading, resultA, resultB, resultRef, compareChartRef, doCompare };
    },
};
