const HistoryPage = {
    template: `
    <div>
        <div class="page-title">📋 历史分析记录</div>
        <el-card class="analyze-card" shadow="hover">
            <el-table :data="items" v-loading="loading" stripe style="width:100%;">
                <el-table-column prop="id" label="ID" width="60" />
                <el-table-column prop="content_preview" label="评论内容" min-width="220" show-overflow-tooltip />
                <el-table-column label="正面" width="70" align="center">
                    <template #default="{ row }">
                        <span style="color:#67c23a;">{{ row.positive_count }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="中性" width="70" align="center">
                    <template #default="{ row }">
                        <span style="color:#e6a23c;">{{ row.neutral_count }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="负面" width="70" align="center">
                    <template #default="{ row }">
                        <span style="color:#f56c6c;">{{ row.negative_count }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="未提及" width="70" align="center">
                    <template #default="{ row }">
                        <span style="color:#c0c4cc;">{{ row.not_mentioned_count }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" label="时间" width="160" />
                <el-table-column label="操作" width="140" align="center">
                    <template #default="{ row }">
                        <el-button type="primary" size="small" link @click="viewDetail(row.id)">查看</el-button>
                        <el-button type="danger" size="small" link @click="doDelete(row.id)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div v-if="total === 0 && !loading" class="empty-state">
                <div class="icon">📭</div>
                <div>暂无历史记录</div>
            </div>
            <div v-if="total > pageSize" style="margin-top:16px;display:flex;justify-content:center;">
                <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="total"
                    :page-size="pageSize"
                    v-model:current-page="page"
                />
            </div>
        </el-card>
    </div>`,
    setup() {
        const loading = Vue.ref(false);
        const items = Vue.ref([]);
        const total = Vue.ref(0);
        const page = Vue.ref(1);
        const pageSize = Vue.ref(20);

        const router = VueRouter.useRouter();

        const fetchData = async () => {
            loading.value = true;
            try {
                const data = await SentimentApi.getHistory(page.value, pageSize.value);
                items.value = data.items;
                total.value = data.total;
            } catch (e) {
                ElMessage.error('加载历史记录失败');
            } finally {
                loading.value = false;
            }
        };

        Vue.watch(page, fetchData, { immediate: true });

        const viewDetail = (id) => { router.push(`/history/${id}`); };
        const doDelete = async (id) => {
            try {
                await ElMessageBox.confirm('确认删除该条记录？', '提示', { type: 'warning' });
                await SentimentApi.deleteHistory(id);
                ElMessage.success('删除成功');
                fetchData();
            } catch (e) { /* 取消 */ }
        };

        return { loading, items, total, page, pageSize, viewDetail, doDelete };
    },
};
