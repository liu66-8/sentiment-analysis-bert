const SentimentApi = {
    async analyze(text) {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` },
            body: JSON.stringify({ text }),
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || '分析失败');
        }
        return res.json();
    },

    async analyzeBatch(file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('content_col', 'content');
        const res = await fetch('/api/analyze/batch', {
            method: 'POST',
            body: formData,
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || '批量分析失败');
        }
        return res.json();
    },

    async getBatchResult(taskId) {
        const res = await fetch(`/api/analyze/batch/${taskId}`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || '获取任务结果失败');
        }
        return res.json();
    },

    async getHistory(page = 1, pageSize = 20) {
        const res = await fetch(`/api/history?page=${page}&page_size=${pageSize}`);
        if (!res.ok) throw new Error('加载历史记录失败');
        return res.json();
    },

    async getHistoryDetail(id) {
        const res = await fetch(`/api/history/${id}`);
        if (!res.ok) throw new Error('记录不存在');
        return res.json();
    },

    async deleteHistory(id) {
        const res = await fetch(`/api/history/${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('删除失败');
        return res.json();
    },

    async getStatus() {
        const res = await fetch('/api/status');
        return res.json();
    },

    async getLabels() {
        const res = await fetch('/api/labels');
        return res.json();
    },

    async getStatsOverview() {
        const res = await fetch('/api/stats/overview');
        return res.json();
    },

    async getSentimentDistribution() {
        const res = await fetch('/api/stats/sentiment-distribution');
        return res.json();
    },

    async getTrend(days = 7) {
        const res = await fetch(`/api/stats/trend?days=${days}`);
        return res.json();
    },
};

function getToken() {
    return localStorage.getItem('sentiment_token') || '';
}
