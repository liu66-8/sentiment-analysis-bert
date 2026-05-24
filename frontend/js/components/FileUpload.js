const FileUpload = {
    template: `
    <div class="upload-area">
        <el-upload
            ref="uploadRef"
            drag
            :auto-upload="false"
            accept=".csv"
            :limit="1"
            :on-change="handleChange"
            :on-remove="handleRemove"
        >
            <div style="font-size:48px;color:#c0c4cc;">📄</div>
            <div style="margin-top:12px;color:#606266;">
                将 CSV 文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
                <div style="margin-top:8px;font-size:12px;color:#909399;">
                    仅支持 .csv 文件，需包含 content 列，最多 5000 条
                </div>
            </template>
        </el-upload>
        <div v-if="hasFile" style="margin-top:16px;">
            <el-button type="primary" @click="handleStart" :loading="loading" :disabled="loading">
                {{ loading ? '分析中...' : '开始批量分析' }}
            </el-button>
        </div>
    </div>`,
    props: { loading: Boolean },
    emits: ['start'],
    setup(props, { emit }) {
        const hasFile = Vue.ref(false);
        let _file = null;

        const handleChange = (uploadFile) => {
            _file = uploadFile.raw;
            hasFile.value = true;
        };
        const handleRemove = () => {
            _file = null;
            hasFile.value = false;
        };
        const handleStart = () => {
            if (_file) emit('start', _file);
        };
        return { hasFile, handleChange, handleRemove, handleStart };
    },
};
