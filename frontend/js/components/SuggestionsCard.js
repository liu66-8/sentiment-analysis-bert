const SuggestionsCard = {
    template: `
    <div v-if="suggestions">
        <el-card shadow="hover" style="border-radius:12px;margin-top:20px;border-left:4px solid #667eea;">
            <div style="font-weight:600;font-size:16px;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
                <span>💡</span><span>AI 智能分析与优化方案</span>
                <el-tag type="success" size="small" effect="dark" style="margin-left:4px;">AI 大模型</el-tag>
            </div>

            <div style="margin-bottom:16px;padding:16px;background:linear-gradient(135deg,#f5f7fa,#e8ecf4);border-radius:12px;">
                <div style="font-size:13px;color:#606266;line-height:1.8;">{{ suggestions.overall_advice }}</div>
            </div>

            <div v-if="suggestions.strengths_summary" style="margin-bottom:16px;padding:12px 14px;background:#f0f9eb;border-radius:8px;font-size:13px;color:#606266;line-height:1.7;border-left:3px solid #67c23a;">
                <span style="color:#67c23a;font-weight:600;">✅ 优势保持：</span>{{ suggestions.strengths_summary }}
            </div>

            <div v-if="suggestions.improvements && suggestions.improvements.length">
                <div style="font-size:14px;font-weight:600;color:#303133;margin-bottom:10px;">
                    🎯 AI 改进建议（{{ suggestions.improvements.length }}项）
                </div>
                <div v-for="(item, idx) in suggestions.improvements" :key="idx"
                    :style="'padding:12px 14px;margin-bottom:8px;border-radius:8px;font-size:13px;line-height:1.8;' + (item.priority==='high'?'background:#fef0f0;border:1px solid #fab6b6;':'background:#fdf6ec;border:1px solid #f3d19e;')">
                    <div style="font-weight:600;margin-bottom:4px;display:flex;align-items:center;gap:6px;">
                        <span :style="item.priority==='high'?'color:#f56c6c;':'color:#e6a23c;'">
                            {{ item.priority === 'high' ? '🔴' : '🟡' }}
                        </span>
                        <span :style="'color:'+(item.priority==='high'?'#f56c6c':'#e6a23c')">{{ item.dimension }}</span>
                        <el-tag :type="item.priority==='high'?'danger':'warning'" size="small" effect="dark">
                            {{ item.priority === 'high' ? '优先改善' : '建议优化' }}
                        </el-tag>
                    </div>
                    <div :style="'color:'+(item.priority==='high'?'#e03434':'#b88230')">{{ item.advice }}</div>
                </div>
            </div>
        </el-card>
    </div>`,
    props: { suggestions: Object },
};
