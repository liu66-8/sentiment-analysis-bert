const HomePage = {
    template: `
    <div>
        <div class="page-title">📝 单条评论情感分析</div>
        <el-card class="analyze-card" shadow="hover">
            <text-input :loading="loading" @analyze="doAnalyze"></text-input>
        </el-card>

        <div v-if="loading" class="loading-overlay">
            <div class="el-loading-spinner">
                <svg class="circular" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none"/></svg>
            </div>
            <span style="color:#909399;margin-top:12px;">正在分析中，请稍候...</span>
        </div>

        <div v-if="result && !loading" class="result-section" ref="resultRef">
            <el-card class="analyze-card" shadow="hover" style="margin-top:20px;">
                <sentiment-gauge :summary="result.summary"></sentiment-gauge>
                <div class="summary-row">
                    <div class="summary-item">
                        <div class="count sentiment-positive">{{ result.summary['正面'] || 0 }}</div>
                        <div class="label">正面</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-neutral">{{ result.summary['中性'] || 0 }}</div>
                        <div class="label">中性</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-negative">{{ result.summary['负面'] || 0 }}</div>
                        <div class="label">负面</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-none">{{ result.summary['未提及'] || 0 }}</div>
                        <div class="label">未提及</div>
                    </div>
                </div>
                <sentiment-cards :predictions="result.predictions"></sentiment-cards>
            </el-card>

            <el-row :gutter="20" style="margin-top:20px;">
                <el-col :span="12">
                    <el-card shadow="hover" style="border-radius:12px;">
                        <radar-chart :predictions="result.predictions"></radar-chart>
                    </el-card>
                </el-col>
                <el-col :span="12">
                    <el-card shadow="hover" style="border-radius:12px;">
                        <pie-chart :summary="result.summary"></pie-chart>
                    </el-card>
                </el-col>
            </el-row>

            <el-card shadow="hover" style="border-radius:12px;margin-top:20px;">
                <bar-chart :predictions="result.predictions"></bar-chart>
            </el-card>

            <suggestions-card :suggestions="result.suggestions"></suggestions-card>

            <div style="display:flex;justify-content:center;margin-top:20px;gap:12px;">
                <el-button type="success" @click="saveAndCompare">🔄 添加到对比</el-button>
            </div>
        </div>

        <div v-if="error" style="margin-top:16px;">
            <el-alert :title="error" type="error" show-icon :closable="true" @close="error=''" />
        </div>
    </div>`,
    setup() {
        const loading = Vue.ref(false);
        const result = Vue.ref(null);
        const error = Vue.ref('');
        const resultRef = Vue.ref(null);
        const router = VueRouter.useRouter();

        const doAnalyze = async (text) => {
            loading.value = true;
            result.value = null;
            error.value = '';
            try {
                const data = await SentimentApi.analyze(text);
                result.value = data;
                Vue.nextTick(() => {
                    if (resultRef.value) {
                        resultRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                });
            } catch (e) {
                error.value = e.message || '分析失败，请稍后重试';
            } finally {
                loading.value = false;
            }
        };

        const saveAndCompare = () => {
            if (result.value) {
                const cache = JSON.parse(sessionStorage.getItem('compare_cache') || '[]');
                cache.push({ content: result.value.content, predictions: result.value.predictions, summary: result.value.summary });
                if (cache.length > 2) cache.shift();
                sessionStorage.setItem('compare_cache', JSON.stringify(cache));
                ElMessage.success('已保存，可前往对比分析页面查看');
                router.push('/compare');
            }
        };

        return { loading, result, error, resultRef, doAnalyze, saveAndCompare };
    },
};
