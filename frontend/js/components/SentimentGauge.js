const SentimentGauge = {
    template: `
    <div class="gauge-container">
        <div style="text-align:center;">
            <div style="font-size:48px;">{{ emoji }}</div>
            <div style="font-size:18px;font-weight:600;color:#303133;margin-top:8px;">{{ overallText }}</div>
        </div>
    </div>`,
    props: { summary: Object },
    setup(props) {
        const overallText = Vue.computed(() => {
            if (!props.summary) return '';
            const pos = props.summary['正面'] || 0;
            const neg = props.summary['负面'] || 0;
            if (pos > neg + 3) return '整体偏向正面 👍';
            if (neg > pos + 3) return '整体偏向负面 👎';
            if (pos === neg) return '正面与负面相当';
            return pos > neg ? '略显正面' : '略显负面';
        });
        const emoji = Vue.computed(() => {
            if (!props.summary) return '🤔';
            const pos = props.summary['正面'] || 0;
            const neg = props.summary['负面'] || 0;
            if (pos >= 12) return '😄';
            if (pos >= 8) return '😊';
            if (neg >= 10) return '😡';
            if (neg >= 5) return '😟';
            return '😐';
        });
        return { overallText, emoji };
    },
};
