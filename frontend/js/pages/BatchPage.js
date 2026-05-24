const BatchPage = {
    template: `
    <div>
        <div class="page-title">📁 批量 CSV 分析</div>
        <el-card class="analyze-card" shadow="hover">
            <file-upload :loading="loading" @start="doBatch"></file-upload>
        </el-card>

        <div v-if="loading" class="loading-overlay">
            <div class="el-loading-spinner">
                <svg class="circular" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none"/></svg>
            </div>
            <span style="color:#909399;margin-top:12px;">正在批量分析中，请稍候...</span>
        </div>

        <div v-if="error" style="margin-top:16px;">
            <el-alert :title="error" type="error" show-icon :closable="true" @close="error=''" />
        </div>
        <div v-if="results.length" ref="resultRef" style="margin-top:20px;">
            <el-card class="analyze-card" shadow="hover">
                <result-table :results="results" :total="results.length"></result-table>
            </el-card>
        </div>
    </div>`,
    setup() {
        const loading = Vue.ref(false);
        const results = Vue.ref([]);
        const error = Vue.ref('');
        const resultRef = Vue.ref(null);

        const doBatch = async (file) => {
            loading.value = true;
            error.value = '';
            results.value = [];
            try {
                const data = await SentimentApi.analyzeBatch(file);
                if (data.results) {
                    results.value = data.results;
                } else if (data.task_id) {
                    const taskRes = await SentimentApi.getBatchResult(data.task_id);
                    results.value = taskRes.results || [];
                }
                ElMessage.success(`成功分析 ${results.value.length} 条数据`);
                Vue.nextTick(() => {
                    if (resultRef.value) {
                        resultRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                });
            } catch (e) {
                error.value = e.message || '批量分析失败';
            } finally {
                loading.value = false;
            }
        };

        return { loading, results, error, resultRef, doBatch };
    },
};
