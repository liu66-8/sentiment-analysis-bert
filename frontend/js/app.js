const { ElMessage, ElMessageBox } = ElementPlus;
window.ElMessage = ElMessage;
window.ElMessageBox = ElMessageBox;
const { ElLoading } = ElementPlus;

const routes = [
    { path: '/login', component: LoginPage, meta: { noAuth: true } },
    { path: '/', component: HomePage },
    { path: '/batch', component: BatchPage },
    { path: '/history', component: HistoryPage },
    { path: '/history/:id', component: HistoryDetail },
    { path: '/stats', component: StatsPage },
    { path: '/compare', component: ComparePage },
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('sentiment_token');
    if (to.meta && to.meta.noAuth) {
        next();
    } else if (token) {
        next();
    } else {
        next('/login');
    }
});

const AppRoot = {
    template: `
    <div v-if="isLoginPage">
        <router-view></router-view>
    </div>
    <el-container v-else>
        <el-header class="app-header">
            <div class="header-left">
                <span class="logo">🍜</span>
                <span class="title">细粒度餐饮评论情感分析系统</span>
            </div>
            <div class="header-right" style="display:flex;align-items:center;gap:12px;">
                <el-tag type="info" size="small">{{ deviceInfo }}</el-tag>
                <el-button size="small" circle @click="handleLogout" title="退出登录">
                    <span>🚪</span>
                </el-button>
            </div>
        </el-header>
        <el-container>
            <el-aside width="200px" class="sidebar">
                <el-menu :default-active="currentRoute" router>
                    <el-menu-item index="/">
                        ✏️ <span style="margin-left:4px;">单条分析</span>
                    </el-menu-item>
                    <el-menu-item index="/batch">
                        📁 <span style="margin-left:4px;">批量分析</span>
                    </el-menu-item>
                    <el-menu-item index="/compare">
                        🔄 <span style="margin-left:4px;">对比分析</span>
                    </el-menu-item>
                    <el-menu-item index="/history">
                        📋 <span style="margin-left:4px;">历史记录</span>
                    </el-menu-item>
                    <el-menu-item index="/stats">
                        📊 <span style="margin-left:4px;">数据统计</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>`,
    setup() {
        const currentRoute = Vue.computed(() => router.currentRoute.value.path);
        const isLoginPage = Vue.computed(() => router.currentRoute.value.path === '/login');
        const deviceInfo = Vue.ref('加载中...');

        SentimentApi.getStatus().then(status => {
            deviceInfo.value = status.gpu_name ? `GPU: ${status.gpu_name}` : 'CPU 模式';
        }).catch(() => { deviceInfo.value = '状态未知'; });

        const handleLogout = () => {
            localStorage.removeItem('sentiment_token');
            localStorage.removeItem('sentiment_user');
            router.push('/login');
        };

        return { currentRoute, isLoginPage, deviceInfo, handleLogout };
    },
};

const app = Vue.createApp(AppRoot);
app.use(router);
app.use(ElementPlus, { locale: ElementPlusLocaleZhCn });

app.component('text-input', TextInput);
app.component('sentiment-gauge', SentimentGauge);
app.component('sentiment-cards', SentimentCards);
app.component('file-upload', FileUpload);
app.component('result-table', ResultTable);
app.component('radar-chart', RadarChart);
app.component('pie-chart', PieChart);
app.component('bar-chart', BarChart);
app.component('suggestions-card', SuggestionsCard);

app.mount('#app');
