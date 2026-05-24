const HistoryDetail = {
    template: `
    <div>
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
            <el-button @click="goBack" circle>
                <span>←</span>
            </el-button>
            <div class="page-title" style="margin-bottom:0;border:none;padding:0;">📋 历史详情 #{{ id }}</div>
        </div>

        <div v-if="loading" class="loading-overlay">
            <el-icon style="font-size:32px;color:#667eea;">⏳</el-icon>
            <span style="color:#909399;">加载中...</span>
        </div>

        <div v-if="record && !loading">
            <el-card class="analyze-card" shadow="hover" style="margin-bottom:20px;">
                <div style="margin-bottom:12px;color:#909399;font-size:13px;">
                    评论原文
                </div>
                <div style="color:#303133;line-height:1.8;padding:12px;background:#f5f7fa;border-radius:8px;">
                    {{ record.content }}
                </div>
                <div style="margin-top:12px;color:#909399;font-size:12px;">
                    分析时间: {{ record.created_at }}
                </div>
            </el-card>

            <el-card class="analyze-card" shadow="hover">
                <div class="summary-row">
                    <div class="summary-item">
                        <div class="count sentiment-positive">{{ record.positive_count }}</div>
                        <div class="label">正面</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-neutral">{{ record.neutral_count }}</div>
                        <div class="label">中性</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-negative">{{ record.negative_count }}</div>
                        <div class="label">负面</div>
                    </div>
                    <div class="summary-item">
                        <div class="count sentiment-none">{{ record.not_mentioned_count }}</div>
                        <div class="label">未提及</div>
                    </div>
                </div>
                <sentiment-cards :predictions="record.predictions"></sentiment-cards>
                <suggestions-card :suggestions="record.suggestions"></suggestions-card>
            </el-card>
        </div>
    </div>`,
    setup() {
        const router = VueRouter.useRouter();
        const route = VueRouter.useRoute();
        const id = Vue.computed(() => route.params.id);

        const loading = Vue.ref(true);
        const record = Vue.ref(null);

        Vue.onMounted(async () => {
            try {
                record.value = await SentimentApi.getHistoryDetail(id.value);
            } catch (e) {
                ElMessage.error('加载详情失败');
            } finally {
                loading.value = false;
            }
        });

        const goBack = () => { router.push('/history'); };

        return { id, loading, record, goBack };
    },
};
