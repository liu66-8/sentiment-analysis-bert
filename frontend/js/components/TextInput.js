const TextInput = {
    template: `
    <div style="display:flex;flex-direction:column;gap:16px;">
        <el-input
            v-model="text"
            type="textarea"
            :rows="5"
            placeholder="请输入一段餐饮评论，例如：这家店环境很好，服务员态度也很棒，上菜速度很快..."
            maxlength="2000"
            show-word-limit
            resize="none"
        />
        <div style="display:flex;justify-content:flex-end;gap:10px;">
            <el-button size="large" @click="text=''" :disabled="!text">🗑️ 清空</el-button>
            <el-button type="primary" size="large" @click="handleAnalyze" :loading="loading" :disabled="!text.trim()">
                {{ loading ? '分析中...' : '🔍 开始分析' }}
            </el-button>
        </div>
    </div>`,
    props: { loading: Boolean },
    emits: ['analyze'],
    setup(props, { emit }) {
        const text = Vue.ref('');
        const handleAnalyze = () => {
            if (text.value.trim()) {
                emit('analyze', text.value.trim());
            }
        };
        return { text, handleAnalyze };
    },
};
