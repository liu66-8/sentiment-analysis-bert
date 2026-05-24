const ResultTable = {
    template: `
    <div v-if="results.length">
        <div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;">
            <span style="color:#606266;">共 {{ total }} 条结果</span>
            <el-button type="success" size="small" @click="handleExport">📥 导出 CSV</el-button>
        </div>
        <el-table :data="pagedResults" border stripe max-height="500" style="width:100%;">
            <el-table-column prop="index" label="#" width="50" />
            <el-table-column prop="content" label="评论内容" min-width="200" show-overflow-tooltip />
            <el-table-column label="正面" width="70" align="center">
                <template #default="{ row }">
                    <span style="color:#67c23a;">{{ row.positive }}</span>
                </template>
            </el-table-column>
            <el-table-column label="中性" width="70" align="center">
                <template #default="{ row }">
                    <span style="color:#e6a23c;">{{ row.neutral }}</span>
                </template>
            </el-table-column>
            <el-table-column label="负面" width="70" align="center">
                <template #default="{ row }">
                    <span style="color:#f56c6c;">{{ row.negative }}</span>
                </template>
            </el-table-column>
            <el-table-column label="未提及" width="70" align="center">
                <template #default="{ row }">
                    <span style="color:#c0c4cc;">{{ row.not_mentioned }}</span>
                </template>
            </el-table-column>
        </el-table>
        <div style="margin-top:12px;display:flex;justify-content:center;">
            <el-pagination
                small
                layout="prev, pager, next"
                :total="total"
                :page-size="pageSize"
                v-model:current-page="currentPage"
            />
        </div>
    </div>`,
    props: { results: Array, total: Number },
    setup(props) {
        const currentPage = Vue.ref(1);
        const pageSize = Vue.ref(20);

        const pagedResults = Vue.computed(() => {
            const start = (currentPage.value - 1) * pageSize.value;
            return props.results.slice(start, start + pageSize.value).map((r, i) => ({
                index: start + i + 1,
                content: (r.content || '').substring(0, 80),
                positive: (r._summary && r._summary['正面']) || 0,
                neutral: (r._summary && r._summary['中性']) || 0,
                negative: (r._summary && r._summary['负面']) || 0,
                not_mentioned: (r._summary && r._summary['未提及']) || 0,
            }));
        });

        const handleExport = () => {
            const header = '\uFEFF序号,评论内容,正面,中性,负面,未提及';
            const lines = props.results.map((r, i) => {
                const content = (r.content || '').replace(/"/g, '""');
                const s = r._summary || {};
                return [
                    i + 1,
                    `"${content}"`,
                    s['正面'] || 0,
                    s['中性'] || 0,
                    s['负面'] || 0,
                    s['未提及'] || 0,
                ].join(',');
            });
            const csvContent = header + '\n' + lines.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'sentiment_analysis_result.csv';
            link.click();
            URL.revokeObjectURL(url);
            ElMessage.success('导出成功');
        };

        return { currentPage, pageSize, pagedResults, handleExport };
    },
};
