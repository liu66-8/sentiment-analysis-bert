const SentimentCards = {
    template: `
    <div v-if="groupedData.length">
        <div v-for="group in groupedData" :key="group.category" class="category-group">
            <div class="category-title">{{ group.category }}</div>
            <div class="dimension-tags">
                <span
                    v-for="dim in group.dimensions"
                    :key="dim.key"
                    :class="['dimension-tag', 'tag-' + dim.tagClass]"
                >
                    <span class="dim-name">{{ dim.display_name }}</span>
                    <span :class="'dim-sentiment sentiment-' + dim.tagClass">
                        {{ dim.sentiment }}
                    </span>
                </span>
            </div>
        </div>
    </div>`,
    props: { predictions: Object },
    setup(props) {
        const groupedData = Vue.computed(() => {
            if (!props.predictions) return [];
            const groups = {};
            for (const [key, val] of Object.entries(props.predictions)) {
                const cat = val.category || '其他';
                if (!groups[cat]) groups[cat] = [];
                let tagClass = 'none';
                if (val.sentiment === '正面') tagClass = 'positive';
                else if (val.sentiment === '负面') tagClass = 'negative';
                else if (val.sentiment === '中性') tagClass = 'neutral';
                groups[cat].push({ key, display_name: val.display_name, sentiment: val.sentiment, tagClass });
            }
            const categoryOrder = ['位置', '服务', '价格', '环境', '菜品', '整体'];
            return categoryOrder.filter(c => groups[c]).map(c => ({ category: c, dimensions: groups[c] }));
        });
        return { groupedData };
    },
};
